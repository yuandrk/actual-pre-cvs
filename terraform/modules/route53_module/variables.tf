variable "domain_name" {
  description = "Root domain name"
  type        = string
}

variable "subdomain_name" {
  description = "Subdomain name"
  type        = string
}

variable "cloudfront_distribution_domain_name" {
  description = "Domain name of the CloudFront distribution"
  type        = string
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "prod"
}
