# Architecture Audit Report - task-manager-api

## Phase 1 - Project Analysis

- Language: Python
- Framework: Flask 3.0.0 with Flask-SQLAlchemy 3.1.1
- Dependencies: flask, flask-sqlalchemy, flask-cors, marshmallow, requests, python-dotenv
- Database: SQLite via SQLAlchemy
- Domain: Task Manager API with users, tasks, categories, reports, and login
- Architecture: Partial layering with models/routes/services/utils, but routes still contain business logic
- Source files analyzed: 13
- Entry point: `app.py`

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 3 |
| HIGH | 3 |
| MEDIUM | 4 |
| LOW | 2 |

## Findings

### 1. [CRITICAL] Hardcoded Secrets And SMTP Credentials

- File: `app.py:11-13`, `services/notification_service.py:7-10`
- Description: Flask secret key, SMTP user, and SMTP password are committed in source.
- Impact: Runtime secrets can leak and be reused.
- Recommendation: Move all secrets to environment-backed configuration.

### 2. [CRITICAL] MD5 Password Hashing

- File: `models/user.py:27-32`
- Description: Passwords are stored and checked with MD5.
- Impact: MD5 is fast and unsuitable for password storage.
- Recommendation: Use `werkzeug.security.generate_password_hash` and `check_password_hash`.

### 3. [CRITICAL] Password Hash Exposed In API Responses

- File: `models/user.py:16-25`, `routes/user_routes.py:207-210`
- Description: `User.to_dict()` includes `password`, and login returns that dictionary.
- Impact: Password hashes leak to API clients.
- Recommendation: Exclude password from serializers and use a separate internal auth path.

### 4. [HIGH] Business Logic Concentrated In Routes

- File: `routes/task_routes.py:85-223`, `routes/user_routes.py:42-132`
- Description: HTTP handlers perform validation, lookup, persistence, serialization, logging, and status decisions.
- Impact: Logic is hard to test and duplicate across endpoints.
- Recommendation: Move orchestration to controllers and rules to services.

### 5. [HIGH] Report Route Mixes Aggregation And Persistence

- File: `routes/report_routes.py:12-101`, `routes/report_routes.py:103-155`
- Description: Report endpoints run many queries and compute metrics directly in route handlers.
- Impact: Reporting logic is coupled to Flask and hard to optimize.
- Recommendation: Move report generation into a report service.

### 6. [HIGH] Fake Authentication Token

- File: `routes/user_routes.py:207-210`
- Description: Login returns a predictable string token based only on user id.
- Impact: Clients may treat a non-secure token as authentication.
- Recommendation: Generate opaque dev tokens or implement real signed tokens.

### 7. [MEDIUM] Deprecated SQLAlchemy Query.get API

- File: `routes/task_routes.py:42`, `routes/task_routes.py:51`, `routes/task_routes.py:67`, `routes/task_routes.py:117`, `routes/task_routes.py:122`, `routes/user_routes.py:29`, `routes/user_routes.py:94`
- Description: SQLAlchemy 2.x marks `Query.get()` as legacy.
- Impact: Future SQLAlchemy upgrades may break or warn.
- Recommendation: Use `db.session.get(Model, id)`.

### 8. [MEDIUM] N+1 Queries In Listing And Reports

- File: `routes/task_routes.py:14-59`, `routes/report_routes.py:53-68`, `routes/report_routes.py:157-165`
- Description: Loops perform extra user/category/task queries per row.
- Impact: Response time grows with table size.
- Recommendation: Use relationships, eager loading, joins, or grouped counts.

### 9. [MEDIUM] Duplicated Overdue And Validation Rules

- File: `routes/task_routes.py:30-39`, `routes/task_routes.py:71-80`, `routes/user_routes.py:171-180`, `utils/helpers.py:57-108`
- Description: Overdue, status, priority, date, and tag logic appears in multiple places.
- Impact: Behavior can drift across endpoints.
- Recommendation: Centralize rules in services/helpers and reuse model methods.

### 10. [MEDIUM] Missing Centralized Error Handling

- File: `routes/task_routes.py:11-299`, `routes/report_routes.py:167-223`
- Description: Handlers mix bare catches, manual rollbacks, and direct error responses.
- Impact: Errors are inconsistent and internal failures can be hidden.
- Recommendation: Use application exceptions and registered error handlers.

### 11. [LOW] Unused Imports

- File: `app.py:7`, `routes/task_routes.py:7`, `routes/user_routes.py:6`, `utils/helpers.py:3-7`
- Description: Several imports are unused.
- Impact: Adds noise and suggests stale code.
- Recommendation: Remove unused imports during refactoring.

### 12. [LOW] Magic Values Spread Across Routes

- File: `routes/task_routes.py:110`, `routes/task_routes.py:113`, `routes/user_routes.py:64`, `utils/helpers.py:110-116`
- Description: Some constants exist in helpers, but routes duplicate literal statuses, roles, and thresholds.
- Impact: Updating business rules requires edits in multiple files.
- Recommendation: Use shared constants from one module.

## Deprecated API Detection

Deprecated API usage found: SQLAlchemy `Query.get()` should be replaced with `db.session.get(Model, id)`.

## Phase 2 Confirmation

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]  
Confirmation recorded: y - user requested full README execution on 2026-06-12.
