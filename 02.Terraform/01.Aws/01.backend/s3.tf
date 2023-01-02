resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.s3_bucket.id
  acl    = var.bucket_acl
}

resource "aws_s3_bucket_versioning" "bucket_versioning" {
  bucket = aws_s3_bucket.s3_bucket.id
  versioning_configuration {
    status = var.bucket_versioning_status
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption_configuration" {
  bucket = aws_s3_bucket.s3_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.kms_key.arn
      sse_algorithm     = var.bucket_sse_algorithm
    }
  }
}

resource "aws_s3_bucket_public_access_block" "bucket_access_block" {
  bucket = aws_s3_bucket.s3_bucket.id

  block_public_acls       = var.bool_true
  block_public_policy     = var.bool_true
  ignore_public_acls      = var.bool_true
  restrict_public_buckets = var.bool_true
}