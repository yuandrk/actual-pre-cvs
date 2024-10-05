# Invoke the Route53 module
module "route53" {
  source = "./modules/route53_module"

  domain_name                         = var.domain_name
  subdomain_name                      = var.subdomain_name
  environment                         = var.environment
  cloudfront_distribution_domain_name = module.cloudfront.cloudfront_domain_name
  aws_region                          = var.aws_region
}

# Data source for Route 53 zone
data "aws_route53_zone" "primary" {
  name         = var.domain_name
  private_zone = false
}
