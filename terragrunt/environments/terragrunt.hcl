# Terragrunt Root Configuration
# This file contains shared configuration for all environments

# Configure Terragrunt to use S3 backend for state storage
remote_state {
  backend = "s3"
  config = {
    bucket = "sudeep-terraform-state"
    key    = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
    
    # Optional: Enable state locking with DynamoDB (if table exists)
    # dynamodb_table = "terraform-locks"
    
    # Enable encryption
    encrypt = true
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

# Generate provider configuration
generate "provider" {
  path = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
EOF
}

# Common inputs for all environments
inputs = {
  aws_region = "us-east-1"
}