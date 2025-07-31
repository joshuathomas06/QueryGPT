#!/usr/bin/env python3
"""
Test script for BigQuery integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from bigquery_inspector import BigQueryInspector
from bigquery_summarizer import BigQuerySchemaSummarizer

def test_bigquery_connection():
    """Test BigQuery connection and basic functionality"""
    
    print("🧪 Testing BigQuery Integration")
    print("=" * 50)
    
    # Get configuration from environment variables
    service_account_path = os.getenv('BIGQUERY_SERVICE_ACCOUNT_PATH')
    project_id = os.getenv('BIGQUERY_PROJECT_ID')
    
    if not service_account_path:
        print("❌ Error: BIGQUERY_SERVICE_ACCOUNT_PATH not set in .env file")
        print("Please set the path to your BigQuery service account JSON file")
        return False
    
    if not os.path.exists(service_account_path):
        print(f"❌ Error: Service account file not found: {service_account_path}")
        return False
    
    try:
        # Initialize BigQuery inspector
        print("🔍 Initializing BigQuery inspector...")
        inspector = BigQueryInspector(service_account_path, project_id)
        
        # Test connection
        print("🔗 Testing connection...")
        if not inspector.test_connection():
            print("❌ Connection test failed")
            return False
        print("✅ Connection successful!")
        
        # Get datasets
        print("📊 Getting datasets...")
        datasets = inspector.get_datasets()
        print(f"Found {len(datasets)} datasets: {', '.join(datasets[:5])}{'...' if len(datasets) > 5 else ''}")
        
        if not datasets:
            print("⚠️  No datasets found in the project")
            return True
        
        # Get tables from first dataset
        first_dataset = datasets[0]
        print(f"📋 Getting tables from dataset '{first_dataset}'...")
        tables = inspector.get_tables_in_dataset(first_dataset)
        print(f"Found {len(tables)} tables in {first_dataset}")
        
        if tables:
            # Get info for first table
            first_table = tables[0]
            print(f"📄 Getting info for table '{first_table}'...")
            table_info = inspector.get_table_info(first_dataset, first_table)
            print(f"Table: {table_info.full_name}")
            print(f"Rows: {table_info.row_count:,}" if table_info.row_count else "Rows: Unknown")
            print(f"Columns: {len(table_info.columns)}")
            
            if table_info.columns:
                print("First few columns:")
                for col_name, col_type in table_info.columns[:3]:
                    print(f"  - {col_name}: {col_type}")
        
        # Test schema summarizer
        print("\n🤖 Testing schema summarizer...")
        summarizer = BigQuerySchemaSummarizer()
        
        # Get limited table info for summary
        print("📝 Getting table information for summary...")
        all_tables = inspector.get_all_tables_info(max_tables_per_dataset=5)  # Limit for testing
        
        if all_tables:
            print(f"✅ Retrieved information for {len(all_tables)} tables")
            
            # Generate summary
            print("\n📋 Generating schema summary...")
            summary = summarizer.summarize_schema(all_tables)
            
            # Print truncated summary
            summary_lines = summary.split('\n')
            if len(summary_lines) > 20:
                print('\n'.join(summary_lines[:20]))
                print(f"... (truncated, showing first 20 lines of {len(summary_lines)} total)")
            else:
                print(summary)
        
        print("\n✅ BigQuery integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during BigQuery test: {e}")
        return False

if __name__ == "__main__":
    success = test_bigquery_connection()
    sys.exit(0 if success else 1)