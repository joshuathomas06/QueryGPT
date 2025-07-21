#!/usr/bin/env python3

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from query_gpt import QueryGPT

app = FastAPI(title="QueryGPT API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QueryGPT instance
query_gpt = None

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]
    explanation: str
    success: bool
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    global query_gpt
    database_url = os.getenv("DATABASE_URL")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not database_url or not anthropic_api_key:
        raise ValueError("Missing required environment variables: DATABASE_URL and ANTHROPIC_API_KEY")
    
    query_gpt = QueryGPT(database_url, anthropic_api_key)
    
    # Initialize schema summary for better performance
    print("🚀 Initializing QueryGPT API...")
    query_gpt.schema_summary = query_gpt.analyze_schema()
    print("✅ QueryGPT API ready!")

@app.get("/")
async def root():
    return {"message": "QueryGPT API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "QueryGPT API is running"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        if not query_gpt:
            raise HTTPException(status_code=503, detail="QueryGPT not initialized")
        
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Check if it's already SQL or natural language
        if query_gpt.is_sql_query(question):
            sql_query = question
        else:
            # Convert natural language to SQL
            sql_query = query_gpt.refiner.convert_natural_language_to_sql(
                question, query_gpt.schema_summary
            )
            
            if sql_query.startswith("Error"):
                return QueryResponse(
                    sql_query="",
                    results=[],
                    explanation=sql_query,
                    success=False,
                    error=sql_query
                )
        
        # Execute the query
        results, explanation = query_gpt.execute_and_explain_query(
            sql_query, query_gpt.schema_summary
        )
        
        if results is not None:
            return QueryResponse(
                sql_query=sql_query,
                results=results,
                explanation=explanation,
                success=True
            )
        else:
            return QueryResponse(
                sql_query=sql_query,
                results=[],
                explanation=explanation,
                success=False,
                error=explanation
            )
    
    except Exception as e:
        return QueryResponse(
            sql_query="",
            results=[],
            explanation=f"Internal server error: {str(e)}",
            success=False,
            error=str(e)
        )

@app.get("/schema")
async def get_schema():
    try:
        if not query_gpt:
            raise HTTPException(status_code=503, detail="QueryGPT not initialized")
        
        return {
            "schema": query_gpt.schema_summary,
            "success": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)