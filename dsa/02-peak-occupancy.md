# Peak Occupancy

## Statement

Badge log with timestamps, clean data (every person's IN/OUT records are
properly paired):

```python
records = [
    ("Alice",   "IN",  9),
    ("Bob",     "IN",  10),
    ("Alice",   "OUT", 12),
    ("Charlie", "IN",  11),
    ("Bob",     "OUT", 11),
    ("Charlie", "OUT", 14),
]
```

Return the maximum number of people inside the building at any moment, and
when that peak occurred.

### Walking the clock

Counts at `t = 9, 10, 11, 12, 14` are `[1, 2, 2, 1, 0]`.
(First pass said `2` at `t=14` — misread Charlie's last punch as an IN.)

### Decided: ties at equal timestamps

At `t = 11` Bob exits and Charlie enters. Order the two events IN-before-OUT,
so the count momentarily reaches **3** and the reported peak is 3.

Reasoning: the records carry no ordering beyond the timestamp, so at equal
timestamps the true sequence is unknowable — whatever you report is a *bound*,
not a measurement. Uncertainty tells you it is a bound; the purpose of the
number tells you which bound. For a capacity / fire-code check, under-reporting
is the dangerous direction, so take the upper bound: process IN before OUT.

A "how empty is the office" metric would want the opposite tie-break.

### Decided: which peak, and what "when" means

Report the **first** moment the peak is reached, as an instant (not the interval
over which it held). Input is not assumed sorted.

## My attempt

### Approach

Sweep line over the events.

1. Sort by `(timestamp, tie_break[punch])`, IN before OUT at equal timestamps.
2. Fold across the sorted events carrying `(count, max, peak_time)`:
   IN increments `count`, OUT decrements it; when `count > max`, write both
   `max` and the current timestamp.

Answer for the sample: peak **3** at `t = 11`.

### Encoding the tie-break

`"IN" < "OUT"` is true in Python, so sorting the raw action string ascending
gives IN-first *by lexicographic accident*. Rejected: rename the vocabulary to
`ENTRY`/`EXIT` and the ordering silently flips, turning the upper bound 3 into
2 with no error — the exact failure the safety argument was guarding against.
Explicit rank instead:

```python
TIE_BREAK = {Punch.IN: 0, Punch.OUT: 1}   # IN first: upper bound on occupancy
records.sort(key=lambda r: (r.timestamp, TIE_BREAK[r.punch]))
```

An unexpected punch value now raises `KeyError` instead of sorting somewhere
plausible. The enum's own member values are deliberately *not* the rank — a
later reorder of the enum would otherwise re-break the sort.

### `>` vs `>=`

First attempt used `count >= max` to keep the first peak. Backwards: `>=`
overwrites `peak_time` on every later tie, so it yields the **last** peak.
`>` keeps the first. The comparison operator *is* the policy.

### Complexity

- Time `O(n log n)`, dominated by the sort; the fold is `O(n)`.
- Space `O(n)` for the sorted copy. In-place `.sort()` would reduce it, at the
  cost of mutating the caller's list.

### Code

Skipped — approach and spec were the target.

## Takeaway

1. **A tie at equal keys is a spec decision, not an implementation detail.**
   Simultaneous IN and OUT made the answer 3 or 2 depending on processing order.
   The order is genuinely unknowable, so the result is a *bound* — and the
   number's purpose (capacity check) picks which bound.
   See [[tie-breaks-are-spec-decisions]].
2. **Never let an invariant live in a lexicographic accident.** Encode the rank
   explicitly next to the reason for it.
3. **`>` vs `>=` selects the first vs the last occurrence of an extremum.**
   See [[first-vs-last-extremum]].
4. Careless read of the sample data (misread Charlie's final OUT as an IN) put a
   `2` where a `0` belonged. Walk the clock literally.

