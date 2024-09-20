# Define AWS region
variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "eu-west-2"
}

# Define S3 bucket name for website hosting
variable "s3_bucket_name" {
  description = "Name of the S3 bucket for static website hosting"
  type        = string
}

# Path to the HTML file for the website
variable "html_file_path" {
  description = "Path to the HTML file to upload to S3"
  type        = string
}

