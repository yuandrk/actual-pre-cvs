// locals.tf

locals {
  full_domain_name = "${var.subdomain_name}.${var.domain_name}"
}
