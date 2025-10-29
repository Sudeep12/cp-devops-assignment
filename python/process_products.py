#!/usr/bin/env python3
"""
Product Data Processor

This script downloads product data from dummyjson.com, filters products
with price >= 100, and uploads the filtered data to S3 for access via CloudFront.

Author: Sudeep Shetty
"""

import json
import requests
import boto3
import os
import sys
from typing import Dict, List, Any
from botocore.exceptions import NoCredentialsError, ClientError


class ProductProcessor:
    """Handles product data processing and AWS S3 operations."""
    
    def __init__(self, bucket_name: str, cloudfront_url: str):
        """
        Initialize the ProductProcessor.
        
        Args:
            bucket_name: Name of the S3 bucket
            cloudfront_url: CloudFront distribution URL
        """
        self.bucket_name = bucket_name
        self.cloudfront_url = cloudfront_url
        self.s3_client = boto3.client('s3')
        self.source_url = "https://dummyjson.com/products"
        self.output_filename = "filtered_products.json"
    
    def download_products(self) -> Dict[str, Any]:
        """
        Download product data from the API.
        
        Returns:
            Dictionary containing product data
            
        Raises:
            requests.RequestException: If the API request fails
        """
        print(f"📥 Downloading product data from {self.source_url}")
        
        try:
            response = requests.get(self.source_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Successfully downloaded {len(data.get('products', []))} products")
            return data
            
        except requests.RequestException as e:
            print(f"❌ Error downloading product data: {e}")
            raise
    
    def filter_products(self, data: Dict[str, Any], min_price: float = 100.0) -> List[Dict[str, Any]]:
        """
        Filter products based on price criteria.
        
        Args:
            data: Raw product data from API
            min_price: Minimum price threshold (default: 100.0)
            
        Returns:
            List of filtered products
        """
        print(f"🔍 Filtering products with price >= ${min_price}")
        
        products = data.get('products', [])
        if not products:
            print("⚠️  No products found in the data")
            return []
        
        # Filter products with price >= min_price
        filtered_products = []
        for product in products:
            price = product.get('price', 0)
            if price >= min_price:
                # Extract only required fields as per the example
                filtered_product = {
                    'id': product.get('id'),
                    'title': product.get('title'),
                    'price': product.get('price'),
                    'quantity': product.get('stock', 1),  # Use stock as quantity
                    'total': product.get('price', 0) * product.get('stock', 1),
                    'discountPercentage': product.get('discountPercentage', 0),
                    'discountedPrice': product.get('price', 0) * (1 - product.get('discountPercentage', 0) / 100),
                    'thumbnail': product.get('thumbnail')
                }
                filtered_products.append(filtered_product)
        
        print(f"✅ Found {len(filtered_products)} products with price >= ${min_price}")
        return filtered_products
    
    def upload_to_s3(self, data: List[Dict[str, Any]]) -> bool:
        """
        Upload filtered data to S3 bucket.
        
        Args:
            data: Filtered product data to upload
            
        Returns:
            True if upload successful, False otherwise
        """
        print(f"📤 Uploading filtered data to S3 bucket: {self.bucket_name}")
        
        try:
            # Convert data to JSON string
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.output_filename,
                Body=json_data,
                ContentType='application/json',
                Metadata={
                    'product-count': str(len(data)),
                    'processor': 'devops-assignment'
                }
            )
            
            print(f"✅ Successfully uploaded {self.output_filename} to S3")
            return True
            
        except NoCredentialsError:
            print("❌ Error: AWS credentials not found")
            return False
        except ClientError as e:
            print(f"❌ Error uploading to S3: {e}")
            return False
    
    def download_from_cloudfront(self) -> bool:
        """
        Download and verify the uploaded file via CloudFront.
        
        Returns:
            True if download and validation successful, False otherwise
        """
        cloudfront_file_url = f"{self.cloudfront_url.rstrip('/')}/{self.output_filename}"
        print(f"📥 Downloading file from CloudFront: {cloudfront_file_url}")
        
        try:
            response = requests.get(cloudfront_file_url, timeout=30)
            response.raise_for_status()
            
            # Try to parse as JSON to validate
            data = response.json()
            
            print(f"✅ Successfully downloaded and validated JSON from CloudFront")
            print(f"📊 File contains {len(data)} products")
            print(f"🌐 CloudFront URL: {cloudfront_file_url}")
            
            # Print sample of the data
            if data:
                print("\n📋 Sample product from CloudFront:")
                print(json.dumps(data[0], indent=2))
            
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error downloading from CloudFront: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Downloaded file is not valid JSON: {e}")
            return False
    
    def process(self) -> bool:
        """
        Execute the complete processing pipeline.
        
        Returns:
            True if all steps successful, False otherwise
        """
        print("🚀 Starting product data processing pipeline")
        print("=" * 50)
        
        try:
            # Step 1: Download product data
            raw_data = self.download_products()
            
            # Step 2: Filter products
            filtered_products = self.filter_products(raw_data)
            
            if not filtered_products:
                print("⚠️  No products match the filter criteria")
                return False
            
            # Step 3: Upload to S3
            upload_success = self.upload_to_s3(filtered_products)
            if not upload_success:
                return False
            
            # Step 4: Download and verify from CloudFront
            download_success = self.download_from_cloudfront()
            
            if download_success:
                print("\n🎉 Processing pipeline completed successfully!")
                return True
            else:
                print("\n❌ Processing pipeline failed at CloudFront verification")
                return False
                
        except Exception as e:
            print(f"\n❌ Unexpected error in processing pipeline: {e}")
            return False


def main():
    """Main function to run the product processor."""
    
    # Get configuration from environment variables
    bucket_name = os.getenv('S3_BUCKET_NAME')
    cloudfront_url = os.getenv('CLOUDFRONT_URL')
    
    if not bucket_name:
        print("❌ Error: S3_BUCKET_NAME environment variable is required")
        sys.exit(1)
    
    if not cloudfront_url:
        print("❌ Error: CLOUDFRONT_URL environment variable is required")
        sys.exit(1)
    
    # Initialize and run processor
    processor = ProductProcessor(bucket_name, cloudfront_url)
    success = processor.process()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()