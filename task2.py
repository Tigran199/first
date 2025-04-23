from typing import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:
    if len(data) < 2:
        return False
    
    if data[0] == 0 and data[1] == 1:
        pass  
    elif data[0] == 1 and data[1] == 1:
        pass  
    else:
        return False  
    
    for i in range(2, len(data)):
        if data[i] != data[i-1] + data[i-2]:
            return False
    
    return True

print(check_fibonacci([0, 1, 1, 2, 3, 5, 8]))
print(check_fibonacci([1, 1, 2, 3, 5, 8]))     
print(check_fibonacci([0, 1, 1, 2, 3, 6]))      
print(check_fibonacci([1, 2, 3, 5, 8]))        
