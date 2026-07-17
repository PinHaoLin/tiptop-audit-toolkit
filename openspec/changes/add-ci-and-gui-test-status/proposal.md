# Add CI And Quality Verification

## Why
The audit tool is used in a production-like weekly MIS workflow, but quality checks were implicit. Contributors need a repeatable verification path while operators keep the main GUI focused on the audit workflow.

## What Changes
- Add frontend smoke tests and a `verify` script.
- Add backend unittest coverage for filename-to-Excel matching logic.
- Add GitHub Actions CI for frontend and backend checks.
- Add GitHub issue and pull request templates.
- Add OpenSpec documentation for the quality-assurance behavior.

## Impact
- No production DataCenter paths are changed.
- No backend network-copy behavior is changed.
- Maintainers gain CI feedback and a clearer PR checklist.
