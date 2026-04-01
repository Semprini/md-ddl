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

---
### Transaction Type
Category of financial transaction representing the movement mechanism and clearing pathway.
```yaml
values:
  Wire Transfer:
    description: Domestic or international credit transfer processed via the local RTGS or wire network
  SWIFT Transfer:
    description: International payment instruction transmitted via the SWIFT network
  EFTPOS:
    description: Electronic funds transfer at point of sale via a card-present terminal
  ATM Withdrawal:
    description: Cash withdrawal initiated at an automated teller machine
  ATM Deposit:
    description: Cash or cheque deposit lodged at an automated teller machine
  Direct Debit:
    description: Pull payment authorised by the account holder and initiated by a creditor
  Direct Credit:
    description: Push payment credited directly to a beneficiary account
  Internal Transfer:
    description: Movement of funds between two accounts held within the same institution
  BPay:
    description: Bill payment processed through the BPAY scheme
  Cash Deposit:
    description: Physical cash lodged to an account at a branch or agency
  Cash Withdrawal:
    description: Physical cash disbursed from an account at a branch or agency
  Cheque:
    description: Payment by paper cheque presented for clearing
  RTGS:
    description: High-value same-day settlement payment processed through the Real-Time Gross Settlement system
```
---
### Transaction Status
Lifecycle state of a transaction from initiation through to final settlement or failure.
```yaml
values:
  Pending:
    description: Transaction has been submitted and is awaiting authorisation or clearing
  Authorised:
    description: Transaction has been authorised but not yet cleared or settled
  Cleared:
    description: Transaction has been cleared through the relevant payment scheme
  Settled:
    description: Final irrevocable settlement has occurred and funds have moved
  Failed:
    description: Transaction could not be processed and no funds were moved
  Reversed:
    description: A previously settled transaction has been reversed and funds returned
  Cancelled:
    description: Transaction was cancelled before settlement at the request of an authorised party
  Under Review:
    description: Transaction has been flagged and is under financial crime or fraud review; settlement is suspended pending outcome
```
---
### Transaction Channel
The channel or medium through which a transaction was initiated or processed.
```yaml
values:
  Branch:
    description: Transaction initiated or processed at a physical branch location by a teller or officer
  Online Banking:
    description: Transaction initiated by a customer through the institution's internet banking platform
  Mobile Banking:
    description: Transaction initiated by a customer through the institution's mobile application
  ATM:
    description: Transaction self-served by a customer at an automated teller machine
  EFTPOS Terminal:
    description: Transaction initiated at a merchant point-of-sale EFTPOS terminal
  SWIFT:
    description: Payment instruction transmitted via the SWIFT network, typically for international transfers
  Direct Entry:
    description: Batch payment submitted directly via the Direct Entry (DE) system
  Third Party:
    description: Transaction initiated by an authorised third party or payment service provider on behalf of a customer
  Internal System:
    description: Transaction generated automatically by an internal system process (e.g., interest capitalisation, fee deduction)
```
---
### Account Status
Operational lifecycle state of an account.
```yaml
values:
  Pending:
    description: Account has been created but has not yet been activated for transacting
  Active:
    description: Account is open and available for deposits, withdrawals, and other permitted operations
  Dormant:
    description: Account has had no customer-initiated transactions for an extended period as defined by the institution's dormancy policy
  Frozen:
    description: Account has been administratively frozen; no debits or credits are permitted pending investigation or regulatory instruction
  Suspended:
    description: Account is temporarily suspended pending compliance review or fraud investigation
  Closed:
    description: Account has been permanently closed; no further transactions are permitted
```
---
### Account Type
Classification of the financial account by its primary purpose and product characteristics.
```yaml
values:
  Savings:
    description: Interest-bearing deposit account intended for accumulation of funds
  Current:
    description: Transaction account (also called cheque or demand deposit account) used for day-to-day banking
  Term Deposit:
    description: Fixed-term deposit account where funds are locked in for a specified period at a contracted interest rate
  Loan:
    description: Credit account representing a disbursed loan obligation
  Line Of Credit:
    description: Revolving credit facility where the customer may draw down and repay up to an approved limit
  Mortgage:
    description: Secured loan account used to finance the purchase of real property
  Offset:
    description: Transaction account linked to a mortgage, where the balance offsets interest charged on the mortgage
  Foreign Currency:
    description: Account denominated in a currency other than the institution's base currency
```
---
### Agreement Status
Lifecycle state of a formal agreement between the institution and a party.
```yaml
values:
  Draft:
    description: Agreement has been created but not yet executed by all required parties
  Active:
    description: Agreement is fully executed and currently in force
  Suspended:
    description: Agreement is temporarily suspended by one or both parties pending resolution of a dispute or compliance matter
  Matured:
    description: Agreement has reached its scheduled maturity date and obligations have been fulfilled
  Terminated:
    description: Agreement has been terminated before its natural maturity, by mutual consent or by one party under agreed termination rights
  Cancelled:
    description: Agreement was cancelled before it became active and never took effect
```
---
### Contact Preference
The customer's preferred channel for outbound communication from the institution.
```yaml
values:
  Email:
    description: Customer prefers communications delivered by email
  SMS:
    description: Customer prefers short message service (text message) notifications
  Post:
    description: Customer prefers physical mail correspondence
  Phone:
    description: Customer prefers to be contacted by telephone call
  In App:
    description: Customer prefers push notifications and messages delivered within the institution's mobile application
  No Contact:
    description: Customer has opted out of all non-essential outbound communications
```
---
### Company Legal Structure
The legal form under which a company or organisation is incorporated or constituted. Relevant to AML risk assessment — certain structures (trusts, shell companies, special purpose vehicles) carry elevated money-laundering risk due to opacity of beneficial ownership.
```yaml
values:
  Private Company:
    description: Privately held limited liability company not listed on a public exchange (e.g., Pty Ltd, Ltd)
  Public Company:
    description: Company whose shares are listed and traded on a public stock exchange
  Partnership:
    description: Business entity where two or more persons carry on a business in common with a view to profit
  Sole Trader:
    description: Unincorporated individual carrying on business in their own name
  Trust:
    description: Legal arrangement where a trustee holds assets for the benefit of beneficiaries; elevated AML risk due to beneficial ownership complexity
  Cooperative:
    description: Member-owned and democratically controlled organisation
  Government Entity:
    description: Entity owned or controlled by a national, state, or local government
  Non-Profit:
    description: Organisation operating for a purpose other than profit; subject to specific AML obligations due to potential misuse for terrorist financing
  Foreign Entity:
    description: Entity incorporated or constituted under the laws of a foreign jurisdiction
  Special Purpose Vehicle:
    description: Entity created for a specific, narrow purpose (e.g., asset securitisation); elevated AML scrutiny due to potential use in layering structures
```
---
### Association Type
The nature of the relationship between two Parties in the Party Related To Party network. Used for beneficial ownership mapping, PEP network screening, and suspicious activity investigation.
```yaml
values:
  Ultimate Beneficial Owner:
    description: Individual who ultimately owns or controls 25% or more of the entity, directly or indirectly
  Beneficial Owner:
    description: Individual with a beneficial interest in the entity below the UBO threshold but still subject to disclosure obligations
  Director:
    description: Individual appointed to the board of directors or equivalent governing body
  Shareholder:
    description: Entity or individual holding shares in a company
  Guarantor:
    description: Party who has provided a guarantee for another party's obligations
  Controlling Person:
    description: Individual who exercises control over an entity through means other than shareholding (e.g., power of attorney, contractual rights)
  Spouse:
    description: Legal spouse or domestic partner; relevant for PEP close associate screening
  Parent:
    description: Direct parent of an individual; relevant for PEP family member screening
  Child:
    description: Direct child of an individual; relevant for PEP family member screening
  Sibling:
    description: Sibling of an individual; relevant for PEP family member screening
  Close Associate:
    description: Individual known to be in close personal or professional relationship with a PEP
  Employer:
    description: Organisation that employs the related party
  Employee:
    description: Individual employed by the related organisation
  Signatory:
    description: Individual authorised to sign on behalf of an entity
```
---
### Account Holder Type
The nature of a customer's holding relationship with an account. Used as a relationship attribute on Customer Holds Account.
```yaml
values:
  Primary Holder:
    description: The principal account owner responsible for the account relationship
  Joint Holder:
    description: Co-owner of the account with equal rights to the Primary Holder
  Signatory:
    description: Individual authorised to transact on the account but without ownership rights
  Beneficial Owner:
    description: Individual who benefits from the account but whose name may not appear as a legal owner
  Guardian:
    description: Individual acting as legal guardian for a minor or incapacitated account holder
  Attorney:
    description: Individual holding power of attorney to operate the account on behalf of the primary holder
```
