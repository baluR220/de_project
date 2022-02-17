resource "aws_db_subnet_group" "nhl" {
	name 		= "nhl_db_subnet_group"
	subnet_ids	= [aws_subnet.nhl_west_2a.id, aws_subnet.nhl_west_2b.id]

	tags = {
		Name = "nhl_db_subnet_group"
	}
}

resource "aws_db_instance" "nhl" {
	allocated_storage 		= 10
	engine 					= "mysql"
	engine_version 			= "8.0.27"
	instance_class			= "db.t2.micro"
	name					= "nhl_app"
	username				= var.db_user
	password				= var.db_secret
	db_subnet_group_name 	= aws_db_subnet_group.nhl.name
	skip_final_snapshot		= true

	tags = {
		Name = "nhl_db"
	}
}