# Invoke the CloudFront module
module "cloudfront" {
  source              = "./modules/cloudfront_module"
  s3_bucket_name      = var.s3_bucket_name
  acm_certificate_arn = aws_acm_certificate_validation.cert_validation.certificate_arn
  domain_names        = [local.full_domain_name]
  aws_region          = var.aws_region
  environment         = var.environment
}

# Adjust the S3 module invocation
module "s3" {
  source = "./modules/s3_module"

  s3_bucket_name = var.s3_bucket_name
  environment    = var.environment
  aws_region     = var.aws_region
  # Pass the OAI IAM ARN from the CloudFront module
  cloudfront_oai_iam_arn = module.cloudfront.cloudfront_oai_iam_arn
}
