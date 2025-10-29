# Development Environment Configuration - S3 Backend
# This file deploys the complete infrastructure for the dev environment using S3 backend

# Include root terragrunt configuration (uses S3 backend: sudeep-terraform-state)
include "root" {
  path = find_in_parent_folders()
}

# Terraform configuration
terraform {
  source = "../../../terraform//"
}

# Environment-specific inputs
inputs = {
  environment = "dev"
  
  # S3 bucket configuration (random suffix will be added by terraform)
  bucket_name = "devops-assignment-products-dev"
  
  # CloudFront configuration
  distribution_name = "devops-assignment"
  
  # Common tags for all resources
  common_tags = {
    Name        = "ProductCloudFront"
    Owner       = "Sudeep Shetty"  # Replace with your name
    Terraform   = "true"
    Environment = "dev"
    Project     = "DevOps-Assignment"
  }
}