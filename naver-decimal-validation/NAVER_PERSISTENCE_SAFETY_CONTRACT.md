# NAVER Persistence Safety Contract

Status: DRAFT
Verification: PARTIAL
Operational authorization: DENIED

## 1. Scope

This contract governs any future connection between NAVER price
observations and operational PRICE/OHLCV persistence.

It does not authorize operational database access.

## 2. Current verified boundary

- NAVER analysis entry is fail-closed for unverified provenance.
- NAVER persistence entry is fail-closed before adapter invocation.
- Raw NAVER observations do not carry persistence authorization.
- Isolated CI validates the current entry contracts.
- Static bypass tests inspect specified tracked NAVER modules.

These checks do not prove that every possible runtime storage
path is protected.

## 3. Mandatory conditions before persistence

All of the following require independent verification:

1. Official NAVER data usage rights are confirmed.
2. Provider identity and source provenance are verified.
3. Adjustment status and price normalization policy are approved.
4. Source file integrity and observation consistency are verified.
5. PRICE and OHLCV consistency rules are satisfied.
6. An isolated rebuild and rollback plan is verified.
7. The actual persistence adapter enforces authorization before
   any database connection or write.
8. Operational database access receives separate explicit approval.

A caller-provided boolean or forged approval object cannot
substitute for independent evidence.

## 4. Existing storage routes

Legacy collection and backfill routes must be assessed against
their current fail-closed provenance enforcement. In particular,
the tracked OHLCV backfill implementation calls the shared
provenance assessment before its protected processing paths.

The full behavior of all legacy FDR routes has not been
established by this document review.

No existing route authorizes unverified NAVER observations,
and no NAVER-to-operational-repository connection is approved.

## 5. Required future integration tests

Before operational integration, verify:

- Unverified NAVER observations cannot invoke repository writes.
- Invalid or forged evidence cannot grant persistence authority.
- Failure occurs before opening a database connection.
- Both PRICE and OHLCV paths reject unauthorized input.
- Partial write failures cannot leave inconsistent price pairs.
- Current legacy collection and backfill provenance enforcement is preserved and covered by focused regressions.
- Isolated CI and full regression pass.

## 6. Current decision

NAVER operational analysis: DENIED
NAVER operational persistence: DENIED
PRICE/OHLCV rebuild: DENIED
Operational database access: DENIED

Reassessment requires verified evidence and explicit approval.
