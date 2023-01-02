variable "bucket_name" {
  type        = string
  description = "The name of the bucket."
}

variable "key_path" {
  type        = string
  description = "Path to the state file inside the S3 Bucket."
}

variable "region" {
  type        = string
  description = "AWS Region of the resource."
}

variable "bool_true" {
  type        = bool
  default     = true
  description = "A boolean value that represent a true conditional."
}

variable "bool_false" {
  type        = bool
  default     = true
  description = "A boolean value that represent a false conditional."
}

variable "dynamodb_table_name" {
  type        = string
  description = "Unique within a region name of the table."
}

variable "kms_alias_name" {
  type        = string
  description = "The display name of the alias."
}

variable "kms_description" {
  type        = string
  default     = "This key is used to encrypt bucket objects"
  description = "The description of KMS Key."
}

variable "kms_deletion_window_in_days" {
  type        = string
  description = "The waiting period, specified in number of days."
}

variable "bucket_acl" {
  type        = string
  description = "The canned ACL to apply to the bucket."
}

variable "bucket_versioning_status" {
  type        = string
  description = "The versioning state of the bucket."
}

variable "bucket_sse_algorithm" {
  type        = string
  description = "The server-side encryption algorithm to use."
}

variable "dynamodb_read_capacity" {
  type        = string
  description = "Number of read units for this table."
}

variable "dynamodb_write_capacity" {
  type        = string
  description = " Number of write units for this index."
}

variable "dynamodb_hash_key" {
  type        = string
  description = "Attribute to use as the hash (partition) key."
}

variable "dynamodb_attribute_name" {
  type        = string
  description = "Name of the attribute."
}

variable "dynamodb_attribute_type" {
  type        = string
  description = "Attribute type."
}

variable vpc_cidr_block {
  type        = string
  description = "The IPv4 CIDR block for the VPC."
}