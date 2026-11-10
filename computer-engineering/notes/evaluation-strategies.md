# Evaluation strategies

From: `01-call-by-value-vs-call-by-name.md`

| strategy | when the argument is evaluated | how many times |
|---|---|---|
| call-by-value `x: T` | once, before the call | exactly 1 |
| call-by-name `x: => T` | inside the body, at each use (a thunk) | 0, 1, or many |
| `lazy val` | at first use | at most 1 (cached) |

Rule of thumb: a by-name argument is not a value, it is an *expression you handed over*.
To reason about it, **count the references to the parameter in the body** — that is the number
of times the expression runs.

Why it matters: short-circuit `&&`/`||`, cheap `assert` messages, `getOrElse` defaults,
`Try {}` / `Future {}` blocks that must run inside the callee.
