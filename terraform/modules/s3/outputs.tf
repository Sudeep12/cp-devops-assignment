# S3 Module Outputs

output "bucket_id" {
  description = "ID of the S3 bucket"
  value       = aws_s3_bucket.s3.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.s3.arn
}

output "bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  value       = aws_s3_bucket.s3.bucket_domain_name
}

output "bucket_regional_domain_name" {
  description = "Regional domain name of the S3 bucket"
  value       = aws_s3_bucket.s3.bucket_regional_domain_name
}