# Create the S3 bucket
resource "aws_s3_bucket" "bucket_website" {
  bucket = var.s3_bucket_name

  # Optionally, you can add tags or other configurations here
  tags = {
    Environment = "Production"
  }
}

# Set the ACL to private
resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.bucket_website.id
  acl    = "private"
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

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Configure website hosting (optional since we'll use CloudFront)
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
  acl          = "private"

  depends_on = [aws_s3_bucket_acl.bucket_acl]
}