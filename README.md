# Kafka101: Comprehensive Kafka Learning & Implementation Guide

A structured, progressive learning resource for Apache Kafka deployment, from Docker-based prototyping to production-grade AWS implementations and real-world data pipelines.

---

## Table of Contents

- [Workspace Overview](#workspace-overview)
- [Quick Start](#quick-start)
- [Folder Structure](#folder-structure)
- [Project Progression](#project-progression)
- [Technology Stack](#technology-stack)
- [Key Concepts](#key-concepts)
- [How to Use This Repository](#how-to-use-this-repository)

---

## Workspace Overview

This repository contains **5 main project folders** progressing from beginner to advanced levels, plus an **old/** folder with archived and legacy content.

**Key Highlights:**
- ✅ **3 fully developed sections** (01, 02, 03)
- 📦 **Docker & EC2 deployment guides**
- 💼 **Real-world stock market data pipeline project**
- 📚 **Educational diagrams and documentation**
- 🔄 **AWS integration examples** (S3, Glue, Athena, Snowflake)

---

## Quick Start

### 🐳 Docker Quick Start (Fastest)
```bash
cd "01 getting started with kafka with docker"
docker-compose up -d
bash commands.sh
```

### 🏗️ Manual EC2 Setup (Production)
```bash
cd "02 kafka manually setup kafka on ec2"
# Follow README.md for step-by-step instructions
```

### 📈 Stock Market Project (Real-World)
```bash
cd "03 stockmarket-kafka-project"
# Follow README.md for end-to-end AWS integration
```

---

## Folder Structure

### 📁 01: Getting Started with Kafka with Docker

**Best For:** Beginners learning Kafka fundamentals

**Contents:**
- **README.md** - Educational guide covering:
  - Kafka architecture (Producers, Brokers, Consumers, Topics, Partitions)
  - Real-time data concepts
  - Visual architecture diagrams
  
- **docker-compose.yml** - Ready-to-run Docker setup:
  - Zookeeper (port 2181)
  - Kafka broker (port 9092)
  - Fully configured environment variables

- **commands.sh** - Handy CLI reference:
  - Docker management commands
  - Kafka topic operations
  - Producer/Consumer startup

- **Producer.ipynb** - Jupyter notebook
  - Python Kafka producer implementation
  - Publishing data to topics

- **Consumer.ipynb** - Jupyter notebook
  - Python Kafka consumer implementation
  - Message consumption patterns

- **images/hands-on/** - Visual guides:
  - Architecture diagrams
  - Broker configuration
  - Partitioning strategies

**Quick Commands:**
```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f kafka

# Stop services
docker-compose down
```

---

### 📁 02: Kafka Manually Setup Kafka on EC2

**Best For:** Production deployments and EC2 learning

**Key Technical Points:**
- **KRaft Mode** (Kafka 4.x): No Zookeeper required - single process architecture
- **Java 17 minimum**: Required for modern Kafka (Java 8 causes UnsupportedClassVersionError)
- **Elastic IP**: Recommended to maintain consistent IP across EC2 restarts
- **Security Group**: Port 9092 must be open for client connections

**Contents:**
- **README.md** - Detailed step-by-step guide:
  1. EC2 instance launch (t2.micro, Amazon Linux 2023)
  2. SSH setup
  3. Java 17 installation
  4. Kafka download and extraction
  5. KRaft mode configuration
  6. Security group setup
  7. Broker startup and verification
  8. Topic creation and testing
  9. Troubleshooting guide

**Important Configuration Notes:**
- `advertised.listeners` must only contain PLAINTEXT (never CONTROLLER)
- All Kafka commands must run from Kafka root directory
- Public IP changes on stop/start unless Elastic IP attached
- Storage formatting required before first run

---

### 📁 03: Stock Market Kafka Project

**Best For:** Real-world, production-like end-to-end pipeline

**Project Objective:**
Stream real-time stock market data → Apache Kafka → AWS S3 → AWS Glue → Amazon Athena

**Architecture:**
```
Stock Data Source → Kafka Producer → Kafka Broker → Kafka Consumer → AWS S3
                                                            ↓
                                                     AWS Glue (Cataloging)
                                                            ↓
                                                   Amazon Athena (SQL Queries)
```

**Contents:**
- **README.md** - Complete project documentation
- **KafkaProducer.ipynb** - Stock data producer implementation
- **KafkaConsumer.ipynb** - Consumer with S3 integration
- **command_kafka.txt** - EC2 setup commands for this project
- **NOTES.md** - Technical reference guide
- **naming-convention.txt** - AWS resource naming standards
- **data/indexProcessed.csv** - Hong Kong Stock Index (HSI) historical data
  - 11,000+ records from 1986-2023
  - Columns: Index, Date, Open, High, Low, Close, Adj Close, Volume, CloseUSD
- **secrets/kp-stockmarket-*.pem** - AWS EC2 key pair for SSH access
- **images/** - Architecture diagrams

**AWS Services Used:**
| Service | Purpose |
|---------|---------|
| EC2 | Kafka broker compute |
| S3 | Data lake storage |
| Glue | ETL and data cataloging |
| Athena | SQL analytics |
| IAM | Access control |

**Naming Convention:**
- EC2 Instance: `ec2-stockmarket-kafka-realtime-us-east1-qh`
- Key Pair: `kp-stockmarket-kafka-realtime-us-east1-qh`

---

### 📁 04: Kafka Snowflake Integration

**Status:** 🔴 Empty (Placeholder for future use)

**Intended Purpose:** Kafka-to-Snowflake direct ingestion examples

---

### 📁 05: MSK and MSK with Snowflake

**Status:** 🔴 Empty (Placeholder for future use)

**Intended Purpose:** AWS Managed Streaming for Kafka (MSK) examples with Snowflake integration

---

### 📁 old/: Archived & Legacy Content

**Status:** Deprecated but historically valuable

**Contents:**
- **01 kafka-hello-world.txt** - Windows-based Zookeeper/Kafka local setup
- **02 kafka-snowflake-integration.txt** - Kafka Connect + Snowflake setup guide
- **03 getting started with msk.txt** - AWS MSK VPC configuration
- **04 aws-msk-connector-for-snowflake.txt** - Partial connector documentation
- **hello-kafka.py** - Simple Python producer (sends 1000 test messages)
- **kafkakafka_logsserver_logs/** - Historical Kafka broker partition logs
- **kafkakafka_logszookeeper/** - Historical Zookeeper state
- **venv/** - Archived Python virtual environment
- **vpc-msk-project.drawio.png** - VPC architecture diagram

**Legacy Notes:**
- Folder contains Kafka 2.7.0 artifacts (now superseded by Kafka 4.x)
- Zookeeper mode (no longer default)
- Java 8 compatibility (now requires Java 17)

---

## Project Progression

```
BEGINNER ────────────────► INTERMEDIATE ────────────────► ADVANCED
   ↓                              ↓                            ↓
Folder 01                    Folder 02                   Folder 03
Docker Setup            Manual EC2 Setup           Stock Market Pipeline
(Local Learning)     (Production Patterns)       (Real-World AWS)
   ↓                              ↓                            ↓
5 min setup         30-45 min setup              90 min+ full setup
Zookeeper mode      KRaft mode                   End-to-end pipeline
Simple topics       Scalable topics              Data lake integration
```

---

## Technology Stack

### Core Technologies
| Component | Version | Notes |
|-----------|---------|-------|
| Apache Kafka | 2.7.0 (Docker), 4.2.0 (EC2) | Transitioning to modern KRaft mode |
| Java | 8 (legacy), 17 (modern) | Java 17 required for Kafka 4.x |
| Python | 3.7+ | Producer/Consumer implementation |
| Docker | Latest | Docker Compose for orchestration |
| Zookeeper | 3.6.3 | Legacy (replaced by KRaft in Kafka 4.x) |

### AWS Services
- **EC2** - Kafka broker compute instances
- **S3** - Data lake storage
- **Glue** - ETL and data cataloging
- **Athena** - SQL query engine
- **IAM** - Identity and access management
- **VPC** - Network isolation (MSK projects)

### Development Tools
- **Jupyter Notebooks** - Interactive development
- **Docker Compose** - Multi-container orchestration
- **SSH** - Remote EC2 access
- **Apache Kafka CLI** - Command-line management

---

## Key Concepts

### Kafka Architecture
- **Producer**: Application that publishes messages to topics
- **Broker**: Kafka server that stores messages
- **Consumer**: Application that reads messages from topics
- **Topic**: Named feed of messages (analogous to database table)
- **Partition**: Topic shard for parallelism and scalability
- **Consumer Group**: Multiple consumers processing same topic
- **Offset**: Message position within partition

### Deployment Models
1. **Docker Compose** (Development/Testing)
   - Fastest setup, fully containerized
   - Ideal for local machine learning

2. **Manual EC2** (Production)
   - KRaft mode (no Zookeeper needed)
   - Scalable across multiple instances
   - Full operational control

3. **AWS MSK** (Managed)
   - AWS-managed Kafka clusters
   - Automatic scaling and patching
   - Integrated with AWS services

### Data Flow Patterns
```
Real-time Ingestion:  Source → Kafka Producer → Broker → Consumer → Destination
Batch Processing:     S3/File → Kafka Topic → Consumer → Data Warehouse
Stream Processing:    Kafka Topic → Processor → Multiple Brokers → Analytics
```

---

## How to Use This Repository

### For Learning Kafka Basics
1. Start with **Folder 01** (Docker setup)
2. Review architecture diagrams in `images/hands-on/`
3. Run Producer.ipynb and Consumer.ipynb
4. Experiment with `commands.sh` for topic management

### For Production Deployment
1. Review **Folder 02** EC2 setup guide
2. Follow Java 17 installation steps
3. Configure KRaft mode properties
4. Set up security groups and Elastic IP
5. Verify with `commands.txt` commands

### For Real-World Integration
1. Study **Folder 03** architecture
2. Review AWS services integration (S3, Glue, Athena)
3. Run KafkaProducer.ipynb with stock data
4. Execute KafkaConsumer.ipynb to write to S3
5. Validate in AWS console

### For Snowflake Integration
1. Reference `old/02 kafka-snowflake-integration.txt`
2. Install Kafka Connect with Snowflake connector
3. Generate RSA key pairs for authentication
4. Configure connector with Snowflake credentials

### For AWS MSK
1. Reference `old/03 getting started with msk.txt`
2. Create VPC with appropriate subnets
3. Launch MSK cluster with security groups
4. Create EC2 client in same VPC
5. Test connectivity with Kafka CLI

---

## Important Notes & Best Practices

### ⚠️ Critical Configuration Points

**Kafka 4.x with KRaft Mode:**
- ✅ No Zookeeper required
- ✅ Single metadata process
- ✅ Better performance
- ⚠️ Java 17+ required (Java 8 incompatible)

**EC2 Considerations:**
- Always use Elastic IP for stable connectivity
- Open port 9092 (or custom) in Security Group
- Keep `advertised.listeners` as PLAINTEXT only
- Run Kafka commands from Kafka root directory

**Docker Setup:**
- Network isolation requires using container names for connections
- Zookeeper must be healthy before Kafka starts
- Port mapping: 2181 (Zookeeper), 9092 (Kafka)

### 📋 Pre-Flight Checks

Before starting any setup:
- [ ] Java 17 installed (for Kafka 4.x)
- [ ] Docker/Docker Compose available (for Folder 01)
- [ ] SSH key pair ready (for EC2 projects)
- [ ] AWS credentials configured (for S3/Glue/Athena)
- [ ] Sufficient disk space for data volumes

### 🔍 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| `UnsupportedClassVersionError` | Upgrade Java to 17+ |
| EC2 IP changed after restart | Use Elastic IP |
| Cannot connect to broker | Check Security Group port 9092 |
| Zookeeper won't start | Check disk space and permissions |
| Consumer group lag | Increase parallelism with partitions |

---

## File Organization

```
kafka101/
├── README.md                                    ← You are here
├── 01 getting started with kafka with docker/
│   ├── README.md
│   ├── docker-compose.yml
│   ├── commands.sh
│   ├── Producer.ipynb
│   ├── Consumer.ipynb
│   └── images/
├── 02 kafka manually setup kafka on ec2/
│   └── README.md
├── 03 stockmarket-kafka-project/
│   ├── README.md
│   ├── NOTES.md
│   ├── command_kafka.txt
│   ├── naming-convention.txt
│   ├── KafkaProducer.ipynb
│   ├── KafkaConsumer.ipynb
│   ├── data/
│   ├── secrets/
│   └── images/
├── 04 kafka snowflake integration/
├── 05 msk and msk with snowflake/
└── old/
    ├── 01 kafka-hello-world.txt
    ├── 02 kafka-snowflake-integration.txt
    ├── 03 getting started with msk.txt
    ├── 04 aws-msk-connector-for-snowflake.txt
    ├── hello-kafka.py
    ├── kafkakafka_logsserver_logs/
    ├── kafkakafka_logszookeeper/
    └── venv/
```

---

## Next Steps

1. **Choose Your Path:**
   - Learning Mode → Start with Folder 01
   - Deploying to AWS → Start with Folder 02
   - Building Data Pipelines → Start with Folder 03

2. **Follow Specific README:**
   - Each folder has its own detailed README.md

3. **Review Architecture Diagrams:**
   - Visual guides in `images/` folders

4. **Run Example Code:**
   - Execute Jupyter notebooks for hands-on practice

5. **Reference Command Files:**
   - Use `commands.sh` and `*.txt` files for CLI operations

---

## Additional Resources

- **Apache Kafka Documentation**: https://kafka.apache.org/documentation/
- **AWS Glue Documentation**: https://docs.aws.amazon.com/glue/
- **Amazon Athena Documentation**: https://docs.aws.amazon.com/athena/
- **Docker Compose**: https://docs.docker.com/compose/

---

## License & Attribution

This workspace contains educational and reference materials for Apache Kafka implementations.

---

**Last Updated:** April 2026  
**Kafka Versions Covered:** 2.7.0 → 4.2.0  
**AWS Services:** EC2, S3, Glue, Athena, IAM, VPC, MSK
