import psycopg
from typing import Dict, List, Tuple
import os
from dataclasses import dataclass


@dataclass
class TableInfo:
    name: str
    columns: List[Tuple[str, str]]  # (column_name, data_type)


class DatabaseInspector:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv('DATABASE_URL')
        if not self.connection_string:
            raise ValueError("Database connection string is required")
    
    def connect(self):
        """Create and return a database connection"""
        try:
            return psycopg.connect(self.connection_string)
        except psycopg.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
    
    def get_table_names(self) -> List[str]:
        """Fetch all table names from the database"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)
                return [row[0] for row in cur.fetchall()]
    
    def get_table_schema(self, table_name: str) -> List[Tuple[str, str]]:
        """Get column names and data types for a specific table"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                    AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """, (table_name,))
                return cur.fetchall()
    
    def get_full_schema(self) -> List[TableInfo]:
        """Get complete schema information for all tables"""
        table_names = self.get_table_names()
        tables = []
        
        for table_name in table_names:
            columns = self.get_table_schema(table_name)
            tables.append(TableInfo(name=table_name, columns=columns))
        
        return tables
    
    def execute_query(self, query: str) -> List[Dict]:
        """Execute a query and return results as list of dictionaries"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]