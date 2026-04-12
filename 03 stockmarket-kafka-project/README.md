# Stock Market Real-Time Data Pipeline

## Overview

This project demonstrates an end-to-end data engineering pipeline for real-time stock market data processing using Apache Kafka and AWS services.

**Objective:** Build a data pipeline that ingests real-time stock market data, processes it through Kafka, and stores it in AWS for querying and analysis.

## Table of Contents

- [Kafka Fundamentals](#kafka-fundamentals)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Pipeline](#running-the-pipeline)
- [Project Execution](#project-execution)

## Architecture

![Project Architecture](./images/architecture.jpg)

The pipeline follows a producer-consumer pattern:
1. **Data Source** → **Kafka Producer** → **Kafka Broker** → **Kafka Consumer** → **AWS S3**
2. **Data Catalog**: AWS Glue Crawler catalogs data for querying
3. **Analytics**: Amazon Athena enables SQL-based analysis

## Technology Stack

| Component | Purpose |
|-----------|---------|
| **Python 3.7+** | Data processing and scripting |
| **Apache Kafka** | Distributed event streaming platform |
| **AWS S3** | Data lake and object storage |
| **AWS EC2** | Compute resources for Kafka cluster |
| **AWS Glue** | ETL and data cataloging |
| **Amazon Athena** | SQL query engine for data analysis |
| **Jupyter Notebook** | Interactive development environment |

## Prerequisites

### Hardware & Environment
- Laptop/Desktop with internet connection
- 4GB+ RAM recommended
- Ability to run terminal/command-line tools

### Software Requirements
- **Python** 3.7 or higher
- **Jupyter Notebook** for interactive development
- **SSH client** for EC2 connection
- **Git** (optional, for version control)

### AWS Account
- Active AWS account with access to:
  - EC2 (EC2 instance for Kafka)
  - S3 (data storage)
  - Glue (data cataloging)
  - Athena (analytics)
  - IAM (access management)

## Project Structure

```
stockmarket-kafka-project/
├── README.md                      # This file
├── KafkaProducer.ipynb           # Producer implementation
├── KafkaConsumer.ipynb           # Consumer implementation
├── command_kafka.txt              # Kafka CLI commands reference
├── data/
│   └── indexProcessed.csv        # Sample stock market dataset
└── images/
    └── [Architecture diagrams]
```

## Installation & Setup

### 1. AWS EC2 Configuration

**Launch EC2 Instance:**
```bash
1. Open AWS Management Console
2. Navigate to EC2 → Instances → Launch Instances
3. Select Amazon Linux 2 AMI or Ubuntu
4. Choose t2.micro (free tier eligible)
5. Create and download a key pair for SSH access
6. Launch the instance
```

**Connect to EC2 Instance:**
```bash
ssh -i your-key-pair.pem ec2-user@<your-ec2-public-ip>
```

### 2. Install Java and Kafka

**Install Java 1.8:**
```bash
sudo yum update -y
sudo yum install java-1.8.0-openjdk -y
sudo yum remove java-1.7.0-openjdk -y
```

**Download and Install Kafka:**
```bash
cd /opt
sudo wget https://archive.apache.org/dist/kafka/2.6.0/kafka_2.13-2.6.0.tgz
sudo tar -xzf kafka_2.13-2.6.0.tgz
sudo mv kafka_2.13-2.6.0 kafka
sudo chown -R ec2-user:ec2-user /opt/kafka
```

### 3. Start Kafka Services

**Start Zookeeper:**
```bash
cd /opt/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
```

**Start Kafka Broker (in a new terminal):**
```bash
cd /opt/kafka
bin/kafka-server-start.sh config/server.properties
```

### 4. Configure Kafka for Remote Access

**Edit server.properties:**
```bash
sudo nano config/server.properties
```

**Locate and modify:**
```properties
# Change from:
advertised.listeners=PLAINTEXT://localhost:9092

# To:
advertised.listeners=PLAINTEXT://<your-ec2-public-ip>:9092
```

**Save changes:** Press `Ctrl+X`, then `Y`, and `Enter`

### 5. Configure AWS Security Groups

Kafka listens on port 9092. Without an inbound rule for this port, all remote connections will time out — including topic creation, producer, and consumer commands.

**Steps:**
1. Open AWS Management Console → EC2 → Instances → click your instance
2. Click the **Security** tab → click the security group link
3. Click **Edit inbound rules**
4. Click **Add rule**:
   - **Type:** Custom TCP
   - **Port Range:** `9092`
   - **Source:** Your IP (recommended) or `0.0.0.0/0` (development only)
5. Click **Save rules**

> **Note:** If topic creation or producer/consumer commands time out even after Kafka is running, a missing port 9092 inbound rule is the most common cause. Always verify this first.

**Verify the rule is working** — from your EC2 instance, confirm port 9092 is bound:
```bash
ss -tlnp | grep 9092
# Expected: LISTEN ... *:9092 ... ("java",pid=...)
```

### 6. Verify Kafka is Running

Before creating topics or running the producer/consumer, confirm Kafka is up:
```bash
ps aux | grep kafka | grep -v grep
```

Expected: a Java process running `kafka.Kafka config/server.properties`. If nothing shows, Kafka is not running — start it first (Step 3).

**Confirm Kafka accepts connections locally:**
```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

If this works but the public IP times out → the EC2 security group is missing the port 9092 inbound rule (see Step 5).

## Running the Pipeline

### 1. Producer - Send Data to Kafka

Open `KafkaProducer.ipynb` in Jupyter and execute to:
- Read stock market data from `data/indexProcessed.csv`
- Publish messages to Kafka topic
- Simulate real-time data streaming

### 2. Consumer - Receive and Store Data

Open `KafkaConsumer.ipynb` in Jupyter and execute to:
- Consume messages from Kafka topic
- Write data to AWS S3
- Transform and batch data as needed

### 3. Catalog Data with AWS Glue

```bash
1. Open AWS Management Console → Glue
2. Create Glue Crawler pointing to your S3 bucket
3. Run crawler to populate data catalog
4. Review schema in Glue Data Catalog
```

### 4. Query with Amazon Athena

```bash
1. Open AWS Management Console → Athena
2. Set output location to S3 bucket
3. Query the cataloged data using SQL
```

## Notes

- Refer to `command_kafka.txt` for quick reference of common Kafka CLI commands
- Ensure security groups allow inbound traffic on port 9092 for Kafka access
- Monitor AWS costs, particularly for EC2 instance hours and data transfer charges
- Consider stopping EC2 instance when not actively developing to minimize costs
- Always use public IP addresses when accessing Kafka from outside the VPC
- Keep your private key file secure and never commit it to version control

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `bin/zookeeper-server-start.sh: No such file or directory` | Running command from inside `bin/` directory, or Kafka 4.x (no Zookeeper) | `cd ~/kafka_2.13-4.2.0` first. Kafka 4.x uses KRaft — no Zookeeper needed |
| `UnsupportedClassVersionError: class file version 61.0` | Java 8 installed, Kafka 4.x requires Java 17+ | `sudo yum install java-17-amazon-corretto -y` |
| `Cannot allocate memory` on startup | t2.micro has 1GB RAM; Kafka defaults to 1GB heap | Set `export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"` before starting Kafka |
| `config/kraft/server.properties: No such file or directory` | Kafka 4.x removed the `kraft/` subfolder | Use `config/server.properties` directly |
| `No readable meta.properties files found` | Storage directory not formatted, or formatted with wrong config path | `rm -rf /tmp/kraft-combined-logs` then re-run `kafka-storage.sh format --standalone` |
| `controller.quorum.voters is not set` on format | Kafka 4.x single-node requires explicit mode flag | Add `--standalone` to the `kafka-storage.sh format` command |
| `CONTROLLER` listener error / broker fails to start | `advertised.listeners` must not include the `CONTROLLER` listener | Set `advertised.listeners=PLAINTEXT://<public-ip>:9092` only — remove `CONTROLLER` entry |
| `Timed out waiting for a node assignment` on topic creation | Kafka not running, or EC2 security group blocking port 9092 | 1. Check `ps aux \| grep kafka`. 2. Verify port 9092 inbound rule in EC2 Security Group. 3. Test with `localhost:9092` first |
| Public IP times out but `localhost:9092` works | EC2 security group missing inbound rule for port 9092 | AWS Console → EC2 → Security Groups → Add inbound rule: Custom TCP port 9092 |
| Producer/consumer commands fail with `Invalid url in bootstrap.servers` | Placeholder text `{Put the Public IP...}` not replaced | Replace with actual EC2 public IP, e.g. `54.89.203.129:9092` |
| EC2 public IP changed after restart | AWS assigns a new public IP on every stop/start unless Elastic IP is used | Check current IP in AWS Console → EC2 → Instances → Public IPv4 address |

## References

- [Apache Kafka Official Documentation](https://kafka.apache.org/documentation/)
- [AWS EC2 Getting Started](https://docs.aws.amazon.com/ec2/index.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Amazon Athena Documentation](https://docs.aws.amazon.com/athena/)