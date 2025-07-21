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


class QueryGPT:
    def __init__(self, database_url: str = None, anthropic_api_key: str = None):
        if not database_url:
            raise ValueError("❌ Error: Database connection string is required (set DATABASE_URL in .env)")
        if not anthropic_api_key:
            raise ValueError("❌ Error: Anthropic API key is required (set ANTHROPIC_API_KEY in .env)")

        self.db_inspector = DatabaseInspector(database_url)
        self.summarizer = SchemaSummarizer()
        self.refiner = ClaudeRefiner(anthropic_api_key)

    def analyze_schema(self, use_claude: bool = True) -> str:
        print("🔍 Analyzing database schema...")
        tables = self.db_inspector.get_full_schema()
        basic_summary = self.summarizer.summarize_schema(tables)
        overview = self.summarizer.generate_schema_overview(tables)
        full_summary = overview + "\n" + basic_summary

        if use_claude:
            print("🤖 Refining summary with Claude...")
            refined_summary = self.refiner.refine_schema_summary(full_summary)
            return refined_summary

        return full_summary

    def suggest_queries(self, schema_summary: str) -> str:
        print("💡 Generating query suggestions...")
        return self.refiner.generate_query_suggestions(schema_summary)

    def execute_and_explain_query(self, query: str, schema_context: str) -> tuple:
        print(f"⚡ Executing query: {query[:50]}...")
        try:
            results = self.db_inspector.execute_query(query)
            explanation = self.refiner.explain_query_results(query, results, schema_context)
            return results, explanation
        except Exception as e:
            return None, f"Error executing query: {e}"

    def interactive_mode(self):
        print("🚀 Welcome to QueryGPT Interactive Mode!")
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
            user_input = input("\nQueryGPT> ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
#!/usr/bin/env python3

import argparse
import sys
from database_inspector import DatabaseInspector
from schema_summarizer import SchemaSummarizer
from claude_refiner import ClaudeRefiner


class QueryGPT:
    def __init__(self, database_url: str = None, anthropic_api_key: str = None):
        self.db_inspector = DatabaseInspector(database_url)
        self.summarizer = SchemaSummarizer()
        self.refiner = ClaudeRefiner(anthropic_api_key)
    
    def analyze_schema(self, use_claude: bool = True) -> str:
        """Analyze database schema and return summary"""
        print("🔍 Analyzing database schema...")
        
        # Get schema information
        tables = self.db_inspector.get_full_schema()
        
        # Generate basic summary
        basic_summary = self.summarizer.summarize_schema(tables)
        overview = self.summarizer.generate_schema_overview(tables)
        
        full_summary = overview + "\n" + basic_summary
        
        if use_claude:
            print("🤖 Refining summary with Claude...")
            refined_summary = self.refiner.refine_schema_summary(full_summary)
            return refined_summary
        
        return full_summary
    
    def suggest_queries(self, schema_summary: str) -> str:
        """Generate query suggestions based on schema"""
        print("💡 Generating query suggestions...")
        return self.refiner.generate_query_suggestions(schema_summary)
    
    def is_sql_query(self, text: str) -> bool:
        """Check if text looks like a SQL query"""
        sql_keywords = ['select', 'insert', 'update', 'delete', 'create', 'drop', 'alter', 'with']
        text_lower = text.lower().strip()
        return any(text_lower.startswith(keyword) for keyword in sql_keywords)

    def execute_and_explain_query(self, query: str, schema_context: str) -> tuple:
        """Execute query and get Claude explanation"""
        print(f"⚡ Executing query: {query[:50]}...")
        
        try:
            results = self.db_inspector.execute_query(query)
            explanation = self.refiner.explain_query_results(query, results, schema_context)
            return results, explanation
        except Exception as e:
            return None, f"Error executing query: {e}"
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("🚀 Welcome to QueryGPT Interactive Mode!")
        print("Type 'help' for commands, 'quit' to exit\n")
        
        # Get initial schema analysis
        schema_summary = self.analyze_schema()
        print("\n" + "="*60)
        print("DATABASE SCHEMA ANALYSIS")
        print("="*60)
        print(schema_summary)
        print("\n" + "="*60)
        
        # Get query suggestions
        suggestions = self.suggest_queries(schema_summary)
        print("\nQUERY SUGGESTIONS")
        print("="*60)
        print(suggestions)
        print("\n" + "="*60)
        
        # Interactive query loop
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
    parser = argparse.ArgumentParser(description="QueryGPT - Intelligent PostgreSQL Schema Analysis")
    parser.add_argument("--database-url", help="PostgreSQL connection string")
    parser.add_argument("--anthropic-api-key", help="Anthropic API key")
    parser.add_argument("--no-claude", action="store_true", help="Skip Claude refinement")
    parser.add_argument("--query", help="Execute a single query and exit")
    
    args = parser.parse_args()
    
    try:
        query_gpt = QueryGPT(args.database_url, args.anthropic_api_key)
        
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
