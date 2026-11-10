# Entry/Exit Log Validation

## Statement (v1 — superseded, kept for the record)

Given a chronological list of `(name, action)` access records, report two buckets:

- **Missing OUT** — entered but never exited
- **Invalid OUT** — exited without an active entry

```python
records = [
    ("Alice", "IN"),
    ("Bob",   "IN"),
    ("Alice", "OUT"),
    ("Charlie", "OUT"),
]
# Missing OUT: ["Bob"]
# Invalid OUT: ["Charlie"]
```

Rejected because strict pairing splits into ever more failure buckets
(double IN, stray OUT, still-inside, ...) and real punch logs are not
reliably paired.

## Statement (v2 — current)

Real office attendance semantics. Per person, only the **first** and **last**
punch of the log are dressed:

- first punch must be `IN`
- last punch must be `OUT`
- anything in between is ignored (forgotten punches, re-punches, etc.)

Report the violations.

### Decided

- One punch => invalid, whichever action it is. Not a separate rule: it is
  forced by the two rules above, since one record cannot be both the first
  IN and the last OUT.
- First punch is `OUT` => invalid. Last punch is `IN` => invalid.
- Output is a **set of people**, not a list of violations: a person who
  breaks both rules is reported exactly once.

### Open questions (to close before coding)

- Output unit confirmed as person (see above).
- Is the log scoped to a single day?

### Assumption

Ordering is positional: the list is already in chronological order, so a
person's first punch is their first occurrence in the list and their last
punch is their last occurrence. Nothing in the tuple enforces this — it
breaks if the log is ever merged across door readers or re-sorted upstream.

## My attempt

### Approach

One fold over the records building `Map[Person -> (first, last)]`:

- person not in map: insert with `first = last = punch`
- person already in map: overwrite `last` only

Then filter the map: a person is **invalid** unless `first == IN and last == OUT`.

### Why no special case for one punch

First instinct was to leave `last` empty until the second punch, then test for
emptiness to catch one-punch people. Unnecessary. Seeding `last` on insert makes
a one-punch person have `first == last`, and the ordinary predicate rejects them
for free:

- `IN` only  -> `last == IN`  -> fails "last must be OUT"
- `OUT` only -> `first == OUT` -> fails "first must be IN"

One fewer branch, same behavior.

### Complexity

- Time `O(n)` for the fold + `O(k)` for the filter; `k <= n`, so `O(n)`.
- Space `O(k)`, where `k` = distinct people.

Space is `O(k)`, not `O(n)`: auxiliary space counts what the algorithm
allocates, not the input it was handed. The map holds one two-punch entry per
person, never the full punch history — which is the entire point of keeping
`(first, last)` instead of a list.

### Code

Skipped deliberately — approach and complexity were the target here.

## Takeaway

1. **The statement was the hard part, not the algorithm.** The original two-bucket
   framing (missing OUT / invalid OUT) fragments into more and more buckets as
   real-world messiness appears. Reframing to "first punch IN, last punch OUT,
   ignore the middle" made the problem smaller *and* more faithful to how the
   office actually works.
2. **Auxiliary space excludes the input.** Called it `O(n + k)` twice. The map is
   the only allocation: `O(k)`. Reporting `O(n)` would have concealed the one real
   design decision — storing `(first, last)` instead of every punch.
   See [[auxiliary-space-excludes-input]].
3. **Seed state uniformly to delete special cases.** Setting `last` on insert (not
   just on later punches) made the one-punch case fall out of the ordinary
   predicate. See [[seed-state-to-kill-special-cases]].
4. **Positional ordering is an assumption, not a fact.** The tuple has no
   timestamp; "first" only means "earliest in the list" because someone upstream
   promised it does.

