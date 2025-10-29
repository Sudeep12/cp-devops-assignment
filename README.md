# DevOps Assignment - AWS S3 + CloudFront Infrastructure

A simple DevOps project that creates AWS infrastructure using Terraform and processes data with Python.

## What This Project Does

- Creates an S3 bucket and CloudFront distribution on AWS
- Processes product data from an API
- Stores filtered data in S3
- Delivers content globally via CloudFront
- Automates everything with GitHub Actions

## Quick Start

### 1. Setup
```bash
git clone <your-repo>
cd devops-assignment
```

### 2. Configure AWS Credentials
Add these secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### 3. Deploy
Push to main branch or run GitHub Actions workflow manually.

## Project Structure

```
devops-assignment/
├── terraform/           # Infrastructure code
├── terragrunt/         # Environment management
├── python/             # Data processing script
├── .github/workflows/  # CI/CD pipeline
└── README.md
```

## What Gets Created

| Resource | Purpose |
|----------|---------|
| S3 Bucket | Stores processed data |
| CloudFront Distribution | Delivers content globally |
| Origin Access Control | Secures S3 access |
| Bucket Policy | Restricts access to CloudFront only |

## How It Works

1. **GitHub Actions** triggers on code push
2. **Terraform** creates AWS infrastructure
3. **Python script** fetches and filters product data
4. **Data** gets uploaded to S3
5. **CloudFront** makes it available worldwide

## Manual Commands

If you want to run manually:

```bash
# Go to terragrunt directory
cd terragrunt/environments/dev

# Initialize and apply
terragrunt init --terragrunt-non-interactive
terragrunt apply --terragrunt-non-interactive -auto-approve

# Run Python script
cd ../../../python
python process_products.py

# Cleanup when done
cd ../terragrunt/environments/dev
terragrunt destroy --terragrunt-non-interactive -auto-approve
```

## Requirements

- Terraform >= 1.5.0
- AWS Account
- GitHub repository with Actions enabled

## Author

**Sudeep Shetty** - DevOps Assignment