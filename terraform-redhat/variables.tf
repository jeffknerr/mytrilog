# These variables come from the terraform.tfvars file
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "aws_region" {
  description = "AWS region for launch."
  default     = "us-east-1"
}

variable "public_key_path" {
  default = "~/.ssh/jeffnotrootTF.pem"
}
