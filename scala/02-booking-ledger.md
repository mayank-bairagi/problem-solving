# 02 — Booking ledger (capstone for the Scala refresher)

Time box: **45 minutes**, then run `scala scala/02-booking-ledger.scala` — all checks must pass.
Code goes in the `.scala` file (skeleton with `???` and checks provided). Attempts and takeaways here.

## Statement

You receive an event log for hotel bookings, one event per line, comma-separated:

```
BOOK,<bookingId>,<hotelId>,<nights>,<pricePerNight>
CANCEL,<bookingId>
AMEND,<bookingId>,<newNights>
```

Build a small ledger that (1) parses lines, (2) replays events into a state, and
(3) reports the top-K hotels by revenue.

### 1. Parse — `parse(line): Either[ParseError, Event]`
- `Event` is a sealed ADT: `Book`, `Cancel`, `Amend`.
- `ParseError` is a sealed ADT:
  - `UnknownType(t)` — first field is not BOOK/CANCEL/AMEND
  - `MalformedLine(line)` — known type, wrong number of fields
  - `BadNumber(field, value)` — a numeric field that isn't an Int (`field` = "nights" / "pricePerNight" / "newNights")
- Report the *first* problem only (Either short-circuits — that's fine).

### 2. Replay — `step(state, event): Either[Rejection, State]` and `replay(events): (State, List[Rejection])`
- `State = Map[bookingId, Booking]`; a `Booking` has a `Status` (`Active` | `Cancelled`).
- Rules (rejected events leave the state unchanged; keep going):
  - `BOOK` with an existing id → `Rejection(event, "duplicate id")`
  - `BOOK`/`AMEND` with nights < 1 → `"nights must be >= 1"` (check this *before* looking up the id)
  - `CANCEL`/`AMEND` unknown id → `"unknown booking"`
  - `CANCEL` an already-cancelled booking → `"already cancelled"`
  - `AMEND` a cancelled booking → `"booking cancelled"`
  - otherwise apply: cancel sets status; amend replaces nights.
- `replay` is **one `foldLeft`**. Rejections come back in input order.

### 3. Report — `topK[A: Ordering](xs, k): List[A]`, `revenue(state): List[HotelRevenue]`, `report(lines, k): Report`
- Revenue per hotel = Σ `nights × pricePerNight` over **Active** bookings only.
- `HotelRevenue(hotelId, revenue: Long)` with an implicit `Ordering` in its
  **companion**: revenue descending, then hotelId ascending. `topK` must be
  generic — it only knows `A: Ordering`.
- `Report(parseErrors, rejections, top)`. Parse errors and rejections are kept
  separately, each in input order.

### Constraints
- No `var`, no `.get` on Option, no `null`, no exception escaping any function
  (`toInt` is wrapped in `Try`).
- Every `match` on a sealed type exhaustive — no guards hiding a missing case.
- Scala 2.12 (`scala file.scala`).

### Before coding (say these out loud, 5 min max)
1. Which of the 7 steps does each function exercise?
2. Complexity of `report` in N = lines, H = hotels.
3. Two edge cases the provided checks *don't* cover.

## My attempt

_(pending)_

## Takeaway

_(pending)_
