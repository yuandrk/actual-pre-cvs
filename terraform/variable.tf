// General Setting
variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  type        = string
  default     = "prod"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS region for the resources"
  type        = string
}

// Domain Setting
variable "subdomain_name" {
  description = "Subdomain for the website"
  type        = string
}

variable "domain_name" {
  description = "Root domain name"
  type        = string
}

variable "acm_certificate_domain" {
  description = "Domain name for the ACM certificate"
  type        = string
}

// S3 Settings
variable "s3_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}