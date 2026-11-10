# Scala refresher

Interview prep (hiring-manager round 2026-09-17, FP/Scala round 2026-09-28).
Scala 2.12 only — run with `scala file.scala`.

Every step has the same shape:
**idea** (one line) → **example** (runnable, output in comments) → **gotchas** →
**check question** → **my attempt** (kept as written) → **takeaway**.

| # | Topic | Status |
|---|---|---|
| 1 | Case classes, ADTs, pattern matching | ✅ |
| 2 | Collections, laziness | ✅ |
| 3 | Option / Either / Try, for-comprehensions | ✅ |
| 4 | Functions as values | ✅ |
| 5 | Traits, companions, apply/unapply | ✅ |
| 6 | Implicits & type classes | ✅ check question skipped |
| 7a | Variance & type bounds | ✅ check question skipped |
| 7b | Futures, tail recursion | ✅ |

---

## 1. Case classes, ADTs, pattern matching

**Idea:** describe data as immutable types; the compiler checks you handled every case.

### Case class
```scala
case class Booking(id: Int, nights: Int)

val b  = Booking(1, 3)          // no `new` — companion `apply` is generated
val b2 = b.copy(nights = 5)     // Booking(1,5) — b is unchanged
b == Booking(1, 3)              // true — compares fields, not references
```
You also get `toString`, `hashCode`, and `unapply` (so it works in `match`).
Equal fields mean equal values, so a case class is safe to use as a `Map` key.

### ADT = `sealed trait` + cases
```scala
sealed trait Payment                          // sealed: every subtype is in this file
case class Card(last4: String) extends Payment
case class Wallet(name: String) extends Payment
case object Cash extends Payment

def label(p: Payment): String = p match {
  case Card(l)   => s"card *$l"
  case Wallet(n) => n
  case Cash      => "cash"
}
// delete one case → warning: "match may not be exhaustive"
```
**Exhaustive** means every possible input has a case. `sealed` is what lets
the compiler check that: it knows the full list of subtypes.

### Gotchas
```scala
val Max = 10
x match {
  case Max => "ten"      // Uppercase → compares: x == Max
  case max => "other"    // lowercase → NEW variable, matches anything
}
```
- The first matching case wins, so order matters.
- `match` is an expression that returns a value. If one branch gives `Int` and
  another gives `String`, the result type is `Any`, which is almost always a bug.
- `case l: List[Int]` only checks `List`. The `Int` is erased at runtime.

### Check question
```scala
sealed trait Shape
case class Circle(r: Double) extends Shape
case class Rect(w: Double, h: Double) extends Shape

def area(s: Shape) = s match {
  case Circle(r) => math.Pi * r * r
  case Rect(w, h) if w == h => w * w
}
```
What does the compiler say, what happens for `Rect(2, 3)`, and why?

### My attempt
> It will fail with match case exception as Rect is not covered for the
> scenarios where w != h

Runtime part correct. Did not answer the compiler part; said "don't know".

### Takeaway
- Runtime: `scala.MatchError: Rect(2.0,3.0)`.
- Compiler: **Scala 2 says nothing** (checked on 2.12, even with `-Xlint`).
  A guard (`if ...`) is runtime code, so the compiler can't evaluate it. Scala 2
  assumes the guarded case covers `Rect`. Scala 3 assumes it doesn't, and warns.
- If you remove the `Rect` case entirely, both versions warn: "would fail on Rect(_, _)".
- Fix: move the condition inside the branch.
  ```scala
  case Rect(w, h) => if (w == h) w * w else w * h
  ```
- **Say:** "A guard silently opts that case out of exhaustiveness checking."

---

## 2. Collections

**Idea:** chain small, pure transformations, and know what each one costs.

### The core combinators
```scala
val xs = List(1, 2, 3, 4)

xs.map(_ * 10)                // List(10, 20, 30, 40)
xs.filter(_ % 2 == 0)         // List(2, 4)
xs.flatMap(x => List(x, x))   // List(1, 1, 2, 2, 3, 3, 4, 4)
xs.foldLeft(0)(_ + _)         // 10
xs.partition(_ > 2)           // (List(3, 4), List(1, 2))
xs.groupBy(_ % 2)             // Map(1 -> List(1, 3), 0 -> List(2, 4))
List("b", "a").zipWithIndex   // List((b,0), (a,1))

List.empty[Int].reduce(_ + _) // throws on empty — prefer foldLeft
```

`foldLeft` can build almost anything. Word count:
```scala
List("a", "b", "a").foldLeft(Map.empty[String, Int]) { (acc, w) =>
  acc.updated(w, acc.getOrElse(w, 0) + 1)
}                              // Map(a -> 2, b -> 1)
```
`groupBy` keeps every element of every group in memory. A fold into
`Map[key, total]` keeps only the running totals.

### Which collection
| Need | Use | Why |
|---|---|---|
| Recursion, `h :: t`, prepend | `List` | head/prepend O(1); index/length/append O(n) |
| General default, indexing | `Vector` | ~O(1) index, append, update |
| Lookup | `Map` / `Set` | ~O(1) get; `TreeMap` if you need sorted keys |
| Hot loop inside one method | `ArrayBuffer`, `mutable.Map` | fast; never let it escape the method |

### Laziness
```scala
def dbl(x: Int) = { println(s"map $x"); x * 2 }
val ys = List(1, 2, 3, 4, 5, 6)

ys.map(dbl).filter(_ > 4).take(2)
// prints map 1 … map 6 — maps all 6, builds a list at each step → List(6, 8)

ys.view.map(dbl).filter(_ > 4).take(2).toList
// prints map 1 … map 4 — one element at a time, stops once it has 2 → List(6, 8)
```
```scala
val it = Iterator(1, 2, 3)
it.size     // 3        — walked to the end
it.toList   // List()   — nothing left: an Iterator is used up after one pass

Stream.from(1).map(_ * 2).take(3).toList   // List(2, 4, 6) — infinite, fine
                                           // (Stream in 2.12; LazyList is 2.13+)
```
| | strict | `view` | `Iterator` | `Stream` |
|---|---|---|---|---|
| Traverse twice? | yes | yes, redoes the work | **no**, used up | yes, cached |
| Use for | small data, reuse | one pipeline, early exit | read a source once | infinite sequences |

Classic bug: `if (it.size > 0) it.foreach(...)`. `size` used up the iterator,
so `foreach` sees nothing.

### Check question
`bookings: List[Booking]`, `case class Booking(hotelId: Int, nights: Int, price: BigDecimal)`,
hotels repeat. Top-3 hotels by total revenue (`nights * price`) in combinators;
which step costs the most?

### My attempt
> foldLeft or groupBy → Map[hotelId, aggregated revenue]; toList; sort by price;
> take 3. Alternatively a min-heap for top-k.
>
> foldLeft O(N); toList O(H); sort H log H — so complexity is H log H.
> Heap variant: O(N).
>
> (after nudge) heap saves most when almost all hotel IDs are unique; with a
> small fixed H (say 100) and huge N, sorting is over a tiny set and doesn't hurt.

### Takeaway
```scala
bookings
  .foldLeft(Map.empty[Int, BigDecimal]) { (acc, b) =>
    acc.updated(b.hotelId, acc.getOrElse(b.hotelId, BigDecimal(0)) + b.nights * b.price)
  }
  .toList
  .sortBy(-_._2)   // by revenue, descending
  .take(3)
```
- Approach right. Mentioning the heap is the Lead-level signal.
- Slip 1: said "sort by price". It should be total revenue, descending.
- Slip 2: dropped the fold's `O(N)`. Total is **`O(N + H log H)`**
  (N bookings, H distinct hotels). H ≤ N, so the fold usually dominates.
- **Say:** "I'd sort first and use a heap only if H is large." Knowing when
  *not* to optimise is the signal.

---

## 3. Option / Either / Try

**Idea:** failure is a return value, not a thrown exception.

```scala
val m = Map("a" -> 1)
m.get("a")                  // Some(1)
m.get("z")                  // None
m.get("z").getOrElse(0)     // 0
m.get("a").map(_ + 1)       // Some(2)

def parse(s: String): Either[String, Int] =
  if (s.nonEmpty && s.forall(_.isDigit)) Right(s.toInt)
  else Left(s"not a number: $s")

parse("42")                 // Right(42)
parse("x")                  // Left(not a number: x)

import scala.util.Try
Try("x".toInt)              // Failure(NumberFormatException: For input string: "x")
Try("x".toInt).toEither     // Left(NumberFormatException...)
```
| Type | Means | Use for |
|---|---|---|
| `Option[A]` | maybe missing, no reason | lookups, `find`, `headOption` |
| `Either[E, A]` | failed, with a reason | domain logic. `E` = your own sealed error type |
| `Try[A]` | caught an exception | wrapping Java/IO calls; convert with `.toEither` |

Never call `.get`. Use `map`, `flatMap`, `getOrElse`, `fold`, `toRight`.

### for-comprehension
```scala
for { a <- parse("1"); b <- parse("2") } yield a + b   // Right(3)
for { a <- parse("x"); b <- parse("2") } yield a + b   // Left(not a number: x)

// the compiler rewrites it to:
parse("1").flatMap(a => parse("2").map(b => a + b))
```
- Every `<-` except the last becomes `flatMap`, the last becomes `map`, and `if` becomes `withFilter`.
- The first `None` or `Left` stops the chain.
- **Every `<-` must use the same container.** Convert first:
  `opt.toRight("err")`, `either.toOption`.
- `Either` stops at the first error. To collect *all* errors, use cats `Validated`
  or `partition` a `List[Either]`.

*traverse*: turn a `List[Option[A]]` into an `Option[List[A]]`:
```scala
ids.foldRight(Option(List.empty[User])) { (id, acc) =>
  for { u <- user(id); us <- acc } yield u :: us
}   // Some(all users), or None if any id is missing
```

### Check question
```scala
def parse(s: String): Either[String, Int]
def lookup(i: Int): Option[Hotel]

val h = for {
  i <- parse("42")
  hotel <- lookup(i)
} yield hotel
```
Explain, via the desugaring, why this doesn't compile; smallest fix.

### My attempt
> it fails because the return type of parse and lookup functions are different;
> for flatMap / for-comprehension we need same type.
>
> (fix) update the signature of lookup to return Either; in case of None pass
> some domain exception in Left.

### Takeaway
- The diagnosis was right. Say the desugaring precisely:
  `parse("42").flatMap(i => lookup(i).map(...))`. `Either.flatMap` needs a
  function that returns an `Either`, but this one returns an `Option`.
- Slip: changing `lookup`'s signature isn't the *smallest* fix, because it
  affects every caller. Fix it at the call site:
  ```scala
  hotel <- lookup(i).toRight("hotel not found")
  ```
- Convert in the direction `Option → Either`, which adds a reason. `.toOption`
  would throw away the parse error.
- Wording: say **domain error**, not "domain exception". A `Left` holds a plain
  value (`Left(HotelNotFound(i))`), not a `Throwable`.

Side Qs: ADT = **Algebraic** Data Type (sealed trait = "one of", case class =
"all of"). `Option` stops at the first `None` just like `Either` stops at the
first `Left`. It just can't say why.

---

## 4. Functions as values

**Idea:** a function is a value. You can pass it, return it, store it, or fill in some of its arguments.

```scala
def add(a: Int, b: Int) = a + b          // method: belongs to an object, not a value
val addF = (a: Int, b: Int) => a + b     // function: a value (an object with `apply`)
val addF2 = add _                        // method → function ("eta-expansion")
```

### Currying vs partial application vs partial function
```scala
// Currying: one argument list at a time
def addC(a: Int)(b: Int) = a + b
val plus5 = addC(5) _                    // Int => Int
plus5(1)                                 // 6

// Partial application: fix some arguments now, the rest later
def log(level: String, msg: String) = s"[$level] $msg"
val warn = log("WARN", _: String)
warn("disk full")                        // [WARN] disk full

// Partial function: only defined for SOME inputs
val half: PartialFunction[Int, Int] = { case x if x % 2 == 0 => x / 2 }
half.isDefinedAt(3)                      // false
half(3)                                  // MatchError
half.lift(3)                             // None — lift makes it safe: Int => Option[Int]
List(1, 2, 3, 4).collect(half)           // List(1, 2) — skips inputs it isn't defined for
```
Interviewers mix up "partial application" and "partial function" on purpose. They are unrelated.

Why multiple parameter lists are useful:
1. Type inference goes left to right: `foldLeft(0)(_ + _)` knows `_` is `Int`.
2. Implicits get their own list at the end.
3. Block syntax: `retry(3) { ... }`.

### Composition, by-name, lazy
```scala
val inc = (x: Int) => x + 1
val dbl = (x: Int) => x * 2
(inc andThen dbl)(3)      // 8 — inc first
(inc compose dbl)(3)      // 7 — dbl first

def twice(x: => Int) = x + x             // by-name: evaluated every time it's used
twice { println("hi"); 1 }               // prints "hi" twice → 2

lazy val y = { println("hi"); 1 }        // evaluated once, on first use, then cached
```
A closure captures the *variable*, not its value, so it sees later changes to a `var`.

### Check question
```scala
def timesN(n: Int)(x: Int): Int = n * x
val triple = timesN(3) _
val r1 = List(1, 2, 3).map(triple)
val r2 = List(1, 2, 3).map(timesN(3))
val r3 = List(1, 2, 3).collect { case x if x > 1 => timesN(3)(x) }
```
Which compile in 2.12, what do they produce, what does r3's block desugar to?

### My attempt
> triple: partial application, timesN eta-expanded, triple is Int => Int.
> r1 → List(3,6,9). r2 → same, List(3,6,9).
> r3 → match error as partial function is not defined for x <= 1.
>
> (after nudge) ahh collect is filter(isDefinedAt) + map → List(6, 9).
> (desugaring) "you answer".

### Takeaway
- `triple`, `r1`, and `r2` were correct. `r2` compiles because `map` *expects* a
  function, so the compiler converts `timesN(3)` for you. Without an expected
  type (`val t = timesN(3)`), 2.12 gives the error "missing argument list".
- Slip: `r3`. `collect` checks `isDefinedAt` before calling, so the result is `List(6, 9)`.
- Desugaring: the compiler creates a `new PartialFunction[Int, Int]` with
  `isDefinedAt(x) = x > 1` and `apply(x)` = the match.
- **Say:** "The expected type decides what a `{ case … }` block becomes:
  a `PartialFunction` if one is expected, a plain function otherwise."

---

## 5. Traits, companions, apply/unapply

**Idea:** traits are mixins you can stack. `super` inside a trait means "the next trait in line", not the parent you wrote.

### Stackable traits
```scala
trait Greeter { def greet(n: String) = s"Hello $n" }
trait Loud extends Greeter {
  override def greet(n: String) = super.greet(n).toUpperCase
}
class Svc extends Greeter with Loud
new Svc().greet("bob")      // HELLO BOB
```
**Linearization** decides which method runs. For `class C extends A with B`,
the rightmost trait wins: `C → B → A`. To build the order:
1. Write out each parent's own chain, from right to left.
2. If a type appears more than once, keep only its **last** occurrence.

`super` in a trait means the *next type in that chain*. The chain depends on
the class that mixes the traits in, not on where the trait is defined.

- Two traits that define the same method *without* `override` → compile error.
  The class has to override it.
- Traits can't take constructor parameters in 2.12. Use an abstract class if you need them.
- Self-type `trait Svc { this: Repo => }` means Svc *requires* a Repo, while
  `extends` means Svc *is* a Repo.

### Companion object, apply, unapply
```scala
class Email private (val value: String)          // constructor hidden
object Email {                                   // companion: same name, same file
  def apply(s: String): Option[Email] =          // smart constructor
    if (s.contains("@")) Some(new Email(s)) else None
  def unapply(e: Email): Option[String] = Some(e.value)   // powers `case Email(v)`
}
Email("a@b.com")                 // Some(Email) — Email(...) is Email.apply(...)
Email("oops")                    // None

object Even { def unapply(n: Int): Boolean = n % 2 == 0 }
4 match { case Even() => "even"; case _ => "odd" }   // "even"
```
- The companion object can access the class's private members.
- Equality: `==` calls `.equals` and is null-safe. `eq` compares references.
  `Array` uses reference equality even with `==`.

### Check question
```scala
trait A { def msg = "A" }
trait B extends A { override def msg = "B" + super.msg }
trait C extends A { override def msg = "C" + super.msg }
class D extends B with C
class E extends C with B
println(new D().msg); println(new E().msg)
```

### My attempt
> D → "C", E → "B"                              (ignored the super chain)
> D → "CABA", E → "BACA"                        (A visited twice; took super = declared parent)
> "if I go with precedence C would get more over B as C appears later, so I
>  thought linearization of C should be preserved?"
> "you reply"

### Takeaway
- Answer: **`CBA`** and **`BCA`** (checked on 2.12).
- Working for D:
  ```
  C's chain: C, A      B's chain: B, A
  D + (right to left) → D, C, A, B, A
  keep last A         → D, C, B, A
  msg: "C" + super(→B) → "C" + "B" + super(→A) → "CBA"
  ```
- Mistake 1: forgot that each `msg` calls `super.msg`. Follow the chain all the way down.
- Mistake 2: treated `super` as the declared parent. It's the next type in the chain.
- Keeping the last occurrence preserves both C's order and B's order, so
  precedence and preservation don't conflict.
- **Say:** "`super` in a trait is resolved late, by the class that mixes it in.
  That's why the order of `with` matters."

---

## 6. Implicits & type classes

**Idea:** an implicit is a value the compiler fills in for you. It finds the value by its **type**.

### Implicit parameters
```scala
case class Timeout(ms: Int)
def call(url: String)(implicit t: Timeout) = s"GET $url, timeout ${t.ms}ms"

implicit val t: Timeout = Timeout(500)
call("/hotels")             // GET /hotels, timeout 500ms — t passed automatically
```
- Exactly one implicit of that type must be in scope. With none you get "could
  not find", with two you get "ambiguous".
- The lookup is by type only, so never write `implicit val x: Int`. Wrap it
  (`Timeout`) as above.
- **Where the compiler looks:** (1) local scope and imports, then (2) the
  companion objects of the type and of its type arguments. Putting an instance
  in the companion means callers don't need an import.

### Type class
A type class adds behaviour to a type without changing the type:
```scala
trait Show[A] { def show(a: A): String }            // 1. the type class

object Show {                                       // 2. instances
  implicit val intShow: Show[Int] = (a: Int) => s"int $a"
  implicit def listShow[A](implicit s: Show[A]): Show[List[A]] =
    (as: List[A]) => as.map(s.show).mkString("[", ", ", "]")
}

def render[A](a: A)(implicit s: Show[A]) = s.show(a)        // 3. use it
def render2[A: Show](a: A) = implicitly[Show[A]].show(a)    //    same, shorter syntax

render(1)            // int 1
render(List(1, 2))   // [int 1, int 2] — compiler built listShow(intShow)
render("x")          // compile error: could not find implicit Show[String]
```
Why use a type class instead of inheritance:
- You can add it to types you don't own, like `Int` or library classes.
- A type can have several instances, e.g. an `Ordering` by price and another by date.
- A missing instance is a compile error, not a runtime error.

Real type classes: `Ordering` (used by `sorted`/`max`), `Numeric` (used by `sum`), Circe `Encoder`, Cats `Monoid`.

### Extension methods
```scala
implicit class RichInt(val n: Int) extends AnyVal { def nights = s"$n nights" }
3.nights             // "3 nights" — AnyVal avoids allocating a wrapper
```
Use implicit classes for extension methods and implicit params for context.
**Avoid implicit conversions** (`implicit def intToX(i: Int): X`), because they
silently make wrong code compile.

| Scala 2 | Scala 3 |
|---|---|
| `implicit val` | `given` |
| `(implicit x: T)` | `(using x: T)` |
| `implicit class` | `extension` |
| `implicitly[T]` | `summon[T]` |

To debug, write `implicitly[Show[Booking]]` and see whether it compiles.

### Check question (skipped)
`List(Booking(...)).sorted` won't compile.
(a) What exactly is the compiler looking for, and where?
(b) Two different ways to make it compile.
(c) Sort by price at one call site, by nights at another — how, and what does
    that say about type classes vs `Comparable`?

### My attempt
_(skipped)_

---

## 7a. Variance & type bounds

**Idea:** if `Cat` is a subtype of `Animal`, variance says whether `Box[Cat]` is a subtype of `Box[Animal]`.

```scala
class Animal; class Cat extends Animal; class Dog extends Animal

val cats: List[Cat]       = List(new Cat)
val animals: List[Animal] = cats          // OK — List[+A] is covariant

val arr: Array[Cat]       = Array(new Cat)
val arr2: Array[Animal]   = arr           // compile error — Array[A] is invariant
// If this were allowed: arr2(0) = new Dog → a Dog inside an Array[Cat].

val showAnimal: Animal => String = _ => "animal"
val showCat: Cat => String       = showAnimal   // OK — function input is contravariant
// Something that can handle any Animal can handle a Cat.
```
| Marker | Meaning | Rule | Examples |
|---|---|---|---|
| `[A]` | invariant: unrelated | can read and write | `Array`, mutable collections, `Ordering` |
| `[+A]` | covariant: `Box[Cat] <: Box[Animal]` | A only as **output** | `List`, `Option`, `Vector`, `Map[K, +V]` |
| `[-A]` | contravariant: `Box[Animal] <: Box[Cat]` | A only as **input** | function params: `Function1[-T, +R]` |

### Bounds
```scala
val mixed = new Dog :: cats          // List[Animal]
// because  def ::[B >: A](x: B): List[B]   — lower bound: widen to a common supertype

def maxU[A <: Comparable[A]](xs: List[A])   // upper bound: A must BE a Comparable
def maxC[A: Ordering](xs: List[A])          // context bound: an Ordering[A] must EXIST
```
The lower bound `B >: A` is how a covariant `List` can still accept new elements.
Contrast: an upper bound uses subtyping, a context bound uses a type class.

`None` is `Option[Nothing]` and `Nil` is `List[Nothing]`. Because `Nothing` is
a subtype of everything, covariance lets them fit any `Option[A]` or `List[A]`.

### Check question (skipped)
`trait Sink[-A] { def put(a: A): Unit }; val catSink: Sink[Cat] = animalSink`
(a) why safe from what `put` does; (b) what if `Sink[+A]`; (c) combining two
covariant `Source[+A]`s — which bound?

---

## 7b. Futures, tail recursion

### Future
**Idea:** a `Future` starts running **as soon as it's created**.
```scala
import scala.concurrent._, ExecutionContext.Implicits.global

// PARALLEL — both start before the for
val fa = Future { slow(1) }
val fb = Future { slow(2) }
for { a <- fa; b <- fb } yield a + b             // ~1s

// SEQUENTIAL — the second Future isn't created until the first finishes
for { a <- Future(slow(1)); b <- Future(slow(2)) } yield a + b   // ~2s
```
- An exception inside `Future { }` gives a `Failure`. `map` and `flatMap` skip
  over it, just like with `Either`. `recover` is the catch.
- `Future.sequence`: `List[Future[A]] → Future[List[A]]`, which fails if any
  one fails. `Future.traverse(ids)(fetch)` = `map` then `sequence`.
- `ExecutionContext` is where the code runs. Don't block the `global` pool. Use
  `blocking { }` or a separate pool for IO.
- `Promise` = the write side of a Future. Use it to wrap callback APIs.
- `Await.result` only at the edges of the program (main, tests).
- Future starts immediately and runs once. cats-effect `IO` / ZIO is a
  description that doesn't run until you run it, so it can be retried. Mention
  this if the team uses them.

### Tail recursion
```scala
def sum(xs: List[Int]): Int = xs match {
  case Nil    => 0
  case h :: t => h + sum(t)       // `+` runs AFTER the call → a stack frame per element → StackOverflow
}

def sum(xs: List[Int]): Int = {
  @tailrec def go(rest: List[Int], acc: Int): Int = rest match {
    case Nil    => acc
    case h :: t => go(t, acc + h) // the call is the last thing → compiled into a loop
  }
  go(xs, 0)
}
```
- `@tailrec` makes compilation fail if the method can't be optimised. Always add it.
- This only works for a method calling itself. For mutual recursion, use `TailCalls`.
- `foldLeft` is already stack-safe. `List.foldRight` in 2.12 is not.

### Quick-fire
- `lazy val` is thread-safe.
- A trait's `val` may still be `null` during initialisation. Use `lazy val` or `def`.
- Types: `Any` is the top type. `AnyVal` covers `Int`, `Boolean`, etc. `AnyRef`
  covers objects. `Nothing` is a subtype of everything (e.g. `throw`). `Null` is
  the type of `null`. `Unit` is `()`.
- String interpolators: `s"$x"`, `f"$x%.2f"`, `raw"\n"`.
