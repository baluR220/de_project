variable "db_user" {
	description	= "Database user name"
	type	= string
	sensitive 	= true
	nullable 	= false
}

variable "db_secret" {
	description	= "Database user secret"
	type		= string
	sensitive 	= true
	nullable 	= false
}


