#!/usr/bin/env python3
"""List tables that might contain cost data"""

from limited_bigquery_inspector import LimitedBigQueryInspector

def list_cost_tables():
    inspector = LimitedBigQueryInspector(
        service_account_path="./bigquery-service-account.json",
        project_id="datastax-datalake"
    )
    
    print("🔍 Finding tables with cost/billing data...")
    
    tables = inspector.get_all_tables_info()
    
    cost_tables = []
    for table in tables:
        table_name_lower = table.table_id.lower()
        if any(keyword in table_name_lower for keyword in ['cost', 'billing', 'charge', 'spend', 'price']):
            cost_tables.append(table)
            print(f"\n📊 {table.full_name}")
            if table.description:
                print(f"   Description: {table.description}")
            if table.row_count:
                print(f"   Rows: {table.row_count:,}")
            if table.columns:
                print(f"   Columns: {', '.join([col[0] for col in table.columns[:5]])}")

    print(f"\n✅ Found {len(cost_tables)} cost-related tables")

if __name__ == "__main__":
    list_cost_tables()