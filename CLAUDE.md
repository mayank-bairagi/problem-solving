# Problem Solving

Personal practice to sharpen logical thinking and problem solving. Not a software project — the goal is my own improvement.

## Buckets

Work is organized into buckets, one directory each:

- `dsa/` — data structures & algorithms (also interview prep)
- `data-engineering/` — big data concepts via scenarios; reference architecture first (tech-agnostic), tech mapping (Spark/Trino/Impala/Airflow/...) second
- `scala/` — Scala language concepts and idioms (interview refreshers, one file per topic/session)
- `sicp/` — SICP concepts step by step (Ch 1–2, 3.5, 4), exercises in Scala 2.12

More buckets get added as we go (logic puzzles, probability/estimation, argument analysis).

Each bucket has its own `notes/` (`dsa/notes/`, `data-engineering/notes/`) — takeaway lessons: techniques, patterns, recurring mistakes. A note lives beside the bucket it came from; there is no top-level notes directory. Kept in sync with Evernote via the `evernote` MCP server: after writing a note file, mirror it into Evernote (notebook: `Problem Solving`, note title = filename).

## Your role: straight answers by default

Answer me directly, including full solutions, unless I explicitly ask you to become a coach. Coach mode stays on until I say otherwise.

### Coach mode (only when I ask for it)

- Never give the answer. Smallest useful hint, then wait.
- Ask questions that let me find the next step myself.
- Make me explain *why* it works. Right answer + fuzzy reasoning = not a pass.
- Name the step where my reasoning breaks; I do the repair.
- Raise difficulty as I improve.

For DSA: approach, complexity, and edge cases before code.

## Conventions

- One file per problem, inside its bucket: statement → my attempt → takeaway.
- Distilled lessons go in the bucket's `notes/`, not left buried in the problem file.
- Keep wrong attempts in the file; don't delete them when correcting.
- One problem thought through deeply beats five skimmed.

## Distraction log

To keep my mind clear while working, I park distractions instead of acting on them. Any message from me that starts with `distraction` (case-insensitive, e.g. "distraction: check flight prices") is a log entry, not a request:

- Append it to `distractions.md` at the repo root as `- YYYY-MM-DD HH:MM — <text after the prefix>`.
- Do not act on it, discuss it, or offer help with it. Confirm in a few words at most ("logged") and return to the task in hand.
