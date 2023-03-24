"""
This file implements radix sort algorithm with help of count sort. Then there
is an analysis of runtime of radix sort with different bases. The last function
implemented is used for find p-rotations.

@author: Jin Luo
@since: 21/03/2020
@input          none
@output         none
@errorHandling  none
@knownBugs      none

"""
import math, random, time, csv
"""
a count sort template from lecture notes (please ignore)
def count_sort(num_list):
    max_value = max(num_list)
    count_array = [0] * (max_value+1)
    position_array = [0] * (max_value+1)
    output_array = [0] * len(num_list)
    for number in num_list:
        count_array[number] += 1
    position_array[0] = 1
    for i in range(1, len(count_array)):
        position_array[i] = position_array[i-1] + count_array[i-1]
    for number in num_list:
        output_array[position_array[number]-1] = number
        position_array[number] += 1
    return(output_array)
"""

#the new count sort will include index and base
def count_sort(num_list, index, base):
    """
    Implements a count sort algorithm that is a non-comparison sorting algorithm.
    This is not required by the assignment specifically, however, in order to
    achieve the desired complexity for the radix sort, count sort must be used.

    @param: num_list      a sorted or unsorted list, for the purpose of sorting
    @param: index         an integer value to assist the algorithm to keep
                          track of which digit it is up to
    @param: base          an integer value from 2 to infinity used for calculation
                          of bases, which is essential for determining the digit
                          number
    @return
    @complexity           O(N + b), where N is the length of list and b is
                          the base
    
    """
    count_array = [0] * base #O(b)
    position_array = [0] * base #O(b)
    output_array = [0] * len(num_list)
    for i in range(len(num_list)): #O(N)
        digit_number = int((num_list[i]//base**index)%base)
        count_array[digit_number] += 1
    position_array[0] = 1 #O(1)
    for i in range(1, len(count_array)): #O(b)
        position_array[i] = position_array[i-1] + count_array[i-1]
    for i in range(len(num_list)): #O(N)
        digit_number = int((num_list[i]//base**index)%base)
        output_array[position_array[digit_number]-1] = num_list[i]
        position_array[digit_number] += 1
    return(output_array)
    #the number % base gives the last digit
    #index is required so we know which digit we are up to
    #send it into an array and compare
    #return output array
    #overall O(n+b), where n is total number of integers and b is the base

def is_empty(alist):
    return alist == []

def radix_sort(num_list, b):
    """
    Implements a non-comparison sorting algorithm called radix sort with 

    @param num_list:       a list for sort to occur
    @param b:              a base number for radix sort 
    @complexity:           O((N+b)m), n being the length of num_list, m
                           being the length longest value in num_list in
                           base b and b being the base
    
    """
    if is_empty(num_list) == True:
        return num_list
    largest_number = max(num_list) #O(n)
    digits = int(math.log(largest_number, b)+1)
    output_array = num_list
    #number of digits in the largest number in base b
    #need logbM count sorts to sort numbers of size M
    #each count sort takes O(N+b), where N is the size of list and b is base
    for i in range(digits): #O(M), where M is the maximum number of digits in
        #base b
        output_array = count_sort(output_array, i, b)
    #Overall it is O((N + b)*M)
    return output_array

def time_radix_sort():
    """
    Implements an algorithm which tracks runtime of sorting random data with
    use of different bases

    @param                  None
    @post                   a csv file will be created and runtime of radix sort
                            and its bases will be recorded in the file
    @complexity             O(1) since everything is constant and does not
                            depend on variables
    """
    test_data = [random.randint(1,(2**64)-1) for _ in range(100000)]
    base_array = [2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7,\
        2**8, 2**9, 2**10,2**11,2**12,2**13,2**14,2**15, 2**16, \
                  100000, 2**17, 2**18, 2**19, 2**20] 
    output_array = []
    with open('task2.csv', 'w', newline='') as csvFile:
        #using csv function to write the excel file
        for i in range(len(base_array)):
            start_time = time.time()
            radix_sort(test_data, base_array[i])
            time_taken = time.time()-start_time
            #basic timing
            thewriter = csv.writer(csvFile)
            thewriter.writerow([base_array[i], time_taken])

                            
def find_rotations(string_list, p):
    """
    Implements an algorithm which rotates a list of strings p places to
    the left, where the p is an integer that is given by the user. Then the
    algorithm returns all strings in the original list whose p-rotation
    also exist in the original list.

    @param: string_list   a list of strings, for the find rotations
    @param: p             an integer value to determine the number of
                          rotations for all the strings in the string_list

    @return               a list of all strings in string_list whose p-rotations
                          also exist in string_list
    @complexity           O(n*m), where n is the number of strings in the
                          input list and m is the maximum number of letters
                          in a string, among all strings in the string_list
    """
    n = len(string_list) #O(1)
    output_array = ['']*n #O(1)
    for i in range(n):
        #for loop take N loops to complete. so O(N),
        #where N is the length of list
        length_string = len(string_list[i]) #O(1)
        new_p = p % length_string #O(1)
        if new_p == 0: #O(1)
            output_array[i] += string_list[i] #O(m), where m is the length of string
        elif p < 0: #O(1)
            output_array[i] += string_list[i][new_p:] + string_list[i][-length_string:new_p]
            #using the rotation number, we add up parts of the original string
            #to form the new output string in p rotations, where p is negative
            #this will cost O(m), where m is the length of string
        else: #O(1)
            output_array[i] += string_list[i][new_p:length_string] + string_list[i][0:new_p]
            #same thing will happen to this part but this applies to where p is
            #greater than 0
        #there is O(comp) here, but it is integer comparison, where p is
        #the rotation and new_p is the remainder, which is p without      
        #numbers of self-rotations, which gives us O(1)
        
            
        #overall in this for loop part is O(N*M), where N is the length of list
        #of strings and M is the maximum number of letters in the longest string
        #in the list
            
    number_array = [0]*2*n #O(n)
    for i in range(n): #O(n), where n is the length of the list
        exp = 0
        for j in range(len(string_list[i])-1 ,-1, -1):
            #max O(m), where m is the size of longest string
            number_array[2*i] += (ord(string_list[i][j])-96)*27**exp #O(1)
            number_array[2*i+1] += (ord(output_array[i][j])-96)*27**exp #O(1)
            #27 is used instead of 26 letters due to logarithm
            #problem, 
            exp += 1
    #O(mn), where m and n are respectively length of string and
    #length of list
    
    collection_array, string_output_array = [], []
    
    number_array = radix_sort(number_array, 27)
    #radix sort takes O((n+b)*m) where n is the length of list,
    #b is the base and m is biggest length of string in base b
    
    #by using base of 27, we get m, as the numbers from ord
    #are transformed into bases of 27
    #then we get O((n+27)*m) -> O(n*m + 27*m)
    
    for i in range(2*n-1): #O(2n), where n is the length of original list
        if number_array[i] == number_array[i+1]:
            collection_array.append(number_array[i])
    for i in range(len(collection_array)):
        #the size of collection_array is maximum n, where n is the size of
        #original string list so it would be O(n)
        new_string = ''
        string_length = int(math.log(collection_array[i], 27)+1)
        new_p = p % string_length
        new_number = collection_array[i]
        for j in range(string_length-1, -1 ,-1):
            #worst complexity is O(m), where m is the maximum number of
            #letters in a word, among all the words in the list
            number_conv_string = (new_number//27**j)+96
            new_string += chr(number_conv_string)
            new_number = new_number -(number_conv_string-96)*27**j
        new_string = new_string[-p:] + new_string[-string_length:-p]
        #this part is also O(m) as it joins parts of strings together
        #where the maximmum number of letters in a word, among all the words
        #in the list is m
        string_output_array.append(new_string)
    return string_output_array
    #overall this part has O(n*2*m) -> O(n*m)

    #in conclusion this whole function has O(5*n*m+27*m),which gives us
    #O(m*n) in the end, where m is the maximum number of letters in a word,
    #among all words in the input list and n is the number of strings in the
    #input list


alist = [44, 254, 23452, 8, -33, 35, 1]
blist = [33,11,32,75,525,13,7,832,20]
clist = [1011, 850, 2120]
dlist = [1,1,1,1,1,1,1]
elist = [18446744073709551615,
18446744073709551614,
1,
11111111111111111111,
2111111111111111111,
311111111111111111]
new_string_list = ["yz"]
string_list = ["aaa","aba","aab","abc","cab","acb","wxyz","yzwx","abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz","cdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzab"]
#print(radix_sort([], 100000))
print(find_rotations(string_list, 3))
#time_radix_sort()
