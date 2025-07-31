# Interactive Table Selection Feature

## Overview

QueryGPT now implements an interactive table selection workflow for BigQuery queries. When users ask questions, the system:

1. **Suggests relevant tables** based on the query
2. **Summarizes each table** with key information  
3. **Prompts users to choose** a specific table
4. **Generates SQL** for the selected table

## How It Works

### Step 1: User Asks a Question
When you type a natural language query like "show me costs by organization", the system first searches for relevant tables.

### Step 2: Table Suggestions
The system presents up to 5 relevant tables with:
- Full table name (dataset.table format)
- Row count
- Key columns
- Relevance score based on keyword matching

### Step 3: User Selection
Interactive buttons appear allowing you to choose "Option 1", "Option 2", etc.

### Step 4: SQL Generation
Once you select a table, the system generates SQL specifically for that table and executes it.

## Example Workflow

**User:** "What are the daily costs by cloud account?"

**System:** 
```
📋 Suggested Tables for Your Query

### Option 1:
📊 datastax-datalake.astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary
   Rows: 138,440
   Key columns: daily_cost, cloud_account, organization_email, cloud_region
   Relevance: ⭐⭐⭐⭐⭐ (matches: daily, cost, account)

### Option 2:
📊 datastax-datalake.billing.gcp_billing_export_v1_002075_FACBC9_A501C5
   Rows: 2,505,086,837
   Key columns: billing_account_id, service, usage_start_time, cost
   Relevance: ⭐⭐⭐⭐ (matches: account, cost)

[Buttons: Option 1 | Option 2]
```

**User:** *Clicks Option 1*

**System:** Generates and executes:
```sql
SELECT cloud_account, SUM(daily_cost) as total_cost
FROM datastax-datalake.astra_fcpmo.tblDailyDedicatedDatabaseNodeCostSummary
GROUP BY cloud_account
ORDER BY total_cost DESC
```

## Technical Implementation

### Backend Components
- `/suggest-tables` endpoint analyzes queries and returns relevant tables
- Intelligent table selector scores tables based on keyword matching
- Session storage maintains table suggestions for follow-up queries

### Frontend Components
- React UI displays table suggestions with interactive buttons
- Handles table selection and sends follow-up query
- Shows loading states during processing

## Benefits

1. **Better Table Discovery** - Users don't need to know exact table names
2. **Informed Decisions** - See row counts and columns before querying
3. **Accurate Queries** - SQL is generated for the specific selected table
4. **Reduced Errors** - Avoids querying wrong or non-existent tables

## Limitations

- Only available for BigQuery connections (not PostgreSQL)
- Limited to first 10 datasets and 3 tables per dataset
- Shows maximum 5 table suggestions per query

## Usage Tips

1. Be specific about what data you want (costs, users, organizations)
2. Mention time periods if relevant (daily, monthly, yearly)
3. Review table options carefully before selecting
4. The system remembers your selection for the current query context