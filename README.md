```
# Portfolio Analytics Data Platform (Fixed Income)

## 📌 Project Overview
This platform is a production-grade data solution designed to automate the ingestion, validation, and analytical modeling of fragmented Fixed Income asset data. 
Implementing a **Medallion Architecture** using **Python** for complex logic/quality gates and **dbt** for dimensional modeling.

---

## 🚀 Business Problems Solved
* **Fragmented Asset Feeds**: Unified disparate CSV sources (Holdings, Market Prices, FX, Ratings) into a single Lakehouse source of truth.
* **Inconsistent Security Attributes**: Standardized credit ratings from multiple agencies (S&P, Moody's) into a unified internal rating scale.
* **Manual Reconciliation**: Replaced manual Excel checks with **Automated Exception-based Controls**.
* **Portfolio Transparency**: Automated the calculation of Portfolio Weights and Duration Contributions for Risk & Actuarial teams.

---

## 🛠️ Tech Stack
* **Language**: Python (Pandas/PySpark)
* **Transformation**: dbt (Core/Cloud)
* **Storage**: Databricks Delta Lake (Simulated via local CSV for demo)
* **Orchestration**: Airflow
* **Environment**: Docker / GitHub Actions (CI/CD)

---

## 📂 Repository Structure

```text
portfolio-analytics-data-platform/
├── main.py                   # Orchestrator (Entry Point for Pipeline)
├── dbt_project/              # Analytics Engineering (Gold Layer)
│   ├── models/
│   │   ├── staging/          # Data cleaning & Casting
│   │   ├── intermediate/     # Complex joins & Currency normalization
│   │   └── marts/            # Star Schema (fct_portfolio_analytics, dim_assets)
├── src/                      # Python Production Code (Bronze & Silver Layer)
│   ├── data_ingestion.py     # Inbound feeds with Audit Fields (_ingested_at)
│   ├── quality_check.py      # Exception-based control checks (Gatekeeper)
│   └── normalization.py      # FX conversion & Attribute standardization
├── data/                     # Data Lake Simulation
│   ├── raw/                  # Source CSVs (Holdings, Prices, FX, Ratings)
│   └── processed/            # Final output for downstream UIs (PowerBI)
├── airflow/                  # Production DAG triggers
└── tests/                    # Pytest & dbt unit tests
```
