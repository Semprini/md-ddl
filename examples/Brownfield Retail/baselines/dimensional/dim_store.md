# dim_store

Baseline documentation for the existing `dim_store` dimension table in the Snowflake data warehouse. This is a Type 1 slowly changing dimension containing store location master data including geographic attributes and store classification.

```yaml
baseline:
  type: dimensional
  source_system: "Snowflake DW"
  captured_date: 2024-01-15
  captured_by: "Data Engineering Team"
  status: active
```

## Source DDL

```sql
CREATE TABLE analytics.dim_store (
    store_key    BIGINT       NOT NULL PRIMARY KEY,
    store_id     VARCHAR(10)  NOT NULL UNIQUE,
    store_name   VARCHAR(200) NOT NULL,
    city         VARCHAR(100) NOT NULL,
    state        VARCHAR(100) NOT NULL,
    country      VARCHAR(50)  NOT NULL,
    region       VARCHAR(50)  NOT NULL,
    store_type   VARCHAR(30)  NOT NULL,
    opening_date DATE         NOT NULL,
    manager_name VARCHAR(200)
);
```

## Column Summary

Column | Type | Nullable | Description
--- | --- | --- | ---
store_key | bigint | no | Surrogate key
store_id | varchar(10) | no | Natural key from store operations system
store_name | varchar(200) | no | Display name of the store
city | varchar(100) | no | City where the store is located
state | varchar(100) | no | State or province
country | varchar(50) | no | Country code (ISO 3166-1 alpha-2)
region | varchar(50) | no | Internal business region classification
store_type | varchar(30) | no | Store format (Flagship, Standard, Express, Outlet)
opening_date | date | no | Date the store opened for business
manager_name | varchar(200) | yes | Current store manager name

## Notes

- **Type 1 SCD**: Store attributes are overwritten in place. There is no history tracking for store name changes or manager changes. This is a known gap — the analytics team has requested SCD2 for `manager_name` and `store_type` but it has not been prioritised.
- **Grain**: One row per store
- **Load**: Daily, SLA available by 05:00 UTC
- **Region values**: Region is a free-text field with inconsistent values across stores (e.g., "EMEA", "Europe", "EU"). Standardisation is pending and should be addressed as an enum in the canonical model.
