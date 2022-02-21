resource "aws_vpc" "nhl" {
  cidr_block = "192.168.0.0/16"

  tags = {
    Name = "nhl_vpc"
  }
}

resource "aws_subnet" "nhl_west_2a" {
  vpc_id                  = aws_vpc.nhl.id
  cidr_block              = "192.168.1.0/24"
  availability_zone       = "us-west-2a"
  map_public_ip_on_launch = true

  tags = {
    Name = "nhl_subnet_west_2a"
  }
}

resource "aws_subnet" "nhl_west_2b" {
  vpc_id            = aws_vpc.nhl.id
  cidr_block        = "192.168.2.0/24"
  availability_zone = "us-west-2b"
  tags = {
    Name = "nhl_subnet_west_2b"
  }
}

resource "aws_security_group" "ssh_for_ec2" {
  name        = "allow_in_ssh"
  description = "Allow ssh inbound"
  vpc_id      = aws_vpc.nhl.id

  ingress {
    description      = "ssh from all"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}

resource "aws_security_group" "mysql_for_db" {
  name        = "allow_in_mysql"
  description = "Allow mysql inbound"
  vpc_id      = aws_vpc.nhl.id

  ingress {
    description      = "mysql from all"
    from_port        = 3306
    to_port          = 3306
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_mysql"
  }
}
