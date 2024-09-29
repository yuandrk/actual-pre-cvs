# Providers and data sources are defined in provider.tf and data.tf respectively

# Data source for Route 53 zone
data "aws_route53_zone" "primary" {
  name         = var.domain_name
  private_zone = false
}

# Create the ACM certificate
resource "aws_acm_certificate" "cert" {
  domain_name       = var.acm_certificate_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  provider = aws.us_east_1
}

# DNS validation records for ACM certificate
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
      record = dvo.resource_record_value
    }
  }

  zone_id = data.aws_route53_zone.primary.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 60
  records = [each.value.record]
}

# Validate the ACM certificate
resource "aws_acm_certificate_validation" "cert_validation" {
  provider = aws.us_east_1

  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

# Create the CloudFront Origin Access Identity
resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for CloudFront access to ${var.s3_bucket_name}"
}

# Outputs for OAI
output "cloudfront_oai_iam_arn" {
  value = aws_cloudfront_origin_access_identity.oai.iam_arn
}

output "cloudfront_oai_id" {
  value = aws_cloudfront_origin_access_identity.oai.id
}

# Invoke the S3 module
module "s3" {
  source = "./modules/s3_module"

  s3_bucket_name         = var.s3_bucket_name
  environment            = var.environment
  aws_region             = var.aws_region
  cloudfront_oai_iam_arn = aws_cloudfront_origin_access_identity.oai.iam_arn
}

# Invoke the CloudFront module
module "cloudfront" {
  source = "./modules/cloudfront_module"

  s3_bucket_name      = var.s3_bucket_name
  acm_certificate_arn = aws_acm_certificate_validation.cert_validation.certificate_arn
  subdomain_name      = var.subdomain_name
  domain_name         = var.domain_name
  aws_region          = var.aws_region
  environment         = var.environment
  cloudfront_oai_id   = aws_cloudfront_origin_access_identity.oai.id
}

# Invoke the Route53 module
module "route53" {
  source = "./modules/route53_module"

  domain_name                         = var.domain_name
  subdomain_name                      = var.subdomain_name
  environment                         = var.environment
  cloudfront_distribution_domain_name = module.cloudfront.cloudfront_domain_name
  aws_region                          = var.aws_region
}
