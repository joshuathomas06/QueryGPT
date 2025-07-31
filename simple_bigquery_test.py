#!/usr/bin/env python3
"""
Simple BigQuery integration test
"""

import os
import sys
from bigquery_inspector import BigQueryInspector

def test_bigquery_basic():
    """Basic BigQuery test"""
    
    print("🧪 Simple BigQuery Test")
    print("=" * 30)
    
    service_account_path = "./bigquery-service-account.json"
    project_id = "datastax-datalake"
    
    try:
        print("🔍 Initializing BigQuery inspector...")
        inspector = BigQueryInspector(service_account_path, project_id)
        print("✅ BigQuery inspector created successfully!")
        
        print("🔗 Testing basic connection...")
        result = inspector.test_connection()
        if result:
            print("✅ Connection test passed!")
        else:
            print("❌ Connection test failed")
            return False
        
        print("📊 Getting datasets...")
        datasets = inspector.get_datasets()
        print(f"Found {len(datasets)} datasets")
        
        if datasets:
            for i, dataset in enumerate(datasets[:3]):  # Show first 3
                print(f"  {i+1}. {dataset}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_bigquery_basic()
    print("\n" + "="*30)
    if success:
        print("✅ BigQuery integration looks good!")
    else:
        print("❌ BigQuery integration failed")
    sys.exit(0 if success else 1)