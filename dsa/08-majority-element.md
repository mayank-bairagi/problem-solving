# 08 — Majority Element, Boyer–Moore (Easy–Medium)

## Statement

Find the value that appears more than n/2 times. Target: O(n) time and O(1) space, so no hash map.

```
2, 2, 1, 1, 1, 2, 2  -> 2
```

## My attempt

### Algorithm

State: `(cand, count)`

```
count == 0 => (x, 1)
x == cand  => (cand, count + 1)
otherwise  => (cand, count - 1)
```

Seed with the first element: `(cand = 2, count = 1)`

### Dry run

```
x      2  1  1  1  2  2
cand   2  2  2  1  1  2
count  2  1  0  1  0  1
```

Answer: `cand = 2`

### Code

```scala
def step(s:(Int,Int),x:Int):(Int,Int) = {
  val (cand,count) = s
  if(count == 0) (x,1)
  else if(cand == x) (cand,count+1)
  else (cand,count-1)
}

def majorityElem(xs:List[Int]):Int = xs match {
  case h :: t => t.foldLeft((h,1))(step)._1
  case Nil    => throw new IllegalArgumentException("input should not be empty")
}

val xs = List(2, 2, 1, 1, 1, 2, 2)
majorityElem(xs)  // 2
```

## Takeaway
