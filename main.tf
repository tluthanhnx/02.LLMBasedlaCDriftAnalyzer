terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-southeast-1"
}

# ✅ EC2 chính, sẽ có thay đổi ở tag Name
resource "aws_instance" "app_server" {
  ami           = "ami-02c7683e4ca3ebf58"
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name # ✅ Đổi tag để sinh ~ change
  }
}

# ❌ Resource cũ, bị xóa để sinh - delete
# resource "aws_instance" "new_instance" {
#   ami           = "ami-02c7683e4ca3ebf58"
#   instance_type = "t2.micro"
#   tags = {
#     Name = "ExtraInstance"
#   }
# }

# ✅ EC2 mới (tạo mới)
resource "aws_instance" "db_server" {
  ami           = "ami-02c7683e4ca3ebf58"
  instance_type = "t3.micro"

  tags = {
    Name = "DBServer"
  }
}

# ✅ Tạo EIP gán cho db_server
resource "aws_eip" "db_eip" {
  instance = aws_instance.db_server.id

  tags = {
    Name = "DBServerEIP"
  }
}

# ✅ Security group mới
resource "aws_security_group" "web_tlu" {
  name        = "web-tlu"
  description = "Allow HTTP and SSH"

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
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
    Name = "WebSecurityGroup"
  }
}
