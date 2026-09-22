# Books Catalogue Data Engineering Pipeline

## Project Overview

This project demonstrates an end-to-end data engineering pipeline
using books.toscrape.com.

The pipeline performs:

Scraping → Cleaning → Currency Conversion → SQLite Storage →
SQL Analysis → Pandas Analysis

## Installation and Running the Pipeline

### Prerequisites

Make sure the following are installed on your system:

- Python 3.9 or higher
- Git
- VS Code (recommended)

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>

### 2.Navigate to the Data Pipeline Folder

 cd data_pipeline

###3. Create a Virtual Environment

###Create a Python virtual environment:

python -m venv venv

###Activate the virtual environment.

###Windows:

venv\Scripts\activate

###macOS/Linux:

source venv/bin/activate

###After activation, the terminal should show (venv).

###4. Install Required Python Packages

###Install the dependencies from requirements.txt

pip install -r requirements.txt


The project requires:

requests
beautifulsoup4
pandas

SQLite is included with Python and does not need to be installed separately.

###5. Open the Jupyter Notebook

Start Jupyter Notebook:

jupyter notebook

This will open Jupyter Notebook in your browser.

Open:

books_scraping.ipynb
###6. Run the Pipeline

Run all cells in books_scraping.ipynb from top to bottom.

Kernel → Restart & Run All

The notebook will:

Scrape the first 5 pages of the Books to Scrape catalogue.
Extract book title, price, rating, availability, and category.
Clean and transform the scraped data.
Convert GBP prices to INR using the fixed rate of 105.50.
Create the SQLite database.
Create the categories and books tables.
Insert the cleaned data into SQLite.
Execute the required SQL queries.
Compare the SQL JOIN result with the equivalent pandas merge() result.


7. Expected Outputs

After successfully running the notebook, the project should contain:

data_pipeline/
├── books_scraping.ipynb
├── books_catalogue.db
├── books_cleaned.csv
├── sql_queries.txt
├── sql_outputs.txt
├── requirements.txt
└── README.md


  along with  above there will be query_output.csv's also


The notebook should produce:

At least 60 scraped books.
Books from at least 3 categories.
price_gbp as a numeric column.
rating as integers from 1 to 5.
in_stock as Boolean values.
price_inr calculated using 1 GBP = 105.50 INR.
SQLite books and categories tables.
At least 5 SQL queries and their outputs.
SQL JOIN and pandas merge() comparison.

Below is the detailed information


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