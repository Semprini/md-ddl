# Snowflake Dialect Reference

## Data Type Mappings

MD-DDL Type | Snowflake Type | Notes
--- | --- | ---
`string` | `VARCHAR` | Default; no length required (Snowflake VARCHAR is variable-length)
`string` with `max_length` | `VARCHAR(n)` | Apply length constraint
`integer` | `NUMBER(38,0)` | Snowflake uses NUMBER for all integer types
`decimal` | `NUMBER(p,s)` | Map `precision` and `scale` from entity YAML
`boolean` | `BOOLEAN` | Direct mapping
`date` | `DATE` | Direct mapping
`datetime` | `TIMESTAMP_NTZ` | Default; use `TIMESTAMP_TZ` when timezone awareness is required
`timestamp` | `TIMESTAMP_NTZ` | Use `TIMESTAMP_LTZ` for local timezone interpretation
`text` | `VARCHAR` | Equivalent to `string` in Snowflake
`binary` | `BINARY` | Direct mapping

## Semi-Structured Data

Snowflake provides native VARIANT, OBJECT, and ARRAY types for semi-structured data.

### When to Use VARIANT

Use `VARIANT` columns when an MD-DDL entity has:

- Attributes marked with `type: json` or `type: object`
- Extension attributes that vary by subtype (alternative to class-table inheritance)
- Attributes that carry nested structures from source systems

### VARIANT Column Patterns

```sql
-- Semi-structured attribute as VARIANT
CREATE TABLE dim_party (
    party_sk       NUMBER GENERATED ALWAYS AS IDENTITY,
    party_id       VARCHAR NOT NULL,
    party_type     VARCHAR NOT NULL,
    extended_attrs VARIANT,  -- subtype-specific attributes stored as JSON
    valid_from     TIMESTAMP_NTZ NOT NULL,
    valid_to       TIMESTAMP_NTZ,
    is_current     BOOLEAN DEFAULT TRUE,
    CONSTRAINT pk_dim_party PRIMARY KEY (party_sk)
);

-- Querying nested attributes
SELECT
    party_id,
    extended_attrs:date_of_birth::DATE AS date_of_birth,
    extended_attrs:nationality::VARCHAR AS nationality
FROM dim_party
WHERE party_type = 'Individual';
```

### LATERAL FLATTEN for Arrays

When a 1:N relationship is stored as a VARIANT array (e.g., contact methods):

```sql
SELECT
    p.party_id,
    f.value:type::VARCHAR AS contact_type,
    f.value:value::VARCHAR AS contact_value
FROM dim_party p,
LATERAL FLATTEN(input => p.extended_attrs:contact_methods) f;
```

## Platform-Specific Features

### Clustering

Use `CLUSTER BY` instead of traditional indexes. Cluster on columns that dominate
WHERE and JOIN predicates:

```sql
-- Fact tables: cluster on date and primary dimension FKs
CREATE TABLE fact_transaction (
    ...
) CLUSTER BY (transaction_date, account_sk);

-- Large dimensions: cluster on natural key and temporal columns
CREATE TABLE dim_customer (
    ...
) CLUSTER BY (customer_id, valid_from);
```

### Transient and Temporary Tables

- Use `TRANSIENT` for staging and intermediate tables (no Fail-Safe, lower cost)
- Use `TEMPORARY` for session-scoped working tables

```sql
CREATE TRANSIENT TABLE stg_transaction_raw (...);
```

### Time Travel and Retention

Snowflake Time Travel provides system-level temporal queries. Use `DATA_RETENTION_TIME_IN_DAYS`
to align with MD-DDL `retention` governance metadata:

```sql
CREATE TABLE dim_party (
    ...
) DATA_RETENTION_TIME_IN_DAYS = 90;
```

### Tags for Governance

Snowflake object tagging maps to MD-DDL governance metadata:

```sql
-- Apply classification
ALTER TABLE dim_party SET TAG governance_classification = 'Confidential';

-- Apply PII flag
ALTER COLUMN dim_party.date_of_birth SET TAG pii = 'true';
ALTER COLUMN dim_party.tax_id SET TAG pii = 'true';
ALTER COLUMN dim_party.tax_id SET TAG masking_strategy = 'hash';
```

### Dynamic Data Masking

Snowflake masking policies map to MD-DDL product-level `masking` strategies:

```sql
-- year-only strategy for dates
CREATE MASKING POLICY mask_year_only AS (val DATE)
RETURNS DATE ->
    CASE
        WHEN CURRENT_ROLE() IN ('ANALYTICS_ROLE')
        THEN DATE_TRUNC('YEAR', val)
        ELSE val
    END;

-- hash strategy for identifiers
CREATE MASKING POLICY mask_hash AS (val VARCHAR)
RETURNS VARCHAR ->
    CASE
        WHEN CURRENT_ROLE() IN ('FULL_ACCESS_ROLE')
        THEN val
        ELSE SHA2(val)
    END;

-- Apply to columns
ALTER TABLE dim_party ALTER COLUMN date_of_birth
    SET MASKING POLICY mask_year_only;
ALTER TABLE dim_party ALTER COLUMN tax_id
    SET MASKING POLICY mask_hash;
```

## Naming Conventions

Element | Convention | Example
--- | --- | ---
Schema | `SNAKE_CASE` | `FINANCIAL_CRIME`
Dimension table | `DIM_<entity>` | `DIM_PARTY`
Fact table | `FACT_<entity>` | `FACT_TRANSACTION`
Bridge table | `BRIDGE_<relationship>` | `BRIDGE_PARTY_ACCOUNT`
Staging table | `STG_<source>_<entity>` | `STG_TEMENOS_TRANSACTION`
Column | `SNAKE_CASE` | `PARTY_ID`, `VALID_FROM`
Surrogate key | `<entity>_SK` | `PARTY_SK`
Natural key | `<entity>_ID` | `PARTY_ID`

## SCD Type 2 Pattern

```sql
CREATE TABLE dim_party (
    party_sk       NUMBER GENERATED ALWAYS AS IDENTITY,
    party_id       VARCHAR NOT NULL,
    party_type     VARCHAR NOT NULL,
    full_name      VARCHAR,
    -- ... business attributes ...
    valid_from     TIMESTAMP_NTZ NOT NULL,
    valid_to       TIMESTAMP_NTZ,
    is_current     BOOLEAN DEFAULT TRUE,
    _loaded_at     TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT pk_dim_party PRIMARY KEY (party_sk)
);
```
