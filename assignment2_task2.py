def longest(m):
    dp_array = []
    confirm_array = []
    directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    nm = len(m)*len(m[0])
    for i in range(nm):
        dp_array.append([])
        confirm_array.append(0)
        for j in range(len(directions)):
            dp_array[i].append(0)
    dp(m, dp_array,confirm_array, directions)
    return dp_array


def dp(m):
    pass

m1 = [[1,2,3],
      [4,5,6],
      [7,8,9]]
print(longest(m1))
