# **Basel (BCBS) - Regulatory Guidance**

## **Overview**

The Basel Accords are a series of international banking regulations (Basel I, II, III, and now IV) set by the **Basel Committee on Banking Supervision (BCBS)**. They aim to ensure financial institutions have enough capital to meet obligations and absorb unexpected losses.

**Relevance**: If modeling core banking, risk management, capital adequacy, or liquidity domains for any internationally active bank.

## **Key Basel Standards for Data Modeling**

### **BCBS 239 - Risk Data Aggregation and Reporting**

**Impact on MD-DDL**:
BCBS 239 is the most significant regulatory driver for MD-DDL modeling. It demands that banks have a strong "Data DNA" with clear lineage and accuracy.

* **Accuracy and Integrity**: Requires precise attribute definitions and validation constraints.
* **Completeness**: Requires that all material exposures are captured in the domain.
* **Adaptability**: The model must be flexible enough to handle stress testing and changing market conditions.

**Metadata to include**:

```yaml
governance:
  bcbs239_scope: true
  data_lineage_required: true
  aggregation_level: "Entity" | "Group" | "Portfolio"
  accuracy_threshold: 0.999
  reconciliation_key: "General Ledger Account"

```

### **Basel III / IV - Capital and Risk-Weighted Assets (RWA)**

**Impact on MD-DDL**:
Requires entities to be categorized by **Asset Class** to determine their risk weighting.

**Metadata to include**:

```yaml
governance:
  basel_asset_class: 
    - "Sovereign"
    - "Public Sector Entity"
    - "Bank"
    - "Corporate"
    - "Retail"
    - "Residential Mortgage"
  risk_weight_approach: "Standardised" | "FIRB" | "AIRB"
  pd_model: "Internal Rating Model v2"
  lgd_estimate: 0.45

```

## **Basel Risk Categories**

When modeling a domain, use the following `risk_category` metadata to align with Basel Pillar 1 requirements:

1. **Credit Risk**: Risk of loss from a counterparty's failure to repay.
2. **Market Risk**: Risk of loss in on- and off-balance-sheet positions arising from movements in market prices.
3. **Operational Risk**: Risk of loss resulting from inadequate or failed internal processes, people, and systems.
4. **Liquidity Risk**: Risk that the bank cannot meet its financial obligations as they come due.

## **Common Basel-Impacted Entities**

| Entity | Basel Relevance | Key Metadata / Attributes |
| --- | --- | --- |
| **Exposure** | Core unit of risk. | `exposure_at_default`, `asset_class` |
| **Counterparty** | The entity the bank is exposed to. | `internal_rating`, `probability_of_default` |
| **Collateral** | Credit Risk Mitigation (CRM). | `collateral_type`, `haircut_percentage` |
| **Financial Instrument** | Market risk exposure. | `valuation_method`, `market_observable` |
| **Loss Event** | Operational risk history. | `gross_loss_amount`, `recovery_amount` |
| **Netting Agreement** | Reducing gross exposure. | `is_enforceable`, `agreement_type` |

## **Basel Data Quality Constraints**

Basel requires strict validation to ensure RWA calculations are not understated.

```yaml
constraints:
  Basel - Exposure Non-Negative:
    check: "Exposure at Default >= 0"
    description: "Credit risk exposures cannot be negative for capital calculation."

  Basel - Rating Validity:
    check: "Internal Rating IN ['1', '2', '3', '4', '5', 'Default']"
    description: "Ensures counterparty ratings align with the approved IRB model."

```

## **Basel + Local Regulator Integration**

Basel is a global framework, but it is implemented via local law. When modeling, you should typically load **both** the Basel guidance and your local regulator guidance (e.g., APRA for Australia, ECB for EU).

**Example MD-DDL Metadata**:

```yaml
governance:
  regulatory_scope:
    - BCBS 239 (Global)
    - Basel III (Global)
    - APRA APS 110 (Local Implementation)

```

## **Resources**

* [BCBS Official Website (BIS)](https://www.bis.org/bcbs/index.htm)
* [BCBS 239 Principles](https://www.bis.org/publ/bcbs239.pdf)
* [Basel III Framework](https://www.bis.org/bcbs/basel3.htm)
* [Basel IV Summary (BCBS d424)](https://www.bis.org/bcbs/publ/d424.htm)
