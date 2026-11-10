# The Nightly Report That Stopped Finishing

## Statement

A ride-hailing company runs one nightly job. For **yesterday**, per city, it
produces four numbers:

1. completed rides
2. gross revenue
3. unique riders
4. p95 rider wait time (request -> driver arrival)

The job is a single SQL query against a read replica of the operational
database, over the `trips` table. It writes 300-odd rows into a dashboard
table. Two years ago it finished in 20 minutes. It now takes ~7 hours and
started missing the 08:00 SLA; some nights it does not finish at all.

Nobody has changed the query.

## Constraints and numbers

- 40M completed trips/day, ~400 bytes/row -> ~16 GB/day of new trip rows
- 300 cities; skewed — the top city is ~12% of all trips, the bottom 100
  cities are ~2% combined
- `trips` holds 3 years of history in one table, no partitioning
- Trip rows are mutated after insert: fare corrections and dispute refunds land
  up to 14 days late and change revenue for an already-reported day
- The dashboard also lets an analyst ask for *any* past day, and for
  month-to-date and year-to-date rollups of the same four numbers
- Read replica: one machine, 32 cores, 256 GB RAM, local SSD
- SLA: yesterday's numbers by 08:00; data stops arriving ~00:30

## My attempt

### Scope decision

Limited to the nightly analytics build. The OLTP store is a given — no schema
changes, no index tuning, no sharding. The one boundary that *is* in scope:
what the analytics side may ask the operational system to hand over (replica
read / CDC / application events). Specifying the input is part of designing the
pipeline; redesigning the source is not.

Parked OLTP intuitions (out of scope, kept so they aren't lost):

- <!-- fill in -->

### First pass — separate the read path from the write path

- Reading the operational DB for the nightly build is risky. CQRS-shaped fix:
  a separate analytics store, populated asynchronously from the operational
  tables.
- That store may not need to be a database at all — object storage (e.g. S3)
  could be enough.
- Better still: application **events** as the input — `ride booked`,
  `payment done`, `ride accepted`, `ride started`, `ride ended` — emitted to a
  log or event store. Events are immutable, so they carry detail that a
  mutable row loses by overwriting it.

Open questions on this pass (to answer before ranking the three inputs):

1. "Risky" — name the mechanism. What specifically breaks, and on which
   machine? Note that a 7-hour scan runs over rows that are being mutated.
2. Three inputs proposed and ranked, but by what test? What has to be true of
   the four output numbers for an event log to be *sufficient* input?
3. Which of the four numbers survive per-city computation + combining, and
   which do not? This decides whether the build can pre-aggregate to 300 rows
   a day at all.

### Second pass — which metrics survive slice-and-combine (Q3)

Rides and revenue combine cleanly. Unique riders and p95 do not — and they fail
for **different** reasons:

- **Unique riders.** A rider can appear in more than one city, so the per-city
  counts overlap and adding them double-counts that rider. The error is
  one-directional (always an over-count), and correcting it needs information
  the per-city count has already discarded: *which* riders, not how many.
- **p95.** Not an overlap problem. Two partitions each report a p95; those are
  not additive, and an average is not available either without knowing how many
  records each partition processed.

Open: does knowing the per-partition counts actually rescue p95? Test with two
equal-sized cities (100 each), where a weighted average reduces to a plain
average — try to build two distributions where that average is not the true
combined p95.

### Third pass — what a slice must carry (Q3 resolved)

The counts do **not** rescue p95. Ten-value counterexample (p80 at position
`ceil(0.8n)`): A = `[1000,1000]`, B = `[1]*8` gives per-city p80s of 1000 and 1
and a true union p80 of **1**; changing one B value from `1` to `5000` leaves
both per-city p80s and both counts untouched but moves the true union p80 to
**1000**. Identical inputs, different truths — so no formula on them works.

Classification of the four metrics:

- rides = **distributive** (count), revenue = **distributive** (sum) — a slice
  hands back one number, combine by summing
- unique riders = **holistic** — a slice must hand back the **set of rider
  IDs**; reduce by union, not sum, because a rider appears in several cities
- p95 wait = **holistic** — a slice must hand back the **distribution**,
  because a percentile is a position in a sorted list and the union's position
  depends on how the slices interleave

Sizes, 16-byte rider IDs:

- one day, worst case all-distinct: `16 B × 40M` = **640 MB** for one metric
- **year-to-date** distinct riders is not the sum of 365 daily numbers either;
  worst case `16 B × 40M × 365` ≈ **234 GB** to deduplicate

Consequence for this scenario: a 300-row-per-day summary table can serve rides
and revenue forever and **cannot answer MTD/YTD unique riders at all** — and
the dashboard requirements explicitly ask for MTD and YTD.

Escape hatch: fixed-size mergeable sketches (HyperLogLog ~16 KB for <1% error;
t-digest/KLL for quantiles) convert holistic into algebraic at the price of
bounded error. Whether that price is payable is a product question for the
dashboard's owner.

Distilled to [[not-every-aggregate-can-be-rolled-up]].

### Still open

1. "Reading the operational DB is risky" — still an unnamed mechanism. A
   7-hour scan runs over rows being mutated.
2. The three candidate inputs (analytics DB / object storage / event stream)
   are still unranked by any stated test.
3. The 14-day correction window vs. the 00:30 cutoff: what does "yesterday's
   numbers by 08:00" actually promise?

## Reference architecture

Skeleton to fill in. Every box has to exist given the constraints; the
**decisions** are the blanks. Rule while filling: a box that can be deleted
without naming what breaks should be deleted.

```
   OPERATIONAL SIDE          |           ANALYTICS SIDE
                             |
 +---------------------+     |
 |  trips (OLTP)       |     |
 |  mutable 14 days    |     |      out of scope to change
 |  3y in one table    |     |
 +----------+----------+     |
            |                |
        (1) |  what crosses this line, in what form, how often?
            v
 +---------------------------------+
 |  (2)  LANDING                   |
 |       holds:        ??          |
 |       grain:        ??          |
 |       mutable:      ??          |
 |       retention:    ??          |
 +----------+----------------------+
        (3) |  transformation: ??
            v
 +---------------------------------+
 |  (4)  MODELED                   |
 |       grain:            ??      |
 |       partitioned by:   ??      |
 |       sorted/clustered: ??      |
 +----------+----------------------+
        (5) |  aggregation: ??
            v
 +---------------------------------+
 |  (6)  SERVING                   |
 |       grain:    ??              |
 |       columns:  ??              |
 +---------------------------------+

 (7) ORCHESTRATION -- spans 1-6 -- trigger? ordering? failure? retry?
 (8) RESTATEMENT   -- a correction lands for a day already reported.
                      which boxes get rewritten, and how far down?
```

### Blanks

1. **The boundary.** Rows or events? Full snapshot or only what changed? Pushed
   continuously or pulled nightly? Old rows mutate, which makes "only what
   changed" harder than it sounds.
2. **Landing.** Append-only, or updated in place? That answer decides whether
   last Tuesday's report can ever be reproduced. What is the smallest thing
   you would be sad to lose here?
3. **Landing -> modeled.** Name the operations, not the tool.
4. **Modeled.** Partitioning is load-bearing. Candidates: trip date, city,
   ingest date. Test each against all three access patterns (nightly build,
   arbitrary past day, MTD/YTD) and against the top city being 12% of volume.
5. **Serving.** Which metrics live here as plain numbers, which need a
   different kind of column, which cannot be precomputed at all? Already
   established in the third pass — apply it.
6. **Orchestration.** What starts the run, given data stops ~00:30 and the
   answer is due 08:00? What happens when a night fails, and what must *not*
   happen when the failed run is retried?
7. **Restatement.** A refund lands on day-10 for a trip from day-3. Which boxes
   change, which rows are rewritten, and what does an analyst see who looked at
   day-3's number yesterday?

## Tech mapping

Full write-up with diagrams: [`01-nightly-report-architecture.html`](01-nightly-report-architecture.html)
(published copy: https://claude.ai/code/artifact/4a05f683-2543-490f-8c46-bbac8b7c9cc5)

| Box | Choice |
|---|---|
| source | PostgreSQL, untouched |
| capture | Debezium (reads the WAL) |
| transport | Kafka |
| landing | S3 via Kafka Connect S3 sink, by `ingest_date`, append-only |
| modeled | Spark + Iceberg + Parquet, by `trip_date`, sorted by city |
| catalog | Glue / Iceberg REST |
| sketches | Apache DataSketches (HLL + KLL) |
| serving | Iceberg table, one row per (date, city) |
| query | Trino |
| orchestration | Airflow |

Includes a ten-record end-to-end trace: the same trip inserted, aggregated, then
rewritten two days later when its refund arrives.

## Takeaway
