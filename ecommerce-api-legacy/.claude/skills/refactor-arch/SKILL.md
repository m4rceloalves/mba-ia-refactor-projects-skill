---
name: refactor-arch
description: Audit and refactor backend codebases to MVC. Use when asked to analyze architecture, identify code smells or anti-patterns, generate an audit report with severities and exact file lines, or refactor Python/Flask, Node.js/Express, or similar backend projects into Models, Views/Routes, Controllers, configuration, and centralized error handling.
---

# Refactor Arch

Use this skill in three mandatory phases. Do not modify project files before Phase 2 is complete and the human confirms Phase 3.

## Phase 1 - Project Analysis

1. Read `references/project-analysis.md`.
2. Detect language, framework, dependencies, database, domain, current architecture, entry point, route files, model/data-access files, and source file count.
3. Print a concise summary with the detected stack and architectural risks.

## Phase 2 - Architecture Audit

1. Read `references/anti-pattern-catalog.md` and `references/report-template.md`.
2. Inspect source code with exact file and line references.
3. Classify each finding as `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
4. Include deprecated or legacy API usage when applicable.
5. Sort findings by severity and write the report to the requested `reports/audit-project-N.md`.
6. Stop and ask: `Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]`

## Phase 3 - MVC Refactoring

Proceed only after explicit confirmation.

1. Read `references/mvc-guidelines.md` and `references/refactoring-playbook.md`.
2. Preserve public endpoints, response shapes, package manifests, and local run commands unless the user requests otherwise.
3. Refactor toward:
   - `config/` for environment-backed settings.
   - `models/` or repositories for data access.
   - `views/` or route modules for HTTP mapping only.
   - `controllers/` for request flow.
   - `services/` for domain logic and integrations.
   - `middlewares/` for error handling.
   - A small entry point that composes the app.
4. Remove or neutralize hardcoded secrets, SQL injection risks, unsafe admin endpoints, weak hashing, duplicated validation, N+1 query patterns, and deprecated APIs.
5. Validate by booting the app and calling representative original endpoints.

## Output Requirements

Always provide:

- Phase 1 analysis summary.
- Phase 2 audit report path and severity counts.
- Phase 3 new structure.
- Validation checklist with commands and endpoint results.
