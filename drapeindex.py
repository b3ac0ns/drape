"""
DRAPE Index v1.1, MIT License
A simple heuristic metric to score detection performance using TP/FP counts.
Authors: Alex Teixeira, 2025 (initial release), 2026 (v1.1)

v1.1 adds an optional third input, inconclusive alerts (IC): alerts that got no
clear verdict, such as a benign or neutral outcome, or alerts closed with no
disposition. Each one counts as a fraction "a" of a false positive. With IC=0
(the default) the score is exactly the v1.0 score.

For more info: https://github.com/inodee/drape

"""

import math

def drape_index(tp, fp, ic=0, k=0.20, w=0.38, a=0.5, empty_value=None):

    """
    Parameters
    ----------
    tp, fp : int
        True positives and false positives counts
    ic : int
        Inconclusive alerts count (no clear verdict). Optional, default 0.
    k : float
        FP penalty weight
    w : float
        Precision reward weight
    a : float
        Inconclusive alert cost, as a share of one false positive (0 to 1).
        a=0 ignores inconclusive alerts, as v1.0 does.
    empty_value : any
        What to return when there is nothing to score (tp + fp + a*ic == 0)

    Returns
    -------
    (score * 10) rounded to 2 decimals, or empty_value

    """

    # Inconclusive alerts count as a fraction of a false positive
    efp = fp + a * ic

    # Empty value treatment
    if tp + efp == 0:
        return empty_value

    # Precision term
    precision = tp / (tp + efp)

    # Avoid exceptions from log10
    tlog = math.log10(tp + 1.0)
    flog = math.log10(efp + 1.0)

    # Calculate score
    score = (tlog * (1.0 + w * precision)) - ((k * flog) / (tlog + 1.0))

    # Round after multiplying by 10
    return round(score * 10.0, 2)

# A few tests (same as v1.0: no inconclusive alerts, same results)
print(drape_index(0, 10, empty_value="-"))
print(drape_index(1, 10, empty_value="-"))
print(drape_index(5, 10, empty_value="-"))
print(drape_index(10, 1, empty_value="-"))
print(drape_index(50, 10, empty_value="-"))
print(drape_index(100, 100, empty_value="-"))
print(drape_index(1000, 100, empty_value="-"))
print(drape_index(0, 150, empty_value="-"))
print(drape_index(100, 0, empty_value="-"))

# The "Zero Line"
print(drape_index(1, 90, empty_value="-"))
print(drape_index(1, 100, empty_value="-"))
print(drape_index(1, 105, empty_value="-"))

# New in v1.1: inconclusive alerts (IC)
print(drape_index(0, 0, empty_value="-"))           # nothing to score
print(drape_index(0, 0, ic=10, empty_value="-"))    # only inconclusive alerts
print(drape_index(0, 0, ic=100, empty_value="-"))
print(drape_index(0, 0, ic=1000, empty_value="-"))
print(drape_index(60, 30, ic=10, empty_value="-"))  # mixed rule
print(drape_index(60, 30, ic=10, a=0, empty_value="-"))  # a=0 gives the v1.0 score
