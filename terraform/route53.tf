data "aws_route53_zone" "primary" {
  name         = var.domain_name
  private_zone = false
}

# DNS validation records for ACM certificate (already included in cloudfront.tf)

# Create an A record alias pointing to the CloudFront distribution
resource "aws_route53_record" "cloudfront_alias" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.subdomain_name # Subdomain, e.g., 'csv'
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.s3_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.s3_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}