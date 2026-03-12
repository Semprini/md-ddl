# dim_product

Baseline documentation for the existing `dim_product` dimension table in the Snowflake data warehouse. This is a Type 2 slowly changing dimension tracking product master data including category hierarchy, brand, and cost information.

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
CREATE TABLE analytics.dim_product (
    product_key    BIGINT        NOT NULL PRIMARY KEY,
    product_id     VARCHAR(20)   NOT NULL,
    product_name   VARCHAR(200)  NOT NULL,
    category       VARCHAR(50)   NOT NULL,
    subcategory    VARCHAR(50),
    brand          VARCHAR(100),
    unit_cost      DECIMAL(10,2) NOT NULL,
    is_active      BOOLEAN       NOT NULL DEFAULT TRUE,
    effective_date DATE          NOT NULL,
    expiry_date    DATE
);
```

## Column Summary

Column | Type | Nullable | Description
--- | --- | --- | ---
product_key | bigint | no | Surrogate key for SCD2 versioning
product_id | varchar(20) | no | Natural key from POS product master
product_name | varchar(200) | no | Display name of the product
category | varchar(50) | no | Top-level product category
subcategory | varchar(50) | yes | Secondary product category
brand | varchar(100) | yes | Product brand name
unit_cost | decimal(10,2) | no | Cost per unit to the retailer
is_active | boolean | no | Whether the product is currently sold
effective_date | date | no | SCD2 effective date for this version
expiry_date | date | yes | SCD2 expiry date; null for current version

## Notes

- **SCD2 handling**: The `product_key` surrogate key changes with each version. The current active version has `expiry_date IS NULL`. Historical fact records retain references to the version-specific `product_key` that was current at the time of the sale.
- **Grain**: One row per product per SCD2 version
- **Load**: Daily, SLA available by 05:00 UTC
- **Category hierarchy**: The `category` / `subcategory` split is flat. There is no separate dimension for category hierarchy — this may warrant a dedicated enum or hierarchy in the canonical model.
