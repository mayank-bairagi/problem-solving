# Not every aggregate can be rolled up

Before designing any pre-aggregation, ask of each metric: **if the data is
split into slices and something is computed per slice, can those per-slice
results be combined into the true answer for the whole?**

Slices can be partitions (cities, shards). They can equally be **days** — and
that reading is the one that bites, because a daily summary table's rows are
exactly the slices a monthly or yearly rollup would try to combine.

## Three classes

| class | what a slice hands back | size | examples |
|---|---|---|---|
| **Distributive** | the same kind of number as the answer | 1 value | `count`, `sum`, `min`, `max` |
| **Algebraic** | fixed-size tuple of distributive parts | k values, k fixed | `average` = (sum, count); variance = (n, Σx, Σx²) |
| **Holistic** | no fixed-size summary exists | **grows with the data** | `count distinct`, percentiles, median, mode, top-K |

The dividing line: for distributive and algebraic metrics a slice's
contribution can be summarized **without knowing anything about the other
slices**. For holistic ones it cannot.

## The two holistic failures are different

Both break, for different reasons — worth keeping separate.

**Distinct counts — overlap.** The same entity appears in more than one slice,
so per-slice counts double-count it. The error is one-directional (always an
over-count) and repairing it needs information the count discarded: *which*
entities, not how many. Fix: carry the **set**, reduce by union.

**Percentiles — interleaving.** A percentile is a *position* in a sorted list,
not a magnitude. The union's percentile depends on how the slices' values
interleave when merged, which a single number per slice has thrown away.

Proof that no formula on the per-slice percentiles can work — ten values,
p80 = value at position `ceil(0.8n)`:

| | values (sorted) | n | pos | p80 |
|---|---|---|---|---|
| A | 1000, 1000 | 2 | 2 | **1000** |
| B | 1,1,1,1,1,1,1,1 | 8 | 7 | **1** |
| union | 1,1,1,1,1,1,1,1,1000,1000 | 10 | 8 | **1** |

Change one value in B, from `1` to `5000` — B's own p80 does not move, it was
already above the cut:

| | values (sorted) | n | pos | p80 |
|---|---|---|---|---|
| A | 1000, 1000 | 2 | 2 | **1000** |
| B | 1,1,1,1,1,1,1,5000 | 8 | 7 | **1** |
| union | 1,1,1,1,1,1,1,**1000,1000**,5000 | 10 | 8 | **1000** |

Identical inputs (`p80_A=1000`, `p80_B=1`, `n_A=2`, `n_B=8`), true answers `1`
and `1000`. No function of those four numbers produces both. The weighted
average says `200.8` — wrong in both. Fix: carry the **distribution**, not the
percentile.

## Why the label is an architecture decision

Ride-hailing nightly report, 40M trips/day, 16-byte rider IDs:

- one day of distinct riders, worst case: `16 B × 40M` = **640 MB** — for one
  metric, one day, against 8 bytes for revenue
- **year-to-date** distinct riders is not the sum of 365 daily numbers (a rider
  rides in March and July). Worst case `16 B × 40M × 365` ≈ **234 GB** to
  deduplicate; even at a realistic 60M distinct riders/year, ~1 GB held and
  merged

So a 300-row-per-day summary table serves rides and revenue forever, and
**cannot answer "unique riders this month" at all** — the rollup is
arithmetically invalid. This is usually discovered after the table is built.

## The escape hatch: sketches

Give up exactness for a **fixed-size, mergeable** summary:

- **distinct** → HyperLogLog, ~16 KB per slice, <1% error, two sketches merge
  into one sketch. YTD becomes: merge 109,500 sketches → one 16 KB object.
- **percentiles** → t-digest / KLL, a few KB, mergeable, most accurate in the
  tails, which is where p95 lives.

What a sketch really does: **converts holistic into algebraic** — fixed size,
independent of data volume — priced in bounded error.

## Worked example: why a sketch merges

Stop remembering *who*; remember enough to estimate *how many*. Hash each ID to
uniform random bits — a hash starting with `k` zeros appears about once per
`2^k` distinct values, so the most extreme run seen estimates the cardinality.
Two properties carry the whole design:

- **duplicates are free** — the same ID always hashes to the same bits, and
  `max(x, x) = x`. A rider appearing on 200 days changes nothing after the
  first. This is exactly what kills the overlap problem.
- **merging is `max`** — elementwise, so order and grouping are irrelevant.

Real HLL uses many registers (first 14 bits of the hash pick one of 16,384)
because one estimator is far too noisy; error ≈ `1.04/√m` ≈ 0.8% in ~12 KB,
independent of whether it saw a thousand IDs or a billion.

Toy version — 4 registers, 8-bit hashes, first 2 bits pick the register,
`ρ` = leading zeros of the tail + 1:

| rider | hash | register | tail | leading 0s | ρ |
|---|---|---|---|---|---|
| R1 | `01 001011` | 1 | `001011` | 2 | 3 |
| R2 | `10 000110` | 2 | `000110` | 3 | 4 |
| R3 | `01 100000` | 1 | `100000` | 0 | 1 |
| R4 | `11 010000` | 3 | `010000` | 1 | 2 |

```
Day 1 (R1, R2, R3)   [ 0 , 3 , 4 , 0 ]     reg1 = max(3,1) = 3
Day 2 (R2, R4)       [ 0 , 0 , 4 , 2 ]     R2 writes the same 4 as Day 1
                     ─────────────────  max
merged               [ 0 , 3 , 4 , 2 ]
```

One pass over R1..R4 from scratch also gives `[0, 3, 4, 2]`. Identical, not
approximately — R2 counted once across two days, its ID never stored.

> `merge(sketch(A), sketch(B)) == sketch(A ∪ B)`

The approximation lives only in the final registers→number step. **The merge
itself is exact.**

## What that buys, per question

One extra 12 KB column on each daily row, and every question is a fold with
`max` over whichever rows it selects:

| question | rows merged | output |
|---|---|---|
| one city, one day | 1 | 12 KB |
| all cities, one day | 300 | 12 KB |
| one city, YTD | 365 | 12 KB |
| company-wide, YTD | 109,500 | 12 KB |

Year of sketches stored: `109,500 × 12 KB` ≈ **1.3 GB**, against ~234 GB and a
full rescan per question. Arbitrary groupings ("south India, Q3, weekends")
need no new precomputation, because `max` is order- and grouping-agnostic.

## The three prices

1. **It is an estimate** — ~±0.8% at 12 KB; registers are a dial against error.
2. **No subtraction.** Merge only, never un-merge: "Q1 minus January" is not
   available. Questions phrased as differences of distinct counts need
   rephrasing.
3. **Hash and precision are frozen forever.** Sketches with different settings
   cannot merge; changing them means rebuilding all history.

The same shape handles p95 — a t-digest is the mergeable object, folded
identically.

## The rule

> For every metric, ask whether a month's answer can be produced from the
> month's daily rows. If yes, store the number. If no, store either something
> that grows with the data, or a sketch.

Which of those two is a **product** question — is this metric allowed to be 1%
off? — not one to settle alone.

## Related

- [[tie-breaks-are-spec-decisions]]
