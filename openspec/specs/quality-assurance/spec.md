# Quality Assurance Specification

## Requirements

### Requirement: Workflow GUI Stability
The application SHALL keep the production audit workflow focused on the step progress, control panel, and execution log.

#### Scenario: User opens the audit tool
- WHEN the React application renders
- THEN the GUI SHALL display the header, step progress, control panel, and terminal log
- AND the GUI SHALL NOT add extra diagnostic panels to the main workflow unless explicitly requested.

### Requirement: CLI Verification
The project SHALL provide repeatable command-line verification for frontend and backend changes.

#### Scenario: Frontend verification runs
- WHEN `npm run verify` is executed in `frontend`
- THEN lint, smoke tests, and production build SHALL run in sequence.

#### Scenario: Backend tests run
- WHEN `python -m unittest discover -s tests -v` is executed in `backend`
- THEN pure backend logic tests SHALL run without requiring DataCenter network access.

### Requirement: GitHub Continuous Integration
The repository SHALL define GitHub Actions checks for pull requests and pushes.

#### Scenario: Pull request is opened
- WHEN a pull request targets `main` or `master`
- THEN GitHub Actions SHALL verify the frontend and backend test suites.

### Requirement: Operational Safeguards
The quality workflow SHALL protect production audit behavior.

#### Scenario: A contributor changes audit behavior
- WHEN a pull request is prepared
- THEN the PR checklist SHALL require verification of DataCenter path safety, manual checkpoints, and Chinese filename handling.
