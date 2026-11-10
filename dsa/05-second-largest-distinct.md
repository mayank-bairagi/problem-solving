# 05 — Second Largest Distinct

## Statement

Given a list of integers, return the second largest **distinct** value.
If there isn't one, return `None`.

```
List(3, 7, 1, 7, 5)   -> Some(5)
List(4, 4, 4)         -> None
List(9)               -> None
List()                -> None
List(-2, -8)          -> Some(-8)
```

Constraint: one pass, O(1) extra space. No sorting.

## My attempt

```scala

def secondLargest(xs: List[Int]): Option[Int] = {

if(xs.toSet.length <= 1) None
else{
  xs

  
  secondLargest
}
}


```

### Session 2026-10-30 — Status: NOT PASSED (studied the solution via override)

Attempt 2 — accumulator `Set` of the two largest. Rejected: a `Set` doesn't
know which value is largest and has no size cap of its own.

Attempt 3 — tuple of `Int`, "two `math.min`s per step". Breaks on the seed
(`Int` has no "not seen yet" value; `Int.MinValue` collides with real input)
and on duplicates (min/max can't tell that a second `7` is a repeat).

Attempt 4 — update rule as cases. **Correct**, including the `x == largest` case:

```
x > largest                -> largest = x; second = largest   # bug: order — second gets x
x == largest               -> ignore
x > second && x < largest  -> second = x
otherwise                  -> ignore
```

Fixed the order (`second = largest; largest = x`). In a fold that case is just
`(x, largest)`, a new tuple, so there's no order to get wrong.

Attempt 5 — dodged the seed with pattern-match special cases:

```scala
list match {
  case Nil => None
  case head :: Nil => None
  case first :: second :: Nil => Some(first, second)   // bug: wrong value & type; List(4,4) -> not None
  case first :: second :: tail => if (first == second) /* recurse dropping first */
    tail.foldLeft(Accumulator(max(first, second), min(first, second))) { ... }
}
```

About nine paths for a four-line rule. Then asked for the solution (override).

### Solution (studied, not mine)

```scala
case class Acc(largest: Option[Int], second: Option[Int])

def secondLargest(xs: List[Int]): Option[Int] =
  xs.foldLeft(Acc(None, None)) { (acc, x) =>
    if (acc.largest.forall(x > _))      Acc(Some(x), acc.largest)
    else if (acc.largest.contains(x))   acc
    else if (acc.second.forall(x > _))  acc.copy(second = Some(x))
    else                                acc
  }.second
```

Verified on Scala 2.12 against all statement examples, plus
`List(Int.MinValue, 5) -> Some(Int.MinValue)`, `List(5, 5, 9) -> Some(5)`, and
`List(9, 5, 5, 7) -> Some(7)`.

Why it works:
- `None` *is* "not seen yet", so `Nil`, `List(9)` and `List(4, 4, 4)` need no
  special cases: `second` simply never gets set.
- `opt.forall(p)` is `true` for `None`, so "x beats an empty slot" holds with
  no branch. (`exists` would be the wrong choice: it's `false` for `None`.)
- The order of the branches matters: the `contains` check must come after the
  `largest` check and before the `second` check, otherwise a duplicate of the
  max would be put into `second`.

### Plain-loop version (for an interviewer who doesn't read Scala)

```scala
def secondLargest(xs: List[Int]): Option[Int] = {
  var largest: Option[Int] = None
  var second: Option[Int] = None
  for (x <- xs) {
    if (largest.isEmpty || x > largest.get) {
      second = largest
      largest = Some(x)
    } else if (x == largest.get) {
      // duplicate of the max: skip
    } else if (second.isEmpty || x > second.get) {
      second = Some(x)
    }
  }
  second
}
```

Same four cases, same seed. `.get` is safe because `||` short-circuits on
`isEmpty`. Verified on 2.12 with the same eight cases.

### Follow-up: `fold` vs `foldLeft` (answer given on request)

- `fold[A1 >: A](z: A1)(op: (A1, A1) => A1)`: the seed, both arguments and the
  result share one type that is a supertype of `Int`. `Acc` isn't, so A1 is
  inferred as `Any` and `acc.largest` doesn't compile. `foldLeft[B]` allows
  accumulator type != element type.
- `fold` may combine in any grouping, so `op` must be associative and `z` an
  identity: a **monoid**. `foldLeft` is sequential and needs neither.
- To parallelise: `x => Acc(Some(x), None)` plus `combine(Acc, Acc)` keeping the
  top two *distinct* values, with identity `Acc(None, None)`. Not yet written.
- Check question (open): why must `combine` dedupe? Give a breaking input.

**Redo from scratch: 2026-10-31**, blank file, 10-minute time box, no peeking.

### Redo 2026-10-31

Attempt 1 — step function:

```scala
def findTopTwo(var largest: Int, var secondLargest: Int, current: Int): (Int, Int) = {
  if (current > largest) {
    secondLargest = largest
    largest = current
    (largest, secondLargest)
  } else if (current < largest && current > secondLargest) {
    secondLargest = current
    (largest, secondLargest)
  } else
    (largest, secondLargest)
}
```

Review: assignment order correct, duplicate handling correct. Problems: `var`
parameters don't compile; `Int` brings back the seed problem; not yet wired into
a fold and doesn't return `Option`.

Attempt 2 — **PASSED** (own code, 2026-11-01). Passes all 9 cases on 2.12.

```scala
def findTopTwo(largest: Int, secondLargest: Int, current: Int): (Int, Int) = {
  if (current > largest) (current, largest)
  else if (current < largest && current > secondLargest) (largest, current)
  else (largest, secondLargest)
}

@tailrec
def findSecondLargest(xs: List[Int]): Option[Int] = {
  xs match {
    case Nil | _ :: Nil          => None
    case first :: second :: tail =>
      if (first == second) findSecondLargest(second :: tail)
      else {
        val s = tail
          .foldLeft(math.max(first, second), math.min(first, second)) {
            case ((largest, secondLargest), current) =>
              findTopTwo(largest, secondLargest, current)
          }
          ._2
        Some(s)
      }
  }
}
```

Different design from the studied solution: it seeds from real data (the
first two distinct elements) instead of `Option`. That's valid, and it matches
the main point of the seed note. Polish: remove the leftover top-level `var`s;
use `foldLeft((a, b))`, because `foldLeft(a, b)` relies on auto-tupling.

## Takeaway

- Your instinct to seed with special cases instead of choosing a type that
  can represent "absent" led to 9 code paths and a bug. When a seed is
  missing, ask *which type can represent "no value yet"* before writing any
  `match`.
- `Option.forall` / `exists` / `contains` are how you compare against a value
  that may be missing. Remember `forall` on `None` is vacuously true.
- Write fold steps as building a new value, not as a sequence of assignments.
  That way the assignment-order bug can't happen.
