#!/usr/bin/env python3
"""
Quick test for BigQuery integration
"""

from bigquery_inspector import BigQueryInspector
from bigquery_summarizer import BigQuerySchemaSummarizer

def test_basic_functionality():
    print("🧪 Testing BigQuery Integration")
    print("=" * 40)
    
    # Test BigQuery connection
    inspector = BigQueryInspector(
        service_account_path="./bigquery-service-account.json",
        project_id="datastax-datalake"
    )
    
    print("✅ BigQuery inspector created")
    
    # Test connection
    if inspector.test_connection():
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        return False
    
    # Get datasets
    datasets = inspector.get_datasets()
    print(f"✅ Found {len(datasets)} datasets")
    
    if datasets:
        # Get tables from first dataset
        first_dataset = datasets[0]
        print(f"📊 Testing dataset: {first_dataset}")
        
        tables = inspector.get_tables_in_dataset(first_dataset)
        print(f"✅ Found {len(tables)} tables in {first_dataset}")
        
        if tables:
            # Get info for first table
            table_info = inspector.get_table_info(first_dataset, tables[0])
            print(f"✅ Table info: {table_info.full_name}")
            print(f"   Rows: {table_info.row_count:,}" if table_info.row_count else "   Rows: Unknown")
            print(f"   Columns: {len(table_info.columns)}")
    
    print("\n🎉 BigQuery integration is working!")
    return True

if __name__ == "__main__":
    test_basic_functionality()