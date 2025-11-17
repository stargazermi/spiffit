-- Mock Sales Performance Data
-- For Genie Space: spg-mocking-bird-sales

USE hackathon;

-- Create sales performance table
CREATE OR REPLACE TABLE hackathon_spiffit.sales_performance (
  employee_name STRING COMMENT 'AE name',
  month STRING COMMENT 'Performance month',
  mrr_actual DECIMAL(10,2) COMMENT 'Actual MRR achieved',
  mrr_quota DECIMAL(10,2) COMMENT 'MRR quota/target',
  deals_closed INT COMMENT 'Number of deals closed',
  new_logos INT COMMENT 'Number of new customers'
) COMMENT 'Mock sales performance metrics for demo';

-- Insert sample data
INSERT INTO hackathon_spiffit.sales_performance VALUES
  ('John Smith', 'November 2024', 125000.00, 100000.00, 12, 4),
  ('Sarah Johnson', 'November 2024', 145000.00, 100000.00, 15, 5),
  ('Mike Chen', 'November 2024', 95000.00, 100000.00, 10, 3),
  ('Lisa Wang', 'November 2024', 110000.00, 100000.00, 11, 4),
  ('David Kim', 'November 2024', 88000.00, 100000.00, 9, 2),
  ('Emma Wilson', 'November 2024', 132000.00, 100000.00, 13, 4);

-- Verify data
SELECT 
  employee_name,
  mrr_actual,
  mrr_quota,
  ROUND((mrr_actual / mrr_quota) * 100, 1) as attainment_pct,
  deals_closed,
  new_logos
FROM hackathon_spiffit.sales_performance
ORDER BY mrr_actual DESC;

