# Route53 Module

This module creates Route53 DNS records to route traffic to your CloudFront distribution.

## Inputs

- **domain_name** (string): Root domain name (e.g., "example.com").
- **subdomain_name** (string): Subdomain for the website (e.g., "www").
- **cloudfront_distribution_domain_name** (string): Domain name of the CloudFront distribution (e.g., "d123456abcdef.cloudfront.net").
- **aws_region** (string): AWS region where the resources are located.
- **environment** (string): Deployment environment (e.g., "dev", "staging", "prod").

## Outputs

- *(No outputs specified in the module.)*

## Usage

```hcl
module "route53" {
  source = "./modules/route53_module"

  domain_name                         = var.domain_name
  subdomain_name                      = var.subdomain_name
  cloudfront_distribution_domain_name = var.cloudfront_distribution_domain_name
  aws_region                          = var.aws_region
  environment                         = var.environment
}
```
