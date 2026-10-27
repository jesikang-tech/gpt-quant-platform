# Platform Verification Kit (PVK)

## Purpose

PVK is a reusable, fail-closed collection of Python verification
contracts for multiple platform projects.

The independently validated core evaluates declarations and evidence
claims. It is not a general-purpose operating-system sandbox, a
trusted execution service, or a broker-order authorization system.

## Current verification baseline

- Branch: `validation/pvk-independent-core`
- P5 commit: `fc9bb7a0d331c4bb07a776a69884a79cf471f129`
- GitHub Actions run: `40475707586`
- CI result: success
- Exact executed test count: not independently established
- Tested CI runtime: GitHub Actions Ubuntu with Python 3.14

A passing CI run verifies the included unit-test contracts. It does
not independently establish provenance, execution authenticity,
runtime isolation, database safety, or broker authorization.

## Module inventory

Core modules:

- `contracts.py`: shared declarations, results, and statuses
- `validation.py`: input and policy validation
- `engine.py`: core evaluation
- `integrity.py`: declared integrity assessment
- `trust.py`: evidence trust assessment
- `outcome.py`: outcome and capture assessment

Additional fail-closed contracts:

- `result_transport_contract.py`: memory-only result envelope checks
- `evidence_acquisition_contract.py`: acquisition design declarations
- `readonly_evidence_boundary.py`: denied-by-default access boundary
- `sqlite_source_protection.py`: SQLite-related protection declarations

The last module must not be interpreted as proof of complete SQLite
isolation or operating database protection.

## Dependencies and portability

The reviewed PVK imports use Python standard-library modules and
relative PVK imports. No third-party Python imports were observed
in the reviewed module set.

This is an import-level observation, not proof of full cross-platform
compatibility.

Keep the `pvk` directory together, including `__init__.py` and
the required internal modules. Preserve UTF-8 without BOM and LF
line endings.

Do not assume the host platform's application dependencies,
database paths, credentials, or broker integrations belong in PVK.

## Proposed reuse workflow

For Platform5, the Kiwoom PAPER order sub-platform, or a new project:

1. Identify the intended contract-only integration scope.
2. Review the destination's existing modules to avoid duplication.
3. Copy only approved PVK source and test modules into an isolated
   feature branch or dedicated validation worktree.
4. Preserve the original project's default behavior and public APIs.
5. Run destination-specific tests in a separately approved environment.
6. Verify fail-closed behavior and review the exact Git diff.
7. Approve integration explicitly before merging or enabling any
   operational functionality.

This document does not authorize copying files to another project
or running tests on an operational host.

## Safety boundaries

- No operating database access is authorized by this package.
- No real broker dispatch or live-order approval is granted.
- No actual market-data provenance is established by declarations.
- Hash consistency alone is not independent source authentication.
- Valid transport envelopes remain unverified without external proof.
- No OS isolation claim is implied by a successful unit test.
- Missing or invalid evidence must not become an implicit approval.
- Real NAVER market-data use requires separate rights and provenance
  verification before analysis, persistence, or database rebuilding.

Keep host Python execution, database access, network execution,
and broker dispatch behind separately reviewed and explicitly
approved project-specific boundaries.

## Verification

The existing workflow is:

`.github/workflows/pvk-core-validation.yml`

Its configured unit-test modules are:

- `pvk.tests.test_core`
- `pvk.tests.test_outcome`
- `pvk.tests.test_trust_boundary`
- `pvk.tests.test_result_transport_contract`

The workflow uses Python 3.14 on GitHub Actions. A passing workflow
does not prove tests outside this configured set have been executed.

## Release and migration checklist

Before adopting PVK in another project, verify:

- source-file hashes and exact Git revision
- complete required internal module dependencies
- destination import compatibility
- existing API and default-value preservation
- fail-closed behavior and no unintended permission escalation
- destination-specific regression results
- no operating database, broker, or live-service access
- explicit user approval for integration

The PVK remains a contract verification component until separate
runtime, provenance, and operational boundaries are independently
verified.
