resource "aws_kms_key" "kms_key" {
  description             = var.kms_description
  deletion_window_in_days = var.kms_deletion_window_in_days
  enable_key_rotation     = var.bool_true
}

resource "aws_kms_alias" "key-alias" {
  target_key_id = aws_kms_key.kms_key.key_id
  name          = var.kms_alias_name
}