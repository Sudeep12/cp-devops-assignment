# CloudFront Distribution Module
# This module creates a CloudFront distribution for the S3 bucket

# Origin Access Control for secure S3 access
resource "aws_cloudfront_origin_access_control" "cloudfront" {
  name                                          = "${var.distribution_name}-oac"
  description                                   = "OAC for ${var.distribution_name}"
  origin_access_control_origin_type             = "s3"
  signing_behavior                              = "always"
  signing_protocol                              = "sigv4"
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "cloudfront" {
  aliases                                       = var.aliases

  origin {
    domain_name                                 = var.s3_bucket_domain_name
    origin_id                                   = "S3-${var.s3_bucket_id}"
    origin_access_control_id                    = aws_cloudfront_origin_access_control.cloudfront.id
  }

  enabled                                       = true
  is_ipv6_enabled                               = true
  default_root_object                           = var.default_root_object

  default_cache_behavior {
    allowed_methods                             = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods                              = ["GET", "HEAD"]
    target_origin_id                            = "S3-${var.s3_bucket_id}"
    compress                                    = true
    viewer_protocol_policy                      = "redirect-to-https"

    forwarded_values {
      query_string                              = false
      cookies {
        forward                                 = "none"
      }
    }

    min_ttl                                     = 0
    default_ttl                                 = 3600
    max_ttl                                     = 86400
  }

  # Price class for cost optimization
  price_class                                   = var.price_class

  restrictions {
    geo_restriction {
      restriction_type                          = "none"
    }
  }

  # SSL/TLS certificate configuration
  viewer_certificate {
    cloudfront_default_certificate              = var.use_default_certificate
    ssl_support_method                          = var.use_default_certificate ? null : "sni-only"
    minimum_protocol_version                    = var.use_default_certificate ? null : "TLSv1.2_2021"
  }

  tags                                          = var.tags

  # Wait for OAC to be created
  depends_on                                    = [aws_cloudfront_origin_access_control.cloudfront]
}