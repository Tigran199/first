from typing import List

def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    max_sum = float('-inf')  
    n = len(nums)

    for i in range(n):
        current_sum = 0
        for j in range(i, min(i + k, n)):
            current_sum += nums[j]
            if current_sum > max_sum:
                max_sum = current_sum
    
    return max_sum

nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = find_maximal_subarray_sum(nums, k)
print(result)  
