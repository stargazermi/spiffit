-- Mock Competitor Intelligence Data
-- For Genie Space: spg-mocking-bird-market

USE hackathon;

-- Create competitor SPIFF programs table
CREATE OR REPLACE TABLE hackathon_spiffit.competitor_spiffs (
  competitor STRING COMMENT 'Competitor name',
  program_name STRING COMMENT 'Their SPIFF program name',
  incentive_type STRING COMMENT 'Type of incentive (Cash, Commission, etc)',
  amount DECIMAL(10,2) COMMENT 'Cash amount (0 if non-cash)',
  target STRING COMMENT 'Target behavior or threshold',
  month STRING COMMENT 'Month/period active'
) COMMENT 'Mock competitor SPIFF programs for demo';

-- Insert sample data
INSERT INTO hackathon_spiffit.competitor_spiffs VALUES
  ('Competitor A', 'Large Deal Bonus', 'Cash', 5000.00, 'Deals > $100K', 'December 2024'),
  ('Competitor B', 'Vertical Expansion', 'Triple Commission', 0.00, 'New verticals', 'December 2024'),
  ('Competitor C', 'Year-End Push', 'Cash', 3000.00, 'Any deal closed by Dec 20', 'December 2024'),
  ('Competitor A', 'Renewal Accelerator', 'Double Commission', 0.00, 'Renewals > $50K', 'Q4 2024'),
  ('Competitor D', 'Holiday Mega Bonus', 'Cash + Gift', 7500.00, 'Deals > $150K', 'December 2024');

-- Verify data
SELECT 
  competitor,
  program_name,
  CASE 
    WHEN amount > 0 THEN CONCAT('$', CAST(amount AS STRING))
    ELSE incentive_type
  END as incentive,
  target,
  month
FROM hackathon_spiffit.competitor_spiffs
ORDER BY month DESC, amount DESC;

