#!/usr/bin/env python3
"""Test the intelligent table suggestion system"""

import asyncio
import aiohttp
import json

async def test_suggestions():
    # First, check if API is running
    try:
        async with aiohttp.ClientSession() as session:
            # Check health
            async with session.get('http://localhost:8000/health') as resp:
                health = await resp.json()
                print(f"✅ API Status: {health['message']}")
                
            # Test 1: Cost-related query
            print("\n🧪 Test 1: Searching for cost tables...")
            query1 = {"question": "Show me daily costs by account"}
            
            async with session.post('http://localhost:8000/suggest-tables', json=query1) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print("\n📋 Table Suggestions:")
                    print(result['suggestions'])
                    print(f"\n✅ Found {len(result['tables'])} relevant tables")
                else:
                    print(f"❌ Error: {resp.status}")
                    
            # Test 2: Different query
            print("\n🧪 Test 2: Searching for cluster tables...")
            query2 = {"question": "Show cluster information"}
            
            async with session.post('http://localhost:8000/suggest-tables', json=query2) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print("\n📋 Table Suggestions:")
                    print(result['suggestions'])
                else:
                    print(f"❌ Error: {resp.status}")
                    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the API is running on port 8000")

if __name__ == "__main__":
    asyncio.run(test_suggestions())