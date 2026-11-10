# Ties at equal keys are spec decisions, not implementation details

When two events carry the same sort key, the processing order changes the
answer. That is not something to settle with whatever the sort happens to do —
it is a question about the domain that has to be answered before the algorithm.

## The case

Peak building occupancy. Bob exits at `t=11` and Charlie enters at `t=11`.

- IN processed first: `2 -> 3 -> 2`, peak **3**
- OUT processed first: `2 -> 1 -> 2`, peak **2**

## How to settle it

1. **Is the true order knowable?** Here, no — the records carry no ordering
   beyond the timestamp. So whatever you report is a **bound**, not a
   measurement. Say that out loud; it reframes the question.
2. **What is the number for?** Uncertainty tells you it is a bound; the purpose
   tells you *which* bound. A fire-code / capacity check makes under-reporting
   the dangerous direction, so take the upper bound and process IN first. A
   "how empty is the office" metric would want the opposite tie-break.

The same pair of questions applies to any equal-key ordering: stable vs unstable
sorts over duplicate keys, interval endpoints that touch, versions with equal
timestamps.

## Implementation half

Do not let the tie-break ride on an accident. `"IN" < "OUT"` is true, so sorting
the raw string ascending gives IN-first for free — until the vocabulary becomes
`ENTRY`/`EXIT` and the order silently flips, with no error and a plausible wrong
number. Write the rank down next to the reason:

```python
TIE_BREAK = {Punch.IN: 0, Punch.OUT: 1}   # IN first: upper bound on occupancy
```

Keep the rank separate from the enum's own member values, so reordering the enum
cannot re-break the sort.

## Related

- [[first-vs-last-extremum]]
