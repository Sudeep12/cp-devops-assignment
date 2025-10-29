# Terraform Outputs

output "s3_bucket_id" {
  description = "ID of the created S3 bucket"
  value       = module.s3.bucket_id
}

output "s3_bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = module.s3.bucket_arn
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = module.cloudfront.distribution_id
}

output "cloudfront_distribution_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = module.cloudfront.distribution_domain_name
}

output "cloudfront_url" {
  description = "Full URL to access the CloudFront distribution"
  value       = "https://${module.cloudfront.distribution_domain_name}"
}

output "filtered_products_url" {
  description = "URL to access the filtered products JSON via CloudFront"
  value       = "https://${module.cloudfront.distribution_domain_name}/filtered_products.json"
}