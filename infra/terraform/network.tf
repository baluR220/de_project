resource "aws_vpc" "nhl" {
	cidr_block = "192.168.0.0/16"

	tags = {
		Name = "nhl_vpc"
	}
}

resource "aws_subnet" "nhl_west_2a" {
	vpc_id 		= aws_vpc.nhl.id
	cidr_block 	= "192.168.1.0/24"
	availability_zone	= "us-west-2a" 
	tags = {
		Name = "nhl_subnet_west_2a"
	}
}

resource "aws_subnet" "nhl_west_2b" {
	vpc_id 		= aws_vpc.nhl.id
	cidr_block 	= "192.168.2.0/24"
	availability_zone	= "us-west-2b" 
	tags = {
		Name = "nhl_subnet_west_2b"
	}
}
