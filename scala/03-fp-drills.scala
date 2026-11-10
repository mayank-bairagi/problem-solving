// FP drills — small problems that showcase functional thinking.
// Fill in the ???s.  Run:  scala scala/03-fp-drills.scala
//
// Rules (these are what's actually being assessed):
//   - no var, no mutable collections, no while/for-loops (for-comprehensions are fine)
//   - no .get on Option, no exceptions, no null
//   - prefer fold / recursion / combinators; say the complexity out loud
//   - every match on a sealed type must be exhaustive

import scala.util.Try

def check[A](name: String, actual: => A, expected: A): Unit = {
  val r = Try(actual)
  val ok = r.toOption.contains(expected)
  println((if (ok) "PASS  " else "FAIL  ") + name + (if (ok) "" else s"\n        expected: $expected\n        actual:   $r"))
}

sealed trait Tree[+A]
case object Leaf extends Tree[Nothing]
case class Node[A](value: A, left: Tree[A], right: Tree[A]) extends Tree[A]

object Drills {

  // 1. Run-length encode: "aaabbc" -> List(('a',3), ('b',2), ('c',1))
  //    One pass. Think: what shape of accumulator lets you extend the last run?
  // --- my attempt 1: Map accumulator (WRONG — a Map cannot hold two separate 'a' runs,
  //     and has no order; also the fold's seed type must equal the step's return type)
  // def rle(s: String): List[(Char, Int)] = s.foldLeft(Map.empty[Char,Int]){
  //   case (a,xs) => a.updated(xs, a.getOrElse(xs, 0) + 1).toList
  // }
  //
  // --- my attempt 2: Info accumulator (right idea; bugs: `previous` never updated on a
  //     run change, new run hardcoded to ('a',1), and the final run never flushed/reversed)
  // case class Info(previous: Char, res: List[(Char,Int)], tpl: (Char,Int))
  // str.toList match {
  //   case Nil => Nil
  //   case head :: tail => tail.foldLeft(Info(head, Nil, (head,1))) {
  //     case (Info(p,r,t), xs) => if (p == xs) Info(p,r,(p,t._2+1)) else Info(p, t :: r, ('a',1))
  //   }
  // }
  //
  // --- fixed: attempt 2 with `previous` dropped (t._1 already holds it), the new run
  //     seeded from the current char, and a flush + reverse after the fold.
  private case class Runs(done: List[(Char, Int)], current: (Char, Int))

  def rle(s: String): List[(Char, Int)] = s.toList match {
    case Nil => Nil
    case head :: tail =>
      val acc = tail.foldLeft(Runs(Nil, (head, 1))) { case (Runs(done, (c, n)), ch) =>
        if (ch == c) Runs(done, (c, n + 1))
        else         Runs((c, n) :: done, (ch, 1))
      }
      (acc.current :: acc.done).reverse
  }

  // Alternative worth knowing — recursive span, no accumulator at all:
  //   def rle(s: String): List[(Char, Int)] = s.toList match {
  //     case Nil    => Nil
  //     case h :: _ => val (run, rest) = s.toList.span(_ == h)
  //                    (h, run.length) :: rle(rest.mkString)
  //   }

  // 2. Balanced parentheses. Other characters are ignored.
  //    Do it WITHOUT a stack and WITHOUT early return — one fold.
  //    Hint: what can an accumulator hold that represents "depth, or already broken"?
  def balanced(s: String): Boolean = ???

  // 3. Group anagrams. Output: groups sorted by their first word, words sorted within a group.
  def anagrams(words: List[String]): List[List[String]] = ???

  // 4. Moving average over a window of k. Fewer than k elements (or k <= 0) -> Nil.
  def movingAvg(xs: List[Int], k: Int): List[Double] = ???

  // 5. First character that appears exactly once. "swiss" -> Some('w'), "aabb" -> None
  def firstNonRepeating(s: String): Option[Char] = ???

  // 6. Split a list of Eithers, preserving order in both outputs. One traversal.
  def partitionEithers[E, A](xs: List[Either[E, A]]): (List[E], List[A]) = ???

  // 7. ONE generic fold over the tree; then express the other three in terms of it.
  //    Do not pattern-match on Tree anywhere except inside `fold`.
  def fold[A, B](t: Tree[A], z: B)(f: (B, A, B) => B): B = ???
  def sum(t: Tree[Int]): Int = ???
  def depth[A](t: Tree[A]): Int = ???                 // Leaf = 0, single Node = 1
  def toListInOrder[A](t: Tree[A]): List[A] = ???     // left, value, right
}

import Drills._

check("rle basic",        rle("aaabbc"),        List(('a',3), ('b',2), ('c',1)))
check("rle single",       rle("a"),             List(('a',1)))
check("rle no runs",      rle("abc"),           List(('a',1), ('b',1), ('c',1)))
check("rle empty",        rle(""),              List())
check("rle repeat later", rle("aabaa"),         List(('a',2), ('b',1), ('a',2)))

check("balanced ok",        balanced("(()())"),  true)
check("balanced wrong order",balanced("())("),   false)
check("balanced empty",     balanced(""),        true)
check("balanced with text", balanced("(a(b)c)"), true)
check("balanced unclosed",  balanced("(("),      false)

check("anagrams", anagrams(List("eat","tea","tan","ate","nat","bat")),
  List(List("ate","eat","tea"), List("bat"), List("nat","tan")))
check("anagrams empty", anagrams(Nil), Nil)

check("movingAvg",        movingAvg(List(1,2,3,4,5), 3), List(2.0, 3.0, 4.0))
check("movingAvg short",  movingAvg(List(1,2), 3),       Nil)
check("movingAvg k=1",    movingAvg(List(1,2), 1),       List(1.0, 2.0))
check("movingAvg k=0",    movingAvg(List(1,2), 0),       Nil)

check("firstNonRepeating", firstNonRepeating("swiss"), Some('w'))
check("fnr none",          firstNonRepeating("aabb"),  None)
check("fnr empty",         firstNonRepeating(""),      None)

check("partitionEithers",
  partitionEithers(List(Right(1), Left("a"), Right(2), Left("b"))),
  (List("a","b"), List(1,2)))
check("partitionEithers empty", partitionEithers(List.empty[Either[String, Int]]), (Nil, Nil))

val t: Tree[Int] = Node(5, Node(3, Node(1, Leaf, Leaf), Leaf), Node(8, Leaf, Node(9, Leaf, Leaf)))
check("tree sum",     sum(t),             26)
check("tree sum leaf",sum(Leaf),          0)
check("tree depth",   depth(t),           3)
check("tree depth leaf", depth(Leaf),     0)
check("tree inorder", toListInOrder(t),   List(1,3,5,8,9))
