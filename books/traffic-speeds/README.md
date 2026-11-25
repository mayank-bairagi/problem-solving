# How Fast Is This Road?

*Data engineering concepts through one simple use case at a map company.*

A concept book: theory only, no hands-on labs. The bet is that if the concepts and decision points are clear, building the thing with coding agents is the easy part.

**Use case:** *Wayline* (fictional maps and navigation company) turns GPS pings from phones into one answer: how fast is traffic on this road right now, and how does that compare with normal?

**Companion text:** *Designing Data-Intensive Applications*, Martin Kleppmann, 1st edition. Every chapter ends with a table mapping its ideas to sections of that book.

## Chapters

| # | Chapter | Tools | Kleppmann | Status |
|---|---|---|---|---|
| 1 | [One Question, Three Clocks](01-one-question-three-clocks.md): the use case, the whole system, how to judge it | all, at a glance | Ch. 1, Part III intro | draft |
| 2 | [The Log](02-the-log.md): where pings land first | Kafka | Ch. 11 (logs), Ch. 6 (partitioning), Ch. 5 (replication), Ch. 4 (encoding) | draft |
| 3 | [Files That Behave Like a Table](03-files-that-behave-like-a-table.md): keeping every ping cheaply | Parquet, Iceberg, S3 | Ch. 3 (column storage), Ch. 7 (snapshots, atomic commit), Ch. 4 (schema evolution), Ch. 10 | draft |
| 4 | [Speed Right Now](04-speed-right-now.md): computing on data that never ends | Flink | Ch. 11 (stream processing), Ch. 8 (clocks), Ch. 9 (atomic commit) | draft |
| 5 | [Speed Normally](05-speed-normally.md): computing on a finished day | Spark | Ch. 10 (batch processing), Ch. 12 (reprocessing) | draft |
| 6 | [Asking Questions](06-asking-questions.md): many machines, one query | Trino, Athena, Redshift and MPP databases, DuckDB | Ch. 3 (analytics, warehousing), Ch. 2 (declarative queries), Ch. 6, Ch. 10 (MPP) | draft |
| 7 | [Serving the Answer](07-serving-the-answer.md): databases built for lookups | Postgres on RDS, DynamoDB | Ch. 3 (B-trees, LSM), Ch. 5 (replication), Ch. 6 (partitioning), Ch. 7 (transactions) | draft |
| 8 | [When Things Go Wrong](08-when-things-go-wrong.md): silence, clocks, zombies, majorities | all | Ch. 8, Ch. 9 | draft |
| 9 | [Keeping It Honest](09-keeping-it-honest.md): running it daily, checking it, changing it | Airflow | Ch. 12, Ch. 10 (workflows), Ch. 1 (maintainability) | draft |

## Part II: technology deep dives

Part I (chapters 1–9) tells the story and explains why each tool is there. Part II goes back over each technology at interview depth: how it works inside, and the topics interviewers ask about.

| # | Chapter | Covers | Status |
|---|---|---|---|
| 10 | [Deep Dive: Kafka](10-deep-dive-kafka.md) | storage, replication and ISR, producer, consumer groups and rebalancing, transactions, compaction, sizing | draft |
| 11 | [Deep Dive: Parquet and Iceberg](11-deep-dive-parquet-iceberg.md) | file layout, metadata tree, partitioning, commits and conflicts, row-level changes, maintenance, time travel, schema evolution | draft |
| 12 | [Deep Dive: Flink](12-deep-dive-flink.md) | runtime, state and rescaling, checkpoints and savepoints, watermarks, windows, exactly-once sinks, backpressure, joins | draft |
| 13 | [Deep Dive: Spark](13-deep-dive-spark.md) | driver and executors, Catalyst and Tungsten, shuffle, joins, AQE, skew, memory, Structured Streaming | draft |
| 14 | [Deep Dive: Trino, Athena and MPP Warehouses](14-deep-dive-trino-athena-mpp.md) | Trino execution, reading plans, join choice and dynamic filtering, memory and resource groups, federation, Athena, Redshift design, interview SQL patterns | draft |
| 15 | [Deep Dive: Postgres on RDS and DynamoDB](15-deep-dive-postgres-dynamodb.md) | B-tree indexes, EXPLAIN, MVCC and vacuum, isolation and locks, WAL and replication on RDS, DynamoDB keys, capacity and hot partitions, secondary indexes and conditional writes | draft |
| 16 | [Deep Dive: Airflow](16-deep-dive-airflow.md) | architecture and executors, DAG files, data intervals, idempotent tasks and backfills, states and retries, sensors and assets, pools and XCom, testing and alternatives | draft |

## Chapter recipe

Every chapter has the same sections, in this order:

1. **The story**: what Wayline needs at this point, in plain words.
2. **Ideas**: 3–5 concepts, each with a diagram, each explained through the pings.
3. **Decision points**: the real choices (this tool or that one, this setting or that one), with what each option buys and costs.
4. **In Kleppmann's book**: a table mapping each idea to a chapter and section.
5. **Check yourself**: 3–5 questions answerable from the chapter.
6. **In the interview room**: 6–8 exchanges, written as **Interviewer:** question and **Candidate:** answer. The interviewer probes like a senior engineer (why this choice, what breaks, what if). The candidate answers in a few clear sentences, as an engineer who built Wayline's system. Go a little deeper here than the main text where it helps.

Style rules:

- Simple first. One idea per section. No jargon without a one-line definition.
- Interesting: every idea starts from something that would go wrong at Wayline.
- Tools appear as the answer to a problem, never as a feature list.
- Target length: 1,500–2,500 words per chapter.

### Deep-dive chapter recipe (Part II)

1. **The technology in one page**: the parts, what it promises, what it does not.
2. **Topics**: 6–8 hot interview topics. Each has a short explanation, a diagram where it helps, a small config, code snippet or query where one applies, and **What interviewers probe**: the follow-up questions with crisp answers.
3. **Rapid-fire questions**: 10–15 one-or-two-line answers.
4. **At Wayline**: a table of the settings and choices the book's system uses, and why.
5. **In Kleppmann's book**: the mapping table.

Deep dives may use the tool's real setting names and go further than Part I. Keep snippets short (under ~15 lines) and only where they make the concept clearer. State version-dependent facts as such.

## Diagrams

- SVG in `diagrams/`, named `<chapter>-<slug>.svg`. From Chapter 3 on they are generated by `diagrams/build_<chapter>.py` using the helpers in `diagrams/_draw.py`; edit the script and re-run it.
- Black, white and grey only, large type, about 1040 px wide, so they read on a Kindle screen.
- At least one diagram per idea.

## Fact-check status (2026-11-25)

Checked against a published source (official docs, or the printed table of contents):

- **Kleppmann:** every section cited from Ch. 3, 5 and 8 matches the printed table of contents. Ch. 1, 2 and 4 headings match a reader's notes that follow the book's headings, and a few in Ch. 6, 9, 10, 11 and 12 were confirmed from search results.
- **Kafka 4.0:** KRaft only; segment 1 GiB; retention 168 h; `replica.lag.time.max.ms` 30 s; `max.poll.interval.ms` 5 min; idempotence on and `acks=all` by default; consumers `read_uncommitted` by default; KIP-848 protocol GA with `group.protocol=consumer`; auto-commit every 5 s; `exactly_once_v2`.
- **Iceberg:** 512 MB target file size; the procedure names and arguments used; deletion vectors in format v3.
- **Trino:** `optimize(file_size_threshold => …)` (default 100 MB; the book's 128 MB is a choice); `"t$snapshots"`; fault-tolerant execution with `retry-policy`; join distribution and reordering settings; right side is the build side; `REPLICATED`; fragment types; dynamic filtering on by default; resource group limits.
- **Spark:** 200 shuffle partitions; 10 MB broadcast threshold; AQE on by default since 3.2; advisory partition size default 64 MB (the book sets 128 MB); `spark.memory.fraction` 0.6; overhead 10%, minimum 384 MB; `EXPLAIN FORMATTED`.
- **Athena and Redshift:** $5 per TB scanned; per-query scan limits on workgroups; Redshift distribution styles, with `AUTO` the default.
- **Postgres:** default isolation Read Committed; Repeatable Read is snapshot isolation; SSI; 8 KB pages; 32-bit transaction ids and wraparound; vacuum and `VACUUM FULL`; index options.
- **RDS:** the classic standby serves no reads; blue/green deployments for Postgres (logical replication only for major upgrades).
- **DynamoDB:** 400 KB items; unit definitions; eventual reads by default, strong reads not available on global indexes; transactions of up to 100 items at double cost; streams kept 24 h; TTL deletes are free and come within days; local indexes only at creation; global tables use last writer wins in the default mode.
- **Airflow 3:** `airflow.sdk` imports and `Asset`; the backfill CLI; SLAs removed in 3.0, deadline alerts added in 3.1; workers report through the API server; `{{ ds }}` and the data-interval templates.
- **Flink 2.x:** `java.time.Duration` for windows and state TTL.
- **The book's own arithmetic** (load numbers, Kafka retention size, the 63% tail figure, the Athena cost examples).

Corrected after checking: DynamoDB "three zones" (docs say several), TTL timing, blue/green replication type, Spark overhead minimum, Parquet row group default attributed to the Java writer, Airflow 3 worker and `DagBag` notes, global-tables modes, deadline alerts.

Still from memory:

- **Kleppmann:** most section names in Ch. 6, 7, 9, 10, 11 and 12, and the title of Part III. O'Reilly refuses automated access, and the only complete tables of contents found online were unauthorised copies of the book, which were not used. Check these against a copy of the book.
- **Smaller facts:** Athena's 10 MB per-query minimum and free DDL; result reuse and the Iceberg CTAS options; Redshift zone maps and automatic vacuum; RDS failover time and RDS Proxy; the Airflow 3 catchup default, sensors, trigger rules, `dag.test()` and the removal of SubDAGs; Parquet's 1 MB page size; Kafka share-group status.
- **Snippets:** none has been compiled or run, and sample plan outputs are illustrative.

## Compiling to Kindle

```
python3 build_kindle.py
```

writes `build/how-fast-is-this-road.epub`. The script converts every SVG in `diagrams/` to PNG with headless Chrome, draws a cover, and runs `pandoc` over the chapters in order, with a divider page before each part. It needs `google-chrome`, and `pandoc` on the PATH or unpacked under `build/tools/`. Title, author and cover text are constants at the top of the script.

To validate, run the W3C EPUBCheck release unpacked under `build/tools/`: `java -jar build/tools/epubcheck-*/epubcheck.jar build/how-fast-is-this-road.epub`. The 2026-11-25 build passed EPUBCheck 5.4.0 with no errors or warnings.

Send the EPUB to a Kindle with Amazon's Send to Kindle (web, app or email). `build/` is generated and is not kept in git.
