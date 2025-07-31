"""
Intelligent Table Selector for BigQuery
Suggests relevant tables based on user query
"""

from typing import List, Dict, Tuple
from bigquery_inspector import BigQueryInspector
import re

class IntelligentTableSelector:
    def __init__(self, inspector: BigQueryInspector):
        self.inspector = inspector
        
    def extract_keywords(self, query: str) -> List[str]:
        """Extract meaningful keywords from user query"""
        # Common words to ignore
        stop_words = {'show', 'me', 'the', 'what', 'how', 'many', 'by', 'for', 'in', 'of', 'a', 'an', 'is', 'are', 'from', 'to', 'with'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Add common data keywords if mentioned
        data_keywords = {
            'cost': ['cost', 'spend', 'expense', 'billing', 'charge', 'payment', 'daily_cost'],
            'user': ['user', 'customer', 'account', 'organization', 'email'],
            'time': ['date', 'daily', 'monthly', 'yearly', 'time', 'period'],
            'cloud': ['cloud', 'aws', 'gcp', 'azure', 'provider', 'region'],
            'database': ['database', 'cluster', 'instance', 'node', 'deployment']
        }
        
        # Expand keywords based on synonyms
        expanded_keywords = []
        for keyword in keywords:
            expanded_keywords.append(keyword)
            for category, synonyms in data_keywords.items():
                if keyword in synonyms:
                    expanded_keywords.extend(synonyms)
                    
        return list(set(expanded_keywords))
    
    def search_tables(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for relevant tables based on query"""
        keywords = self.extract_keywords(query)
        print(f"🔍 Searching for tables with keywords: {', '.join(keywords)}")
        
        relevant_tables = []
        
        try:
            # Get all datasets
            datasets = self.inspector.get_datasets()
            
            for dataset_id in datasets:
                # Check if dataset name matches any keyword
                dataset_score = sum(1 for kw in keywords if kw in dataset_id.lower())
                
                if dataset_score > 0 or any(kw in dataset_id.lower() for kw in ['cost', 'billing', 'usage']):
                    try:
                        # Get tables in this dataset
                        tables = self.inspector.get_tables_in_dataset(dataset_id)
                        
                        for table_id in tables[:20]:  # Check first 20 tables per dataset
                            table_score = dataset_score
                            
                            # Score based on table name
                            table_name_lower = table_id.lower()
                            table_score += sum(2 for kw in keywords if kw in table_name_lower)
                            
                            # Bonus for cost-related tables
                            if any(term in table_name_lower for term in ['cost', 'billing', 'spend', 'charge']):
                                table_score += 3
                                
                            if table_score > 0:
                                try:
                                    # Get table info
                                    table_info = self.inspector.get_table_info(dataset_id, table_id)
                                    
                                    # Score based on column names
                                    column_names = [col[0].lower() for col in table_info.columns]
                                    column_score = sum(1 for kw in keywords for col in column_names if kw in col)
                                    
                                    total_score = table_score + column_score
                                    
                                    relevant_tables.append({
                                        'table_info': table_info,
                                        'score': total_score,
                                        'matching_keywords': [kw for kw in keywords if kw in table_name_lower or any(kw in col for col in column_names)]
                                    })
                                except:
                                    continue
                    except:
                        continue
                        
            # Sort by relevance score
            relevant_tables.sort(key=lambda x: x['score'], reverse=True)
            
            return relevant_tables[:max_results]
            
        except Exception as e:
            print(f"❌ Error searching tables: {e}")
            return []
    
    def format_table_suggestion(self, table_data: Dict) -> str:
        """Format a table suggestion for display"""
        table = table_data['table_info']
        score = table_data['score']
        keywords = table_data['matching_keywords']
        
        suggestion = f"\n📊 **{table.full_name}**\n"
        
        if table.description:
            suggestion += f"   Description: {table.description}\n"
            
        if table.row_count:
            suggestion += f"   Rows: {table.row_count:,}\n"
            
        if table.columns:
            cols = [f"{col[0]}" for col in table.columns[:8]]
            suggestion += f"   Key columns: {', '.join(cols)}\n"
            
        suggestion += f"   Relevance: {'⭐' * min(score, 5)} (matches: {', '.join(keywords)})\n"
        
        return suggestion
    
    def suggest_tables_for_query(self, user_query: str) -> Tuple[List[Dict], str]:
        """Main method to suggest tables based on user query"""
        print(f"\n🤔 Understanding your query: '{user_query}'")
        
        # Search for relevant tables
        relevant_tables = self.search_tables(user_query)
        
        if not relevant_tables:
            return [], "No relevant tables found for your query."
        
        # Format suggestions
        suggestions = "## 📋 Suggested Tables for Your Query\n\n"
        suggestions += f"Based on your query about '{user_query}', here are the most relevant tables:\n"
        
        for i, table_data in enumerate(relevant_tables, 1):
            suggestions += f"\n### Option {i}:"
            suggestions += self.format_table_suggestion(table_data)
        
        suggestions += "\n💡 **Next Step**: Choose a table number (1-{}) to generate a specific query for that table.".format(len(relevant_tables))
        
        return relevant_tables, suggestions