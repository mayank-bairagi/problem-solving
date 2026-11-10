# The Cache Hit Rate Nobody Measured

Drawn from real work: `geoCortex/projects/map-context-mcp` and the Phase 1
reference architecture at
`map-context-cross-layer-test-data/artifacts/2026-09-10-reference-architecture-abstract.html`.

## Statement

An MCP server answers map-feature questions for coding agents. Phase 1 of the
proposed architecture keeps an embedded analytic engine (DuckDB) serving four
of five access patterns by reading files from a shared serving cache, and
states outright that **locality still decides latency** for those four.

Every cost and latency figure in the supporting analysis is quoted at a
**90% cache hit rate**. Nothing measures it.

The task: decide whether 90% is defensible, and what it actually depends on.

## Constraints and numbers (all from the project's own artifacts)

- Germany is **~6,000 level-12 tiles** in region WEU
- modelled hot-path resident footprint: **28.8 MB per tile** — derived from an
  80 MB average tile, which is itself averaged from **two tiles measured 51 MB
  and 207 MB**, i.e. 4× apart (open item A, still unmeasured)
- serving cache sized at **161 GiB**, which is exactly `6,000 × 28.8 MB` —
  so the cache size inherits the ±2.4× uncertainty in the tile average
- **thousands of concurrent sessions**, each exploring *unpredictable
  geography*; tiles are loaded on demand
- workload assumption: **200 features/sec**
- cost spread across the assumptions: **$130 to $30,405/month**
- a page-cache miss on the 1-row-group layout costs up to **437 ms** (full
  column decompress); a hit costs **~1-3 ms**
- **open item D — distinct tiles seen per replica per hour — is marked "cheap"
  and has never been measured.** It gates the largest change in the proposal.

### The coupling that makes it hard

Phase 1 makes two changes that are presented as independent:

1. the session store moves out of the node, so **nodes become interchangeable**
2. the serving cache stays, and **four access patterns still depend on locality**

Session affinity was previously doing locality work by accident — one agent
session explores geographically adjacent tiles, so sticky routing concentrated
a session's working set on one node's page cache. Making nodes interchangeable
means a session's requests can land anywhere.

The architecture's own fourth principle says:

> Locality is an optimisation, never a requirement. Any design where
> correctness of performance depends on which node holds which bytes has
> substituted routing for an index.

Phase 1 is, by that definition, the forbidden thing — and it removes the
accidental locality mechanism in the same phase.

## My attempt

<!-- reasoning goes here, wrong turns kept -->

### Questions to answer in order

1. **What is a "cache hit" here, precisely?** The cache is shared and
   pre-warmed, so nothing is ever *absent*. Name what is actually being hit
   and missed, and on which machine. Until this is defined, 90% means nothing.
2. **Write the hit rate as a formula.** What variables does it depend on?
   Which of them does the team control, and which does the workload set?
3. **Compute the working set per replica.** With R replicas, S concurrent
   sessions, each touching T distinct tiles per hour, and no tile-aware
   routing — how many distinct tiles does one replica see, and how many bytes
   is that? Compare against one replica's RAM.
4. **Does the answer survive the ±2.4× on tile size?** Compute the optimistic
   and pessimistic ends, not the midpoint.
5. **What would move the hit rate?** Rank the levers: tile-aware routing,
   restoring session affinity, more RAM per replica, fewer replicas,
   smaller row groups, reducing the resident footprint further.
6. **Is Phase 1 worth doing at all** if its performance rests on a parameter
   nobody has measured — given that the Target phase deletes the cache
   entirely by indexing everything in a transactional store?
7. **What telemetry would have answered this already?** The architecture has
   no box that collects data about itself. Design the smallest thing that
   closes items A, B, D and E.

## Reference architecture

<!-- tech-agnostic first -->

## Takeaway
