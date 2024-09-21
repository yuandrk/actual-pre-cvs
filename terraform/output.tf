output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.s3_distribution.domain_name
}

output "website_url" {
  description = "URL of the CloudFront-distributed website"
  value       = "https://${var.subdomain_name}.${trim(var.domain_name, ".")}"
}