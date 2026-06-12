# Audit Report Template

Write audit reports in Markdown using this structure:

```markdown
# Architecture Audit Report - <project-name>

## Phase 1 - Project Analysis

- Language: <language/version if known>
- Framework: <framework/version if known>
- Dependencies: <key dependencies>
- Database: <database/ORM>
- Domain: <domain summary>
- Architecture: <current architecture summary>
- Source files analyzed: <count>
- Entry point: `<file>`

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | <n> |
| HIGH | <n> |
| MEDIUM | <n> |
| LOW | <n> |

## Findings

### <id>. [<SEVERITY>] <Finding Title>

- File: `<path>:<line>` or `<path>:<start>-<end>`
- Description: <what was found>
- Impact: <why this matters>
- Recommendation: <concrete fix>

## Phase 2 Confirmation

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
Confirmation recorded: <y/n/source>
```

Rules:

- Sort findings by severity: CRITICAL, HIGH, MEDIUM, LOW.
- Include at least 5 findings per project.
- Include exact file and line references.
- Include deprecated API detection when applicable; if none is found, state that no deprecated API was detected.
