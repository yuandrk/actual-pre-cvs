# S3 Module

This module creates an S3 bucket for static website hosting.

## Inputs

- `s3_bucket_name` (string): Name of the S3 bucket.
- `aws_region` (string): AWS region where the bucket will be created.
- `environment` (string): Deployment environment (dev, staging, prod).
- `cloudfront_oai_iam_arn` (string): IAM ARN of the CloudFront Origin Access Identity.

## Outputs

- `bucket_name`: The name of the created S3 bucket.
- `bucket_region`: The AWS region of the S3 bucket.

## Usage

```hcl
module "s3" {
  source = "./modules/s3_module"

  s3_bucket_name         = var.s3_bucket_name
  aws_region             = var.aws_region
  environment            = var.environment
  cloudfront_oai_iam_arn = var.cloudfront_oai_iam_arn
}
```
