# Development Environment Configuration - Local Backend
# This file deploys the complete infrastructure for the dev environment using local backend

# Include root terragrunt configuration (now uses local backend)
include "root" {
  path = find_in_parent_folders()
}

# Terraform configuration
terraform {
  source = "../../../terraform"
}

# Environment-specific inputs
inputs = {
  environment = "dev"
  
  # S3 bucket configuration (random suffix will be added by terraform)
  bucket_name = "devops-assignment-products-dev"
  
  # CloudFront configuration
  distribution_name = "devops-assignment-dev"
  
  # Common tags for all resources
  common_tags = {
    Name        = "ProductCloudFront"
    Owner       = "Sudeep Shetty"  # Replace with your name
    Terraform   = "true"
    Environment = "dev"
    Project     = "DevOps-Assignment"
  }
}