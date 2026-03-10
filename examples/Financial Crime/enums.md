# [Financial Crime](domain.md)

## Enums

### Party Status

Operational status of a party record.

```yaml
values:
  Active:
    description: Party is active and may participate in relationships and transactions
  Under Review:
    description: Party is under compliance review and must not initiate new transactions
  Restricted:
    description: Party is restricted pending investigation outcome or risk remediation
  Inactive:
    description: Party relationship is dormant or no longer operational
  Closed:
    description: Party record is closed and no new activity is permitted
```

---

### Financial Crime Risk Rating

Institution-assessed ML/TF risk level for a party.

```yaml
values:
  Low:
    description: Low financial crime risk profile
    score: 1
  Medium:
    description: Moderate financial crime risk profile
    score: 2
  High:
    description: Elevated financial crime risk requiring enhanced controls
    score: 3
  Very High:
    description: Severe financial crime risk requiring intensive monitoring
    score: 4
```

---

### Sanctions Screen Status

Outcome of sanctions screening checks.

```yaml
values:
  Not Screened:
    description: Screening has not yet been performed
  Clear:
    description: No match found against applicable sanctions lists
  Potential Match:
    description: Possible match detected and pending investigation
  Confirmed Match:
    description: Match confirmed and services must be blocked
  False Positive:
    description: Potential match reviewed and cleared as not the sanctioned subject
```

---

### Party Role Status

Lifecycle status of a specific party role instance.

```yaml
values:
  Pending:
    description: Role created but not yet activated
  Active:
    description: Role is active and confers its business permissions
  Suspended:
    description: Role is temporarily paused pending review or remediation
  Closed:
    description: Role has ended and is no longer effective
```

---

### Due Diligence Status

CDD/EDD completion state for a role.

```yaml
values:
  Not Started:
    description: Due diligence process has not commenced
  In Progress:
    description: Due diligence activities are underway
  Complete:
    description: Required due diligence is complete
  Expired:
    description: Prior due diligence is no longer current and revalidation is required
  Failed:
    description: Due diligence failed and role must not be activated
```

---

### PEP Status

Politically exposed person classification for individuals.

```yaml
values:
  Not PEP:
    description: Individual is not identified as a politically exposed person or associate
  Domestic PEP:
    description: Individual holds a prominent public function domestically
  Foreign PEP:
    description: Individual holds a prominent public function in a foreign jurisdiction
  International Organisation PEP:
    description: Individual holds a prominent function in an international organisation
  PEP Family Member:
    description: Individual is an immediate family member of a PEP
  PEP Close Associate:
    description: Individual is a known close associate of a PEP
```

---

### Address Type

Structural type of an address record.

```yaml
values:
  Street Address:
    description: Standard physical street address
  PO Box:
    description: Postal box address
  Registered Office:
    description: Registered office address for a legal entity
  Overseas Address:
    description: Address located outside the primary operating jurisdiction
```

---

### Address Purpose

Business purpose for which a party uses an address.

```yaml
values:
  Residential:
    description: Residential/home address for an individual
  Mailing:
    description: Address used for correspondence
  Business:
    description: Primary business operating address
  Registered Office:
    description: Registered legal address for a company
  Billing:
    description: Address used for billing and statement delivery
```

---

### Address Verification Status

Current verification state of a contact address association.

```yaml
values:
  Unverified:
    description: Address not yet verified
  Verified:
    description: Address verified against acceptable evidence
  Pending Reverification:
    description: Existing verification is aging and requires refresh
  Rejected:
    description: Verification attempt failed or evidence was insufficient
  Expired:
    description: Verification is out of date and not valid for current obligations
```

---

### Verification Method

Method used to verify an address.

```yaml
values:
  Documentary:
    description: Verified using accepted documentary evidence
  Electronic:
    description: Verified using an approved electronic data source
  In Person:
    description: Verified face-to-face at branch or approved representative location
  Third Party Attestation:
    description: Verified via trusted attestation from an approved third party
```

---

### Currency Code

ISO 4217 alphabetic currency codes used across account balances and transaction amounts. This is a representative subset — the full ISO 4217 code list is the normative reference.

Standard: [ISO 4217 — Currency codes](https://www.iso.org/iso-4217-currency-codes.html)

```yaml
values:
  AUD:
    description: Australian Dollar
  NZD:
    description: New Zealand Dollar
  USD:
    description: United States Dollar
  EUR:
    description: Euro
  GBP:
    description: Pound Sterling
  JPY:
    description: Japanese Yen
  SGD:
    description: Singapore Dollar
  HKD:
    description: Hong Kong Dollar
  CHF:
    description: Swiss Franc
  CAD:
    description: Canadian Dollar
```
