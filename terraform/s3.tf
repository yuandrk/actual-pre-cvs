# s3.tf

# Create the S3 bucket
resource "aws_s3_bucket" "bucket_website" {
  bucket = var.s3_bucket_name
}

# Set the ACL to public-read
resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.bucket_website.id
  acl    = "public-read"
}

# Set ownership controls
resource "aws_s3_bucket_ownership_controls" "bucket_ownership_controls" {
  bucket = aws_s3_bucket.bucket_website.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Set public access block configuration
resource "aws_s3_bucket_public_access_block" "bucket_public_access_block" {
  bucket = aws_s3_bucket.bucket_website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Configure website hosting
resource "aws_s3_bucket_website_configuration" "website_configuration" {
  bucket = aws_s3_bucket.bucket_website.id

  index_document {
    suffix = var.html_file_path
  }
}

# Upload the HTML file to S3
resource "aws_s3_object" "upload_html" {
  bucket       = aws_s3_bucket.bucket_website.id
  key          = var.html_file_path
  source       = "${path.module}/../templates/${var.html_file_path}"
  content_type = "text/html"
  acl          = "public-read"

  depends_on = [aws_s3_bucket_acl.bucket_acl]
}

# Define the bucket policy to allow public read access
resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.bucket_website.id
  policy = data.aws_iam_policy_document.bucket_policy.json
}

data "aws_iam_policy_document" "bucket_policy" {
  statement {
    sid    = "PublicReadGetObject"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:GetObject"]

    resources = [
      "${aws_s3_bucket.bucket_website.arn}/*",
    ]
  }
}