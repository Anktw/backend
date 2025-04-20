from typing import List
from collections import Counter
import math

class Solution:
    def numRabbits(self, answers: List[int]) -> int:
        count = Counter(answers)
        res = 0
        for k, v in count.items():
            group_size = k + 1
            num_groups = math.ceil(v / group_size)
            res += num_groups * group_size
        return res


solution=Solution()
answers=[1,1,2]
print(solution.numRabbits(answers)) # Output: 5