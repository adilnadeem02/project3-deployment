variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "key_name" {
  description = "Name of the SSH key pair created in AWS"
  default     = "project3-key" 
}