#!/usr/bin/env python3
"""Test QueryGPT with a simple query"""

import requests
import json

def test_query():
    url = "http://localhost:8000/query"
    
    # Simple query that should work
    query = {
        "question": "SELECT cloud_account, SUM(daily_cost) as total FROM astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary GROUP BY cloud_account ORDER BY total DESC LIMIT 5"
    }
    
    print("🧪 Testing query:", query["question"][:50] + "...")
    
    try:
        response = requests.post(url, json=query)
        result = response.json()
        
        print("\n📊 Response:")
        print(f"Success: {result.get('success', False)}")
        print(f"SQL: {result.get('sql_query', 'N/A')[:100]}...")
        
        if result.get('success'):
            print(f"Results: {len(result.get('results', []))} rows")
            if result.get('results'):
                print("\nFirst result:", result['results'][0])
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_query()