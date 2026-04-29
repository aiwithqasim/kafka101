# AWS VPC + EC2 + DynamoDB + S3 via VPC Endpoint

A complete proof-of-concept (POC) demonstrating how to host workloads on AWS using a VPC with public/private subnets, NAT Gateway, and VPC Endpoints to securely access DynamoDB and S3 — without traffic ever leaving the AWS network.

![Uploading Architechture Diagram.jpg…]()


---

## Architecture Overview

```
Internet
    |
Internet Gateway
    |
┌─────────────────────────────────────────────┐
│               VPC (172.16.0.0/16)           │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │         Public Subnet                │   │
│  │         172.16.0.0/24               │   │
│  │                                      │   │
│  │   pub-ec2  ──►  Route Table         │   │
│  │                 0.0.0.0/0 → IGW     │   │
│  │                 NAT Gateway          │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │         Private Subnet               │   │
│  │         172.16.1.0/24               │   │
│  │                                      │   │
│  │   prt-ec2  ──►  Route Table         │   │
│  │                 0.0.0.0/0 → NAT     │   │
│  │                 VPC Endpoint ──────────────► DynamoDB
│  │                               └───────────► S3
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## What This Project Covers

- Creating a custom VPC with public and private subnets
- Launching EC2 instances in each subnet
- Configuring an Internet Gateway and NAT Gateway
- Setting up route tables for public and private traffic
- Accessing a private EC2 via SSH jump through the public EC2
- Creating a DynamoDB table and loading data using Python (boto3)
- Creating an S3 bucket and uploading data
- Creating VPC Endpoints for DynamoDB and S3 so private EC2 traffic never touches the internet
- IAM role configuration for EC2 to access AWS services

---

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed locally (optional)
- A `.pem` key pair downloaded (e.g. `mua-dev.pem`)
- Python 3 and pip3 available on EC2

---

## Phase 1 — VPC & Networking Setup

### Step 1: Create the VPC

| Setting | Value |
|---------|-------|
| Name | `virtual-private-cloud` |
| IPv4 CIDR | `172.16.0.0/16` |
| Host range | `172.16.0.1 – 172.16.255.254` |

> VPC Console → Create VPC → enter above values → Create

---

### Step 2: Create Two Subnets

**Public Subnet:**

| Setting | Value |
|---------|-------|
| Name | `subnet1-virtual-private-cloud` |
| CIDR | `172.16.0.0/24` |
| Auto-assign public IP | **Enabled** |

**Private Subnet:**

| Setting | Value |
|---------|-------|
| Name | `subnet2-virtual-private-cloud` |
| CIDR | `172.16.1.0/24` |
| Auto-assign public IP | Disabled |

---

### Step 3: Create & Attach Internet Gateway

- VPC Console → Internet Gateways → Create
- Name: `igw-virtual-private-cloud`
- After creation → Actions → **Attach to VPC** → select your VPC

---

### Step 4: Create Two Route Tables

**Public Route Table:**
- Name: `public-route`
- Add route: `0.0.0.0/0 → Internet Gateway`
- Associate with: public subnet

**Private Route Table:**
- Name: `private-route`
- No internet route yet (added after NAT Gateway)
- Associate with: private subnet

---

## Phase 2 — IAM Role

### Step 5: Create IAM Role for EC2

- IAM Console → Roles → Create Role
- Trusted entity: **EC2**
- Name: `my-vpc-ec2-s3-dynamodb-access`
- Attach policies:
  - `AmazonDynamoDBFullAccess`
  - `AmazonS3FullAccess`

> This role allows EC2 instances to access DynamoDB and S3 without hardcoded credentials.

---

## Phase 3 — EC2 Instances

### Step 6: Launch pub-ec2 (Public Subnet)

| Setting | Value |
|---------|-------|
| Name | `pub-ec2-virtual-private-cloud` |
| AMI | Amazon Linux 2023 |
| Subnet | Public subnet |
| Auto-assign public IP | Enabled |
| IAM Role | `my-vpc-ec2-s3-dynamodb-access` |
| Key pair | `mua-dev.pem` |
| Security Group | Allow SSH (port 22) from your IP |

---

### Step 7: Launch prt-ec2 (Private Subnet)

| Setting | Value |
|---------|-------|
| Name | `prt-ec2-virtual-private-cloud` |
| AMI | Amazon Linux 2023 |
| Subnet | Private subnet |
| Auto-assign public IP | Disabled |
| IAM Role | `my-vpc-ec2-s3-dynamodb-access` |
| Key pair | `mua-dev.pem` |
| Security Group | Allow SSH (port 22) from `172.16.0.0/24` |

> The private EC2 security group must allow SSH from the **public subnet CIDR**, not the internet.

---

## Phase 4 — NAT Gateway

### Step 8: Create NAT Gateway

- VPC Console → NAT Gateways → Create
- Subnet: **public subnet** (NAT must live in public subnet)
- Elastic IP: Allocate new
- Name: `nat-virtual-private-cloud`

### Step 9: Update Private Route Table

- Add route: `0.0.0.0/0 → NAT Gateway`

> This allows the private EC2 to reach the internet for software installation (e.g. pip3, boto3).

---

## Phase 5 — SSH Access

### Step 10: Set Key Permissions (Local Machine)

```bash
chmod 400 "mua-dev.pem"
```

### Step 11: Copy .pem File to pub-ec2

```bash
scp -i mua-dev.pem mua-dev.pem ec2-user@<pub-ec2-public-ip>:/home/ec2-user/
```

### Step 12: SSH into pub-ec2

```bash
ssh -i "mua-dev.pem" ec2-user@<pub-ec2-public-ip>
```

### Step 13: From pub-ec2, SSH into prt-ec2

```bash
# Inside pub-ec2:
chmod 400 mua-dev.pem
ssh -i "mua-dev.pem" ec2-user@172.16.1.132
```

> **One-liner alternative using ProxyJump (from local machine):**
> ```bash
> ssh -i "mua-dev.pem" \
>     -o ProxyJump="ec2-user@<pub-ec2-public-ip>" \
>     ec2-user@172.16.1.132
> ```

### Step 14: Configure AWS Region on EC2

```bash
aws configure
# AWS Access Key ID: (leave blank — IAM role handles this)
# AWS Secret Access Key: (leave blank)
# Default region name: us-east-1
# Default output format: (leave blank)
```

> Since an IAM role is attached, **do not enter access keys**. If you accidentally enter them, clear with:
> ```bash
> rm -rf ~/.aws/credentials
> ```

---

## Phase 6 — DynamoDB

### Step 15: Create DynamoDB Table (AWS Console)

| Setting | Value |
|---------|-------|
| Table name | `dynamodb-my-mpc-ec2-vpc-endpoint` |
| Partition key | `roll_no` (String) |
| Billing mode | On-demand |

### Step 16: Verify Table from EC2

```bash
aws dynamodb list-tables --region us-east-1
```

Expected output:
```json
{
    "TableNames": [
        "dynamodb-my-mpc-ec2-vpc-endpoint"
    ]
}
```

### Step 17: Install Python Dependencies on EC2

```bash
sudo dnf install python3-pip -y
pip3 install boto3
```

### Step 18: Python Script to Load Data

**`vpc-dynamodb.py`**
```python
import boto3
import json

client_dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = client_dynamo.Table("dynamodb-my-mpc-ec2-vpc-endpoint")

with open('./data-vpc-dynamodb.json', 'r') as datafile:
    records = json.load(datafile)

count = 0
for i in records:
    i['roll_no'] = str(count)
    i['X'] = str(i['X'])
    i['Y'] = str(i['Y'])
    print(i)
    response = table.put_item(Item=i)
    count += 1
```

### Step 19: Copy Script & Data to EC2, Then Run

```bash
# From local machine — copy files to pub-ec2
scp -i mua-dev.pem vpc-dynamodb.py data-vpc-dynamodb.json \
    ec2-user@<pub-ec2-public-ip>:/home/ec2-user/

# From pub-ec2 — copy to prt-ec2
scp -i mua-dev.pem vpc-dynamodb.py data-vpc-dynamodb.json \
    ec2-user@172.16.1.132:/home/ec2-user/

# From inside prt-ec2 — run the script
python3 vpc-dynamodb.py
```

### Step 20: Validate Data in DynamoDB Console

- DynamoDB Console → Tables → `dynamodb-my-mpc-ec2-vpc-endpoint`
- Click **Explore table items** — you should see 44 records (Anscombe's Quartet dataset)

---

## Phase 7 — S3

### Step 21: Create S3 Bucket (AWS Console)

| Setting | Value |
|---------|-------|
| Bucket name | `s3-stock-prices-mua` |
| Region | `us-east-1` |
| Block all public access | Enabled |

### Step 22: Upload Data to S3 from EC2

```bash
aws s3 cp data-vpc-dynamodb.json s3://s3-stock-prices-mua/
```

Expected output:
```
upload: ./data-vpc-dynamodb.json to s3://s3-stock-prices-mua/data-vpc-dynamodb.json
```

### Step 23: Verify S3 Upload

```bash
aws s3 ls s3://s3-stock-prices-mua
```

---

## Phase 8 — VPC Endpoints

VPC Endpoints allow the private EC2 to reach DynamoDB and S3 **without going through the internet or NAT Gateway**.

### Step 24: Create DynamoDB VPC Endpoint

- VPC Console → Endpoints → Create endpoint
- Service: `com.amazonaws.us-east-1.dynamodb` → **Gateway** type
- VPC: your VPC
- Route table: **private route table**
- Click **Create endpoint**

### Step 25: Create S3 VPC Endpoint

- VPC Console → Endpoints → Create endpoint
- Service: `com.amazonaws.us-east-1.s3` → **Gateway** type
- VPC: your VPC
- Route table: **private route table**
- Click **Create endpoint**

### Step 26: Verify Both Endpoints

In VPC Console → Endpoints you should see:

| Service | Type | Status | Route Table |
|---------|------|--------|-------------|
| `dynamodb` | Gateway | Available ✅ | private-route |
| `s3` | Gateway | Available ✅ | private-route |

### Step 27: Verify S3 Access from prt-ec2

```bash
aws s3 ls s3://s3-stock-prices-mua
```

> Traffic now flows: `prt-ec2 → VPC Endpoint → S3/DynamoDB` with **no internet exposure**.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Connection timed out` when SSHing to private IP | Trying to SSH directly from local to private EC2 | SSH into pub-ec2 first, then jump to prt-ec2 |
| `InvalidSignatureException` on AWS CLI | Hardcoded credentials conflicting with IAM role | Run `rm -rf ~/.aws/credentials` |
| `AccessDenied` on S3 PutObject | Role only had `S3ReadOnlyAccess` | Replace with `AmazonS3FullAccess` in IAM role |
| `No public IPv4 address` on prt-ec2 connect | Private EC2 has no public IP (by design) | Use SSH jump via pub-ec2 |

---

## Cleanup (Important — Avoid Charges)

Delete resources in this order:

```
1. Terminate both EC2 instances
2. Delete NAT Gateway
3. Release Elastic IP
4. Delete VPC Endpoints
5. Delete Internet Gateway (detach from VPC first)
6. Delete both Route Tables (custom ones)
7. Delete both Subnets
8. Delete the VPC
9. Delete the DynamoDB table
10. Empty and delete the S3 bucket
11. Delete the IAM Role
```

> ⚠️ **NAT Gateway and Elastic IP are the most common sources of unexpected charges — always delete these first.**

---

## Dataset

The project uses **Anscombe's Quartet** — a classic statistics dataset with 4 series (I, II, III, IV), each containing 11 data points (X, Y values). 44 records total are loaded into DynamoDB.

---

## Tech Stack

| Service | Purpose |
|---------|---------|
| AWS VPC | Isolated virtual network |
| EC2 (Amazon Linux 2023) | Compute — public and private instances |
| Internet Gateway | Public internet access for public subnet |
| NAT Gateway | Outbound internet for private subnet |
| DynamoDB | NoSQL database — stores Anscombe's Quartet |
| S3 | Object storage — stores raw JSON data file |
| VPC Endpoint (Gateway) | Private connectivity to DynamoDB and S3 |
| IAM Role | Credential-free AWS service access from EC2 |
| Python + boto3 | Script to load data into DynamoDB |

---

## Author

**Muhammad Umair Ashraf**  
AWS Data Engineering Project — VPC + DynamoDB + S3 POC
