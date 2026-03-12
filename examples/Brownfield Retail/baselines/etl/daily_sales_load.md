# daily_sales_load

Baseline documentation for the daily sales ETL pipeline that loads POS transaction data into the Snowflake star schema. This pipeline is managed in dbt and runs as part of the nightly batch window.

```yaml
baseline:
  type: etl
  source_system: "dbt"
  captured_date: 2024-01-20
  captured_by: "Data Engineering Team"
  status: active
```

## Pipeline Summary

- **Pipeline**: daily_sales_load
- **Tool**: dbt
- **Source**: pos_system.transactions (Oracle, via Fivetran sync)
- **Target**: analytics.fact_sales
- **Schedule**: daily 02:00 UTC
- **SLA**: Complete by 04:00 UTC
- **Dependencies**: staging_pos_extract, dim_store_load, dim_product_load

## Transformation Logic

The pipeline consists of three dbt models executed in sequence:

### 1. Staging Extract (`stg_pos_transactions`)

Extracts raw transaction records from the POS system's Oracle database via a nightly Fivetran sync into `raw.pos_system.transactions`. The staging model performs:

- Deduplication on `transaction_id` (the POS system occasionally sends duplicate records during network retries)
- Data type casting from Oracle types to Snowflake-native types
- Null handling for optional fields (`customer_id`, `discount_amount`)

### 2. Intermediate Transform (`int_sales_enriched`)

Joins staged transactions with dimension tables to resolve surrogate keys:

- Lookup `store_key` from `dim_store` using `store_id`
- Lookup `product_key` from `dim_product` using `product_id` and `effective_date` / `expiry_date` range (SCD2 point-in-time lookup)
- Calculate `total_amount` as `(quantity * unit_price) - COALESCE(discount_amount, 0)`

### 3. Fact Load (`fact_sales`)

Incremental merge into `analytics.fact_sales`:

- Insert new records identified by `sale_id` not present in the target
- Update existing records where `dw_update_timestamp` has changed (late-arriving corrections from POS)
- Stamp `etl_batch_id` and `dw_load_timestamp` for lineage tracking

## Known Issues

- **Late-arriving data**: The POS system batch closes at 23:59 local time per store. Stores in western time zones may have transactions arriving after the 02:00 UTC pipeline start. A retry run at 06:00 UTC catches stragglers, but there is a window where the dashboard shows incomplete data.
- **SCD2 race condition**: If `dim_product` loads after `fact_sales` on the same day, the point-in-time lookup may resolve to a stale product version. The dependency DAG mitigates this, but manual reruns sometimes break the ordering.
