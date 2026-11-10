# Data Engineering

Big data concepts learned through scenarios, not tutorials.

## How a scenario works

Each file is one realistic situation with real numbers: volumes, rates,
retention, SLA, access pattern. The job is to reason to an architecture, not to
recall a tool.

Two layers, in this order:

1. **Reference architecture (tech-agnostic).** What has to happen to the data
   and why — where it lands, how it is laid out, what is computed when, what
   the failure and recompute story is. Boxes named by role ("append-only raw
   store", "columnar partitioned table", "scheduler"), never by product.
2. **Tech mapping.** Only after layer 1 stands: which of Spark / Trino / Impala
   / Airflow / Kafka / object store / table format fills each box, and what
   each choice buys and costs. A box that no one can justify in layer 1 does
   not get a product name in layer 2.

Code appears only when it settles an argument that prose cannot — proving a
skew, a cardinality, a cost.

## File shape

statement → constraints & numbers → my attempt (kept, including wrong turns)
→ reference architecture → tech mapping → takeaway

Distilled lessons move to `data-engineering/notes/`.

## Scenarios

- `01-nightly-report-stopped-finishing.md` — a nightly per-city report that
  outgrew its operational database. Covers aggregate combinability, CDC vs
  events, partitioning, sketches, restatement.
- `02-cache-hit-rate-nobody-measured.md` — drawn from real work on
  `map-context-mcp`. Covers working-set estimation, locality as a dependency,
  and deciding whether a phase is worth building when its key parameter is
  unmeasured.
- `03-updating-rows-in-files-that-cannot-change.md` — applying a nightly CDC
  feed to a table stored as immutable Parquet files. Covers rewrite cost,
  copy-on-write vs merge-on-read, atomic snapshot switching, and dedup —
  the reasons a table format exists.
