# Books Catalogue Data Engineering Pipeline

## Project Overview

This project demonstrates an end-to-end data engineering pipeline
using books.toscrape.com.

The pipeline performs:

Scraping → Cleaning → Currency Conversion → SQLite Storage →
SQL Analysis → Pandas Analysis

## Data Source

Website:
https://books.toscrape.com/

The first 5 paginated All Products catalogue pages were scraped.

Each page contains approximately 20 books, resulting in approximately
100 scraped books.

## Fields Scraped

- title
- price
- star_rating
- availability
- category

## Data Cleaning

### Price

The GBP currency symbol is removed and the value is converted to
a floating-point column called `price_gbp`.

### Rating

Text ratings are mapped as:

One = 1
Two = 2
Three = 3
Four = 4
Five = 5

### Availability

Availability text containing "In stock" is converted to True.
Availability text containing "Out of stock" is converted to False.

### Missing Values

Numeric parsing failures are handled using median imputation.
Rows missing essential fields such as title or category are dropped.

## Currency Conversion

The project-defined fixed conversion rate is:

1 GBP = 105.50 INR

This is an artificial project baseline and no external currency API
is used.

`price_inr = price_gbp * 105.50`

## Database

SQLite is used as the relational database.

### categories

- category_id - Primary Key
- category_name - Unique category name

### books

- book_id - Primary Key
- title
- price_gbp
- price_inr
- rating
- in_stock
- category_id - Foreign Key

The category_id establishes the relationship between books and
categories.

## SQL Analysis

The project demonstrates:

1. SELECT and WHERE
2. ORDER BY and LIMIT
3. DISTINCT
4. BETWEEN
5. JOIN

SQL query strings and their outputs are saved separately.

## Pandas Analysis

At least two SQL query results are read using `pd.read_sql()`.

The JOIN analysis is independently reproduced using `pd.merge()`
between the in-memory books and categories DataFrames.

The SQL and pandas results are compared for equivalence.