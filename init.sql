-- Cloud Cost Analysis Database Schema
-- This creates the demo_table for QueryGPT with actual cost data

-- Create demo_table with the exact schema from your CSV
CREATE TABLE IF NOT EXISTS demo_table (
    id SERIAL PRIMARY KEY,
    account_id TEXT,
    cloud_provider TEXT,
    environment TEXT,
    subtag TEXT,
    usage_date DATE,
    total_cost NUMERIC(15,8),
    tag TEXT,
    cost_category TEXT,
    cloudprovider_category TEXT,
    cost_center TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_demo_table_date ON demo_table(usage_date);
CREATE INDEX IF NOT EXISTS idx_demo_table_provider ON demo_table(cloud_provider);
CREATE INDEX IF NOT EXISTS idx_demo_table_environment ON demo_table(environment);
CREATE INDEX IF NOT EXISTS idx_demo_table_account ON demo_table(account_id);
CREATE INDEX IF NOT EXISTS idx_demo_table_cost_center ON demo_table(cost_center);
CREATE INDEX IF NOT EXISTS idx_demo_table_category ON demo_table(cloudprovider_category);

-- Note: Actual data will be loaded from CSV file via Docker volume mount