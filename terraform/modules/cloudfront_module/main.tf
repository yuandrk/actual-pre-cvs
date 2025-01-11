resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for CloudFront access to ${var.s3_bucket_name}"
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  enabled             = true
  default_root_object = "upload.html"

  aliases = var.domain_names

  origin {
    domain_name = "${var.s3_bucket_name}.s3.${var.aws_region}.amazonaws.com"
    origin_id   = "s3_origin"

    s3_origin_config {
      origin_access_identity = "origin-access-identity/cloudfront/${aws_cloudfront_origin_access_identity.oai.id}"
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "s3_origin"
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  # Viewer certificate configuration (ACM Certificate for HTTPS)
  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Environment = var.environment
  }

}
