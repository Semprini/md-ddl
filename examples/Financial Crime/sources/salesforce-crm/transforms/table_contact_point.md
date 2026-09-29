# [Financial Crime](../../../domain.md)

## Sources

### [Salesforce CRM](../source.md#salesforce-crm)

#### ContactPoint

One ContactPoint row is a party's use of an address for a purpose. The canonical model splits it into the physical Address, deduplicated across parties, and the Contact Address association.

##### Entity Fan-Out

```yaml
produces:
  - entity: Address
    cardinality: 1
    deduplicated: true
    identity: Address Uniqueness Merge

  - entity: Contact Address
    cardinality: 1
    identity:
      field: ContactPoint.Id
      maps_to: Contact Address · Contact Address Identifier
    references:
      Address: Address Uniqueness Merge
      Party: ContactPoint.PartyExternalId
```

##### Source Schema

A blank Destination means the column is deliberately not mapped.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | Id | Text | 18 | | | no | Salesforce record identifier | Contact Address.Contact Address Identifier
2 | PartyExternalId | Text | 40 | | | no | Enterprise party identifier of the owning account | Reference: Party
3 | Street | Text | 255 | | | no | Street line | Address.Address Line 1, [Transform: Address Uniqueness Merge](#transform-address-uniqueness-merge)
4 | City | Text | 80 | | | yes | City or town | Address.City
5 | State | Text | 80 | | | yes | State or region | Address.State Or Region
6 | PostalCode | Text | 20 | | | yes | Postcode | Address.Postcode, [Transform: Address Uniqueness Merge](#transform-address-uniqueness-merge)
7 | Country | Text | 2 | | | no | ISO 3166-1 alpha-2 country | Address.Country, [Transform: Address Uniqueness Merge](#transform-address-uniqueness-merge)
8 | PurposeCode | Text | 10 | | | no | Purpose of the contact point | [Transform: Map Address Purpose](#transform-map-address-purpose)
9 | IsPrimary | Boolean | | | | no | Primary contact point for its purpose | Contact Address.Is Primary
10 | VerificationResult | Text | 20 | | | yes | Verification workflow result | [Transform: Map Verification Status](#transform-map-verification-status)
11 | VerifiedDate | Date | | | | yes | Date verification completed | Contact Address.Verification Date
12 | ValidFromDate | Date | | | | no | Effective-from date | Contact Address.Valid From
13 | ValidToDate | Date | | | | yes | Effective-to date | Contact Address.Valid To
14 | LastModifiedDate | DateTime | | | | no | Last change to the row | [Transform: Address Uniqueness Merge](#transform-address-uniqueness-merge)

##### Transform: Address Uniqueness Merge

Parties who share a physical address share one Address instance, which is what makes shared-address network analysis possible. The key is the normalised street, postcode, and country. Address is immutable reference data, so when merged rows disagree on the other fields, the first recorded row's values stand.

```yaml
type: deduplication
target: Address · Address Identifier
key:
  - using:
      - field: ContactPoint.Street
      - field: ContactPoint.PostalCode
      - field: ContactPoint.Country
    normalise: [trim, uppercase, collapse_whitespace]
    prefix: "ADDR"
survivorship:
  strategy: earliest
  timestamp_field: ContactPoint.LastModifiedDate
```

##### Transform: Map Address Purpose

CRM purpose codes are an opaque code table.

```yaml
type: lookup
target: Contact Address · Address Purpose
source:
  field: ContactPoint.PurposeCode
lookup:
  inline:
    HOME: Residential
    MAIL: Mailing
    WORK: Business
    BILL: Billing
    REG: Registered Office
fallback: reject
```

##### Transform: Map Verification Status

A pending verification hasn't verified anything yet, so it maps to Unverified. A failed check maps to Rejected.

```yaml
type: conditional
target: Contact Address · Verification Status
evaluation: exclusive
source:
  field: ContactPoint.VerificationResult
cases:
  Verified: "VerificationResult == 'PASS'"
  Unverified: "VerificationResult == 'PENDING' OR VerificationResult IS NULL"
  Rejected: "VerificationResult == 'FAIL'"
fallback: Unverified
```

##### Worked Examples

```yaml
example: Two parties at the same address share one Address
given:
  - Id: "0PA000000000001"
    PartyExternalId: "P-1002"
    Street: "12 Harbour St"
    City: "Wellington"
    PostalCode: "6011"
    Country: "NZ"
    PurposeCode: "HOME"
    IsPrimary: true
    VerificationResult: "PASS"
    VerifiedDate: "2024-03-01"
    ValidFromDate: "2024-03-01"
    LastModifiedDate: "2024-03-01T09:00:00Z"
  - Id: "0PA000000000002"
    PartyExternalId: "P-1005"
    Street: " 12  harbour st "
    City: "Wellington"
    PostalCode: "6011"
    Country: "NZ"
    PurposeCode: "MAIL"
    IsPrimary: true
    VerificationResult: "PENDING"
    ValidFromDate: "2024-05-20"
    LastModifiedDate: "2024-05-20T14:30:00Z"
produces:
  - entity: Address
    cardinality: 1
    Address Identifier: "ADDR:12 HARBOUR ST|6011|NZ"
    Address Line 1: "12 Harbour St"
    Postcode: "6011"
    Country: "NZ"
  - entity: Contact Address
    Contact Address Identifier: "0PA000000000001"
    Address Purpose: Residential
    Verification Status: Verified
    Verification Date: "2024-03-01"
  - entity: Contact Address
    Contact Address Identifier: "0PA000000000002"
    Address Purpose: Mailing
    Verification Status: Unverified
notes: >
  After trimming, uppercasing, and collapsing whitespace, both streets normalise to
  "12 HARBOUR ST", so the rows share the key ADDR:12 HARBOUR ST|6011|NZ and one Address
  instance, which both Contact Addresses reference. Survivorship is earliest, so the
  first row's values stand and the second row's untidy spelling doesn't overwrite them:
  normalisation shapes the key, not the stored value.
```

```yaml
example: Failed verification and an unknown purpose code
given:
  - Id: "0PA000000000003"
    PartyExternalId: "P-1001"
    Street: "1 Quay Rd"
    PostalCode: "2000"
    Country: "AU"
    PurposeCode: "REG"
    IsPrimary: true
    VerificationResult: "FAIL"
    ValidFromDate: "2024-01-10"
    LastModifiedDate: "2024-01-10T08:00:00Z"
  - Id: "0PA000000000004"
    PartyExternalId: "P-1001"
    Street: "PO Box 77"
    PostalCode: "2000"
    Country: "AU"
    PurposeCode: "SHIP"
    IsPrimary: false
    ValidFromDate: "2024-01-10"
    LastModifiedDate: "2024-01-10T08:00:00Z"
produces:
  - entity: Contact Address
    Contact Address Identifier: "0PA000000000003"
    Address Purpose: Registered Office
    Verification Status: Rejected
notes: >
  FAIL maps to Rejected. The second row's purpose code SHIP isn't in the code table, and
  the lookup's fallback is reject, so that row produces nothing and is reported rather
  than loaded with a guessed purpose.
```
