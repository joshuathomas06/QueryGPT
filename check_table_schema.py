#!/usr/bin/env python3
"""Check the actual schema of the cost table"""

from bigquery_inspector import BigQueryInspector

def check_schema():
    inspector = BigQueryInspector(
        service_account_path="./bigquery-service-account.json",
        project_id="datastax-datalake"
    )
    
    print("🔍 Checking schema for astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary")
    
    try:
        # Get full table info
        table_ref = inspector.client.get_table("datastax-datalake.astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary")
        
        print(f"\n📊 Table: {table_ref.table_id}")
        print(f"Rows: {table_ref.num_rows:,}")
        print(f"Created: {table_ref.created}")
        print(f"\n📋 All Columns:")
        
        for i, field in enumerate(table_ref.schema, 1):
            print(f"{i}. {field.name} ({field.field_type})")
            
        # Try a simple query
        print("\n🧪 Testing simple query...")
        query = f"SELECT * FROM `datastax-datalake.astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary` LIMIT 1"
        results = inspector.execute_query(query)
        
        if results:
            print("\n✅ Sample row:")
            for key, value in results[0].items():
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_schema()