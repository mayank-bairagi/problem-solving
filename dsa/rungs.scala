// Ladder to the sliding window, as folds.
// Fill in the ??? one rung at a time.  Run:  scala dsa/rungs.scala

def check[A](name: String, actual: => A, expected: A): Unit = {
  val r =
    try { val a = actual; if (a == expected) "PASS" else s"FAIL   got $a   want $expected" }
    catch { case e: Throwable => s"FAIL   threw ${e.getClass.getSimpleName}" }
  println("%-34s %s".format(name, r))
}

// ---------------------------------------------------------------- rung 1
// Frequency map. One foldLeft. Accumulator is the Map.
// Hint: what is the zero value, and what does the step function return?

def freq(s: String): Map[Char, Int] = s.foldLeft(Map()){
  (a,i) =>
}


println("--- rung 1: freq")
check("freq(\"\")",        freq(""),        Map())
check("freq(\"aab\")",     freq("aab"),     Map('a' -> 2, 'b' -> 1))
check("freq(\"ababc\")",   freq("ababc"),   Map('a' -> 2, 'b' -> 2, 'c' -> 1))

// ---------------------------------------------------------------- rung 2
// Distinct-count after each character.
// "abca" -> List(1, 2, 3, 3)     (after 'a', after 'ab', after 'abc', after 'abca')
// Hint: scanLeft gives you every intermediate accumulator. Watch its first element.

def runningDistinct(s: String): List[Int] = ???

println("--- rung 2: runningDistinct")
check("runningDistinct(\"\")",      runningDistinct(""),      List())
check("runningDistinct(\"abca\")",  runningDistinct("abca"),  List(1, 2, 3, 3))
check("runningDistinct(\"aaa\")",   runningDistinct("aaa"),   List(1, 1, 1))
