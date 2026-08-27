# BumiLu Backend

## Known Limitations / Roadmap

- **No retry/backoff on external calls** (SMTP, S3, routing service). A transient failure of an external dependency currently fails the request instead of being retried.
- **No application-level caching.** Caching for map/place lookups was handled at the gateway layer (`Traefik → Kong`), not in application code.
- **Test coverage** is currently limited to the domain and part of the application layer (`tests/unit`), plus one infrastructure integration test against a real Redis instance (`tests/integration`). E2E flows were covered manually during development, not by automated tests.
