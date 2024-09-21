locals {
  s3_website_endpoint = "${aws_s3_bucket.bucket-1.bucket}.s3-website.${var.aws_region}.amazonaws.com"
}