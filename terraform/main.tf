# Main Terraform Configuration
# This file orchestrates the deployment of S3 and CloudFront resources

# Generate random suffix for unique resource naming
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# S3 Bucket (created first without CloudFront policy)
module "s3" {
  source = "./modules/s3"

  bucket_name = "${var.bucket_name}-${random_string.bucket_suffix.result}"
  tags        = var.common_tags
}

# CloudFront Distribution (references S3 bucket)
module "cloudfront" {
  source = "./modules/cloudfront"

  distribution_name         = var.distribution_name
  s3_bucket_id             = module.s3.bucket_id
  s3_bucket_domain_name    = module.s3.bucket_regional_domain_name
  default_root_object      = "filtered_products.json"
  use_default_certificate  = true
  price_class             = "PriceClass_100"

  tags = var.common_tags
}

# S3 Bucket Policy (applied after CloudFront is created)
resource "aws_s3_bucket_policy" "cloudfront_access" {
  bucket = module.s3.bucket_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipal"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${module.s3.bucket_arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = module.cloudfront.distribution_arn
          }
        }
      }
    ]
  })

  depends_on = [module.s3, module.cloudfront]
}