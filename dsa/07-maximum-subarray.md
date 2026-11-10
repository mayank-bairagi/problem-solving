# 07 — Maximum Subarray, Kadane (Medium)

## Statement

Return the largest sum of a non-empty contiguous subarray.

```
-2, 1, -3, 4, -1, 2, 1, -5, 4  -> 6   // from 4, -1, 2, 1
```

## My attempt

### Algorithm

At each element `x`, the best run ending at `x` either:

- extend: `[.. previous run.., x]`
- restart: `[x]`

State: `(curMax, best)`

```
cur  = x max (cur + x)
best = cur max best
```

Seed both with the first element: `curMax, best = -2`

### Dry run

```
x       1  -3   4  -1   2   1  -5   4
curMax  1  -2   4   3   5   6   1   5
best    1   1   4   4   5   6   6   6
```

Answer: `best = 6`

### Code

```scala
def step(s:(Int,Int),x:Int) : (Int,Int) = {
  val (cur,best) = s
  val c = x max (cur + x)
  val b = c max best
  (c,b)
}

def maxSubArray(xs:List[Int]):Int = {
  require(xs.nonEmpty,"list should be non empty")
  xs.tail.foldLeft((xs.head,xs.head))(step)._2
}
```

## Takeaway

- The state is "the best run that **ends at x**". Each step has only two choices: extend the run (`cur + x`) or restart at `x`. The step that skips x, `cur max (cur + x)`, breaks contiguity and gives the best *subsequence* instead (10 rather than 6 on the example).
- Seed `cur` and `best` with the first element, not 0. Starting at 0 adds the empty subarray as an answer and gets all-negative input wrong (`[-3, -1]` should be `-1`).
- Empty input has no valid answer because the subarray must be non-empty. Make that a precondition with `require`; don't return a made-up value such as 0 or `Int.MinValue`.
- Write the recurrence once and copy it into the code exactly. My trace used the right formula, but my code didn't.
- O(n) time, O(1) extra space: one `foldLeft` over a tuple.
