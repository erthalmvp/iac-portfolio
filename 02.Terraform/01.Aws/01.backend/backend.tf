terraform {

  backend "s3" {
    bucket         = var.bucket_name
    key            = var.key_path
    region         = var.region
    encrypt        = var.bool_true
    kms_key_id     = var.bool_true
    dynamodb_table = var.dynamodb_table
  }
}