# PostgreSQL Dialect Reference

## Data Type Mappings

MD-DDL Type | PostgreSQL Type | Notes
--- | --- | ---
`string` | `VARCHAR(n)` | Length recommended; use `TEXT` when unbounded
`string` with `max_length` | `VARCHAR(n)` | Apply length constraint from entity YAML
`integer` | `BIGINT` | Default; use `INTEGER` for values known to fit 32-bit
`decimal` | `NUMERIC(p,s)` | Map `precision` and `scale` from entity YAML
`boolean` | `BOOLEAN` | Direct mapping
`date` | `DATE` | Direct mapping
`datetime` | `TIMESTAMP` | Without timezone; use `TIMESTAMPTZ` when timezone-aware
`timestamp` | `TIMESTAMPTZ` | With timezone by default for operational tables
`text` | `TEXT` | Unbounded text
`binary` | `BYTEA` | Direct mapping

## Semi-Structured Data

### JSONB for Flexible Attributes

PostgreSQL `JSONB` serves a similar role to Snowflake VARIANT. Use for:

- Extension attributes varying by subtype
- Source system metadata preserved as-is
- Attributes that carry nested structures

```sql
CREATE TABLE party (
    party_id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    party_bk       VARCHAR(50) NOT NULL UNIQUE,
    party_type     VARCHAR(20) NOT NULL,
    extended_attrs JSONB,
    valid_from     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to       TIMESTAMPTZ,
    is_current     BOOLEAN NOT NULL DEFAULT TRUE
);

-- Querying JSONB fields
SELECT
    party_bk,
    extended_attrs->>'date_of_birth' AS date_of_birth,
    extended_attrs->>'nationality' AS nationality
FROM party
WHERE party_type = 'Individual';

-- GIN index for JSONB queries
CREATE INDEX idx_party_extended ON party USING GIN (extended_attrs);
```

## Indexing

PostgreSQL uses traditional B-tree, GIN, GiST, and BRIN indexes.

### Index Strategy by Table Role

Table Role | Primary Index | Additional Indexes
--- | --- | ---
Dimension / Core table | Primary key (auto) | Unique on natural key; B-tree on foreign keys
Fact / Event table | Primary key (auto) | B-tree on timestamp; composite on dimension FKs
Bridge / Junction | Composite primary key | B-tree on each FK column
Reference / Lookup | Primary key (auto) | Unique on code/value

```sql
-- Dimension: natural key + temporal lookup
CREATE UNIQUE INDEX idx_party_bk_current
    ON party (party_bk) WHERE is_current = TRUE;

-- Fact: timestamp range queries
CREATE INDEX idx_transaction_timestamp
    ON transaction (transaction_timestamp);

-- Fact: dimension lookups
CREATE INDEX idx_transaction_account
    ON transaction (account_id);
```

### Partial Indexes

PostgreSQL partial indexes are useful for SCD2 current-record lookups:

```sql
-- Only index current records for fast lookups
CREATE INDEX idx_party_current
    ON party (party_bk) WHERE is_current = TRUE;
```

## Table Partitioning

### Range Partitioning for Fact Tables

Use declarative partitioning for large fact/event tables:

```sql
CREATE TABLE transaction (
    transaction_id   BIGINT GENERATED ALWAYS AS IDENTITY,
    transaction_date DATE NOT NULL,
    amount           NUMERIC(18,2),
    account_id       BIGINT NOT NULL,
    -- ... other columns ...
    PRIMARY KEY (transaction_id, transaction_date)
) PARTITION BY RANGE (transaction_date);

-- Monthly partitions
CREATE TABLE transaction_2025_01
    PARTITION OF transaction
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE transaction_2025_02
    PARTITION OF transaction
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

### Partition Retention

Map MD-DDL governance `retention` to partition management:

```sql
-- Drop partitions beyond retention period (7 years)
DROP TABLE IF EXISTS transaction_2018_01;
```

## Constraints

PostgreSQL supports rich constraints that map to MD-DDL entity YAML:

### Check Constraints for Enums

When enums are kept as inline columns (small, stable):

```sql
CREATE TABLE account (
    account_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_type VARCHAR(30) NOT NULL
        CHECK (account_type IN ('Savings', 'Current', 'Term Deposit', 'Loan')),
    status       VARCHAR(20) NOT NULL
        CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed'))
);
```

### Foreign Keys

PostgreSQL enforces FK constraints at the database level:

```sql
ALTER TABLE transaction
    ADD CONSTRAINT fk_transaction_account
    FOREIGN KEY (account_id) REFERENCES account(account_id);
```

### Domain Types

PostgreSQL domains provide reusable constrained types:

```sql
CREATE DOMAIN currency_code AS VARCHAR(3)
    CHECK (VALUE ~ '^[A-Z]{3}$');

CREATE DOMAIN country_code AS VARCHAR(2)
    CHECK (VALUE ~ '^[A-Z]{2}$');
```

## Row-Level Security

Map MD-DDL product-level `masking` and `classification` to RLS:

```sql
-- Enable RLS
ALTER TABLE party ENABLE ROW LEVEL SECURITY;

-- Policy for restricted classification
CREATE POLICY confidential_access ON party
    USING (current_setting('app.user_role') IN ('data_steward', 'compliance'));
```

## Naming Conventions

Element | Convention | Example
--- | --- | ---
Schema | `snake_case` | `financial_crime`
Dimension table (dimensional) | `dim_<entity>` | `dim_party`
Fact table (dimensional) | `fact_<entity>` | `fact_transaction`
Bridge table (dimensional) | `bridge_<relationship>` | `bridge_party_account`
Core table (3NF) | `<entity>` | `party`
Junction table (3NF) | `<entity_a>_<entity_b>` | `party_account`
Staging table | `stg_<source>_<entity>` | `stg_temenos_transaction`
Column | `snake_case` | `party_id`, `valid_from`
Surrogate key | `<entity>_sk` (dimensional) | `party_sk`
Primary key | `<entity>_id` (3NF) | `party_id`
Sequence | `seq_<entity>` | `seq_party`

## SCD Type 2 Pattern

```sql
CREATE TABLE dim_party (
    party_sk       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    party_bk       VARCHAR(50) NOT NULL,
    party_type     VARCHAR(20) NOT NULL,
    full_name      VARCHAR(200),
    -- ... business attributes ...
    valid_from     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to       TIMESTAMPTZ,
    is_current     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX idx_dim_party_current
    ON dim_party (party_bk) WHERE is_current = TRUE;
```
