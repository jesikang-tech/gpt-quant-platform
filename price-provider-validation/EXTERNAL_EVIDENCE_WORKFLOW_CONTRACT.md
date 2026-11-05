# External Price Evidence Workflow Contract

Status: DESIGN_ONLY / EXTERNAL_CERTIFICATION_PENDING
Scope: KIWOOM Ver1.1; reusable provider-neutral evidence workflow
Related Q&A: KIWOOM 7961, 8123, 8180

## 1. Purpose

Coordinate external evidence records and existing offline assessments.
Do not duplicate verification engines or grant operational authority.

## 2. Evidence record fields

- evidence_id
- provider
- api_id
- evidence_category
- source_reference
- original_artifact_location
- content_sha256
- acquisition_or_publication_timestamp
- observation_identity, where applicable
- independent_authenticity_status
- review_status
- missing_requirements
- related_official_inquiry
- verification_notes

An unavailable field must remain explicitly UNKNOWN or PENDING.
A recorded digest establishes byte integrity only, not provider origin.

## 3. Reusable assessment modules

- provider_evidence.py
- provider_acquisition_evidence.py
- kiwoom_adjustment_binding.py
- provider_corporate_action_evidence.py
- trading_day_certification.py
- provider_quality_integration.py
- provider_platform_integration.py
- provider_license_purpose.py
- provider_certification_acceptance.py
- provider_execution_authorization.py

Existing interfaces remain authoritative for offline assessment.
No replacement implementation is authorized by this document.

## 4. Certification requirement mapping

- source_evidence_present
- raw_binding_present
- adjustment_evidence_present
- calendar_evidence_present
- quality_evidence_present
- licensing_evidence_present

Requirement presence is not independent verification.
All six declared flags being true must not authorize execution.

## 5. Current KIWOOM evidence state

Q&A 7961: official reply observed; independent authenticity unverified.
Q&A 8123: PDF SHA256 baseline preserved; full-text review pending.
Q&A 8180: registration observed 2026-11-05 10:33; reply pending.

Original market-data response provenance: UNVERIFIED.
Corporate-action and adjustment certification: PENDING.
Official trading-day certification: PENDING.
Specific analysis and backtest authorization: UNVERIFIED.

## 6. Safety invariants

- HOST_PYTHON_EXECUTION: DENIED
- OPERATING_DB_ACCESS: PROHIBITED
- REAL_API_CALLS: DENIED
- BROKER_CALLS: DENIED
- PRICE_ANALYSIS_AND_PERSISTENCE: DENIED
- MAIN_MERGE: NOT_AUTHORIZED

No external evidence record may elevate these permissions.

## 7. Future workflow

1. Register an evidence artifact without treating it as authentic.
2. Preserve its identity and integrity metadata.
3. Review independent provider provenance and policy scope.
4. Reuse existing offline assessment modules.
5. Report missing certification requirements.
6. Preserve DENIED decisions and audit the evidence handoff.
7. Require separate approval before any operational integration.

Do not add a coordinator module until a concrete reuse need
is demonstrated and independently tested.
