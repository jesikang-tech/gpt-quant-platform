# NAVER License and Provenance Evidence Checklist

Status: EVIDENCE_PREPARATION_ONLY
Real-data collection: DENIED
Real-data persistence: DENIED
Operational database access and PRICE/OHLCV rebuild: DENIED
No automatic gate enablement is permitted.

## Purpose and interpretation

This document records evidence requirements; it does not state current NAVER
license terms, grant permission, authorize collection, or enable any code path.
All evidence items start PENDING. No official permission is asserted here.

- Inquiry submission is not authorization.
- Hash verification is not source authentication.
- Licensing permission is not operational DB approval.
- Current real-data collection and persistence remain DENIED.
- No automatic gate enablement is permitted, even if checklist items are VERIFIED.

VERIFIED means the specific documented evidence and scope were independently
reviewed; it never means runtime authorization. PENDING means evidence is absent,
incomplete, or awaiting review. REJECTED means the proposed scope or evidence was
refused, contradicted, expired, revoked, or failed verification. Preserve reasons
and history; do not overwrite an adverse decision with a caller assertion.

## Partnership inquiry record

| Field | Recorded value |
|---|---|
| Submitted | 2026-10-25 |
| Registration | 2026-16110-080421 |
| Status | RESPONSE_PENDING |
| Record basis | User-supplied inquiry metadata; no external verification performed |
| Permission granted | None established |

A submission receipt, acknowledgement, or absence of a response is not permission.
Record an official response as a separate evidence artifact and assess its exact
scope; do not treat a general partnership reply as a blanket data license.

## Implemented safeguards and reusable contracts

| Existing contract | Reusable capability | Does not establish |
|---|---|---|
| [Shared provenance gate](../core/price_provenance_gate.py) | Fail-closed assessment and analysis/persistence enforcement; no current successful authorization path | License rights or real-data approval |
| [NAVER persistence entry](../core/naver_persistence_entry.py) | Shared gate before persistence adapter invocation | An authorized operational adapter |
| [Source evidence](core/naver_source_evidence.py) | Provider claims, acquisition context, observation identity, evidence references, and contradiction checks | Independent authenticity; its decisions remain blocked |
| [Trust anchor](core/naver_trust_anchor.py) | Separates independent trust configuration from caller claims | A verified anchor; successful verification is currently unsupported |
| [Offline evidence verifier](real_evidence_verifier.py) | Integrity, parsing, classification, and consistency checks for explicitly supplied files | Source authentication, licensing, or persistence authority |
| [Rebuild preflight](price_rebuild_preflight.py) | Counts candidate rows without writes | Real-data rebuild approval; outputs remain UNVERIFIED |
| [Persistence safety contract](NAVER_PERSISTENCE_SAFETY_CONTRACT.md) | Mandatory prerequisites and separate operational approval requirement | Current permission to collect or write |

The persistence safety document remains **DRAFT / PARTIAL / DENIED**.
Its legacy collection, repository writer, backfill, and direct FDR
descriptions were reconciled with the inspected shared provenance gates.
The current checks do not establish exhaustive runtime-path protection,
source authentication, licensing rights, or operational authorization.
All existing denial boundaries remain in force.

## Evidence records

Create one record per independently scoped artifact or permission. Copy the
record fields within the relevant section when several documents are required.
All fields below are mandatory: unknown values remain explicitly PENDING, never
implicitly approved. An explicit prohibition can be verified as a fact while
the requested use remains REJECTED.

### E1. Authorized access and acquisition method

Required evidence: Obtain an official agreement or response identifying the authorized entity, NAVER service and dataset, instruments, endpoints or delivery channel, authentication method, geographic scope, access limits, and effective period. Confirm the issuer can grant the stated rights, including any upstream rights conditions.

| Record field | Current value |
|---|---|
| Evidence item ID | E1 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E2. Automated collection and local storage

Required evidence: Obtain explicit permission covering automated retrieval, OHLCV fields, collection frequency and volume, historical downloads, raw responses, local files and database storage, internal analysis, security requirements, and permitted environments. Public availability or a working endpoint is not permission.

| Record field | Current value |
|---|---|
| Evidence item ID | E2 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E3. Historical retention and deletion obligations

Required evidence: Confirm permitted historical depth, retention periods for raw and normalized observations, caches and backups, correction handling, deletion deadlines, and obligations following expiration, termination, or revocation. Record how deletion and backup expiry will be demonstrated.

| Record field | Current value |
|---|---|
| Evidence item ID | E3 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E4. Adjusted/unadjusted OHLCV semantics

Required evidence: Obtain authoritative definitions for adjusted versus unadjusted Open/High/Low/Close and Volume, corporate actions, adjustment factors and effective dates, units, rounding, trading-session dates, missing/special rows, corrections, and historical revisions. Separately review the internal normalization policy; do not infer semantics from numerical agreement.

| Record field | Current value |
|---|---|
| Evidence item ID | E4 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E5. Redistribution and commercial use

Required evidence: Resolve internal versus external use, dashboard display, client access, raw-data redistribution, derived outputs, commercial services, attribution, fees, sublicensing, and third-party access. Record explicit prohibitions as restrictions; do not infer commercial or redistribution rights from access permission.

| Record field | Current value |
|---|---|
| Evidence item ID | E5 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E6. Independent source authentication

Required evidence: Define and independently validate the approved acquisition channel, issuer identity and authority, trust-anchor origin, verification procedure, and binding between source evidence and each acquisition. Provider labels, URLs, caller booleans, and self-declared issuer names cannot establish authenticity.

| Record field | Current value |
|---|---|
| Evidence item ID | E6 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E7. Observation integrity and reproducibility

Required evidence: After access is separately authorized, define an authorized evidence manifest containing acquisition method/time, source reference, ticker/date/field identities, raw byte count and SHA-256, parser/schema version, adjustment evidence, classification counts, and PRICE/OHLCV consistency results. Plan reproducible offline checks and anomaly disposition without collecting data under this checklist.

| Record field | Current value |
|---|---|
| Evidence item ID | E7 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

### E8. Separate operational approval

Required evidence: Require explicit internal approval for the exact operational database, adapter, tables, instruments, date range, read/write operations, execution window, and responsible operator. Require a reviewed implementation enforcing authorization before connection/write, isolated atomicity and rollback validation, regression results, and a reviewed rebuild plan. Licensing evidence alone cannot grant this approval.

| Record field | Current value |
|---|---|
| Evidence item ID | E8 |
| Issuer | PENDING - not independently established |
| Document reference/version | PENDING - attach exact artifact reference and version |
| Issue date | PENDING |
| Effective date(s) | PENDING |
| Exact permission scope | PENDING - no permission established; record exact grant and applicable clauses |
| Restrictions | PENDING - record limits and explicit prohibitions |
| Expiration or revocation conditions | PENDING - include notification and suspension obligations |
| Independent verification method | PENDING - identify trusted channel, procedure, reviewer, and review date |
| Status | PENDING |
| Decision rationale / supporting references | PENDING |

## Official response dependencies and internal work

E1-E3 and E5 depend on an official grant or applicable terms whose authority,
version, and applicability have been independently established. E4 requires
authoritative source semantics; any adjustment policy not resolved by the reply
requires follow-up. E6 depends on the approved source channel and an independent
verification method, not simply possession of an email or a hash.

E7 validation design and E8 approval planning can proceed without collecting
actual prices. Actual acquisition, sample inspection, persistence, and rebuild
must wait for the permissions and separate approvals applicable to each action.
The submitted inquiry does not satisfy any evidence item by itself.

## Review sequence before any proposal to enable real-data writes

1. Authenticate the official response/agreement and retain its exact reference,
   version, dates, clauses, and independently checked issuer authority.
2. Complete E1-E6 for the intended use. Resolve omissions, contradictions, expiry,
   and upstream rights; unsupported uses remain denied.
3. Obtain separate permission for any evidence acquisition, then complete E7
   using only that permitted scope. Integrity checks cannot substitute for E6.
4. Reconcile the draft safety contract and obtain the separate E8 approval,
   including isolated adapter, atomicity, rebuild, and rollback validation.
5. Submit a separate explicit implementation and authorization review. The
   existing gate remains unchanged; no checklist status, license artifact,
   environment flag, or caller-provided value may automatically enable writes.

## Current readiness decision

Evidence preparation may proceed. Real-data access/collection, persistence,
rebuild, and operational DB access remain DENIED. Licensing scope, authoritative
adjustment semantics, independent authentication, observation evidence, and
operational approval remain pending. No price data was collected or modified to
prepare this checklist.
