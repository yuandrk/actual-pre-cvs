output "s3_bucket_name" {
  value = module.s3.bucket_name
}

output "cloudfront_domain_name" {
  value = module.cloudfront.cloudfront_domain_name
}
