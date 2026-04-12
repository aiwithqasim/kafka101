# Kafka Manual Setup on AWS EC2

A step-by-step guide to manually setting up Apache Kafka 4.x on an AWS EC2 instance using KRaft mode (no Zookeeper).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Key Notes Before You Start](#key-notes-before-you-start)
- [Step 1: Launch EC2 Instance](#step-1--launch-ec2-instance)
- [Step 2: Connect to EC2 via SSH](#step-2--connect-to-ec2-via-ssh)
- [Step 3: Install Java 17](#step-3--install-java-17)
- [Step 4: Download and Extract Kafka](#step-4--download-and-extract-kafka)
- [Step 5: Configure Kafka](#step-5--configure-kafka)
- [Step 6: Configure EC2 Security Group](#step-6--configure-ec2-security-group)
- [Step 7: Format Storage and Start Kafka](#step-7--format-storage-and-start-kafka)
- [Step 8: Verify Kafka is Running](#step-8--verify-kafka-is-running)
- [Step 9: Create a Topic](#step-9--create-a-topic)
- [Step 10: Test with Producer and Consumer](#step-10--test-with-producer-and-consumer)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- AWS account with EC2 access
- SSH client (Terminal on Mac/Linux, PowerShell or PuTTY on Windows)
- Basic familiarity with Linux command line

---

## Key Notes Before You Start

> **Read these before running any command.**

1. **Kafka 4.x does not use Zookeeper.** It uses KRaft mode — a single process manages everything. There is no `zookeeper-server-start.sh` in Kafka 4.x.

2. **Kafka 4.x requires Java 17 minimum.** Java 8 will throw `UnsupportedClassVersionError`. Do not install Java 8.

3. **Always run Kafka commands from inside the Kafka root directory** (`~/kafka_2.13-4.2.0`), not from inside `bin/`. Check with `pwd` before running anything.

4. **EC2 public IP changes on every stop/start** unless you attach an Elastic IP. Always verify your current public IP in AWS Console before connecting.

5. **Port 9092 must be open in your EC2 Security Group.** Without this, all remote connections time out silently.

6. **`advertised.listeners` must only contain the `PLAINTEXT` listener** — never add `CONTROLLER` to it.

---

## Step 1: Launch EC2 Instance

1. Open **AWS Management Console → EC2 → Instances → Launch Instances**
2. Configure:
   - **AMI:** Amazon Linux 2023 (or Amazon Linux 2)
   - **Instance type:** `t2.micro` (free tier eligible — 1GB RAM)
   - **Key pair:** Create a new key pair, download the `.pem` file, keep it safe
   - **Security group:** Create a new one — you will add Kafka port rules in Step 6
3. Click **Launch Instance**

---

## Step 2: Connect to EC2 via SSH

```bash
# Protect your key file (run once, on your local machine)
chmod 400 your-key-pair.pem

# SSH into the instance
ssh -i your-key-pair.pem ec2-user@<your-ec2-public-ip>
```

Find your EC2 public IP in: **AWS Console → EC2 → Instances → Public IPv4 address**

---

## Step 3: Install Java 17

Kafka 4.x requires Java 17. Java 8 (the default on many AMIs) will not work.

```bash
# Check current Java version
java -version

# Install Java 17
sudo yum install java-17-amazon-corretto -y

# Confirm Java 17 is active
java -version
# Expected: openjdk version "17.x.x"
```

---

## Step 4: Download and Extract Kafka

```bash
# Download Kafka 4.2.0
wget https://downloads.apache.org/kafka/4.2.0/kafka_2.13-4.2.0.tgz

# Confirm download
ls -lh | grep kafka

# Extract
tar -xvf kafka_2.13-4.2.0.tgz

# Enter the Kafka directory
cd kafka_2.13-4.2.0
```

> All subsequent commands assume you are inside `~/kafka_2.13-4.2.0`.

---

## Step 5: Configure Kafka

Edit `config/server.properties` to set the public IP so external clients can connect.

```bash
sudo nano config/server.properties
```

**Find and update `advertised.listeners`:**

Use `Ctrl+W` in nano to search for `advertised`.

Change from (commented out or localhost):
```
#advertised.listeners=PLAINTEXT://localhost:9092
```

To (your EC2 public IP):
```
advertised.listeners=PLAINTEXT://<your-ec2-public-ip>:9092
```

Example:
```
advertised.listeners=PLAINTEXT://54.89.203.129:9092
```

**Also verify `listeners` is bound to all interfaces:**
```
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
```

> **Important:** Do NOT add `CONTROLLER` to `advertised.listeners`. The controller listener is internal only. Only `PLAINTEXT` should be advertised.

Save and exit: `Ctrl+X` → `Y` → `Enter`

**Validate your changes:**
```bash
grep -E "^listeners|^advertised" config/server.properties
# Expected output:
# listeners=PLAINTEXT://:9092,CONTROLLER://:9093
# advertised.listeners=PLAINTEXT://54.89.203.129:9092
```

---

## Step 6: Configure EC2 Security Group

Kafka listens on port 9092. Without an inbound rule, all remote connections time out.

1. Open **AWS Console → EC2 → Instances** → click your instance
2. Click the **Security** tab → click the security group link
3. Click **Edit inbound rules → Add rule**:
   - **Type:** Custom TCP
   - **Port range:** `9092`
   - **Source:** Your IP (recommended) or `0.0.0.0/0` (development only)
4. Click **Save rules**

> **If topic creation or producer/consumer commands time out**, a missing port 9092 inbound rule is the most common cause. Always check this first.

---

## Step 7: Format Storage and Start Kafka

### Format storage (run once only)

KRaft mode requires the storage directory to be formatted before first use. If you need to reformat, delete the log directory first:

```bash
# Check where logs are stored
grep "^log.dirs" config/server.properties
# Default: /tmp/kraft-combined-logs

# Delete existing (only if reformatting)
rm -rf /tmp/kraft-combined-logs
```

Then format:

```bash
# Generate a unique cluster ID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

# Format storage — --standalone is required for single-node Kafka 4.x
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
```

### Start Kafka

```bash
# Set heap size — required on t2.micro (1GB RAM), otherwise Kafka crashes
export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"

# Start Kafka (runs in foreground — keep this terminal open)
bin/kafka-server-start.sh config/server.properties
```

> Kafka runs in the foreground. Keep this terminal session open. Open a new SSH session for all subsequent commands.

---

## Step 8: Verify Kafka is Running

Open a new SSH session and run:

```bash
cd kafka_2.13-4.2.0

# Confirm the Kafka process is running
ps aux | grep kafka | grep -v grep
# Expected: a Java process with "kafka.Kafka config/server.properties"

# Confirm port 9092 is bound
ss -tlnp | grep 9092
# Expected: LISTEN ... *:9092 ... ("java",pid=...)

# Test local connectivity
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
# Expected: empty list (no topics yet) — confirms Kafka is accepting connections
```

---

## Step 9: Create a Topic

```bash
cd kafka_2.13-4.2.0

bin/kafka-topics.sh --create \
  --topic demo-testing \
  --bootstrap-server <your-ec2-public-ip>:9092 \
  --replication-factor 1 \
  --partitions 1
```

Example:
```bash
bin/kafka-topics.sh --create \
  --topic demo-testing \
  --bootstrap-server 54.89.203.129:9092 \
  --replication-factor 1 \
  --partitions 1
```

Confirm it was created:
```bash
bin/kafka-topics.sh --list --bootstrap-server 54.89.203.129:9092
```

---

## Step 10: Test with Producer and Consumer

### Start Producer (Terminal 2)

```bash
cd kafka_2.13-4.2.0
bin/kafka-console-producer.sh \
  --topic demo-testing \
  --bootstrap-server <your-ec2-public-ip>:9092
```

Type messages and press Enter to send each one.

### Start Consumer (Terminal 3)

Open a third SSH session:

```bash
cd kafka_2.13-4.2.0
bin/kafka-console-consumer.sh \
  --topic demo-testing \
  --bootstrap-server <your-ec2-public-ip>:9092 \
  --from-beginning
```

Messages typed in the producer terminal should appear here in real time.

---

## Troubleshooting

| Error / Symptom | Cause | Fix |
|-----------------|-------|-----|
| `bin/zookeeper-server-start.sh: No such file or directory` | Kafka 4.x removed Zookeeper, or running from wrong directory | Use KRaft mode. Run commands from `~/kafka_2.13-4.2.0`, not from inside `bin/` |
| `UnsupportedClassVersionError: class file version 61.0` | Java 8 installed; Kafka 4.x needs Java 17 | `sudo yum install java-17-amazon-corretto -y` |
| `Cannot allocate memory` on startup | t2.micro has 1GB RAM; Kafka default heap is 1GB | `export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"` before starting |
| `config/kraft/server.properties: No such file or directory` | Kafka 4.x has no `kraft/` subfolder | Use `config/server.properties` directly |
| `No readable meta.properties files found` | Storage not formatted, or formatted with wrong config path | `rm -rf /tmp/kraft-combined-logs` then re-run `format --standalone` |
| `controller.quorum.voters is not set` | Kafka 4.x single-node requires explicit mode | Add `--standalone` flag to `kafka-storage.sh format` |
| Broker fails to start with CONTROLLER error | `advertised.listeners` incorrectly includes `CONTROLLER` | Set `advertised.listeners=PLAINTEXT://<ip>:9092` only — no CONTROLLER |
| `Timed out waiting for a node assignment` | Kafka not running, or port 9092 blocked by Security Group | Check `ps aux \| grep kafka`. Test with `localhost:9092`. Check Security Group inbound rules |
| Localhost works but public IP times out | EC2 Security Group missing port 9092 inbound rule | AWS Console → EC2 → Security Groups → Add Custom TCP port 9092 inbound rule |
| `Invalid url in bootstrap.servers` | Placeholder `{Put the Public IP...}` not replaced | Replace with actual IP, e.g. `54.89.203.129:9092` |
| EC2 public IP changed | AWS reassigns public IP on every stop/start | Check current IP in AWS Console → EC2 → Instances → Public IPv4 address |

---

## References

- [Apache Kafka Official Documentation](https://kafka.apache.org/documentation/)
- [Kafka KRaft Mode Guide](https://kafka.apache.org/documentation/#kraft)
- [AWS EC2 Getting Started](https://docs.aws.amazon.com/ec2/index.html)
- [Amazon Corretto Java Downloads](https://aws.amazon.com/corretto/)
