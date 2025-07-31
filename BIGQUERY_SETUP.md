# BigQuery Integration Setup Guide

This guide will help you set up QueryGPT to work with BigQuery instead of PostgreSQL.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure BigQuery Access

Your BigQuery service account JSON file is already created as `bigquery-service-account.json` with access to the `datastax-datalake` project.

### 3. Set Environment Variables

Copy the BigQuery configuration:

```bash
cp .env.bigquery .env
```

Then edit `.env` and add your Anthropic API key:

```bash
# BigQuery Configuration
USE_BIGQUERY=true
BIGQUERY_SERVICE_ACCOUNT_PATH=./bigquery-service-account.json
BIGQUERY_PROJECT_ID=datastax-datalake

# Claude AI Configuration (REQUIRED - Add your key here)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Test the Setup

Run the simple test:

```bash
python simple_bigquery_test.py
```

You should see:
```
✅ BigQuery integration looks good!
```

## 🎯 Usage Examples

### Command Line Usage

#### Interactive Mode with BigQuery
```bash
python query_gpt.py --bigquery --service-account-path ./bigquery-service-account.json --bigquery-project-id datastax-datalake
```

#### Single Query Mode
```bash
python query_gpt.py --bigquery --query "SELECT dataset_id FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 5"
```

### API Usage

Start the API server:

```bash
python api.py
```

The API will automatically use BigQuery if `USE_BIGQUERY=true` is set in your `.env` file.

#### Test API Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What datasets are available?"}'
```

## 📊 Available Data

Your BigQuery project `datastax-datalake` contains **98 datasets** including:

- `Billing2023` - Billing information
- `SLA` - Service level agreement data  
- `airflow` - Airflow workflow data
- And 95+ more datasets

## 🤖 Natural Language Examples

Once you have your Anthropic API key configured, you can ask questions like:

- "What datasets are available in this project?"
- "Show me the largest tables by row count"
- "What's in the Billing2023 dataset?"
- "Find tables related to SLA monitoring"

## 🛠️ Troubleshooting

### Connection Issues

1. **Authentication Error**: Ensure your service account JSON file is valid and has BigQuery permissions.

2. **Project Not Found**: Verify the project ID `datastax-datalake` is correct.

3. **API Key Missing**: Make sure you've added your Anthropic API key to the `.env` file.

### Test Commands

```bash
# Test BigQuery connection only
python simple_bigquery_test.py

# Test full integration (requires Anthropic API key)
python test_bigquery.py

# Test via API
curl http://localhost:8000/health
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `USE_BIGQUERY` | Enable BigQuery mode | `true` |
| `BIGQUERY_SERVICE_ACCOUNT_PATH` | Path to service account JSON | `./bigquery-service-account.json` |
| `BIGQUERY_PROJECT_ID` | BigQuery project ID | `datastax-datalake` |
| `ANTHROPIC_API_KEY` | Claude AI API key | `sk-ant-...` |

### Performance Tuning

The BigQuery integration includes intelligent optimizations:

- **Limited table discovery**: By default, only processes first 50 tables per dataset to avoid overwhelming Claude
- **Column sampling**: Only sends first 10 columns per table for schema analysis
- **Smart table ranking**: Prioritizes larger, more recently modified tables

You can adjust these in the code:

```python
# In bigquery_inspector.py
all_tables = inspector.get_all_tables_info(max_tables_per_dataset=50)  # Adjust limit

# In bigquery_inspector.py  
columns = table_ref.schema[:10]  # Adjust column limit
```

## 🚀 Next Steps

1. **Add your Anthropic API key** to the `.env` file
2. **Test the integration** with `python simple_bigquery_test.py`
3. **Start exploring your data** with natural language queries!

The BigQuery integration provides intelligent table selection based on:
- Table size (row count)
- Recency (last modified date)
- Naming patterns (fact tables, dimension tables, etc.)
- Table descriptions and metadata

This helps Claude suggest the most relevant tables for your queries automatically.