# Seed state uniformly to delete special cases

When folding a stream into per-key state, initialize **every** field on first
insert — even fields that "logically" only apply once more data arrives. A field
left empty as a sentinel becomes a branch you have to test forever after.

## Concrete case

Tracking each person's first and last punch in an attendance log.

**First instinct** — set `first` on insert, set `last` only on subsequent
punches. A one-punch person then has an empty `last`, needing its own check:

```
if last is empty: invalid          # extra branch
if first != IN or last != OUT: invalid
```

**Better** — set `first = last = punch` on insert, overwrite `last` every time
after. Now a one-punch person has `first == last`, and the ordinary predicate
rejects them with no extra code:

- `IN` only  -> `last == IN`  -> fails "last must be OUT"
- `OUT` only -> `first == OUT` -> fails "first must be IN"

```
if first != IN or last != OUT: invalid    # that's all
```

## The general shape

An "empty" sentinel is a second state your predicate must know about. Seeding
the field with real data collapses the degenerate case into the general one.
Ask of any special case: *can I choose an initial value that makes this case
ordinary?*

## When there is no real data to seed with

Sometimes nothing real exists yet, as with a fold over a possibly-empty list
(`dsa/05`). Then pick a **type** that can represent absence (`Option[Int]`,
seed `None`), not a sentinel value (`Int.MinValue` collides with real input)
and not pattern-match cases peeled off the front of the list. Compare against
the empty slot with `opt.forall(x > _)`, which is vacuously true for `None`,
so "anything beats empty" needs no branch.

## Related

- [[auxiliary-space-excludes-input]]
