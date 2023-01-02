output "kms_key_arn" {
  description = " The Amazon Resource Name (ARN) of the key."
  value       = aws_kms_key.kms_key.arn
}

output "kms_key_id" {
  description = "The globally unique identifier for the key."
  value       = aws_kms_key.kms_key.key_id
}

output "bucket_arn" {
  description = "Arn of the S3 bucket."
  value       = aws_s3_bucket.s3_bucket.arn
}

output "bucket_name" {
  description = "Name of the S3 bucket."
  value       = aws_s3_bucket.s3_bucket.id
}

output "dynamodb_arn" {
  description = "Arn of the DynamoDB table."
  value       = aws_dynamodb_table.dynamodb.arn
}

output "dynamodb_table" {
  description = "Unique within a region name of the table."
  value       = aws_dynamodb_table.dynamodb.id
}