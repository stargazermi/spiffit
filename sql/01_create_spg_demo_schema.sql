-- Setup for SPG Demo Data
-- Run this first in Databricks SQL Editor or Notebook

-- Using team schema: hackathon.hackathon_spiffit
-- Schema should already exist, but verify it's accessible:

USE hackathon;

-- Verify schema exists
SHOW SCHEMAS LIKE 'hackathon';

-- Next: Run the table creation scripts (02, 03, 04)
-- All tables will be created in hackathon.hackathon_spiffit

