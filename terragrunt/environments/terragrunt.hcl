# Terragrunt root configuration
# This file defines common settings for all environments

# Get AWS account ID for unique bucket naming
locals {
  aws_account_id = get_aws_account_id()
  aws_region     = "us-east-1"
}

# Configure remote state storage
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "terraform-state-devops-assignment-${local.aws_account_id}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    encrypt        = true
    
    # Enable S3 bucket creation
    s3_bucket_tags = {
      Name        = "TerraformState"
      Owner       = "DevOps-Assignment"
      Terraform   = "true"
      Environment = "shared"
    }
    
    # DynamoDB table for state locking (will be created automatically)
    dynamodb_table = "terraform-lock-devops-assignment"
  }
}

# Generate provider configuration
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "random" {}
EOF
}

# Common inputs for all environments
inputs = {
  aws_region = local.aws_region
}