# Architecture Audit Report - ecommerce-api-legacy

## Phase 1 - Project Analysis

- Language: JavaScript
- Framework: Express 4.18.2
- Dependencies: express, sqlite3
- Database: SQLite in-memory via `sqlite3`
- Domain: LMS checkout API with users, courses, enrollments, payments, and admin reports
- Architecture: Single AppManager class owns database setup, routes, checkout, payment, reporting, and deletion
- Source files analyzed: 3
- Entry point: `src/app.js`

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 3 |
| HIGH | 4 |
| MEDIUM | 3 |
| LOW | 2 |

## Findings

### 1. [CRITICAL] Hardcoded Production-Like Credentials

- File: `src/utils.js:1-6`
- Description: Database credentials, SMTP user, and payment gateway key are committed in source.
- Impact: Secrets can leak and be reused outside local development.
- Recommendation: Move values to environment-backed config with safe defaults.

### 2. [CRITICAL] Insecure Custom Password Hashing

- File: `src/utils.js:17-22`, `src/AppManager.js:66-72`
- Description: Passwords are transformed with repeated base64 truncation.
- Impact: Stored passwords are trivial to recover or brute force.
- Recommendation: Use Node `crypto.scrypt`/`pbkdf2` or a maintained password hashing library.

### 3. [CRITICAL] Card And Gateway Key Logged

- File: `src/AppManager.js:43-46`
- Description: Checkout logs the full card number and gateway key.
- Impact: Sensitive payment data is exposed in logs.
- Recommendation: Never log full card data or secrets; log only masked operational metadata.

### 4. [HIGH] God Class Owns The Entire Application

- File: `src/AppManager.js:4-138`
- Description: One class creates schema, seeds data, registers routes, handles checkout, runs reports, and deletes users.
- Impact: Responsibilities are tightly coupled and difficult to validate.
- Recommendation: Split into config, database, models, controllers, routes, services, and middleware.

### 5. [HIGH] Checkout Route Contains Business And Persistence Flow

- File: `src/AppManager.js:28-78`
- Description: Route handler validates input, creates users, processes payment, enrolls, records payment, audits, and mutates cache.
- Impact: Error handling and transaction boundaries are fragile.
- Recommendation: Move orchestration to a controller and domain logic to services/models.

### 6. [HIGH] Admin Financial Report Has No Access Control

- File: `src/AppManager.js:80-129`
- Description: Administrative revenue and student report is publicly exposed.
- Impact: Sensitive business data is available to any client.
- Recommendation: Add authorization or remove from public examples.

### 7. [HIGH] User Delete Leaves Orphaned Data

- File: `src/AppManager.js:131-136`
- Description: Deleting a user intentionally leaves enrollments and payments behind.
- Impact: Data integrity is broken.
- Recommendation: Use foreign keys, cascading cleanup, or explicit transactional deletion.

### 8. [MEDIUM] N+1 Query Pattern In Financial Report

- File: `src/AppManager.js:89-127`
- Description: Each course triggers enrollment queries, then each enrollment triggers user and payment queries.
- Impact: Report latency grows quickly with data volume.
- Recommendation: Use joined aggregate queries.

### 9. [MEDIUM] Missing Centralized Error Handling

- File: `src/AppManager.js:37-77`, `src/AppManager.js:83-128`
- Description: Errors are handled inline with plain text messages and some callback errors are ignored.
- Impact: Responses are inconsistent and failures can be hidden.
- Recommendation: Add async wrappers and Express error middleware.

### 10. [MEDIUM] Global Mutable Cache

- File: `src/utils.js:9-15`
- Description: Shared mutable cache is exported globally without lifecycle or invalidation.
- Impact: State leaks across requests and tests.
- Recommendation: Encapsulate cache behavior in a service or remove it.

### 11. [LOW] Poor Request Field Names

- File: `src/AppManager.js:29-33`
- Description: Inputs use short names such as `usr`, `eml`, `pwd`, `c_id`, and `cc`.
- Impact: Handler intent is harder to understand.
- Recommendation: Normalize request fields in a controller while preserving backward compatibility.

### 12. [LOW] Unused Export

- File: `src/utils.js:10`, `src/utils.js:25`
- Description: `totalRevenue` is exported but not used.
- Impact: Dead state obscures real application behavior.
- Recommendation: Remove unused global state.

## Deprecated API Detection

No framework-deprecated API usage was detected in this project.

## Phase 2 Confirmation

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]  
Confirmation recorded: y - user requested full README execution on 2026-06-12.
