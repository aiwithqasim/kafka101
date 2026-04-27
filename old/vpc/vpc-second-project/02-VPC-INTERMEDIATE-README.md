# VPC Intermediate: Multi-Subnet Architecture - Beginner's Guide

## Overview
This guide teaches you how to build a more sophisticated VPC with both **public and private subnets**. This is a production-like architecture where different tiers of your application are isolated from each other.

---

## Architecture Diagram

![alt text](./02%20vpc-intermediate.drawio.png)


## End Goal

![alt text](./old/vpc/vpc-second-project/End-Goal.png)

## What You're Building

```
Internet Users
       ↓
Internet Gateway
       ↓
   VPC (10.0.0.0/16)
   ├── Public Subnet (10.0.0.0/24)
   │   ├── EC2 Instance (Web Server)
   │   └── Route Table: 0.0.0.0/0 → IGW
   │
   └── Private Subnet (10.0.1.0/24)
       ├── EC2 Instance (Database Server)
       └── Route Table: Only local traffic
```

---

## Why Public and Private Subnets?

**Security by Isolation:**
- **Public Subnet**: Your web server needs to be accessible from the internet
- **Private Subnet**: Your database should NOT be accessible from the internet
- If a hacker breaks into your web server, they still can't directly access your database

**Real-world Example:**
```
Imagine your e-commerce store:
- Public Subnet = Your checkout page (customers visit)
- Private Subnet = Your customer database (hidden from customers)
- Only your web server can talk to the database
- The database cannot be reached directly from the internet
```

---

## Prerequisites
- Completed "01-VPC-INTRO-README.md"
- Basic understanding of VPC, Subnets, and EC2
- About 45 minutes

---

## Step-by-Step Implementation

### STEP 1: Create a New VPC (or Use Existing)

If you already have "my-first-vpc" from the intro guide, you can use that. Otherwise:

1. Go to VPC Dashboard → "VPCs"
2. Click "Create VPC"
3. Fill in:
   ```
   VPC Name:        intermediate-vpc
   IPv4 CIDR Block: 10.0.0.0/16
   ```
4. Click "Create VPC"
5. ✅ VPC Created!

---

### STEP 2: Create Public Subnet

A public subnet is one that has a route to the Internet Gateway.

**How to Create:**

1. Go to "Subnets" in VPC Dashboard
2. Click "Create Subnet"
3. Fill in:
   ```
   VPC ID:               intermediate-vpc
   Subnet Name:          public-subnet-a
   Availability Zone:    us-east-1a
   IPv4 CIDR Block:      10.0.1.0/24
   ```

**IP Address Breakdown:**
```
10.0.0.0/24 = IPs from 10.0.0.0 to 10.0.0.255
- 10.0.0.0: Network address (reserved)
- 10.0.0.1-10.0.0.3: AWS reserved
- 10.0.0.4-10.0.0.254: Available for EC2 instances (251 usable)
- 10.0.0.255: Broadcast address (reserved)
```

4. Click "Create Subnet"
5. ✅ Public Subnet Created!

---

### STEP 3: Create Private Subnet

A private subnet has NO route to the Internet Gateway.

**How to Create:**

1. Go to "Subnets" in VPC Dashboard
2. Click "Create Subnet"
3. Fill in:
   ```
   VPC ID:               intermediate-vpc
   Subnet Name:          private-subnet-b
   Availability Zone:    us-east-1b (different from public subnet)
   IPv4 CIDR Block:      10.0.2.0/24
   ```

**Why different Availability Zone?**
- If the data center for us-east-1a has issues, your private subnet will still be available in us-east-1b
- This provides redundancy and high availability

4. Click "Create Subnet"
5. ✅ Private Subnet Created!

---

### STEP 4: Create Internet Gateway

1. Go to "Internet Gateways"
2. Click "Create Internet Gateway"
3. Fill in:
   ```
   Name: intermediate-igw
   ```
4. Click "Create Internet Gateway"
5. Select the newly created IGW
6. Click "Attach to VPC"
7. Select "intermediate-vpc"
8. Click "Attach Internet Gateway"
9. ✅ Internet Gateway Created and Attached!

---

### STEP 5: Create and Configure Route Tables

You need **two route tables**:
- One for the public subnet (with route to Internet Gateway)
- One for the private subnet (with no internet access)

**Configure Default Route Table:**

1. Go to **VPC Dashboard** → **"Route Tables"**
2. You should see the default route table for "intermediate-vpc" (check the VPC column)
3. Select the default route table and rename it "public-route-table"
4. Click **"Routes"** tab
5. You should see only:
   ```
   Destination    Target    Status
   10.0.0.0/16  → local     Active
   ```
6. Click **"Edit Routes"**
7. Click **"Add Route"**
8. Fill in:
   ```
   Destination:     0.0.0.0/0  (Anywhere on the internet)
   Target:          Internet Gateway
   Select:          my-first-igw

**Create Private Route Table:**

1. Go to "Route Tables"
2. Click "Create Route Table"
3. Fill in:
   ```
   Name:   private-route-table
   VPC:    intermediate-vpc
   ```
4. Click "Create Route Table"
5. Select the newly created route table
6. Click "Subnet Associations" tab
7. Click "Edit Subnet Associations"
8. Select "private-subnet-b"
9. Click "Save Associations"

**Important**: Do NOT add any routes to this private route table. It should only have local routes (10.0.0.0/16).

10. ✅ Private Route Table Created and Associated!

---

### STEP 6: Create Security Groups

You need **two security groups**:
- One for web servers in public subnet
- One for database servers in private subnet

**Create Web Server Security Group:**

1. Search for "Security Groups"
2. Click "Create Security Group"
3. Fill in:
   ```
   Name:           web-sg
   Description:    Security group for web servers
   VPC:            intermediate-vpc
   ```
4. Add Inbound Rules:
   - **HTTP**:
     ```
     Type:       HTTP
     Protocol:   TCP
     Port:       80
     Source:     0.0.0.0/0 (anyone from internet)
     ```
   - **HTTPS**:
     ```
     Type:       HTTPS
     Protocol:   TCP
     Port:       443
     Source:     0.0.0.0/0
     ```
   - **SSH** (for administration):
     ```
     Type:       SSH
     Protocol:   TCP
     Port:       22
     Source:     0.0.0.0/0 (or restrict to your IP)
     ```
     you can restrict to your IP by selecting My IP in source

5. Click "Create Security Group"
6. ✅ Web Server Security Group Created!

**Create Database Security Group:**

1. Click "Create Security Group"
2. Fill in:
   ```
   Name:           db-sg
   Description:    Security group for databases
   VPC:            intermediate-vpc
   ```
3. Add Inbound Rules:
   - **MySQL** (only from web servers):
     ```
     Type:       MySQL/Aurora
     Protocol:   TCP
     Port:       3306
     Source:     web-sg (IMPORTANT: Use the web-sg security group!)
     ```
   
   **Why select web-sg as source?**
   - This means: "Only allow traffic from instances in web-sg"
   - So only your web servers can connect to the database
   - This is much more secure than allowing traffic from anywhere (0.0.0.0/0)

   - **SSH** (for administration from web server):
     ```
     Type:       SSH
     Protocol:   TCP
     Port:       22
     Source:     web-sg ip address (10.0.1.143/32)
     ```
   - **ICMP** (for administration from web server):
      ```
      Type:       ALL ICMP-IPv4
      Protocol:   ICMP
      Port:       ALL
      Source:     web-sg ip address (10.0.1.143/32)
      ```
   
   **Why use web-sg for SSH?**
   - Only the web server can SSH into the database server
   - The database remains hidden and inaccessible from the internet
   - Secure bastion host pattern: Web server acts as gateway to database

4. Click "Create Security Group"
5. ✅ Database Security Group Created!

---

### STEP 7: Launch Web Server EC2 Instance (Public Subnet)

**How to Launch:**

1. Go to EC2 Dashboard
2. Click "Instances"
3. Click "Launch Instances"
4. Fill in:

**Name and OS:**
```
Name:               web-server
Operating System:   Amazon Linux 2
Instance Type:      t2.micro
```

**Key Pair:**
```
Create a key value pair by clicking in Create new key pair name it "kp-web-server" select RSA for key pair type and .pem for private key file format. Click on create key-pair it will download the file.
```

**Network Settings:**
```
VPC:                      intermediate-vpc
Subnet:                   public-subnet-a
Auto-assign Public IP:    Enable ✓ (IMPORTANT for public subnet)
Security Group:           web-sg
```

**Storage:**
```
Volume Size: 8 GB
```

5. Review settings
6. Click "Launch Instances"
7. Wait for instance to reach "Running" state
8. ✅ Web Server Launched!

**Get the Public IP:**
- Go to Instances
- Select your web-server instance
- In Details tab, find "Public IPv4 Address"
- Note this down

---

### STEP 8: Launch Database Server EC2 Instance (Private Subnet)

**How to Launch:**

1. Click "Launch Instances"
2. Fill in:

**Name and OS:**
```
Name:               database-server
Operating System:   Amazon Linux 2
Instance Type:      t2.micro
```

**Key Pair:**
```
Create a key value pair by clicking in Create new key pair name it "kp-database-server" select RSA for key pair type and .pem for private key file format. Click on create key-pair it will download the file.
```

**Network Settings:**
```
VPC:                      intermediate-vpc
Subnet:                   private-subnet-b
Auto-assign Public IP:    Disable ✗ (IMPORTANT for private subnet)
Security Group:           db-sg
```

**Storage:**
```
Volume Size: 8 GB
```

3. Review settings
4. Click "Launch Instances"
5. Wait for instance to reach "Running" state
6. ✅ Database Server Launched!

---

### STEP 9: Connect to Web Server and Copy Database Key

**Step 1: Copy the database key to the web server (from your local computer):**



Since you'll need to access the database server FROM the web server, copy the database key file to the web server:

`make sure that you change the ip address for below command according to your instance.`

```bash
# Copy kp-database-server.pem to web server's home directory
scp -i kp-web-server.pem kp-database-server.pem ec2-user@100.53.231.39:/home/ec2-user/
```

**Why?** The web server needs the database server's key to SSH into it from the private network.

**Step 2: Connect to the web server:**

Now SSH into the web server using the web server's key:

`make sure that you change the ip address for below command according to your instance.`

```bash
ssh -i kp-web-server.pem ec2-user@100.53.231.39
```

Once connected, you're now inside your web server instance!

---

### STEP 10: Access Database Server from Web Server

Now you're SSH-ed into the web server. From here, you can access the database server in the private subnet!

**From Web Server terminal, SSH to the database server:**

The database server is in the private subnet with private IP 10.0.2.47. Use the database key you just copied:

`make sure that you change the ip address for below command according to your instance.`

```bash
chmod 400 "kp-database-server.pem"
ssh -i ~/kp-database-server.pem ec2-user@10.0.2.47
```

You can now reach it! ✅

**Important: Key Separation Benefits**
- 🔒 Web server has its own key (kp-web-server.pem) - for your local access
- 🔒 Database server has its own key (kp-database-server.pem) - stored on web server only
- 🔒 If web server is compromised, database key is isolated
- 🔒 Better security than using the same key for both

**Why can the web server reach the database?**
- Both are in the same VPC (10.0.0.0/16)
- The security group rules allow it (web-sg can reach db-sg on port 22)
- Network routes allow local VPC traffic (both subnets are local routes)
- Database is HIDDEN from internet (no public IP)

---

### STEP 11: Verify Private Subnet Isolation

Now you're on the database server (10.0.2.47) in the private subnet!

**Verify it cannot reach the internet:**

```bash
ping -c 5 google.com
```

**Expected Output:**
```
PING google.com (142.251.179.139) 56(84) bytes of data.

--- google.com ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4134ms
```

**What This Means:** ✅
- ✅ DNS works (google.com → 142.251.179.139 resolved)
- ❌ Actual internet traffic is blocked (100% packet loss)
- ✅ This is secure and expected!

**Why?**
The private subnet's route table only has a local route (10.0.0.0/16 → local). There's no route to the internet (no NAT Gateway, no IGW), so packets destined for external IPs are dropped. The database server cannot initiate outbound connections to the internet, keeping it completely isolated and secure.

**Verify you can reach other servers in the VPC:**



```bash
ctrl + d
ping <enter private subnet(ec2) ip>  # Web server in the VPC
```

This should work! ✅

## Communication Flow Summary

```
1. User Request:
   User → Internet → IGW → Web Server (public subnet)

2. Application Logic:
   Web Server → Private Network → Database Server (private subnet)

3. Response:
   Database Server → Web Server → IGW → Internet → User
```

---

## Security Benefits

✅ **Web Server is Publicly Accessible:**
- Users can reach it from the internet
- It serves web pages and handles requests

✅ **Database Server is Completely Hidden:**
- No public IP address
- Cannot reach the internet
- Only accessible from web servers via private network
- Even if web server is hacked, database is in a separate security group

✅ **Defense in Depth:**
- Multiple layers of security
- Network isolation (public vs private subnets)
- Security group rules (only web can talk to database)
- No direct internet access for database

---

## Testing Checklist

Run through these tests to verify everything works:

- [ ] Can you SSH into the web server? ✅
- [ ] Can you ping google.com from web server? ✅
- [ ] Can you ping database server's private IP from web server? ✅
- [ ] Can you NOT ping google.com from database server? ✅
- [ ] Can you SSH from web server into database server? ✅

---

## Troubleshooting

**Can't connect to web server?**
- Check web-sg allows SSH (port 22)
- Verify public IP is assigned
- Check your key file permissions

**Can't connect from web server to database?**
- Verify database server has private IP in 10.0.1.0/24 range
- Check db-sg allows MySQL from web-sg
- Check if both instances are running

**Database server has internet access (shouldn't!)?**
- Verify private-route-table has NO route to IGW
- Check if you accidentally added a route

---

## Cost Estimate
- **VPCs, Subnets, Route Tables, IGWs, Security Groups**: All FREE
- **2× EC2 t2.micro instances**: Free (under AWS free tier for first 12 months)
- **Total**: FREE

---

## Key Concepts Learned

| Concept | What It Does | Example |
|---------|-------------|---------|
| Public Subnet | Connected to Internet Gateway | Web Server Subnet |
| Private Subnet | NOT connected to Internet Gateway | Database Server Subnet |
| Route Table | Rules for routing traffic | public-route-table |
| IGW Route | Rule to route internet traffic | 0.0.0.0/0 → IGW |
| Security Group Chaining | Using SG as source in another SG | web-sg → db-sg |
| Availability Zones | Physical data centers | us-east-1a, us-east-1b |

---

## Next Steps

1. Try launching a second web server in public subnet for redundancy
2. Learn about **NAT Gateways** for private subnet internet access (see "03-VPC-NATGATEWAY-README.md")
3. Implement load balancing across multiple web servers
4. Set up a real database (RDS)

---

## Cleanup: Delete Resources When Done

When you're finished, **delete all resources to avoid unnecessary charges**. Follow the steps in this exact order!

### Step 1: Terminate EC2 Instances

1. Go to EC2 Dashboard → Instances
2. Select "web-server" instance
3. Click "Instance State" → "Terminate Instance"
4. Confirm
5. Select "database-server" instance
6. Click "Instance State" → "Terminate Instance"
7. Confirm
8. Wait for both to reach "Terminated" state
9. ✅ Instances Terminated!

**Critical:** Must terminate instances BEFORE deleting VPC!

---

### Step 2: Delete Internet Gateway

1. Go to VPC Dashboard → "Internet Gateways"
2. Select "intermediate-igw"
3. Click "Actions" → "Detach from VPC"
4. Select your VPC and confirm
5. Select the IGW again
6. Click "Actions" → "Delete Internet Gateway"
7. ✅ IGW Deleted!

---

### Step 3: Delete Route Tables

1. Go to VPC → "Route Tables"
2. Find "public-route-table"
3. Click "Actions" → "Delete Route Table"
4. Confirm
5. Find "private-route-table"
6. Click "Actions" → "Delete Route Table"
7. Confirm
8. ✅ Route Tables Deleted!

---

### Step 4: Delete Subnets

1. Go to VPC → "Subnets"
2. Select "public-subnet-a"
3. Click "Actions" → "Delete Subnet"
4. Confirm
5. Select "private-subnet-b"
6. Click "Actions" → "Delete Subnet"
7. Confirm
8. ✅ Subnets Deleted!

---

### Step 5: Delete VPC

1. Go to VPC → "VPCs"
2. Select "intermediate-vpc"
3. Click "Actions" → "Delete VPC"
4. Confirm (automatically deletes any remaining subnets)
5. ✅ VPC Deleted!

---

### Step 6: Delete Security Groups (Optional)

1. Go to EC2 → "Security Groups"
2. Select "web-sg"
3. Click "Actions" → "Delete Security Group"
4. Confirm
5. Select "db-sg"
6. Click "Actions" → "Delete Security Group"
7. Confirm
8. ✅ Security Groups Deleted!

**Note:** Default security group cannot be deleted.

---

## Cleanup Checklist

- [ ] Web server terminated?
- [ ] Database server terminated?
- [ ] Internet Gateway detached and deleted?
- [ ] Public route table deleted?
- [ ] Private route table deleted?
- [ ] Public subnet deleted?
- [ ] Private subnet deleted?
- [ ] VPC deleted?
- [ ] Security groups deleted (optional)?

---

## Cost Summary

If you completed this guide within 1 month:

```
AWS Service              Cost
─────────────────────────────
VPC & Subnets            FREE ✅
Route Tables             FREE ✅
Internet Gateway         FREE ✅
Security Groups          FREE ✅
2× EC2 t2.micro          FREE ✅ (free tier, 12 months)
─────────────────────────────
Total Cost               $0.00 ✅
```

No charges if within free tier limits!

---

## Prevention: Stop vs Terminate

If you want to keep your setup but pause it:

**Stop Instances (Cheaper):**
```
Cost: $0.10/GB storage only (no compute charge)
Action: Instance State → Stop
Restart: Instance State → Start (anytime)
Data: Preserved
Time to restart: ~1 minute
```

**Terminate Instances (Deletes Data):**
```
Cost: $0.00 (no charges)
Action: Instance State → Terminate
Restart: Must launch new instance
Data: Lost forever
```

💡 **Strategy:**
- Taking a 1-week break? STOP instances
- Done learning? TERMINATE instances

---

## Verify All Deleted

To confirm everything is deleted:

1. Go to VPC Dashboard
2. Check "VPCs" - should not see "intermediate-vpc"
3. Check "Subnets" - should not see your subnets
4. Check "Internet Gateways" - should not see "intermediate-igw"
5. Check "Route Tables" - should not see your custom tables
6. Go to EC2 → Instances - should not see your instances
7. Go to EC2 → Security Groups - should not see your SGs

✅ If all above show nothing, you've successfully cleaned up!

---

## If You Get Deletion Errors

**"Cannot delete VPC - has dependencies"**
- Verify all EC2 instances are terminated
- Verify IGW is detached
- Verify all subnets are deleted
- Try deleting VPC again

**"Cannot delete subnet - has dependencies"**
- Check if instances are still running
- Check if ENIs (network interfaces) exist
- Terminate all instances first

**"Cannot delete security group"**
- Some security groups are in use by instances
- Terminate instances first
- Then delete security group

---

**Great work! You've built a production-like VPC architecture!** 🎉
