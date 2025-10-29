# Terragrunt root configuration
# This file defines common settings for all environments

# Configure remote state storage
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket  = "your-terraform-state-bucket"  # Update with your state bucket
    key     = "${path_relative_to_include()}/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
    
    # DynamoDB table for state locking
    dynamodb_table = "terraform-lock-table"
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
  aws_region = "us-east-1"
}