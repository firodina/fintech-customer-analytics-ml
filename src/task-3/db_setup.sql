-- ----------------------------------------------------------------------
-- Database Setup Script: bank_reviews
-- ----------------------------------------------------------------------

-- 1. Create the database if it does not exist
-- NOTE: This command must be executed while connected to the default 'postgres' database.
-- CREATE DATABASE bank_reviews;

-- 2. Connect to the newly created database (or run these commands manually)
-- \c bank_reviews;

-- 3. Banks Table: Stores unique bank information.

CREATE TABLE Banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(100)
);

-- 4. Reviews Table: Stores all processed review data.

CREATE TABLE Reviews (
    review_id VARCHAR(50) PRIMARY KEY, -- Unique ID from the source data
    bank_id INTEGER REFERENCES Banks(bank_id) ON DELETE RESTRICT, -- Foreign Key to Banks table
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(10), -- e.g., 'positive', 'negative', 'neutral'
    sentiment_score REAL,        -- Numerical score from VADER/Transformer
    themes TEXT,                 -- Comma-separated themes (from 03_theme_mapping.py)
    source VARCHAR(50)           -- e.g., 'Google Play Store', 'App Store'
);

-- 5. Verification Queries (for the KPI check)
-- These queries will be run by the Python script to verify data integrity.

Check total number of reviews
SELECT COUNT(*) FROM Reviews;

-- Check average rating per bank
SELECT 
    b.bank_name, 
    AVG(r.rating) AS average_rating,
    COUNT(r.review_id) AS total_reviews
FROM 
    Reviews r
JOIN 
    Banks b ON r.bank_id = b.bank_id
GROUP BY 
    b.bank_name
ORDER BY 
    total_reviews DESC;

-- Count positive/negative/neutral reviews per bank
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) AS sentiment_count
FROM 
    Reviews r
JOIN 
    Banks b ON r.bank_id = b.bank_id
GROUP BY 
    b.bank_name, 
    r.sentiment_label
ORDER BY 
    b.bank_name, 
    sentiment_count DESC;