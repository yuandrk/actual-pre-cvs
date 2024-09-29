variable "s3_bucket_name" {
  description = "Name of the S3 bucket for static website hosting"
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

variable "cloudfront_oai_iam_arn" {
  description = "IAM ARN of the CloudFront Origin Access Identity"
  type        = string
}
