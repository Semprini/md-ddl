# BIAN Source Manifest

Track provenance for pinned BIAN source artifacts committed to this repository.

Version | File | Source URL | Retrieved (UTC) | Checksum (SHA256) | Notes
--- | --- | --- | --- | --- | ---
14.0.0 | BOClassesLite.json | `https://bian-modelapi-v8.azurewebsites.net/BOClassesLite/BIAN/14.0.0` | 2026-03-08 | N/A | v8 requires auth (`401` unauthenticated); v4 endpoint returns `404`, fallback `/BOClassesBasic/BIAN/14.0.0` returns `[]`.
14.0.0 | BOEnumerationsLite.json | `https://bian-modelapi-v8.azurewebsites.net/BOEnumerationsLite/BIAN/14.0.0` | 2026-03-08 | N/A | v8 requires auth (`401` unauthenticated); v4 endpoint returns `404`, fallback `/BOEnumerationsBasic/BIAN/14.0.0` returns `[]`.
14.0.0 | BusinessAreas.json | `https://bian-modelapi-v8.azurewebsites.net/BusinessAreas/BIAN/14.0.0` | 2026-03-08 | N/A | v8 requires auth (`401` unauthenticated); v4 endpoint returns `[]`.
14.0.0 | BusinessDomains.json | `https://bian-modelapi-v8.azurewebsites.net/BusinessDomains/BIAN/14.0.0` | 2026-03-08 | N/A | v8 requires auth (`401` unauthenticated); v4 endpoint returns `[]`.
14.0.0 | ServiceDomainsBasic.json | `https://bian-modelapi-v8.azurewebsites.net/ServiceDomainsBasic/BIAN/14.0.0` | 2026-03-08 | N/A | v8 requires auth (`401` unauthenticated); v4 endpoint returns `[]`.

Notes:

- Use immutable source links where possible (release tag or commit SHA).
- Record checksum after download and before commit.
- Update this table whenever sources are refreshed.
