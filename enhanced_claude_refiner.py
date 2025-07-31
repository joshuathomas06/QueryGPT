"""
Enhanced Claude Refiner that suggests tables before generating SQL
"""

from claude_refiner import ClaudeRefiner

class EnhancedClaudeRefiner(ClaudeRefiner):
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        
    def suggest_and_generate_sql(self, natural_query: str, schema_context: str) -> dict:
        """
        First suggest relevant tables, then generate SQL for the most relevant one
        """
        
        # Step 1: Ask Claude to identify relevant tables
        table_suggestion_prompt = f"""
Given this BigQuery database schema:
{schema_context}

And this user query: "{natural_query}"

Please identify the 3 most relevant tables for this query. For each table:
1. Table name (in dataset.table format)
2. Why it's relevant
3. Key columns that would be useful

Format your response as:
TABLE_SUGGESTIONS:
1. dataset.table_name - reason - columns: col1, col2, col3
2. dataset.table_name - reason - columns: col1, col2, col3
3. dataset.table_name - reason - columns: col1, col2, col3

Then generate SQL for the MOST relevant table:
SQL_QUERY:
<your SQL here>
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": table_suggestion_prompt}]
            )
            
            full_response = response.content[0].text
            
            # Parse the response
            suggestions = []
            sql_query = ""
            
            if "TABLE_SUGGESTIONS:" in full_response:
                suggestions_part = full_response.split("SQL_QUERY:")[0]
                suggestions_text = suggestions_part.split("TABLE_SUGGESTIONS:")[1].strip()
                
                # Parse each suggestion line
                for line in suggestions_text.split('\n'):
                    if line.strip() and line[0].isdigit():
                        suggestions.append(line.strip())
            
            if "SQL_QUERY:" in full_response:
                sql_query = full_response.split("SQL_QUERY:")[1].strip()
                # Clean up the SQL
                sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            return {
                "suggestions": suggestions[:3],
                "sql_query": sql_query,
                "explanation": f"Based on your query '{natural_query}', I found {len(suggestions)} relevant tables and generated SQL for the most appropriate one."
            }
            
        except Exception as e:
            # Fallback to original method
            sql_query = self.convert_natural_language_to_sql(natural_query, schema_context)
            return {
                "suggestions": [],
                "sql_query": sql_query,
                "explanation": "Generated SQL query directly."
            }