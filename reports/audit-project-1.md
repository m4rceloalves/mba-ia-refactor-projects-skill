# Architecture Audit Report - code-smells-project

## Phase 1 - Project Analysis

- Language: Python
- Framework: Flask 3.1.1
- Dependencies: flask, flask-cors
- Database: SQLite via `sqlite3`
- Domain: E-commerce API for products, users, orders, login, and sales reports
- Architecture: Monolithic Flask app with root-level controllers and model/data-access module
- Source files analyzed: 4
- Entry point: `app.py`

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 4 |
| HIGH | 3 |
| MEDIUM | 3 |
| LOW | 2 |

## Findings

### 1. [CRITICAL] Arbitrary SQL Execution Endpoint

- File: `app.py:59-78`
- Description: `/admin/query` accepts raw SQL from the request body and executes it directly.
- Impact: Remote callers can read or mutate any table.
- Recommendation: Remove the endpoint or replace it with narrowly scoped administrative operations protected by authorization.

### 2. [CRITICAL] SQL Injection Through String Concatenation

- File: `models.py:28`, `models.py:47-49`, `models.py:109-110`, `models.py:289-299`
- Description: SQL statements concatenate request-controlled values.
- Impact: Attackers can alter queries and bypass intended filters.
- Recommendation: Use parameterized SQL for every user-supplied value.

### 3. [CRITICAL] Hardcoded Secret And Debug Enabled

- File: `app.py:7-8`
- Description: Flask secret key and debug mode are committed in source.
- Impact: Sessions and error pages become unsafe in shared environments.
- Recommendation: Load configuration from environment-backed settings.

### 4. [CRITICAL] Plaintext Password Storage

- File: `database.py:75-83`, `models.py:83`, `models.py:99`, `models.py:126-128`
- Description: Seeded and newly created user passwords are stored and returned as plaintext.
- Impact: Any DB or API exposure compromises credentials.
- Recommendation: Hash passwords with a password-hashing function and hide them from responses.

### 5. [HIGH] Sensitive Configuration Exposed In Health Check

- File: `controllers.py:264-290`
- Description: `/health` returns `secret_key`, `db_path`, and debug state.
- Impact: Operational details and secrets leak to clients.
- Recommendation: Return only status and safe counts.

### 6. [HIGH] God Data Module

- File: `models.py:1-314`
- Description: One module mixes product, user, order, search, report, validation, and persistence logic.
- Impact: Changes are risky and hard to test in isolation.
- Recommendation: Split by domain into model/repository and service/controller layers.

### 7. [HIGH] Unsafe Administrative Reset

- File: `app.py:47-57`
- Description: `/admin/reset-db` deletes all records without authentication or environment guard.
- Impact: Any caller can wipe application data.
- Recommendation: Remove it from public routing or protect it with explicit admin controls.

### 8. [MEDIUM] N+1 Queries In Order Listing

- File: `models.py:171-201`, `models.py:203-233`
- Description: Each order performs extra item and product queries inside loops.
- Impact: Report/list endpoints slow down as order volume grows.
- Recommendation: Use joined queries or batched lookups.

### 9. [MEDIUM] Duplicated Validation In Controllers

- File: `controllers.py:24-96`
- Description: Product create/update validation repeats field and range checks.
- Impact: Validation behavior can drift between endpoints.
- Recommendation: Extract validation helpers or service-layer validators.

### 10. [MEDIUM] No Centralized Error Handling

- File: `controllers.py:5-292`
- Description: Handlers repeat broad `try/except` blocks and return raw exception strings.
- Impact: Responses are inconsistent and may leak internal details.
- Recommendation: Use application exceptions and a centralized error middleware.

### 11. [LOW] Magic Values Spread Through Code

- File: `controllers.py:52`, `controllers.py:242`, `models.py:256-262`
- Description: Categories, statuses, and discount thresholds are inline literals.
- Impact: Rules are harder to audit and update.
- Recommendation: Move constants into services or config modules.

### 12. [LOW] Unused Import

- File: `models.py:2`
- Description: `sqlite3` is imported but unused.
- Impact: Lowers readability.
- Recommendation: Remove unused imports during refactoring.

## Deprecated API Detection

No framework-deprecated API usage was detected in this project.

## Phase 2 Confirmation

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]  
Confirmation recorded: y - user requested full README execution on 2026-06-12.
