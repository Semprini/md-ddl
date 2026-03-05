# [Salesforce CRM](./source.md)

## Preference

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PreferredChannelCode | Text | 30 | | | yes | Preferred communication channel code | Customer Preferences.Preferred Contact Channel
2 | MarketingOptInFlag | Text | 1 | | | yes | Opt-in indicator for marketing messages | [Map Marketing Consent](#map-marketing-consent)

### Map Marketing Consent

Maps marketing consent flag into canonical consent status.

```yaml
type: conditional
target: Customer Preferences · Marketing Consent
source:
  field: Preference.MarketingOptInFlag
cases:
  Consented: "MarketingOptInFlag == 'Y'"
  Declined: "MarketingOptInFlag == 'N'"
  Unknown: "MarketingOptInFlag == null"
fallback: Unknown
```
