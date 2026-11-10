# 01 — Substitution Model

## Concept

Three things every language gives you: primitive expressions, means of combination, means of abstraction.

Evaluating a combination: evaluate operator and operands, then apply the operator to the argument values.
Applying a user-defined procedure: substitute each argument for its parameter in the body, then evaluate the body.

## Statement

```scala
def square(x: Int) = x * x
def sumOfSquares(x: Int, y: Int) = square(x) + square(y)
def f(a: Int) = sumOfSquares(a + 1, a * 2)
```

Trace `f(5)` by hand with the substitution model, evaluating operands *before* substituting.
One line per step, no skipped steps.

## My attempt

```
f(5)
→ sumOfSquares(5 + 1, 5 * 2)
→
```

## Takeaway
