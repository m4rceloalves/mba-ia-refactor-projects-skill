# Anti-Pattern Catalog

Use these severities unless local impact clearly changes the risk.

## CRITICAL

1. **Unsafe dynamic query execution**: endpoint accepts SQL or builds arbitrary SQL from user input. Detect `cursor.execute(query)`, string-concatenated SQL, admin query endpoints.
2. **Hardcoded sensitive credentials**: secrets, SMTP passwords, gateway keys, DB passwords, or Flask `SECRET_KEY` committed in source.
3. **Weak password storage or crypto**: plaintext passwords, MD5/SHA1 for passwords, reversible/base64 "hashing", or custom crypto.

## HIGH

4. **God class/module/controller**: one file or class owns routing, persistence, business rules, validation, integrations, and bootstrapping.
5. **Business logic inside routes**: long HTTP handlers perform validation, calculations, persistence, notifications, and response assembly directly.
6. **Sensitive data exposure**: API responses expose password hashes, secret keys, DB paths, card numbers, or internal exception details.

## MEDIUM

7. **N+1 query or callback cascade**: loop performs extra queries per row or nested callbacks hide flow and error paths.
8. **Duplicated validation and serialization**: same status, priority, field-length, or DTO logic appears in multiple handlers.
9. **Missing centralized error handling**: repeated `try/except` or `try/catch`, bare catches, raw stack/error messages, inconsistent status codes.
10. **Deprecated or legacy API usage**: framework APIs marked legacy, such as SQLAlchemy `Query.get()` in SQLAlchemy 2.x; replace with modern equivalents like `db.session.get(Model, id)`.

## LOW

11. **Poor naming and magic values**: unclear names (`u`, `p`, `cid`), literal statuses, roles, ports, lengths, and thresholds spread through code.
12. **Unused imports or dead state**: imports not used, global cache/revenue counters without lifecycle, stale helper functions.
