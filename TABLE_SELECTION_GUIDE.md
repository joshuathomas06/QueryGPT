# 🎯 Intelligent Table Selection in QueryGPT

## How It Works

When you ask a question, QueryGPT now:

1. **Analyzes your query** to understand what data you're looking for
2. **Identifies relevant tables** from your BigQuery project
3. **Generates SQL** for the most appropriate table
4. **Executes the query** and returns results with explanations

## Example Workflow

### User asks: "I want to analyze costs"

**What happens behind the scenes:**

1. **Keywords extracted**: `costs`, `analyze`

2. **Tables searched**: The system looks for tables with:
   - Names containing: cost, billing, spend, charge
   - Datasets related to financial data
   - Columns with cost-related names

3. **Best match found**: `astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary`
   - Has `daily_cost` column
   - Contains 138,440 rows of cost data
   - Includes cloud account and organization details

4. **SQL generated**:
   ```sql
   SELECT cloud_account, SUM(daily_cost) as total_cost 
   FROM datastax-datalake.astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary
   GROUP BY cloud_account
   ORDER BY total_cost DESC;
   ```

## Available Cost Table

Based on your BigQuery project, the main cost analysis table is:

**`astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary`**

Columns:
- `daily_cost` - Daily cost amount
- `instance_count` - Number of instances
- `cloud_account` - Cloud account identifier
- `cluster_id` - Database cluster ID
- `organization_email` - Organization email
- `cloud_region` - AWS/GCP region
- `deployment_type` - Type of deployment
- `usage_date` - Date of the cost

## Smart Query Examples

Try these queries to see intelligent table selection in action:

1. **"Show me daily costs by region"**
   - Finds the cost table
   - Groups by cloud_region

2. **"What are the costs for each organization?"**
   - Uses organization_email column
   - Sums daily_cost

3. **"Analyze costs over time"**
   - Uses usage_date for time analysis
   - Shows cost trends

4. **"Which accounts have the highest costs?"**
   - Groups by cloud_account
   - Orders by total cost

## Current Limitations

- Only sees first 10 datasets (out of 94)
- Maximum 3 tables per dataset
- First 5 columns per table

This keeps the system fast while still finding relevant data for most queries.

## Tips for Better Results

1. **Be specific about the data type**: "costs", "users", "clusters"
2. **Mention time periods**: "daily", "monthly", "last week"
3. **Include grouping hints**: "by account", "per region", "for each organization"

The system will automatically select the most appropriate table and generate optimized BigQuery SQL!