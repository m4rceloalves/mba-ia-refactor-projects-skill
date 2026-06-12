# Project Analysis Heuristics

## Stack Detection

- Python/Flask: `requirements.txt` contains `flask`, files import `Flask`, routes use `@app.route`, `Blueprint`, or `add_url_rule`.
- Node.js/Express: `package.json` contains `express`, source imports `express`, routes use `app.get`, `app.post`, `router`, or middleware.
- Database: detect `sqlite3`, `SQLAlchemy`, `knex`, `sequelize`, raw SQL strings, migration folders, or database files.
- Entry point: identify `app.py`, `src/app.js`, `server.js`, `main.py`, or the package `main` script.

## Architecture Mapping

Count application source files and classify each one:

- Entry/composition: app creation, middleware, route registration, server start.
- Views/Routes: HTTP verb/path mapping and request/response serialization.
- Controllers: request orchestration, status decisions, calls to services.
- Services: domain rules, integrations, calculations, notifications.
- Models/Repositories: entities, queries, persistence, schema setup.
- Config: environment variables, ports, database URLs, secrets.

## Domain Detection

Infer domain from route names, table names, models, seed data, README, and endpoint examples. Report the domain plainly, such as "E-commerce API", "LMS checkout API", or "Task Manager API".

## Risk Signals

Flag monolithic files, mixed responsibilities, inline SQL, hardcoded secrets, global mutable state, weak crypto, route handlers longer than 40 lines, repeated validation, raw exception responses, and APIs marked deprecated by the framework.
