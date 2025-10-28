# CloudFront Module Variables

variable "distribution_name" {
  description = "Name for the CloudFront distribution"
  type        = string
}

variable "s3_bucket_id" {
  description = "ID of the S3 bucket to serve content from"
  type        = string
}

variable "s3_bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  type        = string
}

variable "aliases" {
  description = "Alternative domain names for the distribution"
  type        = list(string)
  default     = []
}

variable "default_root_object" {
  description = "Default root object for the distribution"
  type        = string
  default     = "index.html"
}

variable "price_class" {
  description = "Price class for the distribution"
  type        = string
  default     = "PriceClass_100"
}

variable "use_default_certificate" {
  description = "Whether to use the default CloudFront certificate"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to the CloudFront distribution"
  type        = map(string)
  default     = {}
}