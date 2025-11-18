-- Setup for SPG Demo Data
-- Run this first in Databricks SQL Editor or Notebook

-- IMPORTANT: Set the catalog to hackathon (Unity Catalog)
USE CATALOG hackathon;

-- Verify you're in the right catalog
SELECT current_catalog();
-- Should return: hackathon

-- Verify the schema exists
SHOW SCHEMAS LIKE 'hackathon_spiffit';

-- Next: Run the table creation scripts (02, 03, 04)
-- All tables will be created in hackathon.hackathon_spiffit

