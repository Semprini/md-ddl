# collibra_product

Baseline documentation for the Product asset as catalogued in Collibra. This captures the governance metadata, ownership, and data quality information maintained in the enterprise data catalog.

```yaml
baseline:
  type: catalog
  source_system: "Collibra"
  captured_date: 2024-02-01
  captured_by: "Data Governance Team"
  status: active
```

## Catalog Metadata

- **Tool**: Collibra
- **Asset**: Product
- **Classification**: Internal
- **PII**: No
- **Data Owner**: Sarah Chen, Head of Merchandising
- **Data Steward**: Mike Torres, Data Governance Analyst
- **Quality Score**: 0.92
- **Lineage**: POS System (Oracle) -> Fivetran -> Snowflake raw.pos_system.products -> dbt -> analytics.dim_product

## Governance Notes

- **Classification**: Product data is classified as Internal. No PII is present in the product dimension. Unit cost data is considered commercially sensitive but does not meet the threshold for Confidential classification under the current policy.
- **Data quality**: The 0.92 quality score reflects two known issues:
  1. Approximately 5% of products have null `subcategory` values where the POS system did not enforce the field prior to 2022
  2. Brand names have inconsistent casing (e.g., "ACME", "Acme", "acme") — a cleansing rule was proposed but not yet implemented
- **Certification**: The Product asset was certified in Collibra on 2023-11-15 by the Data Governance Council. Recertification is due 2024-11-15.
- **Usage**: The Product asset is referenced by 12 downstream reports and 3 data products in Collibra's lineage graph.
