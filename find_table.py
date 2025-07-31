#!/usr/bin/env python3
"""Find which dataset contains a specific table"""

from bigquery_inspector import BigQueryInspector

def find_table():
    inspector = BigQueryInspector(
        service_account_path="./bigquery-service-account.json",
        project_id="datastax-datalake"
    )
    
    target_table = "tblDailyDedicatedDatabaseNodeCostSummary"
    
    datasets = inspector.get_datasets()[:20]  # Check first 20 datasets
    
    for dataset_id in datasets:
        try:
            tables = inspector.get_tables_in_dataset(dataset_id)
            for table in tables:
                if target_table.lower() in table.lower():
                    print(f"✅ Found: {dataset_id}.{table}")
        except:
            pass

if __name__ == "__main__":
    find_table()