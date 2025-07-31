#!/usr/bin/env python3

import argparse
import os
import sys
from dotenv import load_dotenv

# Always load .env from the same folder as this script
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from database_inspector import DatabaseInspector
from schema_summarizer import SchemaSummarizer
from claude_refiner import ClaudeRefiner
from limited_bigquery_inspector import LimitedBigQueryInspector
from bigquery_summarizer import BigQuerySchemaSummarizer
from bigquery_sql_fixer import BigQuerySQLFixer


class QueryGPT:
    def __init__(self, database_url: str = None, anthropic_api_key: str = None, 
                 use_bigquery: bool = False, service_account_path: str = None, 
                 bigquery_project_id: str = None):
        if not anthropic_api_key:
            raise ValueError("❌ Error: Anthropic API key is required (set ANTHROPIC_API_KEY in .env)")

        self.use_bigquery = use_bigquery
        self.refiner = ClaudeRefiner(anthropic_api_key)
        
        if use_bigquery:
            self.db_inspector = LimitedBigQueryInspector(service_account_path, bigquery_project_id)
            self.summarizer = BigQuerySchemaSummarizer()
            self.db_type = "BigQuery"
            self.sql_fixer = None  # Will be initialized after schema is loaded
        else:
            if not database_url:
                raise ValueError("❌ Error: Database connection string is required (set DATABASE_URL in .env)")
            self.db_inspector = DatabaseInspector(database_url)
            self.summarizer = SchemaSummarizer()
            self.db_type = "PostgreSQL"

    def analyze_schema(self, use_claude: bool = True) -> str:
        print(f"🔍 Analyzing {self.db_type} schema...")
        
        if self.use_bigquery:
            tables = self.db_inspector.get_all_tables_info()
            # Initialize SQL fixer with known table names
            table_names = [table.full_name for table in tables]
            self.sql_fixer = BigQuerySQLFixer(table_names)
        else:
            tables = self.db_inspector.get_full_schema()
            
        basic_summary = self.summarizer.summarize_schema(tables)
        overview = self.summarizer.generate_schema_overview(tables)
        full_summary = overview + "\n" + basic_summary

        if use_claude:
            print("🤖 Refining summary with Claude...")
            # Add BigQuery-specific context to the summary
            if self.use_bigquery:
                full_summary = f"IMPORTANT: This is a BigQuery database. All table references MUST use the format: dataset_name.table_name\n\n{full_summary}"
            refined_summary = self.refiner.refine_schema_summary(full_summary)
            return refined_summary

        return full_summary

    def suggest_queries(self, schema_summary: str) -> str:
        print("💡 Generating query suggestions...")
        return self.refiner.generate_query_suggestions(schema_summary)

    def is_sql_query(self, text: str) -> bool:
        """Check if text looks like a SQL query"""
        sql_keywords = ['select', 'insert', 'update', 'delete', 'create', 'drop', 'alter', 'with']
        text_lower = text.lower().strip()
        return any(text_lower.startswith(keyword) for keyword in sql_keywords)

    def execute_and_explain_query(self, query: str, schema_context: str) -> tuple:
        print(f"⚡ Executing query: {query[:50]}...")
        try:
            # Fix SQL for BigQuery if needed
            if self.use_bigquery and hasattr(self, 'sql_fixer') and self.sql_fixer:
                original_query = query
                query = self.sql_fixer.fix_sql(query)
                if original_query != query:
                    print(f"🔧 Fixed SQL: {query[:100]}...")
            
            results = self.db_inspector.execute_query(query)
            explanation = self.refiner.explain_query_results(query, results, schema_context)
            return results, explanation
        except Exception as e:
            return None, f"Error executing query: {e}"

    def interactive_mode(self):
        print(f"🚀 Welcome to QueryGPT Interactive Mode ({self.db_type})!")
        print("Type 'help' for commands, 'quit' to exit\n")

        # Get initial schema analysis
        schema_summary = self.analyze_schema()
        print("\n" + "=" * 60)
        print("DATABASE SCHEMA ANALYSIS")
        print("=" * 60)
        print(schema_summary)
        print("\n" + "=" * 60)

        # Get query suggestions
        suggestions = self.suggest_queries(schema_summary)
        print("\nQUERY SUGGESTIONS")
        print("=" * 60)
        print(suggestions)
        print("\n" + "=" * 60)

        while True:
            try:
                user_input = input("\nQueryGPT> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    print("""
Available commands:
- help: Show this help message
- schema: Re-analyze database schema
- suggest: Get new query suggestions
- quit/exit/q: Exit the program
- Or enter any SQL query to execute and get explanation
- Or enter natural language questions (e.g., "how many users are there?")
""")
                
                elif user_input.lower() == 'schema':
                    schema_summary = self.analyze_schema()
                    print(schema_summary)
                
                elif user_input.lower() == 'suggest':
                    suggestions = self.suggest_queries(schema_summary)
                    print(suggestions)
                
                elif user_input.strip():
                    # Check if it's SQL or natural language
                    if self.is_sql_query(user_input):
                        # Execute SQL directly
                        results, explanation = self.execute_and_explain_query(user_input, schema_summary)
                    else:
                        # Convert natural language to SQL first
                        print("🤖 Converting natural language to SQL...")
                        sql_query = self.refiner.convert_natural_language_to_sql(user_input, schema_summary)
                        
                        if sql_query.startswith("Error"):
                            print(f"❌ {sql_query}")
                            continue
                        
                        print(f"📝 Generated SQL: {sql_query}")
                        
                        # Execute the generated SQL
                        results, explanation = self.execute_and_explain_query(sql_query, schema_summary)
                    
                    if results is not None:
                        print(f"\n📊 Query returned {len(results)} results")
                        print("\n🤖 Claude's Explanation:")
                        print("-" * 40)
                        print(explanation)
                        
                        if results and len(results) <= 10:
                            print(f"\n📋 Results ({len(results)} rows):")
                            for i, row in enumerate(results, 1):
                                print(f"{i}: {row}")
                        elif results:
                            print(f"\n📋 First 5 results (total: {len(results)} rows):")
                            for i, row in enumerate(results[:5], 1):
                                print(f"{i}: {row}")
                    else:
                        print(f"\n❌ {explanation}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="QueryGPT - Intelligent Database Schema Analysis")
    parser.add_argument("--database-url", help="PostgreSQL connection string")
    parser.add_argument("--anthropic-api-key", help="Anthropic API key")
    parser.add_argument("--no-claude", action="store_true", help="Skip Claude refinement")
    parser.add_argument("--query", help="Execute a single query and exit")
    parser.add_argument("--bigquery", action="store_true", help="Use BigQuery instead of PostgreSQL")
    parser.add_argument("--service-account-path", help="Path to BigQuery service account JSON file")
    parser.add_argument("--bigquery-project-id", help="BigQuery project ID")
    
    args = parser.parse_args()
    
    try:
        query_gpt = QueryGPT(
            database_url=args.database_url,
            anthropic_api_key=args.anthropic_api_key,
            use_bigquery=args.bigquery,
            service_account_path=args.service_account_path,
            bigquery_project_id=args.bigquery_project_id
        )
        
        if args.query:
            # Single query mode
            schema_summary = query_gpt.analyze_schema(not args.no_claude)
            results, explanation = query_gpt.execute_and_explain_query(args.query, schema_summary)
            
            if results is not None:
                print(f"Results: {len(results)} rows")
                print(f"Explanation: {explanation}")
                for row in results[:10]:  # Show first 10 results
                    print(row)
            else:
                print(explanation)
        else:
            # Interactive mode
            query_gpt.interactive_mode()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()