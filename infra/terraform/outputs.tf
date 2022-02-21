output "ec2_public_ip" {
  description = "Public IP of ec2 instance"
  value       = aws_instance.nhl_ec2.public_ip
}

output "mysql_endpoint_name" {
  description = "Endpoint name of db instance"
  value       = aws_db_instance.nhl.endpoint
}
