# Data Tables

## Transaction & Account

| type | Authorisation | is_recurring | amount | code | transaction_type | source_account.type | source_account.name | source_account.number | source_account.customer.type | customer.customer_number | customer.legal_type | customer.status |
|------|--------------|--------------|--------|------|-----------------|-------------------|-------------------|----------------------|----------------------------|------------------------|-------------------|----------------|
| Payment | 12345 | FALSE | 12.34 | 123456 | Payment | Account | Test Account | 1 | Customer | 1 | test | Active |

---

## Address & Region

| address.type | address.name | address.address_type | address.id | region.type | region.name | country.type | iso_code | country.name | country.type2 |
|-------------|-------------|---------------------|-----------|------------|------------|-------------|---------|-------------|--------------|
| Address | test address | Postal | 1 | Region | Auckland | Country | NZL | New Zealand | Country |

---

## Individual & Customer

| individual.type | individual.date_of_birth | individual.first_name | individual.last_name | individual.name | individual.id | customer.organisation |
|----------------|------------------------|----------------------|---------------------|----------------|--------------|----------------------|
| Individual | 10/11/2020 | Test | McTest | Test McTest | 1 | |

## Sample Code

```python
import pandas as pd
import json

data = json.loads(json_data)
data = pd.json_normalize(data)
print(data.to_csv())
```
