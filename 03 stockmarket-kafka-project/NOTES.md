## Kafka Fundamentals

### What is Apache Kafka?

**Definition:** Apache Kafka is a distributed event store and stream processing platform designed for high-throughput, real-time data streaming.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Events** | Actions taken online (clicks, likes, shares, transactions) |
| **Distributed Event Store** | Events distributed and stored across multiple networks for reliability |
| **Stream Processing** | Continuous calculations on endless data streams, similar to flowing water |
| **Real-Time Applications** | Used for instant notifications in e-commerce, banking, and analytics |

### Use Cases
- Real-time notifications for e-commerce platforms
- Financial transaction processing
- Web analytics and user behavior tracking
- Social media activity feeds
- IoT sensor data collection

---

## Kafka Architecture

### Core Components

**Producers**
- Entities that generate and send data to Kafka
- Examples: sensors, web applications, databases
- Can be written in various programming languages (Python, Java, etc.)

**Brokers**
- Kafka cluster servers that store and serve messages
- One physical node = one broker
- Multiple brokers work together as a cluster for fault tolerance

**Consumers**
- Entities that read and process data from Kafka topics
- Can subscribe to one or multiple topics
- Support multiple programming languages

**Zookeeper**
- Manages the Kafka cluster orchestration
- Ensures cluster stability and availability
- Handles access control and coordination

### Topics and Partitions

**Topics:** Logical categories where data is organized
- Example: `stock-prices`, `market-orders`, `trade-alerts`
- Can have multiple consumers reading the same topic

**Partitions:** Sub-divisions of a topic
- Each partition stores ordered messages
- Enables parallel processing and horizontal scaling
- Example: partition by customer ID or stock symbol for efficient retrieval

### Log Files and Data Management

**Log Files:**
- Incoming events are appended sequentially to log files
- Maintains order of events
- Immutable append-only structure

**Data Replication:**
- Data replicated across multiple brokers
- Ensures fault tolerance and high availability
- Configurable replication factor per topic