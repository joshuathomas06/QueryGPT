#!/usr/bin/env python3

import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

from query_gpt import QueryGPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="QueryGPT API", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
query_gpt = None
initialization_lock = asyncio.Lock()
is_initialized = False

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]
    explanation: str
    success: bool
    error: Optional[str] = None

async def initialize_query_gpt():
    """Initialize QueryGPT asynchronously"""
    global query_gpt, is_initialized
    
    async with initialization_lock:
        if is_initialized:
            return
            
        try:
            logger.info("🚀 Initializing QueryGPT API...")
            
            # Check if we should use BigQuery
            use_bigquery = os.getenv("USE_BIGQUERY", "false").lower() == "true"
            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
            
            if not anthropic_api_key:
                raise ValueError("Missing required environment variable: ANTHROPIC_API_KEY")
            
            if use_bigquery:
                service_account_path = os.getenv("BIGQUERY_SERVICE_ACCOUNT_PATH")
                project_id = os.getenv("BIGQUERY_PROJECT_ID")
                
                if not service_account_path:
                    raise ValueError("Missing required environment variable: BIGQUERY_SERVICE_ACCOUNT_PATH")
                
                query_gpt = QueryGPT(
                    anthropic_api_key=anthropic_api_key,
                    use_bigquery=True,
                    service_account_path=service_account_path,
                    bigquery_project_id=project_id
                )
                logger.info("🚀 Initialized with BigQuery")
            else:
                database_url = os.getenv("DATABASE_URL")
                
                if not database_url:
                    raise ValueError("Missing required environment variable: DATABASE_URL")
                
                query_gpt = QueryGPT(database_url, anthropic_api_key)
                logger.info("🚀 Initialized with PostgreSQL")
            
            # Initialize schema in background to avoid timeout
            logger.info("📊 Loading schema (this may take a moment)...")
            query_gpt.schema_summary = query_gpt.analyze_schema()
            
            is_initialized = True
            logger.info("✅ QueryGPT API ready!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize QueryGPT: {e}")
            raise

@app.on_event("startup")
async def startup_event():
    """Start initialization in background"""
    asyncio.create_task(initialize_query_gpt())
    logger.info("📋 Started initialization task")

@app.get("/")
async def root():
    return {"message": "QueryGPT API is running", "initialized": is_initialized}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "QueryGPT API is running",
        "initialized": is_initialized
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # Ensure initialization is complete
        if not is_initialized:
            await initialize_query_gpt()
        
        if not query_gpt:
            raise HTTPException(status_code=503, detail="QueryGPT not initialized")
        
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Process query with timeout protection
        try:
            # Check if it's already SQL or natural language
            if query_gpt.is_sql_query(question):
                sql_query = question
            else:
                # Convert natural language to SQL with timeout
                sql_query = await asyncio.wait_for(
                    asyncio.to_thread(
                        query_gpt.refiner.convert_natural_language_to_sql,
                        question, 
                        query_gpt.schema_summary
                    ),
                    timeout=30.0  # 30 second timeout
                )
                
                if sql_query.startswith("Error"):
                    return QueryResponse(
                        sql_query="",
                        results=[],
                        explanation=sql_query,
                        success=False,
                        error=sql_query
                    )
            
            # Execute the query with timeout
            results, explanation = await asyncio.wait_for(
                asyncio.to_thread(
                    query_gpt.execute_and_explain_query,
                    sql_query,
                    query_gpt.schema_summary
                ),
                timeout=60.0  # 60 second timeout
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
                
        except asyncio.TimeoutError:
            logger.error("Query processing timed out")
            return QueryResponse(
                sql_query="",
                results=[],
                explanation="Query processing timed out. Please try a simpler query.",
                success=False,
                error="Timeout"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
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
        if not is_initialized:
            await initialize_query_gpt()
            
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