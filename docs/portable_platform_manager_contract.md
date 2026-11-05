# Portable Platform Manager (PPM) Common Contract

Status: DESIGN_ONLY
Version: 0.1
Scope: Windows portable ZIP deployment
Execution authority: DENIED until separately verified

## 1. Purpose

PPM is a reusable deployment manager for independently developed
platforms, including GPT Quant Platform Ver1.1 and future platforms.

The common engine MUST NOT contain platform-specific trading,
analysis, market-data acquisition, or database business logic.

## 2. Platform Manifest

Each platform MUST provide a declarative manifest containing:

- platform_id
- platform_version
- package_format_version
- supported_operating_systems
- runtime_requirements
- install_directory_policy
- data_directory_policy
- log_directory_policy
- permitted_entrypoints
- execution_authority_policy
- backup_policy
- uninstall_policy

Unknown or malformed manifest fields MUST fail closed.

## 3. Package Integrity

- Package inventory and SHA256 evidence are mandatory.
- Archive extraction MUST reject absolute paths and traversal.
- Symlinks, reparse points, and unsafe path aliases MUST be denied.
- Package contents MUST NOT include credentials or tokens.
- Integrity failure MUST prevent installation.
- Hash verification alone does not establish publisher authenticity.

## 4. Installation

- Installation MUST require an explicit target directory.
- Existing user data MUST NOT be overwritten.
- Installation MUST NOT initialize or modify operating databases.
- Installation MUST NOT trigger price collection or broker calls.
- Partial installation MUST be recoverable without deleting user data.

## 5. Execution

- Installation authority and application execution authority
  MUST be separate.
- Unverified market-data collection and broker execution
  MUST remain denied.
- Entrypoints MUST be allowlisted by the platform manifest.
- Default behavior MUST NOT automatically launch applications.

## 6. Backup and Restore

- Data ownership and approved backup scope MUST be explicit.
- Operating database access is prohibited in the current phase.
- Restore MUST NOT overwrite existing data without authorization.
- Backups MUST exclude credentials unless separately protected.
- Failed restore MUST preserve the previous valid state.

## 7. Uninstallation

- Default uninstall MUST preserve user data.
- Only verified installation-owned files may be removed.
- Deletion outside approved installation boundaries is denied.
- Data deletion requires a separate explicit authorization.
- Unknown ownership or unsafe paths MUST fail closed.

## 8. Portability

- The common engine MUST remain platform independent.
- Platform-specific behavior MUST be expressed through
  manifests or minimal adapters.
- No absolute machine-specific path may be embedded
  in the common engine.
- Synthetic fixtures for multiple distinct platforms
  MUST pass before claiming portability.

## 9. Verification

- Static contract validation is required.
- Synthetic install, update, rollback, and uninstall
  tests are required.
- Cross-platform fixture tests and CI are required.
- Real deployment and operating data migration require
  separate approval and verification.

## 10. Current Safety Boundary

HOST_PYTHON_EXECUTION: DENIED
OPERATING_DB_ACCESS: PROHIBITED
REAL_API_CALLS: DENIED
BROKER_CALLS: DENIED
MAIN_MERGE: NOT_AUTHORIZED

## 11. Administrative Authentication

Status: DESIGN_ONLY

### Mandatory Authentication

- Install MUST require administrator password authentication.
- Reinstall and update MUST require authentication.
- Uninstall MUST require administrator password authentication.
- Destructive data removal MUST require separate explicit approval.
- Authentication failure MUST deny the requested operation.
- Authentication MUST occur before protected changes begin.

### Credential Security

- Plaintext passwords MUST NOT be stored in packages or source.
- Passwords MUST NOT appear in command arguments or logs.
- Password verification MUST use an established salted
  password-hashing mechanism with appropriate work factors.
- Authentication secrets MUST remain outside portable ZIP files.
- Authentication configuration MUST have protected ownership.
- Password comparison and failure handling MUST avoid
  unnecessary information disclosure.

### Initial Enrollment and Recovery

- Initial administrator enrollment MUST be separately designed.
- Initial enrollment MUST NOT allow an unauthorized user
  to claim an existing installation.
- Password recovery MUST require separately verified authority.
- No undocumented authentication bypass is permitted.

### Authorization Boundary

- Password authentication does not replace OS access controls.
- Installation and deletion MUST verify target ownership.
- Uninstall MUST preserve user data by default.
- Authentication does not authorize market-data acquisition,
  operating database access, or broker execution.
- Platform-specific authentication MUST remain independent.

### Verification Requirements

- Correct-password acceptance tests are required.
- Wrong-password and missing-password denial tests are required.
- Unauthorized install and uninstall MUST fail closed.
- Credential leakage and password reset boundary tests
  are required.
- Synthetic multi-platform authentication tests are required.
