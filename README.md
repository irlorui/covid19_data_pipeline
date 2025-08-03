# 🧬 Clinical Trials Data Pipeline

This project implements a modular, production-style data pipeline that ingests a [COVID-19 Clinical Trials dataset](https://www.kaggle.com/datasets/parulpandey/covid19-clinical-trials-dataset) from Kaggle, loads it into a PostgreSQL database, transform it into an efficient storage schema, checks the resulting quality and. 

The goal is to ensure traceability, data quality, and a clean architecture.

---

## 🧱 Architecture Overview

                +------------------------+
                |   Kaggle CSV Source    |
                +-----------+------------+
                            |
                            v
     +------------------------------------------+
     |       ETL Service (Python, Docker)       |
     |  - Extract from Kaggle or local fallback |
     |  - Load raw data to Postgres (raw schema)|
     +----------------------+-------------------+
                            |
                            v
             +-------------------------------+
             | PostgreSQL DB (Docker)        |
             | - Schemas: raw, staging, analytics |
             | - Roles: dataops, analytics    |
             +-------------------------------+


---

## 🛠️ Technologies Used

- **Docker**: Containerization of all services
- **PostgreSQL**: Central data warehouse
- **Python (ETL)**: Extraction and raw data loading
- **DBT**: Transformation for the table

---


## ⚙️ Setup Instructions

1. **Install Docker**:

2. **Project Structure**:



3. **Run the project**:

```bash
docker compose up --build
```


## 📂 Time Allocation

| Task                         | Time Spent |
|-----------------------------|------------|
| Architecture & Docker setup | 1.5h       |
| PostgreSQL schema + roles   | 0.5h       |
| ETL logic + Kaggle fallback | 1.5h       |
| Documentation               | 0.5h       |
| **Total**                   | **~4h**    |


## 📌 Design Decisions & Trade-offs

- A `raw` schema is used for traceability and future audit needs.
- Roles and schemas are designed to enforce separation of responsibilities (dataops vs analytics).
- The ETL pipeline focuses only on initial extraction and raw loading for this challenge.


## 💬 Bonus Questions

### 1. **Scalability**
To scale the solution for 100x more data:
- Add table partitioning in PostgreSQL based on time or study phase.
- Consider switching from pandas to `polars` or `Dask` for faster memory usage.
- Add support for incremental loads using timestamps or checksums.
- Introduce parallelism via Airflow or Prefect tasks.

### 2. **Data Quality**
Additional validations I would implement:
- Enforce required fields (`nct_number`, `start_date`, etc.).
- Check that dates make logical sense (e.g., start_date < completion_date).
- Validate the `phase` and `status` values against known controlled vocabularies.
- Detect and flag duplicates or conflicting entries.
- Use a tool like Great Expectations to codify data quality rules.

### 3. **Compliance (GxP environment)**
For a GxP-compliant environment:
- Implement strict change tracking (version control, change logs).
- Store raw and transformed data with full audit trails.
- Use validated software components and document pipeline behavior.
- Ensure strict access control and role-based privileges.
- Document and validate all transformations as part of validation protocols.

### 4. **Monitoring**
In production, I would monitor the pipeline with:
- **Airflow**: task-level retries, failures, and SLA monitoring.
- **Prometheus + Grafana**: database and container metrics.
- **Structured logs** to file or central logging service (e.g., ELK).
- Alerting on anomalies in row counts, load times, and data quality issues.

### 5. **Security**
Security measures I would implement:
- Store credentials securely using Docker secrets or environment variables.
- Avoid hardcoded passwords in scripts or configuration files.
- Use TLS/SSL for PostgreSQL connections.
- Limit each service’s DB access by role (e.g., `etl_user` → raw only).
- Encrypt backups and sensitive fields (if applicable).
- Run regular vulnerability scans on containers (e.g., with Trivy).

## 📎 Future Improvements

Streamlit dashboard for reporting.

Including the possibility of considering data from multiple sources besides CSV files; JSON APIs, SQL databases, plain text files, etc.

CI/CD pipeline with unit tests and dbt models.