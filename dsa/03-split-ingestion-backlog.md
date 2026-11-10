# Splitting the Ingestion Backlog

## Statement

A chronologically ordered list of daily log volumes (GB) must be assigned to
`k` worker machines. Each worker takes a **contiguous** block — order cannot be
rearranged, because downstream processing depends on chronology. Every file
goes to exactly one worker; workers run in parallel, so the job finishes when
the slowest worker finishes.

Minimize the largest total assigned to any single worker, and return that
minimum.

```python
volumes = [7, 2, 5, 10, 8]
k = 2
# best split: [7,2,5] = 14 | [10,8] = 18  ->  answer 18
```

### Status: PAUSED mid-solution — resume here

Wrong turns worth keeping:

1. **Work-stealing idea.** "Give each worker the next day's file as it frees
   up." A better real-world scheduler, but it violates the contiguity
   constraint (worker A ends up with days 1 and 4). It also beats 18, which is
   exactly why the contiguity constraint needs justification rather than
   assumption.
2. **Two pointers from both ends.** Balanced a left and right running sum. Two
   bugs: it walks one step past the correct split and double-counts an index,
   and — fatally — it hard-codes `k = 2`. Three workers leave the middle with
   no pointer. Two pointers is the wrong tool.

### What was established

- **The answer is a worker's total load**, not a file size. First bounds
  attempt returned 2 and 10 (min and max element) — falsified immediately,
  since the known answer 18 is outside `[2, 10]`.
- **Search space:** `[max(volumes), sum(volumes)]` = `[10, 32]`.
  Lower bound from `k = 100`: every file sits alone, the slowest worker holds
  the largest single file. Upper bound from `k = 1`: one worker takes all.
- **Feasibility check for a candidate `L`:** walk left to right filling a
  worker until the next file would push it over `L`, then close it and start a
  new one. Feasible iff worker count <= `k`.
  - `L = 15` -> `[7,2,5] | [10] | [8]` = 3 workers > 2 -> no
  - `L = 18` -> feasible

### Next step when resuming

Is `feasible(L)` monotone in `L` — does it flip from all-no to all-yes exactly
once, and why can a larger `L` never require more workers? What does that
structure let you do to the range `[10, 32]`?

## My attempt

<!-- brute force + complexity, then the improvement -->

## Takeaway

