# Repository Guidelines

## Project Structure & Module Organization

This repository is an MBA refactoring-skill challenge with three apps:

- `code-smells-project/`: Python/Flask e-commerce API in `app.py`, `models.py`, `controllers.py`, and `database.py`.
- `task-manager-api/`: Python/Flask task API with layers under `models/`, `routes/`, `services/`, and `utils/`.
- `ecommerce-api-legacy/`: Node.js/Express LMS API under `src/`; request examples live in `api.http`.

Keep changes scoped to the relevant project. Generated audit outputs should follow `reports/audit-project-1.md`, `reports/audit-project-2.md`, and `reports/audit-project-3.md`. If implementing the required skill, use the selected tool convention, for example `code-smells-project/.claude/skills/refactor-arch/`.

## Build, Test, and Development Commands

Run commands from the project being changed:

- `cd code-smells-project && pip install -r requirements.txt && python app.py`: install dependencies and start the e-commerce API on `localhost:5000`.
- `cd task-manager-api && pip install -r requirements.txt && python seed.py && python app.py`: install dependencies, seed `tasks.db`, and start the task API.
- `cd ecommerce-api-legacy && npm install && npm start`: install dependencies and start the Express API on `localhost:3000`.

There is no root build command. Avoid committing generated SQLite databases, virtual environments, or dependency folders.

## Coding Style & Naming Conventions

Use idiomatic Python with 4-space indentation, snake_case modules/functions, and clear separation between routes, controllers/services, models, and database access. For JavaScript, use the existing CommonJS style, 2-space indentation, and camelCase identifiers. Prefer small functions with explicit inputs.

## Testing Guidelines

No automated test framework is configured. For changes, boot the affected API and exercise representative endpoints with `curl`, Postman, or `ecommerce-api-legacy/api.http`. When adding tests, use `pytest` for Flask projects under `tests/`; use Jest or Supertest for the Express API.

## Commit & Pull Request Guidelines

History uses Conventional Commits, for example `chore: initial commit with refactor challenge boilerplate`. Continue with prefixes such as `feat:`, `fix:`, `refactor:`, `test:`, and `docs:`.

Pull requests should name the affected project, summarize architectural changes, list validation commands, and link any related issue or assignment item. Include screenshots only when they clarify API tooling or generated reports.

## Security & Configuration Tips

Do not add real credentials, tokens, or private endpoints. Keep secrets in environment variables or local `.env` files, and document required variables without committing their values. Treat hardcoded credentials, SQL injection risks, and unsafe request validation as high-priority findings during refactoring.
