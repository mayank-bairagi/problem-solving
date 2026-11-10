# 06 — Max Profit, One Trade

## Statement

You get a list of stock prices, where `prices(i)` is the price on day `i`.
You can buy once and sell once later, and you have to buy before you sell.
Return the maximum profit, or `0` if no profitable trade exists.

```scala
def maxProfit(prices: List[Int]): Int
```

Examples:

```
List(7, 1, 5, 3, 6, 4)  -> 5   // buy at 1 (day 1), sell at 6 (day 4)
List(7, 6, 4, 3, 1)     -> 0   // prices only fall, so no profitable trade
```

## My attempt

Trace, starting from `(lo = 7, best = 0)`:

```
x    lo    profit    best
1    1      -6        0
5    1       4        4
3    1       2        4
6    1       5        5
4    1       3        5
```

```scala
def step(minSoFar: Int, best: Int, current: Int): (Int, Int) = {
  (math.min(minSoFar, current), math.max(best, current - minSoFar))
}

def maxProfit(prices: List[Int]): Int = {
  prices match {
    case Nil | _ :: Nil => 0
    case head :: tail => tail.foldLeft((head,0)){
       case ((lo,best),current) => step(lo,best,current)
    }._2
  }
}
```

## Takeaway
