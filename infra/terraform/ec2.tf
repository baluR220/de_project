data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

data "local_file" "pub_key" {
  filename = var.pub_key_path
}

resource "aws_key_pair" "ec2_key" {
  key_name   = "ec2_key"
  public_key = data.local_file.pub_key.content
}

resource "aws_instance" "nhl_ec2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  availability_zone      = "us-west-2a"
  key_name               = aws_key_pair.ec2_key.id
  subnet_id              = aws_subnet.nhl_west_2a.id
  vpc_security_group_ids = [aws_security_group.ssh_for_ec2.id]

}