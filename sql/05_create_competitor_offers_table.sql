-- Competitor Intelligence Table
-- Schema based on supportingAlternate.md recommendations
-- Stores real-time competitor offers from web scraping

USE CATALOG hackathon;
USE SCHEMA hackathon_spiffit;

-- Drop existing if recreating
DROP TABLE IF EXISTS competitor_offers;

-- Create competitor offers table
CREATE TABLE competitor_offers (
  -- Provider information
  provider STRING COMMENT 'ISP provider name (e.g., AT&T Business, Spectrum Business)',
  plan_name STRING COMMENT 'Name of the business plan or offer',
  
  -- Technical specs
  download_speed STRING COMMENT 'Download speed (e.g., "300 Mbps", "1 Gbps")',
  upload_speed STRING COMMENT 'Upload speed (e.g., "300 Mbps", "1 Gbps")',
  
  -- Pricing
  price_monthly DECIMAL(10,2) COMMENT 'Monthly price in dollars',
  price_promo DECIMAL(10,2) COMMENT 'Promotional price if applicable',
  price_display STRING COMMENT 'Human-readable price (e.g., "$199.99/mo (promo 12 months)")',
  
  -- Promotion details
  promo_description STRING COMMENT 'Short description of promotion',
  promo_start_date DATE COMMENT 'Promotion start date',
  promo_end_date DATE COMMENT 'Promotion end date',
  
  -- Contract terms
  contract_term_months INT COMMENT 'Contract term in months',
  contract_term_display STRING COMMENT 'Human-readable term (e.g., "12 months", "2 years")',
  
  -- Eligibility & SLA
  eligibility STRING COMMENT 'Eligibility requirements (e.g., "New business customers only")',
  sla_guarantee STRING COMMENT 'Service level agreement (e.g., "99.99% uptime")',
  
  -- Source tracking
  page_url STRING COMMENT 'Source URL where offer was found',
  zip_code STRING COMMENT 'ZIP code for localized offers (optional)',
  
  -- Metadata
  scraped_at TIMESTAMP COMMENT 'When this data was collected',
  is_active BOOLEAN COMMENT 'Whether offer is currently active',
  data_quality STRING COMMENT 'Quality indicator: complete, partial, contact_only'
)
COMMENT 'Competitor business internet offers scraped from ISP websites';

-- Insert sample data for testing
INSERT INTO competitor_offers VALUES
(
  'AT&T Business',
  'Business Fiber 300',
  '300 Mbps',
  '300 Mbps',
  249.99,
  199.99,
  '$199.99/mo (promo 12 months)',
  'First 12 months discounted',
  '2024-11-01',
  '2025-10-31',
  12,
  '12 months',
  'New business customers only; available in select ZIPs',
  '99.99% uptime SLA (business tier)',
  'https://business.att.com/plans/business-fiber-300',
  NULL,
  CURRENT_TIMESTAMP(),
  TRUE,
  'complete'
),
(
  'Spectrum Business',
  'Business Internet 500',
  '500 Mbps',
  '50 Mbps',
  299.99,
  249.99,
  '$249.99/mo (promo 24 months)',
  'New customer pricing for 2 years',
  '2024-10-15',
  '2026-10-14',
  24,
  '24 months',
  'New business accounts in serviceable areas',
  '99.9% uptime guarantee',
  'https://business.spectrum.com/internet/plans',
  NULL,
  CURRENT_TIMESTAMP(),
  TRUE,
  'complete'
),
(
  'Comcast Business',
  'Business Internet 250',
  '250 Mbps',
  '25 Mbps',
  199.99,
  NULL,
  '$199.99/mo',
  'Standard business rate',
  NULL,
  NULL,
  12,
  '1 year',
  'Business locations in Comcast service areas',
  'Business-class support included',
  'https://business.comcast.com/internet/business-internet',
  NULL,
  CURRENT_TIMESTAMP(),
  TRUE,
  'partial'
),
(
  'Verizon Business',
  'Business Fios Gigabit',
  '940 Mbps',
  '880 Mbps',
  399.99,
  349.99,
  '$349.99/mo (promo 12 months)',
  'First year promotional rate',
  '2024-11-01',
  '2025-10-31',
  12,
  '12 months',
  'New Verizon Business customers with 2-year term',
  '99.99% network reliability',
  'https://www.verizon.com/business/products/internet/business-fios/',
  NULL,
  CURRENT_TIMESTAMP(),
  TRUE,
  'complete'
),
(
  'Cox Business',
  'Business Internet 500',
  '500 Mbps',
  '100 Mbps',
  279.99,
  NULL,
  'Contact for pricing',
  NULL,
  NULL,
  NULL,
  12,
  '1 year agreement',
  'Business customers in Cox service areas',
  'Priority technical support',
  'https://www.cox.com/business/internet.html',
  NULL,
  CURRENT_TIMESTAMP(),
  TRUE,
  'contact_only'
);

-- Verify data
SELECT 
  provider,
  plan_name,
  price_display,
  promo_description,
  eligibility,
  data_quality
FROM competitor_offers
ORDER BY price_monthly;

