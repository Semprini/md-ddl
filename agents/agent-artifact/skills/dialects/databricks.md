# Databricks Dialect Reference

## Data Type Mappings

MD-DDL Type | Databricks Type | Notes
--- | --- | ---
`string` | `STRING` | Unbounded string
`string` with `max_length` | `STRING` | Databricks STRING is always variable-length; length constraints are logical only
`integer` | `BIGINT` | Default integer; use `INT` for values known to fit 32-bit
`decimal` | `DECIMAL(p,s)` | Map `precision` and `scale` from entity YAML
`boolean` | `BOOLEAN` | Direct mapping
`date` | `DATE` | Direct mapping
`datetime` | `TIMESTAMP` | Databricks TIMESTAMP is always UTC-normalized (TIMESTAMP_NTZ available on Unity Catalog)
`timestamp` | `TIMESTAMP` | Direct mapping
`text` | `STRING` | Equivalent to `string`
`binary` | `BINARY` | Direct mapping

## Delta Lake Features

All Databricks tables use Delta format by default. Delta provides ACID transactions,
time travel, and schema evolution — all relevant to MD-DDL governance requirements.

### Table Creation

```sql
-- Managed table (Unity Catalog)
CREATE TABLE financial_crime.canonical.dim_party (
    party_sk       BIGINT GENERATED ALWAYS AS IDENTITY,
    party_id       STRING NOT NULL,
    party_type     STRING NOT NULL,
    full_name      STRING,
    valid_from     TIMESTAMP NOT NULL,
    valid_to       TIMESTAMP,
    is_current     BOOLEAN DEFAULT TRUE
)
USING DELTA
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true'
);
```

### Change Data Feed

Enable CDF for slowly changing dimensions to capture change history automatically.
This aligns with MD-DDL's `mutability: slowly_changing` and `temporal.tracking: transaction_time`:

```sql
ALTER TABLE dim_party SET TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- Query changes for downstream ETL
SELECT * FROM table_changes('financial_crime.canonical.dim_party', 2)
WHERE _change_type IN ('insert', 'update_postimage');
```

### Time Travel

Delta time travel maps to MD-DDL governance `retention` requirements:

```sql
-- Query as of timestamp (audit replay)
SELECT * FROM dim_party TIMESTAMP AS OF '2025-01-15T00:00:00';

-- Set retention for compliance
ALTER TABLE dim_party SET TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 2555 days',  -- 7 years
    'delta.deletedFileRetentionDuration' = 'interval 2555 days'
);
```

## Unity Catalog Integration

### Three-Level Namespace

Databricks Unity Catalog maps naturally to MD-DDL domain structure:

Unity Catalog Level | MD-DDL Equivalent | Example
--- | --- | ---
Catalog | Organisation or programme | `enterprise_data`
Schema | Domain | `financial_crime`
Table | Entity physical realisation | `dim_party`

```sql
CREATE CATALOG enterprise_data;
CREATE SCHEMA enterprise_data.financial_crime;
CREATE TABLE enterprise_data.financial_crime.dim_party (...);
```

### Column-Level Governance

Unity Catalog tags map to MD-DDL governance metadata:

```sql
-- Classification
ALTER TABLE dim_party SET TAGS ('classification' = 'Confidential');

-- PII tagging
ALTER TABLE dim_party ALTER COLUMN date_of_birth SET TAGS ('pii' = 'true');
ALTER TABLE dim_party ALTER COLUMN tax_id SET TAGS ('pii' = 'true');
```

### Row and Column Filters

Unity Catalog row filters and column masks map to MD-DDL product-level `masking`:

```sql
-- Column mask for year-only strategy
CREATE FUNCTION mask_year_only(val DATE)
RETURNS DATE
RETURN CASE
    WHEN IS_MEMBER('analytics_group') THEN DATE_TRUNC('YEAR', val)
    ELSE val
END;

ALTER TABLE dim_party ALTER COLUMN date_of_birth
    SET MASK mask_year_only;

-- Column mask for hash strategy
CREATE FUNCTION mask_hash(val STRING)
RETURNS STRING
RETURN CASE
    WHEN IS_MEMBER('full_access_group') THEN val
    ELSE SHA2(val, 256)
END;

ALTER TABLE dim_party ALTER COLUMN tax_id
    SET MASK mask_hash;
```

## Clustering

### LIQUID Clustering

Databricks LIQUID clustering replaces traditional partitioning and Z-ordering.
Use for large tables:

```sql
-- Fact tables: cluster on date and primary dimension keys
CREATE TABLE fact_transaction (
    ...
)
USING DELTA
CLUSTER BY (transaction_date, account_sk);

-- Large dimensions with temporal queries
CREATE TABLE dim_party (
    ...
)
USING DELTA
CLUSTER BY (party_id, valid_from);
```

### Legacy Partitioning (Pre-LIQUID)

If LIQUID clustering is not available, use traditional partitioning:

```sql
CREATE TABLE fact_transaction (
    ...
)
USING DELTA
PARTITIONED BY (transaction_date);
```

## Struct and Array Types

Databricks supports complex types natively. Use for bounded 1:N or nested attributes:

```sql
-- Nested struct for composite attributes
CREATE TABLE dim_party (
    party_sk    BIGINT GENERATED ALWAYS AS IDENTITY,
    party_id    STRING NOT NULL,
    address     STRUCT<
        line1: STRING,
        line2: STRING,
        city: STRING,
        postcode: STRING,
        country: STRING
    >,
    contact_methods ARRAY<STRUCT<
        type: STRING,
        value: STRING,
        is_primary: BOOLEAN
    >>
);

-- Querying nested fields
SELECT party_id, address.city, address.country
FROM dim_party;
```

## Naming Conventions

Element | Convention | Example
--- | --- | ---
Catalog | `snake_case` | `enterprise_data`
Schema | `snake_case` | `financial_crime`
Dimension table | `dim_<entity>` | `dim_party`
Fact table | `fact_<entity>` | `fact_transaction`
Bridge table | `bridge_<relationship>` | `bridge_party_account`
Staging table | `stg_<source>_<entity>` | `stg_temenos_transaction`
Column | `snake_case` | `party_id`, `valid_from`
Surrogate key | `<entity>_sk` | `party_sk`
Natural key | `<entity>_id` | `party_id`

## SCD Type 2 Pattern

```sql
CREATE TABLE dim_party (
    party_sk       BIGINT GENERATED ALWAYS AS IDENTITY,
    party_id       STRING NOT NULL,
    party_type     STRING NOT NULL,
    full_name      STRING,
    -- ... business attributes ...
    valid_from     TIMESTAMP NOT NULL,
    valid_to       TIMESTAMP,
    is_current     BOOLEAN DEFAULT TRUE,
    _loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
USING DELTA
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true')
CLUSTER BY (party_id, valid_from);
```
