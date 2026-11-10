// nums(i) = the furthest you can jump forward from index i
// Array(2, 3, 1, 1, 4) → true   (0 → 1 → 4)
// Array(3, 2, 1, 0, 4) → false  (every path gets stuck at index 3)
val a = Array(2, 3, 1, 1, 4)

/*
i     0    1
num   2
reach 0
 */

def canJump(nums: Array[Int]): Boolean = {
  var reach = 0
  var i = 0
  while(i < nums.length){
    if(i > reach) return false
    reach = math.max(reach, i + nums(i))
    i += 1
  }
  true
}
