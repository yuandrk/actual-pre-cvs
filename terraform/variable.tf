# Define AWS region
variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "eu-west-2"
}

# Define S3 bucket name for website hosting, string should be with dot in the end  
variable "s3_bucket_name" {
  description = "Name of the S3 bucket for static website hosting"
  type        = string
}

# Path to the HTML file for the website 
variable "html_file_path" {
  description = "Path to the HTML file to upload to S3"
  type        = string
}

variable "domain_name" {
  description = "Domain name for the website"
  type        = string

}

variable "s3_website_hosted_zone_id" {
  description = "Hosted zone ID for S3 website endpoint in the specified region"
  type        = string
}
