output "bucket_name" {
  value       = aws_s3_bucket.bucket_website.bucket
  description = "Name of the S3 bucket"
}

output "bucket_region" {
  value       = var.aws_region
  description = "AWS region of the S3 bucket"
}
