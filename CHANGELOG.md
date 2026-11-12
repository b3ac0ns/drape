# Changelog

## v1.1 (2026)

### Added
- Optional third input `IC`, inconclusive alerts: alerts that got no clear verdict, such as a benign or neutral outcome, or alerts closed with no disposition.
- Weight `a` (default 0.5): each inconclusive alert counts as this share of one false positive (`EFP = FP + a × IC`).
- A rule with only inconclusive alerts now gets a score. For example, 100 inconclusive alerts score -3.42 instead of no score.

### Unchanged
- With `IC=0` (the default), every score is exactly the v1.0 score. Existing calls `drape_index(tp, fp)` keep their results.
- `k=0.20` and `w=0.38`.

### Fixed
- SPL: the weights now match the Python implementation (`k=0.20`, `w=0.38`). v1.0's SPL used `k=0.18` and `w=0.22`, so the two implementations gave different scores.
- SPL: the empty value. v1.0 set the score to `"-"` and then multiplied and rounded it, which turned `"-"` into an empty field. The guard now runs last.
- SPL: the weights are plain numbers. v1.0 built them with `printf`, which returns text.

## v1.0 (2025)
- Initial release: Python and SPL implementations, TP and FP inputs, weights `k` and `w`.
