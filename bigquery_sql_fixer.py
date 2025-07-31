"""
BigQuery SQL Fixer - Ensures SQL queries are properly formatted for BigQuery
"""
import re
from typing import Dict, List, Tuple

class BigQuerySQLFixer:
    def __init__(self, known_tables: List[str]):
        """
        Initialize with a list of known table names in format: dataset.table
        """
        self.known_tables = known_tables
        self.table_map = {}
        
        # Build a map of table_name -> full_qualified_name
        for full_name in known_tables:
            if '.' in full_name:
                dataset, table = full_name.split('.', 1)
                self.table_map[table.lower()] = full_name
    
    def fix_sql(self, sql: str) -> str:
        """
        Fix SQL to ensure BigQuery compatibility
        """
        # Try to extract SQL from text that might contain explanations
        sql = sql.strip()
        
        # Look for SQL starting with common keywords
        sql_keywords = ['SELECT', 'WITH', 'INSERT', 'UPDATE', 'DELETE']
        
        # If the text contains SQL keywords, try to extract the SQL part
        for keyword in sql_keywords:
            if keyword in sql.upper():
                # Find where the SQL starts
                start_pos = sql.upper().find(keyword)
                sql = sql[start_pos:]
                break
        
        # Check if it's valid SQL now
        if not any(sql.upper().startswith(keyword) for keyword in sql_keywords):
            # Return a default query if the SQL is not valid
            return "SELECT 'Invalid SQL query provided' as error_message"
        
        # Fix table references
        fixed_sql = self._fix_table_references(sql)
        
        # Fix INFORMATION_SCHEMA references
        fixed_sql = self._fix_information_schema(fixed_sql)
        
        return fixed_sql
    
    def _fix_table_references(self, sql: str) -> str:
        """
        Replace unqualified table names with fully qualified ones
        """
        # Pattern to find FROM and JOIN table references
        from_pattern = r'(FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_table(match):
            keyword = match.group(1)
            table_name = match.group(2)
            
            # Check if it's already qualified (contains a dot)
            if '.' in table_name:
                return match.group(0)
            
            # Look up the full name
            full_name = self.table_map.get(table_name.lower())
            if full_name:
                return f"{keyword} {full_name}"
            
            # If not found, return as is
            return match.group(0)
        
        return re.sub(from_pattern, replace_table, sql, flags=re.IGNORECASE)
    
    def _fix_information_schema(self, sql: str) -> str:
        """
        Fix INFORMATION_SCHEMA references for BigQuery
        """
        # Replace generic information_schema with BigQuery format
        sql = re.sub(
            r'information_schema\.tables',
            '`datastax-datalake.INFORMATION_SCHEMA.TABLES`',
            sql,
            flags=re.IGNORECASE
        )
        
        sql = re.sub(
            r'information_schema\.schemata',
            '`datastax-datalake.INFORMATION_SCHEMA.SCHEMATA`',
            sql,
            flags=re.IGNORECASE
        )
        
        return sql