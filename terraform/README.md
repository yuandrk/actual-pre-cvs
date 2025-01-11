# Terraform Project Documentation

## Project Overview

This Terraform project sets up a secure and scalable infrastructure on AWS to serve a static website using S3, CloudFront, ACM (for SSL certificates), and Route53 for DNS management. The infrastructure includes:

- An S3 bucket for hosting static content.

- A CloudFront distribution for content delivery.

- An ACM certificate for HTTPS support.

- Route53 DNS records for domain mapping.

- Secure access configurations using Origin Access Identity (OAI).

## Prerequisites

Before you begin, ensure you have the following:

- **AWS Account** : An active AWS account with appropriate permissions.

- **Terraform Installed** : Terraform v1.5.7 or compatible installed on your machine.

- **AWS CLI Configured** : AWS CLI installed and configured with your AWS credentials.

- **Domain Name** : A registered domain name, managed in AWS Route53.

## Directory Structure

```css
├── acm.tf
├── cloudfront.tf
├── main.tf
├── output.tf
├── provider.tf
├── route53.tf
├── terraform.tfstate
├── terraform.tfvars
├── variable.tf
├── modules/
│   ├── cloudfront_module/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── s3_module/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   └── route53_module/
│       ├── main.tf
│       ├── variables.tf
│       └── README.md
└── templates/
    └── upload.html
```

## Modules Explanation

CloudFront Module (`modules/cloudfront_module`)

- **Purpose** : Creates a CloudFront distribution and an Origin Access Identity (OAI) to securely serve content from the S3 bucket over HTTPS.

- **Key Resources** :
  - `aws_cloudfront_distribution`

  - `aws_cloudfront_origin_access_identity`
S3 Module (`modules/s3_module`)
- **Purpose** : Creates an S3 bucket for static website hosting, configures bucket policies, and uploads the initial `upload.html` file.

- **Key Resources** :
  - `aws_s3_bucket`

  - `aws_s3_bucket_policy`

  - `aws_s3_bucket_public_access_block`

  - `aws_s3_object`
Route53 Module (`modules/route53_module`)
- **Purpose** : Manages Route53 DNS records to route traffic to the CloudFront distribution.

- **Key Resources** :
  - `aws_route53_record`

  - Data source `aws_route53_zone`

## Variables and Configuration

Required Variables (`variable.tf`)

- `s3_bucket_name`: Name of the S3 bucket.

- `acm_certificate_domain`: Domain name for the ACM certificate (e.g., `www.example.com`).

- `subdomain_name`: Subdomain for the website (e.g., `www`).

- `domain_name`: Root domain name (e.g., `example.com`).

- `aws_region`: AWS region for the resources (e.g., `us-east-1`).

- `environment`: Deployment environment (`dev`, `staging`, `prod`).

### Variable Definitions

Define your variables in the `terraform.tfvars` file or pass them via command-line or environment variables.Example `terraform.tfvars`:**

```hcl
s3_bucket_name         = "your-bucket-name"
acm_certificate_domain = "your.domain.com"
subdomain_name         = "www"
domain_name            = "your.domain.com"
aws_region             = "us-east-1"
environment            = "prod"
```

## Usage Instructions

### Step 1: Clone the Repository

```bash
git clone 
cd repo 
```

### Step 2: Initialize Terraform

```bash
terraform init
```

### Step 3: Validate the Configuration

```bash
terraform validate
```

### Step 4: Review the Execution Plan

```bash
terraform plan
```

### Step 5: Apply the Configuration

```bash
terraform apply
```

Type `yes` when prompted to confirm the deployment.

### Step 6: Access Your Website

After the deployment is complete, you can access your website using the domain name specified.

## Deployment Steps Explained

1. **ACM Certificate Creation (`acm.tf`)** :

- Creates an ACM certificate in `us-east-1` (required for CloudFront).

- Validates the certificate using DNS validation via Route53.

2. **S3 Bucket Setup (`main.tf` invoking `s3_module`)** :

- Creates an S3 bucket for static website hosting.

- Configures bucket policies to allow access from CloudFront via OAI.

- Uploads the `upload.html` file to the bucket.

3. **CloudFront Distribution Setup (`main.tf` invoking `cloudfront_module`)** :

- Creates a CloudFront distribution pointing to the S3 bucket.

- Sets up an OAI for secure access to the S3 bucket.

- Configures SSL using the ACM certificate.

4. **Route53 DNS Records (`route53.tf` invoking `route53_module`)** :

- Creates an A record in Route53 pointing your domain to the CloudFront distribution.

## Troubleshooting

### Access Denied Errors

If you encounter `Access Denied` errors when accessing your website, ensure:

- The S3 bucket policy correctly references the OAI's IAM ARN.

- The CloudFront distribution is using the correct OAI.

- The S3 bucket does not allow public access and relies solely on CloudFront for content delivery.

### Common Commands

- **Refresh State** : `terraform refresh`

- **Destroy Resources** : `terraform destroy`

- **View State** : `terraform state list`

### Potential Issues and Solutions

- **Certificate Validation Failed** : Ensure your domain is correctly set up in Route53 and that the DNS validation record has been created.

- **OAI Conflicts** : Avoid defining multiple OAIs across modules. Manage the OAI within the `cloudfront_module` to prevent conflicts.

## Best Practices

- **Module Encapsulation** : Keep modules self-contained to promote reusability and maintainability.

- **State Management** : Use remote state backends like S3 with state locking enabled to prevent concurrent modifications.

- **Version Control** : Track your Terraform configurations in a version control system like Git.

- **Variable Management** : Use Terraform variables and `tfvars` files to manage environment-specific configurations.

- **Resource Naming** : Use consistent naming conventions for resources to make management easier.

## Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)

- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

- [Terraform Best Practices](https://www.terraform-best-practices.com)
