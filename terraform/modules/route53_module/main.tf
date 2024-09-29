data "aws_route53_zone" "primary" {
  name         = var.domain_name
  private_zone = false
}

# Create an A record alias pointing to the CloudFront distribution
resource "aws_route53_record" "cloudfront_alias" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.subdomain_name
  type    = "A"

  alias {
    name                   = var.cloudfront_distribution_domain_name
    zone_id                = "Z2FDTNDATAQYW2" # CloudFront Hosted Zone ID
    evaluate_target_health = false
  }
}
