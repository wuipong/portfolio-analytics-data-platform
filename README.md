```
portfolio-analytics-data-platform/
├── dbt_project/              
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
├── src/                      # Python Production Code
│   ├── data_ingestion.py
│   ├── quality_check.py
│   └── ai_enrichment.py
├── notebooks/                # Databricks exploration
├── airflow/                  # DAGs
├── tests/                    # Pytest & dbt unit tests 
├── data/                     # Sample CSV/JSON feeds
│   ├── raw/
│   ├── processed/
│   └── reference/
└── README.md
```
