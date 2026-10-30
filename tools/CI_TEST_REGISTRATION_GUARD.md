# CI Test Registration Guard

## Purpose

Prevent silent omission of test files from the explicit pytest
registration list in the isolated parallel price provider workflow.

## Scope

- Workflow: `.github/workflows/parallel-price-provider-contract.yml`
- Target job: `synthetic-contract`
- Test directory: `price-provider-validation/tests`
- Test pattern: `test_*.py` at the directory's top level
- Supported command: one single-line `python -m pytest -q` invocation
- Registered arguments: explicit `tests/test_*.py` file paths

## Checks

The guard rejects:

- Missing test registrations
- Registrations referring to nonexistent files
- Duplicate test registrations
- Unsupported pytest arguments
- Unsupported shell syntax in the matched command
- Missing required job boundaries
- Missing required workflow or test directory
- Multiple supported pytest commands in the target job

## CI Integration

The workflow contains two independent jobs:

1. `synthetic-contract`: existing provider contract tests
2. `ci-registration-guard`: synthetic guard tests and registration check

Changes to either guard source file trigger this workflow through
the configured push path filters.

## Verification Evidence

- Commit: `27fe77ba0df046f5daddde9ac5b5762e0265e84f`
- GitHub Actions run: `40991856296`
- Workflow conclusion: `success`
- `synthetic-contract`: `success`
- `ci-registration-guard`: `success`

## Limitations

This guard does not establish:

- CI coverage of all tests in the repository
- Runtime execution coverage within individual test files
- Independent certification of market data provenance
- Official trading calendar certification
- Corporate-action or adjusted-price correctness
- Authorization to access operating databases
- Authorization for production analysis, persistence or trading

The implementation is scoped to the documented workflow format.
Changes to the workflow structure require review and regression tests.

## Safety Boundaries

- No operating database access
- No live market data acquisition
- No broker dispatch
- No Windows Sandbox dependency
- No host Python execution required for office-PC verification
- Actual Python tests run in GitHub Actions

## Preserved Baseline

The previous synthetic provider baseline remains at:

`476deaa08e0fd6a6767c38f5dede9f16e9f72714`

Tag:

`price-providers-synthetic-ci-baseline-20261030`

This document does not alter that baseline.
