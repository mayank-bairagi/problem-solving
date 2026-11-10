// Booking ledger — see 02-booking-ledger.md for the spec.
// Fill in the ???s.  Run:  scala scala/02-booking-ledger.scala
// NB: the file won't compile until the implicit Ordering in HotelRevenue's companion
// exists (the topK checks need it) — do that first, then everything else runs as FAIL → PASS.
import scala.util.Try

def check[A](name: String, actual: => A, expected: A): Unit = {
  val r = Try(actual)
  val ok = r.toOption.contains(expected)
  println((if (ok) "PASS  " else "FAIL  ") + name + (if (ok) "" else s"\n        expected: $expected\n        actual:   $r"))
}

// ---- domain -------------------------------------------------------------

sealed trait Event
case class Book(id: String, hotelId: String, nights: Int, pricePerNight: Int) extends Event
case class Cancel(id: String) extends Event
case class Amend(id: String, newNights: Int) extends Event

sealed trait ParseError
case class UnknownType(t: String) extends ParseError
case class MalformedLine(line: String) extends ParseError
case class BadNumber(field: String, value: String) extends ParseError

sealed trait Status
case object Active extends Status
case object Cancelled extends Status

case class Booking(id: String, hotelId: String, nights: Int, pricePerNight: Int, status: Status)
case class Rejection(event: Event, reason: String)

case class HotelRevenue(hotelId: String, revenue: Long)
object HotelRevenue {
  // TODO: implicit Ordering — revenue desc, then hotelId asc
}

case class Report(parseErrors: List[ParseError], rejections: List[Rejection], top: List[HotelRevenue])

// ---- ledger -------------------------------------------------------------

object Ledger {
  type State = Map[String, Booking]

  def parse(line: String): Either[ParseError, Event] = ???

  def step(state: State, event: Event): Either[Rejection, State] = ???

  def replay(events: List[Event]): (State, List[Rejection]) = ???

  def topK[A: Ordering](xs: Iterable[A], k: Int): List[A] = ???

  def revenue(state: State): List[HotelRevenue] = ???

  def report(lines: List[String], k: Int): Report = ???
}

// ---- checks -------------------------------------------------------------

import Ledger._

// parse
check("parse BOOK",          parse("BOOK,b1,h1,3,100"), Right(Book("b1", "h1", 3, 100)))
check("parse CANCEL",        parse("CANCEL,b2"),        Right(Cancel("b2")))
check("parse AMEND",         parse("AMEND,b1,5"),       Right(Amend("b1", 5)))
check("parse unknown type",  parse("FOO,b6"),           Left(UnknownType("FOO")))
check("parse bad number",    parse("BOOK,b6,h1,x,100"), Left(BadNumber("nights", "x")))
check("parse bad price",     parse("BOOK,b6,h1,2,y"),   Left(BadNumber("pricePerNight", "y")))
check("parse malformed",     parse("BOOK,b7"),          Left(MalformedLine("BOOK,b7")))
check("parse empty",         parse(""),                 Left(MalformedLine("")))

// step
val s0: State = Map.empty
val s1 = Map("b1" -> Booking("b1", "h1", 3, 100, Active))
check("step book",           step(s0, Book("b1", "h1", 3, 100)), Right(s1))
check("step duplicate",      step(s1, Book("b1", "h9", 1, 1)),   Left(Rejection(Book("b1", "h9", 1, 1), "duplicate id")))
check("step book 0 nights",  step(s0, Book("b1", "h1", 0, 100)), Left(Rejection(Book("b1", "h1", 0, 100), "nights must be >= 1")))
check("step cancel",         step(s1, Cancel("b1")),             Right(Map("b1" -> Booking("b1", "h1", 3, 100, Cancelled))))
check("step cancel unknown", step(s1, Cancel("zz")),             Left(Rejection(Cancel("zz"), "unknown booking")))
check("step amend",          step(s1, Amend("b1", 5)),           Right(Map("b1" -> Booking("b1", "h1", 5, 100, Active))))
check("step amend 0",        step(s1, Amend("b1", 0)),           Left(Rejection(Amend("b1", 0), "nights must be >= 1")))
val sc = Map("b1" -> Booking("b1", "h1", 3, 100, Cancelled))
check("step cancel twice",   step(sc, Cancel("b1")),             Left(Rejection(Cancel("b1"), "already cancelled")))
check("step amend cancelled",step(sc, Amend("b1", 2)),           Left(Rejection(Amend("b1", 2), "booking cancelled")))

// replay
check("replay keeps going past rejections",
  replay(List(Book("b1", "h1", 3, 100), Cancel("zz"), Amend("b1", 5))),
  (Map("b1" -> Booking("b1", "h1", 5, 100, Active)), List(Rejection(Cancel("zz"), "unknown booking"))))
check("replay empty", replay(Nil), (Map.empty[String, Booking], Nil))

// topK / ordering
check("topK ints", topK(List(5, 1, 4), 2), List(1, 4))
check("topK ordering desc revenue then id",
  topK(List(HotelRevenue("h3", 500), HotelRevenue("h1", 600), HotelRevenue("h2", 500)), 3),
  List(HotelRevenue("h1", 600), HotelRevenue("h2", 500), HotelRevenue("h3", 500)))
check("topK k > size", topK(List(1), 5), List(1))

// revenue
check("revenue ignores cancelled",
  revenue(Map(
    "b1" -> Booking("b1", "h1", 5, 100, Active),
    "b2" -> Booking("b2", "h2", 2, 250, Cancelled),
    "b3" -> Booking("b3", "h1", 1, 100, Active))).sortBy(_.hotelId),
  List(HotelRevenue("h1", 600)))

// full report
val lines = List(
  "BOOK,b1,h1,3,100", "BOOK,b2,h2,2,250", "BOOK,b3,h1,1,100", "CANCEL,b2", "AMEND,b1,5",
  "BOOK,b4,h3,4,80", "BOOK,b1,h9,1,1", "CANCEL,b7", "AMEND,b2,3", "BOOK,b5,h2,2,250",
  "FOO,b6", "BOOK,b6,h1,x,100", "BOOK,b7", "AMEND,b4,0", "CANCEL,b2", "BOOK,b8,h3,1,180")
val r = report(lines, 2)
check("report parse errors", r.parseErrors,
  List(UnknownType("FOO"), BadNumber("nights", "x"), MalformedLine("BOOK,b7")))
check("report rejections", r.rejections.map(x => (x.event, x.reason)), List(
  (Book("b1", "h9", 1, 1), "duplicate id"),
  (Cancel("b7"), "unknown booking"),
  (Amend("b2", 3), "booking cancelled"),
  (Amend("b4", 0), "nights must be >= 1"),
  (Cancel("b2"), "already cancelled")))
check("report top-2 (h2/h3 tie on 500 → h2)", r.top, List(HotelRevenue("h1", 600), HotelRevenue("h2", 500)))
