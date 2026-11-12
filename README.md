# DRAPE: A simple heuristic metric for measuring detection performance
<p align="center"><img src=logo_small.png></p>

**DRAPE** stands for **D**etection **R**eliability **A**nd **P**recision **E**fficiency which is basically a unified index (score) that quantifies:

- **Reliability**: Are the detections actually finding true attacks? (TP)
- **Precision Efficiency**: Are they doing so with minimal noise? (FP)

The algorithm outputs a simple heuristic metric to score detection performance using TP/FP counts. The index score can be either negative or positive with the extremes implying the following characteristics:

- Negative = noisy, unreliable detection.
- Positive = precise, efficient, valuable detection.

The index is a composite measure of the individual TP/FP data points which can be used to measure detection/rule performance over time.

It reveals whether a rule is _signal-dominant_ (+) or _noise-dominant_ (–) by inspecting the number of its TP and FPs alerts over a period of time.

## How does it work? 
The formula rewards rules that spots a decent amount of threats (TP) with good precision, while penalizing noisy rules, especially those that haven't yet "proven" themselves with enough TPs.

The formula captures the real-world tradeoff between TP and FP figures better than precision or simple raw counts. Most single-number metrics are either:

- too forgiving of noise (TP-heavy rules look great even when they're a FP factory), or
- too punishing (precision destroys high-value, high-volume rules).

DRAPE models that tradeoff how detection engineers think in practice:

- High TP → good
- High precision → better
- Extremely noisy rules → bad
- Slight noise on high-value rules → acceptable

This mirrors actual triage experience so I encourage you to try it out.

## Inputs and weights (v1.1)

| Input | Meaning |
|---|---|
| `TP` | True positives: alerts confirmed as real threats. |
| `FP` | False positives: alerts confirmed as not a threat. |
| `IC` | Inconclusive alerts (optional, new in v1.1): alerts that got no clear verdict, such as a benign or neutral outcome, or alerts closed with no disposition. |

| Weight | Default | Meaning |
|---|---|---|
| `k` | 0.20 | FP penalty: how much false positives pull the score down. |
| `w` | 0.38 | Precision reward: how much a rule gains for being right most of the time. |
| `a` | 0.5 | Inconclusive alert cost (new in v1.1): each inconclusive alert counts as this share of one false positive. `a=0` ignores them, as v1.0 does. |

The formula, with `EFP = FP + a × IC` (effective false positives):

```
precision = TP / (TP + EFP)
score     = 10 × [ log10(TP + 1) × (1 + w × precision) − k × log10(EFP + 1) / (log10(TP + 1) + 1) ]
```

The score is rounded to 2 decimals. When there is nothing to score (`TP + EFP = 0`), it returns an empty value.

### Why inconclusive alerts? (v1.1)
A new rule that raises 100 alerts in its first week, none of them with a clear verdict, still costs analysts time without proving anything. In v1.0 it had no score at all, so it sat with the rules that never fired. In v1.1 it scores **-3.42**, among the rules that need attention: worse than 10 false positives (-2.08), but not as bad as 100 confirmed false positives (-4.01). Rules that catch threats barely move.

Without inconclusive alerts (`IC=0`, the default), v1.1 returns exactly the v1.0 score.

## Implementations
- Python: [drapeindex.py](drapeindex.py)
- Splunk (SPL): [drapeindex.spl](/drapeindex.spl)

### Output Sample (v1.1)
<p align="center"><img src=drapev1.1_output.svg></p>

### Output Sample (v1.0)
<p align="center"><img src=drapev1_output.png></p>

## Changes
See [CHANGELOG.md](CHANGELOG.md).

## More details
Intro blog post on Detect.FYI website: [https://detect.fyi/introducing-the-drape-index-how-to-measure-in-success-in-a-threat-detection-practice-154fd977f731](https://detect.fyi/introducing-the-drape-index-how-to-measure-in-success-in-a-threat-detection-practice-154fd977f731)
