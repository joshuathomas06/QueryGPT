"""
Limited BigQuery inspector for QueryGPT to avoid token limits
"""
from bigquery_inspector import BigQueryInspector, BigQueryTableInfo
from typing import List

class LimitedBigQueryInspector(BigQueryInspector):
    """BigQuery inspector with aggressive limits for token management"""
    
    def get_all_tables_info(self, max_tables_per_dataset: int = 3) -> List[BigQueryTableInfo]:
        """
        Get LIMITED information about tables to avoid token limits
        
        Args:
            max_tables_per_dataset: Max 3 tables per dataset
        """
        all_tables = []
        
        try:
            datasets = self.get_datasets()
            # Limit to first 10 datasets
            datasets = datasets[:10]
            print(f"Limiting to {len(datasets)} datasets for token management")
            
            for dataset_id in datasets:
                try:
                    tables = self.get_tables_in_dataset(dataset_id)
                    print(f"Dataset {dataset_id}: found {len(tables)} tables, limiting to {max_tables_per_dataset}")
                    
                    # Limit tables per dataset
                    tables_to_process = tables[:max_tables_per_dataset]
                    
                    for table_id in tables_to_process:
                        try:
                            table_info = self.get_table_info(dataset_id, table_id)
                            all_tables.append(table_info)
                        except Exception as e:
                            print(f"Warning: Failed to get info for {dataset_id}.{table_id}: {e}")
                            continue
                            
                except Exception as e:
                    print(f"Warning: Failed to process dataset {dataset_id}: {e}")
                    continue
            
            return all_tables
            
        except Exception as e:
            raise Exception(f"Failed to get all tables info: {e}")