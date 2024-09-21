output "website_url" {
  description = "URL of the S3 static website"
  value       = "http://${local.s3_website_endpoint}"
}