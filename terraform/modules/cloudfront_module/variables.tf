variable "s3_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate"
  type        = string
}

variable "subdomain_name" {
  description = "Subdomain for the website"
  type        = string
}

variable "domain_name" {
  description = "Root domain name"
  type        = string
}

variable "aws_region" {
  description = "AWS region where the S3 bucket is located"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "prod"
}
