"""
This file implements a longest_oscillation function where it finds the longest
oscillation in a list and return the length and a position array of the longest
oscillation.
It also implements a longest_walk function where it finds the longest increasing
walk in a table.

@author: Jin Luo
@since: 20/04/2020
@input          none
@output         none
@errorHandling  none
@knownBugs      longest_walk function does not always work

"""
def longest_oscillation(L):
    """
    Finds the longest oscillation in a list and return the length and positions
    of the oscillation.

    @param: L          a list of integers
    @return            a tuple with the first element containing the length
                       of the longest oscillation and and list containing
                       positions of the longest oscillation in L
    @complexity        O(n), n being the length of L
    """
    output_array = []
    sign = 0
    #sign will be used to indicate increase or decrease while oscillating
    #1 indicate increase, 2 indicate decrease 0 means they are equal
    if L == []:
        return (0, [])
    #check for empty list
    output_array.append(0)
    #first element will always be in the list
    set_num = 1
    #set_num will indicate if we can make changes to the output list
    #0 indicates we can set the last element of output list to the position,
    #1 indicates we can add the ith element into the list
    #2 indicates do nothing

    for i in range(1, len(L)): #O(n), n being the length of L
        if L[output_array[len(output_array)-1]] < L[i]: #O(1) amortised
            if sign == 1:
                set_num = 0
            else:
                set_num = 1
            sign = 1 #increasing as small to large
        elif L[output_array[len(output_array)-1]] > L[i]:
            if sign == 2:
                set_num = 0
            else:
                set_num = 1
            sign = 2 #decreasing as large to small
        else:
            sign = 0
            set_num = 2 #not set
        if set_num == 1:
            output_array.append(i) #add to output array
        elif set_num == 0:
            output_array[len(output_array)-1] = i
            #still increasing or decreasing, can take the bigger value or
            #smaller value
    return(len(output_array), output_array)

alist = [1,2,1,2,1,2,1,2,1,2]
blist = [1,1,6,1,1,-1]
clist = [1,5,7,4,6,8,6,7,1]
dlist = [1,2,3,4, 2]
#print(longest_oscillation(alist))
#print(longest_oscillation(blist))
#print(longest_oscillation(clist))
#print(longest_oscillation(dlist))

def longest_walk(M):
    """
    Implements a function to find the longest increasing walk in a table M
    This is done by using the largest element in the table and use recursion
    to find the largest number of walks
    The general idea of this function is to implement a recursive function
    to find the largest number of elements smaller than itself
    Then we can find the largest number, record the coordinates back to the
    smallest number and reverse the list to give us an increasing longest walk

    @param: M            a n*m sized table with possible duplicate integers
    @complexity          O(n*m), n being the number of rows and m being the
                         number of columns in the table M
    @return              a tuple containing the length of the longest walk and
                         the coordinates of the longest increasing walk from
                         start to end
    """
    dp_array = []
    #dp array is used for checking the previous steps, which records the
    #maximum number of elements that are smaller than the one at the i,j coord
    confirm_array = []
    #confirm array is to check whether we have visited the coordinate
    #this is because when we visit the smallest element in the table, there
    #will be nothing smaller than it so it will always be 0
    #so we do not know if it is just the smallest element or there is nothing
    #smaller than the element at the position
    #the confirm array provides a 1 if the coord is visited 0 if not
    directions = [(0,1),(0,-1),(1,1),(1,-1),(1,0),(-1,0),(-1,1),(-1,-1)]
    #directions is used to check all directions 
    
    for i in range(len(M)):
        dp_array.append([])
        confirm_array.append([])
        for j in range(len(M[0])):
            dp_array[i].append(0)
            confirm_array[i].append(0)
    #O(nm) up to this step to create new matrices of zeros
    M_max = []
    new_ara = []
    for i in range(len(M)): #O(n)
        M_max.append(max(M[i]))
    max_val = max(M_max)
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] == max_val:
                #loop through the entire table to find the largest element
                #takes O(nm) 
                new_ara.append((i,j))
                break
        else:
            continue
        break
    
    dp_walk(M, new_ara[0][0], new_ara[0][1], dp_array,confirm_array, directions)
    #calls dp_walk -> O(8nm) -> O(nm)
    #this does not always work as the maximum number might not always
    #mean it be the last element which has the longest walk
    #this can be solved by:
    #for i in range(len(M)):
    #   for j in range(len(M[0])):
    #       dp_walk(M, i, j, dp_array,confirm_array, directions)
    #but will take O(n^2m^2)
    for i in range(len(M)):
        for j in range(len(M[0])):
            if dp_array[i][j] == 0:
                #if not calculated yet by dp_walk
                for k in range(len(directions)): #O(1)
                    r = directions[k][0] + i
                    c = directions[k][1] + j
                    if 0<= r < len(M) and 0<= c < len(M[0]) and M[i][j] > M[r][c]:
                        dp_array[i][j] = max(dp_array[i][j], dp_array[r][c]+1)
                    #find the maximum it can add
    #O(nm), n being number of rows and m being number of columns
    
    
    end_max = []
    for i in range(len(M)):
        end_max.append(max(dp_array[i]))
    #find the maximum number in dp_array
    return_array = [0, []]
    for i in range(len(M)):
        for j in range(len(M[0])):
            if dp_array[i][j] == max(end_max):
                return_array[1].append((i,j))
        #append the coordinate of the max number 
                break
        else:
            continue
        break
    
    while len(return_array[1]) != max(end_max)+1:
        #O(nm) here since the worst case can be O(nm) because
        #max(end_max) + 1 cannot be greater than nm
        n = len(return_array[1])-1
        i = return_array[1][n][0] 
        j = return_array[1][n][1]
        #find the coord of last coord recorded in return_array 
        for k in range(len(directions)):
            #O(1) since always loop 8 cycles
            r = directions[k][0] + i
            c = directions[k][1] + j
            if 0<= r < len(M) and 0<= c < len(M[0]) and dp_array[r][c] == dp_array[i][j]-1:
                return_array[1].append((r, c))
                #append to the return_array if the element in dp_array is
                #1 smaller than the i,j element
                break
    
    return_array[0],return_array[1] = len(return_array[1]),return_array[1][::-1]
    #O(nm) for the reversed list
    return return_array

def dp_walk(M, i, j, dp_array,confirm_array, directions):
    """
    Used for assisting the implementation of longest_walk, which is basically
    a recursive function which calculates the max number of steps the i, j coord
    can take

    @param: M          M is the original table given to us
    @param: i          i th coord of the element (the row coord)
    @param: j          j th coord of the element (the column coord)
    @param: dp_array   an array full of zeroes to record the max number of steps
                       the coord can record
    @param: confirm_array     an array original full of zeros used for recording
                              if the coord has been visited or not
    
    """
    for k in range(len(directions)):
    #O(1) since it is constantly going be cycle of 8
        r = directions[k][0] + i
        c = directions[k][1] + j
        if confirm_array[i][j] == 1:
            return dp_array[i][j]
        #we use the confirm array to confirm if we have visited the coord
        #if it was visited and already has a value, we do not have to calculate
        #it again and save on time complexity
        elif 0<= r < len(M) and 0<= c < len(M[0]) and M[i][j] > M[r][c]:
            #given that r and c are in bounds and the new element is smaller
            #than the one we are on
            if confirm_array[r][c] == 1:
                #if steps at the new pos is calculated, we can use max function
                #to find the bigger between the two
                dp_array[i][j] = max(dp_array[r][c] + 1,dp_array[i][j])
            else:
                #if not calculated yet, we will have to call this recursively
                #worst case it would have to run O(mn)
                dp_array[i][j] = dp_walk(M, r, c, dp_array, confirm_array, directions) + 1
        
        if k == len(directions)-1:
        #after looping through every possible element next to it, we can
        #confirm the array has been visited and return the max value on the coord
            confirm_array[i][j] = 1
            return dp_array[i][j]
    #overall worst case time complexity O(nm), n being the number of rows and m
    #being number of columns in table M as we used confirm array to cut down work
    #that was already done


m1 = [[1,2,3],
      [4,5,6],
      [7,8,9]]
m2 = [[1,2,3],
      [1,2,1],
      [2,1,3]]
m3 = [[4,6],
      [7,2]]
m4 = [[9,8,7],
      [4,5,6],
      [3,2,1]]
m5 = [[5,4,3,2,1],
      [10,9,8,7,6]]
m6 = [[9,1,2],
      [1,1,3]]


#print(longest_walk(m1))
#print(longest_walk(m2))
#print(longest_walk(m3))
#print(longest_walk(m4))
#print(longest_walk(m5))
#print(longest_walk(m6))



