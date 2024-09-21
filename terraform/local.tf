locals {
  # Construct the S3 website endpoint manually to avoid deprecated attributes
  s3_website_endpoint = "${aws_s3_bucket.bucket_website.bucket}.s3-website.${var.aws_region}.amazonaws.com"
}