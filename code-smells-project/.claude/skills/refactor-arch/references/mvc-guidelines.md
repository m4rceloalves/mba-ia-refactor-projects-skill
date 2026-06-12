# MVC Architecture Guidelines

## Target Responsibilities

- `config/`: read environment variables, define defaults, expose safe settings. Never hardcode real secrets.
- `models/`: define entities and persistence/repository functions. No HTTP request/response objects.
- `views/` or `routes/`: map URLs and HTTP verbs to controllers. Keep handlers thin.
- `controllers/`: parse request input, call services, select status codes, return serialized responses.
- `services/`: hold domain rules, calculations, validation, notifications, payment decisions, and report aggregation.
- `middlewares/`: centralize error responses and not-found handlers.
- Entry point: create and configure the app, initialize DB, register routes/middleware, and start the server.

## Refactoring Rules

- Preserve existing public endpoints and response semantics where possible.
- Keep SQL parameterized; never concatenate user input into SQL.
- Move secrets to environment-backed settings with safe local defaults.
- Hide password hashes and credentials from serialized API responses.
- Replace deprecated APIs with current framework-supported calls.
- Prefer small pure helpers for validation and serialization.
- Keep database initialization deterministic for local execution.

## Validation Rules

After refactoring, boot the app and call representative original endpoints. Validate list, detail, create/update where safe, reports/stats, health, and one error case.
