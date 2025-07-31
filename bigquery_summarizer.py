from typing import List, Dict
from bigquery_inspector import BigQueryTableInfo


class BigQuerySchemaSummarizer:
    @staticmethod
    def format_data_type(data_type: str) -> str:
        """Convert BigQuery data types to human-readable format"""
        type_mapping = {
            'STRING': 'text',
            'INTEGER': 'whole number',
            'INT64': 'whole number', 
            'FLOAT': 'decimal number',
            'FLOAT64': 'decimal number',
            'NUMERIC': 'decimal number',
            'BOOLEAN': 'true/false',
            'BOOL': 'true/false',
            'TIMESTAMP': 'timestamp',
            'DATETIME': 'date and time',
            'DATE': 'date',
            'TIME': 'time',
            'BYTES': 'binary data',
            'ARRAY': 'array/list',
            'STRUCT': 'structured object',
            'RECORD': 'structured record',
            'GEOGRAPHY': 'geographic data',
            'JSON': 'JSON data'
        }
        return type_mapping.get(data_type.upper(), data_type.lower())
    
    @staticmethod
    def summarize_table(table: BigQueryTableInfo) -> str:
        """Generate a human-friendly summary of a single table"""
        summary = f"**{table.full_name}**"
        
        if table.description:
            summary += f" - {table.description}"
        
        summary += f" ({table.table_type.lower()})"
        
        if table.row_count is not None:
            if table.row_count > 1000000:
                summary += f" - {table.row_count:,} rows (large table)"
            elif table.row_count > 10000:
                summary += f" - {table.row_count:,} rows (medium table)"
            else:
                summary += f" - {table.row_count:,} rows (small table)"
        
        summary += "\n"
        
        # Add column information
        if table.columns:
            summary += "  Columns:\n"
            for column_name, data_type in table.columns:
                readable_type = BigQuerySchemaSummarizer.format_data_type(data_type)
                summary += f"    - {column_name}: {readable_type}\n"
        
        # Add additional metadata
        if table.labels:
            summary += f"  Labels: {', '.join([f'{k}:{v}' for k, v in table.labels.items()])}\n"
        
        if table.created:
            summary += f"  Created: {table.created[:10]}\n"  # Just the date part
        
        return summary
    
    @staticmethod
    def summarize_schema(tables: List[BigQueryTableInfo]) -> str:
        """Generate human-friendly summary of all tables"""
        if not tables:
            return "No tables found in BigQuery project."
        
        # Group tables by dataset
        datasets = {}
        for table in tables:
            if table.dataset_id not in datasets:
                datasets[table.dataset_id] = []
            datasets[table.dataset_id].append(table)
        
        summary = f"BigQuery project contains {len(tables)} tables across {len(datasets)} datasets:\n\n"
        
        for dataset_id, dataset_tables in datasets.items():
            summary += f"📊 **Dataset: {dataset_id}** ({len(dataset_tables)} tables)\n"
            
            # Sort tables by row count (largest first) for better prioritization
            sorted_tables = sorted(dataset_tables, 
                                 key=lambda t: t.row_count if t.row_count else 0, 
                                 reverse=True)
            
            for table in sorted_tables:
                table_summary = BigQuerySchemaSummarizer.summarize_table(table)
                # Indent the table summary
                indented_summary = '\n'.join(['  ' + line for line in table_summary.split('\n')])
                summary += indented_summary + "\n"
            
            summary += "\n"
        
        return summary.strip()
    
    @staticmethod
    def generate_schema_overview(tables: List[BigQueryTableInfo]) -> str:
        """Generate a high-level overview of the BigQuery schema"""
        if not tables:
            return "No BigQuery tables available for analysis."
        
        # Collect statistics
        total_tables = len(tables)
        datasets = set(table.dataset_id for table in tables)
        table_types = {}
        total_rows = 0
        
        for table in tables:
            table_type = table.table_type
            table_types[table_type] = table_types.get(table_type, 0) + 1
            if table.row_count:
                total_rows += table.row_count
        
        # Find largest tables
        tables_with_rows = [t for t in tables if t.row_count and t.row_count > 0]
        largest_tables = sorted(tables_with_rows, key=lambda t: t.row_count, reverse=True)[:5]
        
        overview = f"""🔍 BigQuery Schema Overview:
- Total tables: {total_tables}
- Datasets: {len(datasets)} ({', '.join(sorted(datasets))})
- Table types: {', '.join([f'{count} {type_name.lower()}s' for type_name, count in table_types.items()])}
- Total rows across all tables: {total_rows:,}

📈 Largest tables (by row count):"""
        
        for i, table in enumerate(largest_tables[:5], 1):
            overview += f"\n  {i}. {table.full_name} - {table.row_count:,} rows"
        
        overview += "\n"
        return overview
    
    @staticmethod
    def get_intelligent_table_suggestions(tables: List[BigQueryTableInfo], query_context: str = "") -> List[str]:
        """
        Suggest the most relevant tables based on size, recency, and naming patterns
        
        Args:
            tables: List of BigQuery table info
            query_context: Optional context about what the user is looking for
        """
        if not tables:
            return []
        
        # Score tables based on various factors
        scored_tables = []
        
        for table in tables:
            score = 0
            
            # Size factor (larger tables are often more important)
            if table.row_count:
                if table.row_count > 1000000:
                    score += 10
                elif table.row_count > 100000:
                    score += 5
                elif table.row_count > 10000:
                    score += 2
            
            # Recency factor (more recently modified tables)
            if table.modified:
                # This is a simple heuristic - in practice you'd want more sophisticated date handling
                if '2024' in table.modified or '2023' in table.modified:
                    score += 3
            
            # Table type factor (tables over views)
            if table.table_type == 'TABLE':
                score += 2
            
            # Name factor (certain patterns suggest important tables)
            table_name_lower = table.table_id.lower()
            if any(keyword in table_name_lower for keyword in ['fact', 'main', 'core', 'primary']):
                score += 5
            if any(keyword in table_name_lower for keyword in ['dim', 'lookup', 'ref']):
                score += 3
            
            # Description factor
            if table.description:
                score += 1
            
            scored_tables.append((table, score))
        
        # Sort by score and return top suggestions
        scored_tables.sort(key=lambda x: x[1], reverse=True)
        
        suggestions = []
        for table, score in scored_tables[:10]:  # Top 10 suggestions
            suggestion = f"{table.full_name}"
            if table.description:
                suggestion += f" - {table.description[:100]}..."
            if table.row_count:
                suggestion += f" ({table.row_count:,} rows)"
            suggestions.append(suggestion)
        
        return suggestions