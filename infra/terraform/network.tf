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

resource "aws_internet_gateway" "nhl_igw" {
  vpc_id = aws_vpc.nhl.id

  tags = {
    Name = "nhl_igw"
  }
}

resource "aws_route_table" "nhl_rt" {
  vpc_id = aws_vpc.nhl.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.nhl_igw.id
  }

  tags = {
    Name = "nhl_rt"
  }
}

resource "aws_main_route_table_association" "rt_as" {
  vpc_id         = aws_vpc.nhl.id
  route_table_id = aws_route_table.nhl_rt.id
}

resource "aws_security_group" "sg_for_ec2" {
  name        = "sg_for_ec2"
  description = "Security group for ec2 instance"
  vpc_id      = aws_vpc.nhl.id

  tags = {
    Name = "sg_for_ec2"
  }
}

resource "aws_security_group" "sg_for_db" {
  name        = "sg_for_db"
  description = "Security group for db instance"
  vpc_id      = aws_vpc.nhl.id

  tags = {
    Name = "sg_for_db"
  }
}

resource "aws_security_group_rule" "in_mysql_db" {
  type              = "ingress"
  description       = "mysql from all"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.sg_for_db.id
}

resource "aws_security_group_rule" "out_all_db" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.sg_for_db.id
}

resource "aws_security_group_rule" "in_ssh_ec2" {
  type              = "ingress"
  description       = "ssh from all"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.sg_for_ec2.id
}

resource "aws_security_group_rule" "out_all_ec2" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.sg_for_ec2.id
}
