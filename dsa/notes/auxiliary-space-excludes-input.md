# Auxiliary space excludes the input

Space complexity means **what the algorithm allocates**, not what it was handed.
The input array/list is the caller's; it is not part of your space bound.

## The mistake

Log-validation problem: fold `n` records into a map of `k` distinct people
holding `(first, last)` per person. Stated the space as `O(n + k)`, then
`O(n + k)` again. There is no `n`-sized allocation anywhere in the solution.
Correct answer: `O(k)`.

## Why it matters beyond pedantry

`k <= n`, so `O(n + k) = O(n)` — the loose bound is not *false*. It is worse
than false: it is **true and uninformative**. The entire design decision was
keeping two punches per person instead of the full punch history, specifically
to avoid an `n`-sized allocation. Reporting `O(n)` throws away the property the
design bought.

## Check to run

Before stating a space bound, name every structure you allocate and its size.
If you cannot point at an object of that size, the term does not belong in the
bound.
