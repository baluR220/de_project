variable "db_user" {
  description = "Database user name"
  type        = string
  sensitive   = true
  nullable    = false
}

variable "db_secret" {
  description = "Database user secret"
  type        = string
  sensitive   = true
  nullable    = false
}

variable "pub_key_path" {
  description = "Path to ssh public key"
  type        = string
  sensitive   = true
  nullable    = false
}
