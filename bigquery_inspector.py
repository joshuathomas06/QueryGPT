import os
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from google.cloud import bigquery
from google.oauth2 import service_account


@dataclass
class BigQueryTableInfo:
    full_name: str  # project.dataset.table
    dataset_id: str
    table_id: str
    description: Optional[str]
    row_count: Optional[int]
    columns: List[Tuple[str, str]]  # (column_name, data_type)
    table_type: str  # TABLE, VIEW, EXTERNAL
    created: Optional[str]
    modified: Optional[str]
    labels: Optional[Dict[str, str]]


class BigQueryInspector:
    def __init__(self, service_account_path: str = None, project_id: str = None):
        """
        Initialize BigQuery client with service account credentials
        
        Args:
            service_account_path: Path to service account JSON file
            project_id: GCP project ID (if not in service account file)
        """
        self.service_account_path = service_account_path or os.getenv('BIGQUERY_SERVICE_ACCOUNT_PATH')
        self.project_id = project_id or os.getenv('BIGQUERY_PROJECT_ID')
        
        if not self.service_account_path:
            raise ValueError("BigQuery service account path is required (set BIGQUERY_SERVICE_ACCOUNT_PATH in .env)")
        
        if not os.path.exists(self.service_account_path):
            raise FileNotFoundError(f"Service account file not found: {self.service_account_path}")
        
        # Load service account credentials
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_path,
                scopes=["https://www.googleapis.com/auth/bigquery"]
            )
            
            # Get project ID from service account file if not provided
            if not self.project_id:
                with open(self.service_account_path, 'r') as f:
                    sa_info = json.load(f)
                    self.project_id = sa_info.get('project_id')
            
            if not self.project_id:
                raise ValueError("Project ID not found in service account file or environment variable")
            
            self.client = bigquery.Client(credentials=credentials, project=self.project_id)
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize BigQuery client: {e}")
    
    def get_datasets(self) -> List[str]:
        """Get all dataset IDs in the project"""
        try:
            datasets = list(self.client.list_datasets())
            return [dataset.dataset_id for dataset in datasets]
        except Exception as e:
            raise Exception(f"Failed to list datasets: {e}")
    
    def get_tables_in_dataset(self, dataset_id: str) -> List[str]:
        """Get all table IDs in a specific dataset"""
        try:
            dataset_ref = self.client.dataset(dataset_id)
            tables = list(self.client.list_tables(dataset_ref))
            return [table.table_id for table in tables]
        except Exception as e:
            raise Exception(f"Failed to list tables in dataset {dataset_id}: {e}")
    
    def get_table_info(self, dataset_id: str, table_id: str) -> BigQueryTableInfo:
        """Get detailed information about a specific table"""
        try:
            table_ref = self.client.get_table(f"{self.project_id}.{dataset_id}.{table_id}")
            
            # Get column information (limit to first 10 for efficiency)
            columns = []
            for field in table_ref.schema[:5]:  # First 5 columns
                columns.append((field.name, field.field_type))
            
            return BigQueryTableInfo(
                full_name=f"{self.project_id}.{dataset_id}.{table_id}",
                dataset_id=dataset_id,
                table_id=table_id,
                description=table_ref.description,
                row_count=table_ref.num_rows,
                columns=columns,
                table_type=table_ref.table_type,
                created=table_ref.created.isoformat() if table_ref.created else None,
                modified=table_ref.modified.isoformat() if table_ref.modified else None,
                labels=dict(table_ref.labels) if table_ref.labels else None
            )
        except Exception as e:
            raise Exception(f"Failed to get table info for {dataset_id}.{table_id}: {e}")
    
    def get_all_tables_info(self, max_tables_per_dataset: int = 10) -> List[BigQueryTableInfo]:
        """
        Get information about all tables in all datasets
        
        Args:
            max_tables_per_dataset: Limit tables per dataset to avoid overwhelming results
        """
        all_tables = []
        
        try:
            datasets = self.get_datasets()
            print(f"Found {len(datasets)} datasets")
            
            for dataset_id in datasets:
                try:
                    tables = self.get_tables_in_dataset(dataset_id)
                    print(f"Dataset {dataset_id}: {len(tables)} tables")
                    
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
    
    def execute_query(self, query: str, max_results: int = 1000) -> List[Dict]:
        """Execute a BigQuery SQL query and return results"""
        try:
            query_job = self.client.query(query)
            results = query_job.result(max_results=max_results)
            
            # Convert to list of dictionaries
            rows = []
            for row in results:
                rows.append(dict(row))
            
            return rows
            
        except Exception as e:
            raise Exception(f"Failed to execute query: {e}")
    
    def get_sample_data(self, dataset_id: str, table_id: str, limit: int = 5) -> List[Dict]:
        """Get sample data from a table"""
        query = f"""
        SELECT *
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def test_connection(self) -> bool:
        """Test the BigQuery connection"""
        try:
            # Simple query to test connection
            query = "SELECT 1 as test"
            self.execute_query(query)
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False