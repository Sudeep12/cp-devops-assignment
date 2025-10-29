#!/usr/bin/env python3
"""
Test script for the product processor.

This script runs basic tests to validate the product processing functionality.
"""

import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path to import the processor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from process_products import ProductProcessor


class TestProductProcessor(unittest.TestCase):
    """Test cases for ProductProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = ProductProcessor("test-bucket", "https://test-cloudfront.amazonaws.com")
    
    def test_filter_products_basic(self):
        """Test basic product filtering functionality."""
        sample_data = {
            "products": [
                {
                    "id": 1,
                    "title": "Cheap Product",
                    "price": 50,
                    "stock": 10,
                    "discountPercentage": 10,
                    "thumbnail": "https://example.com/1.jpg"
                },
                {
                    "id": 2,
                    "title": "Expensive Product",
                    "price": 150,
                    "stock": 5,
                    "discountPercentage": 5,
                    "thumbnail": "https://example.com/2.jpg"
                },
                {
                    "id": 3,
                    "title": "Exactly 100 Product",
                    "price": 100,
                    "stock": 8,
                    "discountPercentage": 0,
                    "thumbnail": "https://example.com/3.jpg"
                }
            ]
        }
        
        filtered = self.processor.filter_products(sample_data)
        
        # Should return 2 products (price >= 100)
        self.assertEqual(len(filtered), 2)
        
        # Check that prices are >= 100
        for product in filtered:
            self.assertGreaterEqual(product['price'], 100)
        
        # Verify specific product data
        expensive_product = next(p for p in filtered if p['id'] == 2)
        self.assertEqual(expensive_product['title'], "Expensive Product")
        self.assertEqual(expensive_product['price'], 150)
        self.assertEqual(expensive_product['total'], 750)  # 150 * 5
    
    def test_filter_products_empty(self):
        """Test filtering with empty product data."""
        empty_data = {"products": []}
        filtered = self.processor.filter_products(empty_data)
        self.assertEqual(len(filtered), 0)
    
    def test_filter_products_none_match(self):
        """Test filtering when no products match criteria."""
        cheap_data = {
            "products": [
                {"id": 1, "title": "Cheap 1", "price": 10, "stock": 1, "discountPercentage": 0, "thumbnail": ""},
                {"id": 2, "title": "Cheap 2", "price": 50, "stock": 1, "discountPercentage": 0, "thumbnail": ""}
            ]
        }
        filtered = self.processor.filter_products(cheap_data)
        self.assertEqual(len(filtered), 0)
    
    @patch('requests.get')
    def test_download_products_success(self, mock_get):
        """Test successful product download."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"products": [{"id": 1, "title": "Test"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.processor.download_products()
        
        self.assertIn("products", result)
        mock_get.assert_called_once_with(self.processor.source_url, timeout=30)
    
    @patch('boto3.client')
    def test_upload_to_s3_success(self, mock_boto_client):
        """Test successful S3 upload."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Create new processor instance to get the mocked client
        processor = ProductProcessor("test-bucket", "https://test-cloudfront.amazonaws.com")
        
        test_data = [{"id": 1, "title": "Test Product", "price": 100}]
        result = processor.upload_to_s3(test_data)
        
        self.assertTrue(result)
        mock_s3.put_object.assert_called_once()
    
    def test_discounted_price_calculation(self):
        """Test that discounted prices are calculated correctly."""
        sample_data = {
            "products": [
                {
                    "id": 1,
                    "title": "Discounted Product",
                    "price": 200,
                    "stock": 1,
                    "discountPercentage": 20,
                    "thumbnail": "https://example.com/1.jpg"
                }
            ]
        }
        
        filtered = self.processor.filter_products(sample_data)
        product = filtered[0]
        
        # 200 * (1 - 20/100) = 200 * 0.8 = 160
        expected_discounted_price = 160
        self.assertEqual(product['discountedPrice'], expected_discounted_price)


def run_tests():
    """Run all tests."""
    print("🧪 Running product processor tests...")
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestProductProcessor)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print results
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)