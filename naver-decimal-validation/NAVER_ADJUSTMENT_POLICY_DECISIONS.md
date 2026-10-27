# NAVER Adjustment Policy Decisions

Scope: current pure preparation and synthetic comparison contracts only.
Official NAVER adjustment semantics: NOT ESTABLISHED.
Real-data collection, persistence, analysis, and rebuild remain DENIED.

## Status interpretation

- IMPLEMENTED: behavior is present in inspected source.
- SYNTHETICALLY_VERIFIED: covered by existing synthetic assertions; this is not
  proof of NAVER semantics. No tests were executed for this document.
- PENDING_OFFICIAL_POLICY: authoritative source definitions or approval required.
- NOT_IMPLEMENTED: no corresponding transformation or policy mechanism exists.

The focused synthetic regressions are included in NAVER Decimal Validation CI run 40472050317 (commit 639ed5b), which completed successfully. This does not establish official NAVER adjustment semantics.

## Decision table

| Item | Current decision and evidence | Status |
|---|---|---|
| ADJUSTED / UNADJUSTED declarations | Both labels are accepted by [source preparation](core/decimal_source_integration.py) and the synthetic rebuild adapter. They are caller declarations, not authenticated adjustment evidence. Existing `test_explicit_synthetic_adjustment` covers acceptance. | IMPLEMENTED / SYNTHETICALLY_VERIFIED; semantics PENDING_OFFICIAL_POLICY |
| UNKNOWN adjustment | Rejected by numeric preparation; preserved as UNKNOWN by [raw observations](core/naver_raw_observation.py) and unverified preflight. Existing pipeline, raw-observation, and preflight tests cover these distinct contracts. | IMPLEMENTED / SYNTHETICALLY_VERIFIED |
| Label validation versus transformation | Accepted labels do not alter supplied numbers. No factors, inferred basis, or automatic conversion are applied. The label-invariance regression is included in the successful isolated CI. | IMPLEMENTED validation; transformation NOT_IMPLEMENTED |
| PRICE/OHLCV identity | [Row preparation](core/naver_decimal_price_pipeline.py) shares one Decimal Close and ticker/date across both rows. Existing `test_naver_price_rows_share_exact_close` and `test_price_ohlcv_identity_and_decimal_precision` cover this. Internal identity is not independent source corroboration. | IMPLEMENTED / SYNTHETICALLY_VERIFIED |
| Provider or adjustment-basis mismatch | [Conflict classifier](core/decimal_price_conflict.py) rejects unequal provider/basis labels even if numbers match. Matching labels do not establish trust. The direct classifier regressions are included in the successful isolated CI. | IMPLEMENTED |
| Splits and reverse splits | No factor series, effective-date application, or price/volume adjustment formula. Do not infer events from price jumps. | NOT_IMPLEMENTED / PENDING_OFFICIAL_POLICY |
| Dividends | No dividend reinvestment, cash-dividend adjustment, or total-return transformation. | NOT_IMPLEMENTED / PENDING_OFFICIAL_POLICY |
| Corporate-action corrections | No correction precedence or automated repair policy. Special-row classification does not establish an event cause or permission to repair. | NOT_IMPLEMENTED / PENDING_OFFICIAL_POLICY |
| Historical revisions and versions | Conflict labels contain provider and basis only; no source-revision, factor-version, or as-of metadata. No revision merge/overwrite policy is established. | NOT_IMPLEMENTED / PENDING_OFFICIAL_POLICY |
| Decimal precision and rounding | Decimal construction preserves supplied string/int values; floats are rejected. Comparison uses exact equality. Difference subtraction uses ambient Decimal precision/rounding; no explicit quantization policy exists. The controlled-context regressions are included in the successful isolated CI. | IMPLEMENTED; official rounding PENDING_OFFICIAL_POLICY |

## Existing and new synthetic verification

Reuse these existing modules; do not introduce another adjustment engine:

- [Decimal conflict contract](core/decimal_price_conflict.py): NEW, MATCH,
  CONFLICT, evidence-label equality, and context-dependent difference.
- [Decimal source contract](core/decimal_source_integration.py): input conversion,
  label checks, OHLC range checks; higher-level trusted comparison remains denied.
- [Decimal bridge](core/decimal_synthetic_bridge.py): preserves numeric values,
  rejects unverified persistence. Numeric pairs do not retain adjustment evidence.
- [Pipeline tests](test_naver_decimal_price_pipeline.py): precision, float and
  invalid-range rejection, unknown-label rejection, paired Close identity.
- [Rebuild tests](test_price_rebuild_adapter.py): fractional values, synthetic
  declaration, accepted labels, and denial of real rebuild.

[New focused tests](test_decimal_adjustment_policy.py) add direct classifier
coverage for matching labels, NEW/MATCH/CONFLICT, provider/basis mismatches,
long operands under explicit Decimal contexts, and numeric label invariance.
They do not re-test existing UNKNOWN handling, storage, or provenance gates.
Characterizing rounded differences is not approval of that rounding policy.

## Official-response dependencies and next decision

Resolve [license checklist E4](NAVER_LICENSE_EVIDENCE_CHECKLIST.md#e4-adjustedunadjusted-ohlcv-semantics)
using authoritative field definitions: price and volume basis, corporate actions,
adjustment factors and dates, dividend treatment, units, precision/rounding,
corrections, and historical revision/version policy. The integer-only raw parser
and fraction-capable generic preparation are different input contracts; neither
proves the format of any officially authorized feed.

Do not create split/dividend formulas or revision resolution from synthetic
examples. Review an internal policy only after source semantics are established.
The [persistence safety contract](NAVER_PERSISTENCE_SAFETY_CONTRACT.md) and
[shared gate](../core/price_provenance_gate.py) remain binding denial boundaries.
Neither numeric agreement, synthetic tests, nor an adjustment label grants
provenance, licensing rights, operational approval, or automatic gate enablement.
