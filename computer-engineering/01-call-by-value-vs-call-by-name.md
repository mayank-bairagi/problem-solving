# Call-by-value vs call-by-name (Scala)

## Statement

Predict the output:

```scala
def loud(): Int = { println("computing..."); 42 }

def byValue(x: Int): Int   = x + x
def byName(x: => Int): Int = x + x

println(byValue(loud()))
println("---")
println(byName(loud()))
```

Follow-ups:
- What if the body is `def byName(x: => Int): Int = 10`?
- Why must `b` be by-name in `def and(a: Boolean, b: => Boolean) = if (a) b else false`?

## My attempt

First guess:
```
computing..
43
--
computing...
43
```
Wrong on two counts: 42 + 42 = 84 (slip), and `byName` prints `computing...` twice — one per
reference to `x` in `x + x`.

Corrected:
```
computing...
84
---
computing...
computing...
84
```

For the `= 10` body I guessed `computing... / 10` — wrong. `x` is never referenced, so `loud()`
never runs; only `10` prints.

Also wrote "by making B call by value we enforce short-circuit" — meant call by **name**.

## Takeaway

- **By-value** `x: Int` — argument evaluated exactly once, *before* the body runs; `x` holds a value.
- **By-name** `x: => Int` — compiler passes a **thunk** (`() => expr`); it runs every time the body
  mentions `x`: 0, 1, or many times.
- To get "at most once" with by-name: `lazy val v = x` inside the body.
- Short-circuit `&&`/`||` is just by-name: `s != null && s.length > 3` — `s.length` is never evaluated
  when `s` is null.
- Real uses: `&&`, `||`, `assert(cond, msg: => Any)`, `Option.getOrElse(default: => B)`,
  `Try { }`, `Future { }`.
- My mistake pattern: I reasoned about *when* the argument is evaluated but not *how many times*.
  Count the references to the parameter.
