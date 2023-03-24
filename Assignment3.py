"""
This file implements a Trie class and a Trie node class. The Trie node class is
used to support the Trie class. In the Trie class, there is finding frequency
of prefix, finding occurrences of a word and wildcard prefix methods.

@author: Jin Luo
@since: 20/05/2020
@input          none
@output         none
@errorHandling  none
@knownBugs      none

"""

class TrieNode:
    """
    this class is required because we need properties of
    each trie node in order to build the trie
    """
    def __init__(self):
        """
        this builds a empty array of size 28 for a-z plus the prefix and existence count
        temp is used for storing children
        """
        self.array = [None] * 28
        self.temp = []
        #array to store children
        

class Trie:
    def __init__(self, text):
        """
        This builds an initial state of trie using the text given by the user
        There is no output, but the rootNode will contain the entire tree

        @param: text                a list of strings in lowercase
        @complexity:                O(T), T being the total character over
                                    all strings in the list
        @return:                    None
        """
        self.word_list = []
        #word_list will contain all the elements that need to be
        #printed in task 4
        self.rootNode = self.getNode()
        #used to create a new empty Node
        self.total_nodes = []

        for i in range(len(text)):
            new_node = self.rootNode
            if new_node.array[27] == None:
                new_node.array[27] = 1
            else:
                new_node.array[27] += 1
            #loop through the entire input list of strings
            #set root node to be new_node at start of
            #every new string
            for j in range(len(text[i])):
                index = ord(text[i][j]) - 97
                #loop through entire string that is
                #currently on and create a index using ord
                if new_node.array[index] == None:
                    new_node.array[index] = self.getNode()
                    new_index = 0
                    while len(new_node.temp) > new_index and index > new_node.temp[new_index]:
                        new_index += 1
                    new_node.temp.insert(new_index, index)
                    #check whether the index has a node, if not, make one
                    #the while and insert part will take constant time
                    #because they are dependent on the number of items in temp
                    #which is the children array for each node and each node
                    #cannot have over 26 children
                    #the while and insert parts can be replaced by count sorting
                    #in wildcard but is similar complexity
                new_node = new_node.array[index]
                #make the new_node go to the one with new index
                if new_node.array[27] == None:
                    new_node.array[27] = 1
                else:
                    new_node.array[27] += 1
                #if last element is empty, make it 1
                #else add 1 to it
            if new_node.array[26] != None:
                new_node.array[26] += 1
            else:
                new_node.array[26] = 1
            # if second last element is empty, make it 1
            # else add 1 to it
        
    def getNode(self):
        #returns a node class created from above
        return TrieNode()

    def string_freq(self, query_str):
        """
        This function returns the number of times a string has occurred in the text

        :param query_str:           the input string that is used for seraching
        :return:                    a number which shows number of times it was in the text
        :complexity:                O(q), with q being the length of query_str
        """
        new_node = self.rootNode
        for i in range(len(query_str)):
            #O(q)
            index = ord(query_str[i]) - 97
            if new_node.array[index] != None:
                new_node = new_node.array[index]
            else:
                return 0
        if new_node.array[26] != None:
            return new_node.array[26]
        else:
            return 0
        #start with rootNode, loop through the string to find the node of final
        #char, then return the 26th element of node, which is set up in __init__
        #to store the number of times it occurs in the text

    def prefix_freq(self, query_str):
        """
        This function finds how many words in the text have query_str as a prefix

        :param query_str:           a string acting as a prefix
        :return:                    number of strings that have that prefix
        :complexity:                O(q), q being the length of query string
        """
        new_node = self.rootNode
        output_value = 0
        for i in range(len(query_str)):
            #O(q)
            index = ord(query_str[i]) - 97
            if new_node.array[index] != None:
                new_node = new_node.array[index]
            else:
                return 0
        if new_node.array[27] != None:
            return new_node.array[27]
        else:
            return 0
        # start with rootNode, loop through the string to find the node of final
        # char, then return the 27th element of node, which is set up in __init__
        # to store the number of times it has the query_str as a prefix

    def wildcard_prefix_freq(self, query_str):
        """
        This function takes a query_str, which is a string containing a ?, where this ?
        symbol represents exactly one character. The function returns the list of strings
        in the text that have query_str as a prefix

        :param query_str:           string containing lowercase characters and exactly 1 ?
                                    ? can represent any letter
        :return:                    a list of words that have query_str as prefix
        :complexity:                O(S + q), q being the length of query_str and S being
                                    the total number of characters in all strings of the text
        """
        new_node = self.rootNode
        temp, temp2 = 0,0
        output_value, node_list = [], []
        for i in range(len(query_str)):
            index = ord(query_str[i]) - 97
            if query_str[i] == '?':
                break
            elif new_node.array[index] != None:
                new_node = new_node.array[index]
                temp += 1
            else:
                return []
            #loop through O(q) and check where the question mark is
        temp_node = new_node
        temp2 += temp
        temp_str = str(query_str[:temp2])
        #store the current new_node
        #make temp2 a copy of temp
        #temp_str = the string that has been looped through before question mark
        for i in range(len(new_node.temp)):
            temp_str += str(chr(new_node.temp[i]+97))
            new_node = new_node.array[new_node.temp[i]]
            temp2 += 1
            #go through the children of the current node at question mark
            #add its char form to temp_str and make the new_node to that index node
            while temp2 < len(query_str):
                index = ord(query_str[temp2]) - 97
                if new_node.temp == [] or new_node.array[index] == None:
                    break
                else:
                    temp_str += query_str[temp2]
                    new_node = new_node.array[index]
                temp2 += 1
            #go through the char after the question mark and keep looping
            if len(temp_str) == len(query_str):
                output_value.append(temp_str)
                node_list.append(new_node)
            #output_value is used to record the strings that fit the prefix
            #after trials of question mark
            #node_list records the node where these strings are left off at
            if new_node.array[26] != None and len(temp_str) == len(query_str):
                for i in range(new_node.array[26]):
                    self.word_list.append(temp_str)
            #append to word_list the number of times the string exists in the text
            temp2 = temp
            temp_str = str(query_str[:temp2])
            new_node = temp_node
        #this whole for loop would take worst case complexity of O(S)
        for i in range(len(node_list)):
            self.wildcard_prefix_freq2(output_value[i], node_list[i])
        #this for loop would take worst case complexity of O(S) as well
        return self.word_list
        #In total, the final complexity is O(S + q)
    

    def wildcard_prefix_freq2(self, temp_word, node):
        """
        This function is used for recursive calls with looping to every possible char
        in the trie

        :param temp_word:               the part of the string that is already formed
        :param node:                    the node that is at the end of the half formed
                                        string
        :return:                        None
        :complexity:                    O(S), S being the total number of characters in text
                                        however not exactly O(S) because there is prefix
        """
        for i in range(len(node.temp)):
            temp_word += str(chr(node.temp[i]+97))
            self.total_nodes.append(node)
            node = node.array[node.temp[i]]
            #store the current node in total_nodes
            #move onto next possible node
            if node.array[26] != None:
                for i in range(node.array[26]):
                    self.word_list.append(temp_word)
                    #add however many times the word is in the text to final output
            self.wildcard_prefix_freq2(temp_word, node)
            #recursively call next possible node in the tree
            node = self.total_nodes.pop(-1)
            temp_word = temp_word[:len(temp_word) - 1]
            # O(1), used for removing last element of list
            # store the temp_word


if __name__ == "__main__":
    x = Trie(['aa','aab','aaab','abaa','aa','abba','aaba','aaa','aa','aaab','abnbbbbbbbfg','baaa','baa','bba','bbab'])
    #print(x.string_freq('aaab'))
    #print(x.prefix_freq('b'))
    #print(x.wildcard_prefix_freq('?'))
