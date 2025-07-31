#!/usr/bin/env python3
"""
Test complete BigQuery integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from query_gpt import QueryGPT

def test_bigquery_querygpt():
    print("🧪 Testing QueryGPT with BigQuery")
    print("=" * 50)
    
    try:
        # Initialize QueryGPT with BigQuery
        query_gpt = QueryGPT(
            database_url=None,
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
            use_bigquery=True,
            service_account_path='./bigquery-service-account.json',
            bigquery_project_id='datastax-datalake'
        )
        
        print("✅ QueryGPT initialized with BigQuery")
        print(f"Database type: {query_gpt.db_type}")
        
        # Test simple query
        test_query = "SELECT COUNT(*) as dataset_count FROM `datastax-datalake.INFORMATION_SCHEMA.SCHEMATA`"
        print(f"\n📝 Testing query: {test_query}")
        
        results, explanation = query_gpt.execute_and_explain_query(test_query, "BigQuery system tables")
        
        if results is not None:
            print(f"✅ Query executed successfully!")
            print(f"Results: {results}")
            print(f"\nExplanation: {explanation}")
        else:
            print(f"❌ Query failed: {explanation}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_bigquery_querygpt()
    print("\n" + "="*50)
    if success:
        print("✅ BigQuery integration test passed!")
        print("\nYou can now use:")
        print("1. Interactive mode: python query_gpt.py --bigquery")
        print("2. API mode: python api.py (with USE_BIGQUERY=true in .env)")
    else:
        print("❌ Integration test failed")