from typing import List
from collections import Counter
import math
from collections import defaultdict


class Solution:
    def countCompleteSubarrays(self, nums: List[int]) -> int:
        def at_most_k_distinct(k):
            freq = defaultdict(int)
            left = 0
            total = 0

            for right in range(len(nums)):
                freq[nums[right]] += 1

                while len(freq) > k:
                    freq[nums[left]] -= 1
                    if freq[nums[left]] == 0:
                        del freq[nums[left]]
                    left += 1

                total += right - left + 1

            return total
        distinct_count = len(set(nums))
        return at_most_k_distinct(distinct_count) - at_most_k_distinct(distinct_count - 1)
        


solution=Solution()
nums = [1, 3, 1, 2, 2]
print(solution.countCompleteSubarrays(nums))