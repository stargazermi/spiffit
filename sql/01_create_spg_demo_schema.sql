-- Create schema for SPG demo data
-- Run this first in Databricks SQL Editor or Notebook

CREATE SCHEMA IF NOT EXISTS spg_demo
COMMENT 'Mock data schema for SPG SPIFF agent demo';

USE spg_demo;

-- Verify schema created
SHOW SCHEMAS LIKE 'spg_demo';

