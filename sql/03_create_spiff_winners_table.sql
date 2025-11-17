-- Mock SPIFF Winners / Analytics Data
-- For Genie Space: spg-mocking-bird-analytics

USE spg_demo;

-- Create SPIFF winners table
CREATE OR REPLACE TABLE spiff_winners (
  employee_name STRING COMMENT 'Winner name',
  month STRING COMMENT 'Month earned',
  spiff_program STRING COMMENT 'SPIFF program name',
  earned_amount DECIMAL(10,2) COMMENT 'Amount earned',
  rank INT COMMENT 'Ranking position'
) COMMENT 'Mock SPIFF winners and rankings for demo';

-- Insert sample data
INSERT INTO spiff_winners VALUES
  ('Sarah Johnson', 'November 2024', 'Double MRR', 45230.00, 1),
  ('Mike Chen', 'November 2024', 'Double MRR', 38150.00, 2),
  ('Lisa Wang', 'November 2024', 'Double MRR', 32400.00, 3),
  ('John Smith', 'November 2024', 'New Logo Bonus', 25000.00, 4),
  ('Emma Wilson', 'November 2024', 'Double MRR', 28600.00, 5),
  ('Sarah Johnson', 'November 2024', 'New Logo Bonus', 12500.00, NULL),
  ('John Smith', 'November 2024', 'Renewal Rescue', 8000.00, NULL);

-- Verify data with aggregates
SELECT 
  employee_name,
  COUNT(*) as programs_won,
  SUM(earned_amount) as total_earned,
  STRING_AGG(spiff_program, ', ') as programs
FROM spiff_winners
GROUP BY employee_name
ORDER BY total_earned DESC;

