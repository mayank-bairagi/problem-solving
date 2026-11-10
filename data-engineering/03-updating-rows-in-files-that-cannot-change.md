# Updating Rows in Files That Cannot Change

Small scenario, one concept. Sized for the Credit Acceptance Staff SWE (Data)
role: lakehouse principles, Delta Lake, CDC. Do this one before touching any
product name.

## Statement

An auto-loan servicer keeps its loans in an operational database. Every night
the core system emits a **change feed**: one row per loan whose state changed
that day (payment posted, balance updated, status moved to `delinquent`,
`paid_off`, ...).

Analytics wants a single table, `loans_current`, with **exactly one row per
loan** holding the latest state, queryable by many teams the next morning.

The table lives on object storage as Parquet files. Object storage and Parquet
share one property that decides everything here: **a file, once written, is
never modified — only replaced or added to.** You cannot change row 4,127 of
a file. You can write a new file.

The task: design how tonight's changes get applied so that `loans_current` is
correct at 06:00 — and say what it costs.

## Constraints and numbers

- **3,000,000** loans in `loans_current`, ~**200 bytes** per row in Parquet
  → about **600 MB** total, stored as **600 files of ~1 MB**
- nightly change feed: **~400,000** rows (13% of loans), each carrying the
  full new state of the loan, keyed by `loan_id`
- changed loans are **spread across all files**: a loan's row lands in a file
  by `loan_id` hash, so ~13% of *every* file's rows change each night
- the feed can contain the **same `loan_id` more than once** in one night
  (two payments on one day); each row carries `updated_at`
- the feed is **at-least-once**: a row may be delivered twice, identical
- readers: ~40 queries between 06:00 and 09:00, most of them
  `SELECT ... WHERE status = 'delinquent'` or a full scan for a dashboard
- a Parquet file write runs at roughly **50 MB/s** per worker; you have
  **4 workers**
- write window: feed arrives at **01:00**, table must be correct by **06:00**
- a reader that starts mid-write must see **either yesterday's table or
  today's — never a mix**

## Questions to answer, in order

1. Naive approach: what is the simplest thing that produces a correct table,
   and what does it cost in bytes written and wall-clock time?
2. Where is the waste in (1)? Point at the exact bytes that did not need to
   be written.
3. Can the layout of the table be changed so that fewer files need rewriting?
   What would it take, and what does it do to the readers?
4. Instead of rewriting, what if tonight's changes are just *added* as new
   files? What does a reader now have to do to get "one row per loan", and
   who pays for it?
5. The "never a mix" rule: with files being added and replaced under a live
   reader, what single piece of extra state makes an atomic switch possible?
6. Duplicates: the same `loan_id` twice in a night, and the same row delivered
   twice. Where in the design are these resolved, and are they the same
   problem?

## My attempt

<!-- reasoning goes here, wrong turns kept -->

## Reference architecture

<!-- tech-agnostic; boxes by role -->

## Tech mapping

<!-- only after the reference architecture stands -->

## Takeaway

<!-- distilled lessons move to data-engineering/notes/ -->
