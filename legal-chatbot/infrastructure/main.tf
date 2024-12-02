provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "legal_chatbot_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name         = "LegalChatbotVPC"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "legal_chatbot_igw" {
  vpc_id = aws_vpc.legal_chatbot_vpc.id

  tags = {
    Name         = "LegalChatbotIGW"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "internet-gateway"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.legal_chatbot_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name         = "PublicSubnet"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "subnet"
  }
}

# Route Table
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.legal_chatbot_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.legal_chatbot_igw.id
  }

  tags = {
    Name         = "PublicRouteTable"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "route-table"
  }
}

# Route Table Association
resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

# S3 Bucket for Documents
resource "aws_s3_bucket" "documento_bucket" {
  bucket = "legal-chatbot-documentos-${random_string.bucket_suffix.result}"

  tags = {
    Name         = "LegalChatbotDocuments"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "s3-bucket"
  }
}

# Random string to ensure unique bucket name
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "documento_bucket_versioning" {
  bucket = aws_s3_bucket.documento_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "documento_bucket_encryption" {
  bucket = aws_s3_bucket.documento_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Security Group for EC2
resource "aws_security_group" "chatbot_security_group" {
  name   = "ChatbotSecurityGroup"
  vpc_id = aws_vpc.legal_chatbot_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name         = "ChatbotSecurityGroup"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "security-group"
  }
}

# AMI for EC2
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# EC2 Instance
resource "aws_instance" "chatbot_ec2" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.chatbot_security_group.id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install python3 -y
    sudo pip3 install boto3 langchain python-telegram-bot pypdf python-dotenv
    cd /home/ec2-user/app
    python3 main.py
  EOF

  provisioner "file" {
    source      = "app/"
    destination = "/home/ec2-user/app"
  }

  tags = {
    Name         = "ChatbotInstance"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "instances"
  }

  volume_tags = {
    Name         = "ChatbotInstance-Volume"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "volumes"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "legal_chatbot_logs" {
  name              = "/aws/chatbot/legal-documents"
  retention_in_days = 7

  tags = {
    Name         = "LegalChatbotLogs"
    Project      = "LegalChatbot"
    CostCenter   = "12345"
    ResourceType = "log-group"
  }
}

# Outputs
output "s3_bucket_name" {
  value = aws_s3_bucket.documento_bucket.id
}

output "ec2_instance_id" {
  value = aws_instance.chatbot_ec2.id
}

output "ec2_instance_public_ip" {
  value = aws_instance.chatbot_ec2.public_ip
}