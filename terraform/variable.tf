variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-2"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for static website hosting"
  type        = string
}

variable "html_file_path" {
  description = "Name of the HTML file to upload to S3 (e.g., 'upload.html')"
  type        = string
}

variable "domain_name" {
  description = "Domain name for the website (e.g., 'yuandrk.net.')"
  type        = string
}