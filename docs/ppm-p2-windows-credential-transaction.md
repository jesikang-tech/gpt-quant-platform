# PPM P2 Windows Credential Transaction Contract

Status: DESIGN_ONLY / EXECUTION_DENIED

## Scope

This contract defines the intended Windows credential-state
transaction boundary. It does not authorize credential file I/O.

## Existing reusable modules

- auth_attempts.py: pure authentication attempt and lockout policy
- credential_record.py: canonical credential record and revision candidate
- storage_policy.py: declarative storage preconditions
- windows_credential_store.py: Windows location, handle, ACL and identity inspection
- windows_storage_boundary.py: fail-closed execution assessments

## Required transaction order

1. Validate Windows credential-store location and trusted parent.
2. Establish trusted ownership, ACL, path and handle identity.
3. Acquire an OS-enforced exclusive lock before mutable state access.
4. Re-read and validate the current record while holding that lock.
5. Verify the expected revision and trusted file identity.
6. Evaluate authentication and attempt state using existing pure policies.
7. Prepare the next credential record with incremented revision.
8. Create a protected temporary file in the trusted destination.
9. Validate temporary-file security and write the canonical record.
10. Perform a verified atomic replacement with defined durability guarantees.
11. Verify the resulting record and identity before confirming success.
12. Release resources safely without granting execution on failure.

## Fail-closed invariants

- A verified password alone is not protected-operation authority.
- Declared security flags alone are never storage authority.
- A candidate revision transition alone is never persistence authority.
- No successful protected operation may be reported before required
  credential-state persistence and security checks succeed.
- Invalid, corrupt or ambiguous records are denied, not silently reset.
- Revision conflict is denied; no lost update is accepted.
- Unexpected path, owner, ACL, identity or reparse-point changes deny.
- Lock acquisition failure denies.
- Temporary-file creation, write, flush, replace or verification
  failure denies and must not grant protected execution.
- Interrupted transactions require explicit safe recovery rules.
- Any rollback or replay ambiguity denies until resolved.
- No operating database or broker connection is part of this boundary.

## Pending implementation gates

P2-12: Windows location and ACL enforcement
P2-13: trusted exclusive lock
P2-14: atomic and durable replacement
P2-15: revision and TOCTOU enforcement
P2-16: authentication persistence integration
P2-17: initial enrollment and credential replacement
P2-18: failure, concurrency and adversarial verification
P2-19: Windows CI and final handoff

## Current authority

Credential file IO: DENIED
Storage execution: DENIED
Exclusive lock: NOT_ESTABLISHED
Atomic persistence: NOT_IMPLEMENTED
TOCTOU protection: NOT_ESTABLISHED
Protected operation execution: DENIED
Main merge: NOT_AUTHORIZED
