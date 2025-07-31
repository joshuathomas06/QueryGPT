import anthropic
import os
from typing import Optional


class ClaudeRefiner:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def refine_schema_summary(self, schema_summary: str) -> str:
        """Use Claude to refine and improve the schema summary"""
        prompt = f"""
Please refine and improve this database schema summary to make it more clear and user-friendly:

{schema_summary}

Please:
1. Make the language more natural and conversational
2. Identify potential relationships between tables (if any seem obvious)
3. Suggest what kind of application or domain this database might be for
4. Highlight any interesting patterns or observations
5. Keep it concise but informative

Return only the refined summary, no additional commentary.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error refining summary: {e}\n\nOriginal summary:\n{schema_summary}"
    
    def generate_query_suggestions(self, schema_summary: str) -> str:
        """Generate helpful SQL query suggestions based on the schema"""
        prompt = f"""
Based on this database schema:

{schema_summary}

Generate 5-7 useful SQL query examples that would be interesting to run against this database. Include:
1. Simple SELECT queries for each table
2. JOIN queries if relationships are apparent
3. Aggregate queries (COUNT, SUM, AVG, etc.)
4. Filtering examples with WHERE clauses

Format each query clearly with a brief explanation of what it does.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating query suggestions: {e}"
    
    def convert_natural_language_to_sql(self, natural_query: str, schema_context: str) -> str:
        """Convert natural language query to SQL"""
        # Check if this is BigQuery based on schema context
        is_bigquery = "BigQuery" in schema_context or "dataset" in schema_context.lower()
        
        prompt = f"""
Given this database schema context:
{schema_context}

User query: "{natural_query}"

STEP 1: First, identify which tables from the schema are most relevant for this query.

STEP 2: Then generate a SQL query using the most appropriate table.

Important guidelines:
1. Generate a valid {"BigQuery" if is_bigquery else "SQL"} query that answers the question
2. {"CRITICAL: This is BigQuery - you MUST use fully qualified table names in the format: dataset_name.table_name (e.g., astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary)" if is_bigquery else "Use proper table names from the schema"}
2. Use proper table and column names from the schema
3. For COUNT, SUM, AVG and other aggregations, always use GROUP BY appropriately
4. When asked for "count by category" or similar, use: SELECT category, COUNT(*) FROM table GROUP BY category
5. When asked for "total cost by provider", use: SELECT provider, SUM(total_cost) FROM table GROUP BY provider
6. Include appropriate JOINs if multiple tables are needed
7. Use proper WHERE clauses for filtering
8. Order results by count/sum descending when showing aggregations
9. For cost tables in BigQuery, use these EXACT column names: daily_cost (not total_cost), cloud_account, organization_email, cloud_region, deployment_type, usage_date

CRITICAL INSTRUCTIONS:
- Return ONLY the SQL query
- Do NOT include any explanations, introductions, or text before/after the SQL
- Start your response with SELECT, WITH, or other SQL keywords
- If you cannot generate a query, return: SELECT 'No matching tables found' as message;
- NEVER start with "Here is", "Based on", "The following", etc.

Example correct response:
SELECT cloud_account, SUM(daily_cost) as total_cost FROM astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary GROUP BY cloud_account ORDER BY total_cost DESC;
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"Error converting query: {e}"

    def explain_query_results(self, query: str, results: list, schema_context: str) -> str:
        """Explain query results in human-friendly terms"""
        results_preview = str(results[:5]) if len(results) > 5 else str(results)
        
        prompt = f"""
Given this database schema context:
{schema_context}

And this SQL query:
{query}

Which returned these results (showing first 5 rows):
{results_preview}

Please provide a clear, human-friendly explanation of:
1. What the query is doing
2. What the results mean
3. Any interesting insights from the data
4. Total number of results: {len(results)}

Keep it conversational and accessible to non-technical users.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error explaining results: {e}"