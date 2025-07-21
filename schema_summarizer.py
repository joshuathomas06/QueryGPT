from typing import List
from database_inspector import TableInfo


class SchemaSummarizer:
    
    @staticmethod
    def format_data_type(data_type: str) -> str:
        """Convert PostgreSQL data types to human-readable format"""
        type_mapping = {
            'integer': 'whole number',
            'bigint': 'large whole number',
            'smallint': 'small whole number',
            'numeric': 'decimal number',
            'real': 'decimal number',
            'double precision': 'decimal number',
            'character varying': 'text',
            'varchar': 'text',
            'text': 'text',
            'char': 'single character',
            'boolean': 'true/false',
            'date': 'date',
            'timestamp': 'date and time',
            'timestamp without time zone': 'date and time',
            'timestamp with time zone': 'date and time with timezone',
            'time': 'time',
            'uuid': 'unique identifier',
            'json': 'JSON data',
            'jsonb': 'JSON data'
        }
        return type_mapping.get(data_type.lower(), data_type)
    
    @staticmethod
    def summarize_table(table: TableInfo) -> str:
        """Generate a human-friendly summary of a single table"""
        summary = f"**{table.name}** table:\n"
        
        if not table.columns:
            summary += "  - No columns found\n"
            return summary
        
        for column_name, data_type in table.columns:
            readable_type = SchemaSummarizer.format_data_type(data_type)
            summary += f"  - {column_name}: {readable_type}\n"
        
        return summary
    
    @staticmethod
    def summarize_schema(tables: List[TableInfo]) -> str:
        """Generate a comprehensive human-friendly summary of the entire schema"""
        if not tables:
            return "No tables found in the database."
        
        summary = f"Database contains {len(tables)} tables:\n\n"
        
        for table in tables:
            summary += SchemaSummarizer.summarize_table(table)
            summary += "\n"
        
        return summary.strip()
    
    @staticmethod
    def generate_schema_overview(tables: List[TableInfo]) -> str:
        """Generate a high-level overview of the database schema"""
        if not tables:
            return "Empty database with no tables."
        
        total_columns = sum(len(table.columns) for table in tables)
        table_names = [table.name for table in tables]
        
        overview = f"Database Overview:\n"
        overview += f"- Total tables: {len(tables)}\n"
        overview += f"- Total columns: {total_columns}\n"
        overview += f"- Table names: {', '.join(table_names)}\n\n"
        
        return overview