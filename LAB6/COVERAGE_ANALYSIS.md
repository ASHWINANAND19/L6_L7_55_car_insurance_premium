# Lab 6 — Coverage Analysis: `car_insurance_premium.py`

Tools: Python 3.14.7, pytest 9.2.0, coverage 7.17.0.

The module has 39 statements and 30 branches: 15 `if`/`elif` decisions, each with a True and a False outcome.

## 1. Code (line) coverage — `CodeCoverageTest_car_insurance_premium.py`

Commands:

```bash
coverage run -m pytest CodeCoverageTest_car_insurance_premium.py
coverage report -m
coverage run --branch -m pytest CodeCoverageTest_car_insurance_premium.py
coverage report -m
```

| Test file | Tests | Line coverage | Branches taken | Branch-mode "Cover" | Missing |
|---|---|---|---|---|---|
| `test_car_insurance_premium.py` (starter) | 2 | 18/39 = **46%** | 10/30 | 41% | 6, 8, 11, 13, 16-17, 19, 25, 27, 29, 31, 36-45 |
| `CodeCoverageTest_car_insurance_premium.py` | 15 | 39/39 = **100%** | 29/30 | 99% | `16->18` |

**Approach.** The starter tests only ran the "sedan, age 30, no claims" path and the 0-year bonus. I added one test per line in the starter's Missing column:

- `annual_premium`: an unknown car type, a driver under 18, a young driver with an anti-theft device, and a senior driver with more than 2 claims
- `no_claim_bonus`: negative years, and the 5-, 3- and 1-year tiers
- `claim_payout`: negative damage, total loss, damage within the deductible, a payout capped at the insured value, and a normal payout

**Result.** Every line runs (100% line coverage), but branch coverage still reports one missing arc: **`16->18`**.

**Why line coverage misses it.** In `annual_premium`:

```python
14    if claims_last_3_years == 0:
15        premium -= premium // 5
16    elif claims_last_3_years > 2:
17        premium = premium * 2
18    if has_anti_theft:
```

The arc `16->18` is the path where a driver has **1 or 2 claims**. Line 14 is False, line 16 is False, and control jumps straight to line 18. That path has no line of its own, so a line-coverage tool counts it as "covered" even though no test ever checks that 1–2 claims leave the premium unchanged. This is the false sense of security the handout warns about.

**Reading the report.** In branch mode, the "Cover" column combines lines and branches: (39 lines run + 29 branches taken) / (39 + 30) = 68/69 = 99%. Pure branch coverage is 29/30 = 96.7%. The report also lists the test file itself (always 100%). The row that matters is `car_insurance_premium.py`.
