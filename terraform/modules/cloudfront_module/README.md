# CloudFront Module

This module creates a CloudFront distribution to serve content from an S3 bucket securely using HTTPS.

## Inputs

- **s3_bucket_name** (string): Name of the S3 bucket serving as the origin.
- **acm_certificate_arn** (string): ARN of the ACM certificate for HTTPS support.
- **subdomain_name** (string): Subdomain for the website (e.g., "www").
- **domain_name** (string): Root domain name (e.g., "example.com").
- **aws_region** (string): AWS region where the resources are located.
- **cloudfront_oai_id** (string): ID of the CloudFront Origin Access Identity.
- **environment** (string): Environment name (e.g., "dev", "staging", "prod").

## Outputs

- **cloudfront_domain_name**: The domain name of the CloudFront distribution (e.g., "d123456abcdef.cloudfront.net").

## Usage

```hcl
module "cloudfront" {
  source = "./modules/cloudfront_module"

  s3_bucket_name      = var.s3_bucket_name
  acm_certificate_arn = var.acm_certificate_arn
  subdomain_name      = var.subdomain_name
  domain_name         = var.domain_name
  aws_region          = var.aws_region
  environment         = var.environment
  cloudfront_oai_id   = var.cloudfront_oai_id
}
```