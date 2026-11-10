# `>` vs `>=` selects the first or the last extremum

When scanning for a maximum and also recording **where** it happened, the
comparison operator is the policy for which occurrence you keep.

- `count > max` -> keeps the **first** time the max was reached
- `count >= max` -> overwrites on every tie, keeping the **last**

## Trace

```
t=1  count 2   max=2, peak_time=1
t=2  count 1
t=5  count 2   ">= " is true (2 >= 2) -> peak_time = 5
```

Wanting "the first peak" and writing `>=` gets you `t=5`. The mistake is easy
because `>=` *feels* more inclusive, but inclusive here means "keep replacing".

## Rule

Decide first-or-last as a spec question ("if the peak occurs twice, which do we
report?"), then let the operator follow. Whenever an extremum comes with a
location, index, or timestamp, that spec question exists — even when nobody
asked it.

## Related

- [[tie-breaks-are-spec-decisions]] — the same "which of several equally valid
  answers" question, one level earlier in the pipeline.
