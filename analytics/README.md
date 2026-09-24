# Titanic Analytics — From EDA to Predictive Modeling

## Project Overview

This project implements an end-to-end analyst-to-data-scientist workflow using the classic Titanic dataset.

The project covers:

- Dataset profiling and data cleaning
- Missing-value analysis and handling
- Univariate and bivariate exploratory data analysis
- Multivariate data visualization
- Feature correlation analysis
- Feature standardization
- Classification modeling
- Model evaluation and comparison
- Class-imbalance handling
- Hyperparameter tuning
- Regression analysis
- Model persistence and reloading

The project is designed as one cohesive pipeline. The raw Titanic dataset is loaded once using Seaborn's built-in dataset loader, saved as an offline CSV fallback, cleaned, analyzed, and then used for the subsequent modeling workflow.

---

## Project Structure

```text
analytics/
│
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── titanic_cleaned.csv
└── titanic_pipeline.joblib