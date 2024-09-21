data "aws_route53_zone" "primary" {
  name         = var.domain_name
  private_zone = false
}

resource "aws_route53_record" "s3_website_cname" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "csv" # Subdomain, resulting in csv.yuandrk.net
  type    = "CNAME"
  ttl     = 300

  records = [local.s3_website_endpoint]
}