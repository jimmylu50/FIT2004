"""
This file implements different functions about shortest distances

@author: Jin Luo
@since: 11/06/2020
@input          none
@output         none
@errorHandling  none
@knownBugs      none

"""
import math

class adj_node:
    def __init__(self,data = None, weight = 0):
        """
        Create a adjacency node for adjacency list

        @param: data            the vertex number
        @param: weight          the weight of edge from the current vertex
                                to that specific vertex
        @complexity             O(1)
        """
        self.vertex = data
        self.next = None
        self.weight = weight
        self.size = 1

class min_heap:
    
    def __init__(self, length, start):
        """
        Create a min heap class used for dijkstra algorithm

        @param: length            number of vertices in the graph
        @param: start             tells where the dijkstra algorithm starts
        @complexity:              O(v), v being the number of vertices in graph
        """
        self.queue = []
        for i in range(length):
            # O(v), v being the number of vertices in graph
            self.queue.append([math.inf, i])
        self.min_extract = 0
        #min_extract is to make sure which element we are up to
        self.size = length
        self.s = start
        self.size2 = length
        self.queue[start][0] = 0
        #make whereever we are starting to 0
        self.pos = []
        for i in range(length):
            # O(v), make the positions point to themselves
            self.pos.append(i)
        
    def swap(self, i, j):
        """
        Swap elements in queue

        complexity:             O(1)
        """
        self.queue[i], self.queue[j] = self.queue[j], self.queue[i]

    def swap_pos(self, i, j):
        """
        Swap positions of elements so we know where each element is

        complexity:             O(1)
        """
        self.pos[self.queue[i][1]], self.pos[self.queue[j][1]] = i, j

    def is_not_empty(self):
        """
        Check if the queue is empty

        complexity:             O(1)
        """
        return self.min_extract != self.size
        #return self.size != 0

    def heapify(self, index):
        """
        Let the element at index go down the min heap if it is greater than
        its left child or its right child

        complexity:             O(log(v)), v being the number of vertices
        """
        left = 2*(index-self.min_extract) + 1 + self.min_extract
        right = 2*(index-self.min_extract) + 2 + self.min_extract
        #instead of 2*index + 1 and 2*index + 2, because we do not
        #pop the actual element (due to pop left is O(n)), we make
        #the indices to be according to self.min_extract
        if left <= self.size - 1 and right <= self.size - 1:
            if self.queue[index][0] > self.queue[left][0] or self.queue[index][0] > self.queue[right][0]:
                if self.queue[left][0] < self.queue[right][0]:
                    self.swap(index, left)
                    self.swap_pos(index, left)
                    self.heapify(left)
                else:
                    self.swap(index, right)
                    self.swap_pos(index, right)
                    self.heapify(right)
        #swap with the elements if the elements below are greater than the
        #current node
        elif 0 <= left and left <= self.size - 1:
            if self.queue[index][0] > self.queue[left][0]:
                self.swap(index, left)
                self.swap_pos(index, left)
                self.heapify(left)
        
    def decrease_key(self, v, dist):
        """
        Add the distance to the v node and check if it is in the right location
        If its parent is greater than the distance of v node, swap with
        the parent

        complexity:             O(log(v)), v being the number of vertices
        """
        i = self.pos[v]
        self.queue[i][0] = dist
        #(i - self.min_extract - 1)//2 + self.min_extract
        while (i - self.min_extract - 1)//2 >= 0 and self.queue[i][0] < self.queue[(i - self.min_extract - 1)//2 + self.min_extract][0]:
            n = (i - self.min_extract - 1)//2 + self.min_extract
            self.swap(i, n)
            self.swap_pos(i, n)
            i = n
        #instead of going straight (i-1)//2, we need to use self.min_extract
        #to get the index of the parent and possibly swap place with the parent
        #if the parent is greater than the child

    def pop_min(self):
        """
        Get the minimum element in the min heap

        complexity:             O(log(v)), v being the number of vertices
                                this is because heapify and decrease_key are used
        """
        if self.is_not_empty() == False:
            return
        if self.min_extract == 0:
            self.decrease_key(self.s, 0)
        root = self.queue[self.min_extract][1]
        self.min_extract += 1
        self.heapify(self.min_extract)
        #heapify takes log(v), v being the number of vertices
        #for pop min, nothing is popped because popping will disrupt the
        #ordering and popleft would take O(v), which would not be
        #efficient for task 3
        return root


class Graph:
    def __init__(self, gfile):
        """
        Create adjacency list and table to store the graph that is given by gfile

        @param: gfile                   a file containing vertices and edges
        @complexity                     O(v^2), v being the number of vertices
        """
        self.adj_tab = []
        f = open(gfile, 'r')
        f1 = f.readlines()
        self.length = int(f1[0])
        #reading lines and getting the number of vertices
        self.adj_list = [None] * self.length
        #O(v^2) is used when v is looped through 2 times to create a table
        for i in range(self.length):
            self.adj_tab.append([])
            for j in range(self.length):
                """
                if i == j:
                    self.adj_tab[i].append(0)
                else:
                """
                self.adj_tab[i].append(math.inf)
        for i in range(1, len(f1)):
            #loop through the entire document
            #add the edges between vertices to the table
            #O(E + v), e being number of edges and v being vertices
            #E dominates v as E can be V^2 if dense so O(E) here

            new_edge = f1[i]
            index = 0
            v1, v2, v3 = '', '', ''
            while new_edge[index] != ' ':
                v1 += new_edge[index]
                index += 1
            index += 1
            v1 = int(v1)
            while new_edge[index] != ' ':
                v2 += new_edge[index]
                index += 1
            index += 1
            v2 = int(v2)
            while index < len(new_edge):
                v3 += new_edge[index]
                index += 1
            v3 = int(v3)
            self.adj_tab[v1][v2] = self.adj_tab[v2][v1] = v3
        #This creates an adjacency list for use in task 3
        #O(V^2) is used because it is taking values from the adj_table
        for i in range(len(self.adj_tab)):
            for j in range(len(self.adj_tab[i])):
                if self.adj_tab[i][j] != math.inf:
                    node = adj_node(j, self.adj_tab[i][j])
                    node.next = self.adj_list[i]
                    self.adj_list[i] = node
        #Overall complexity would be O(V^2 + E) but since E can be O(V^2)
        #the complexity would just be O(V^2)

    def shallowest_spanning_tree(self):
        """
        Finds the point where it has the shallowest spanning tree
        and returns the maximum weight it has to go through

        @:complexity             O(v^3), v being the number of vertices
        @:return                 the vertex that has the minimum shallow spanning tree
                                 and the depth of that vertex
        """
        new_tab = []
        for i in range(self.length):
            #make a new table for storing 1's because this function ignores the
            #edge weights, complexity is O(v^2)
            new_tab.append([])
            for j in range(self.length):
                if i == j:
                    new_tab[i].append(0)
                elif self.adj_tab[i][j] != math.inf:
                    new_tab[i].append(1)
                else:
                    new_tab[i].append(math.inf)
        for k in range(self.length):
            #O(v^3) is used here, v being the number of vertices
            #Floyd warshall principle is used here
            #but with ignoring the actual edge weights
            for i in range(self.length):
                for j in range(self.length):
                    new_tab[i][j] = min(new_tab[i][j], new_tab[i][k] + new_tab[k][j])
        shallow_vert, shallow_dist = 0, max(new_tab[0])
        for i in range(len(new_tab)):
            new_dist = max(new_tab[i])
            #O(v^2) because max requires O(v) as well
            if new_dist < shallow_dist:
                shallow_dist = new_dist
                shallow_vert = i
            #finds the vertex that has minimum shallow spanning tree
            #and store the maximum distance from that vertex to any
            #other point in the tree
        return((shallow_vert, shallow_dist))
            
    def shortest_errand(self, home, dest, ice_locs, ice_cream_locs):
        """
        Find the shortest route from home to an ice shop, then to an ice cream
        shop, then to dest, and provide the route and distance

        @:param home                starting point in the graph
        @:param dest                ending point in the graph
        @:param ice_locs            list of vertices of ice locations
        @:param ice_cream_locs      list of vertices of ice cream locations
        @complexity                 O(Elog(v)), e being the number of edges and v
                                    being the number of vertices in the graph
        @:return                    shortest distance from home to 1 ice location, 1 ice
                                    cream location and to dest
                                    the shortest route with each vertices listed
        """
        start_array, mid_array, end_array = [], [], []
        ret_array = []
        final_weight = 0
        start = self.dijkstra(home)
        end = self.dijkstra(dest)
        #run dijkstra 2 times for home and dest locations
        self.adj_list.append(None)
        new_home = self.length
        self.adj_list.append(None)
        new_dest = self.length + 1
        self.length += 2
        #set 2 new vertices to the adjacency list, one is pretending to be
        #connection point to all ice_locs, another is pretending to be
        #connection point to all ice_cream_locs
        
        for loc in ice_locs:
            #O(v), v being the number of vertices in the ice locations
            #this can be in worst case all the vertices of the graph
            node = adj_node(loc, start[0][loc])
            node.next = self.adj_list[new_home]
            self.adj_list[new_home] = node
            #make all the ice locations adjacent to the first new vertex
            node2 = adj_node(new_home, start[0][loc])
            node2.next = self.adj_list[loc]
            self.adj_list[loc] = node2
            #make all the locations adjacent to this vertex as well

        for loc in ice_cream_locs:
            # O(v), v being the number of vertices in the ice cream locations
            # this can be in worst case all the vertices of the graph
            node = adj_node(loc, end[0][loc])
            node.next = self.adj_list[new_dest]
            self.adj_list[new_dest] = node
            # make all the ice cream locations adjacent to the second new vertex
            node2 = adj_node(new_dest, end[0][loc])
            node2.next = self.adj_list[loc]
            self.adj_list[loc] = node2
            # make all the locations adjacent to this vertex as well


        middle = self.dijkstra(new_home)
        new_index = middle[1][new_dest]
        while new_index != None:
            #O(v) since there can only be v vertices that go through
            #the dijkstra algo
            mid_array.append(new_index)
            new_index = middle[1][new_index]
            if new_index == None:
                mid_array.pop(-1)
                break
        new_ice_loc, new_ice_cream_loc = mid_array[len(mid_array)-1], mid_array[0]

        final_weight = middle[0][new_dest]

        new_index = start[1][new_ice_loc]
        while new_index != None:
            # O(v) since there can only be v vertices that go through
            # the dijkstra algo
            start_array.append(new_index)
            new_index = start[1][new_index]

        new_index = end[1][new_ice_cream_loc]
        while new_index != None:
            # O(v) since there can only be v vertices that go through
            # the dijkstra algo
            end_array.append(new_index)
            new_index = end[1][new_index]


        #these for loops are to combine all the parts together, consisting of
        #from start to ice loc, ice loc to ice cream loc and ice cream loc to dest
        for i in range(len(start_array)-1, -1, -1):
            # O(v) since there can only be v vertices that go through
            # the dijkstra algo
            ret_array.append(start_array[i])
        for i in range(len(mid_array)-1, -1, -1):
            # O(v) since there can only be v vertices that go through
            # the dijkstra algo
            ret_array.append(mid_array[i])
        for i in range(len(end_array)):
            # O(v) since there can only be v vertices that go through
            # the dijkstra algo
            ret_array.append(end_array[i])

        return ((final_weight, ret_array))

    def dijkstra(self, s):
        """
        Implementation of dijkstra algorithm for shortest errand function

        @:param s                   starting point from the graph
        @complexity                 O(elog(v)), e being the numbers of vertices
                                    and v being the number of vertices in the graph
        @:return                    the shortest distance from starting point
                                    to any other point in the graph
                                    and the predecessors of these vertices
        """
        dist = [math.inf] * self.length
        pred = [None] * self.length
        dist[s] = 0
        q = min_heap(self.length, s)
        #set a min heap data structure
        #loop through it until there is nothing else in the queue
        while q.is_not_empty:
            if q.min_extract == q.size:
                break
            u = q.pop_min()
            #get the min from q
            #this is log(v)
            node = self.adj_list[u]
            if node == None:
                break
            while node.next != None:
                #this is checking all the vertices that are adjacent to u
                #this is a part of O(e), but not entire O(e)
                new_min = node.vertex
                if dist[u] + node.weight < dist[new_min]:
                    dist[new_min] = dist[u] + node.weight
                    pred[new_min] = u
                    q.decrease_key(new_min, dist[new_min])
                    #decrease_key takes O(log(v))
                node = node.next
            #this step is done one more time because when node.next is None
            #the current adjacent vertex was not included in the loop
            new_min = node.vertex
            if dist[u] + node.weight < dist[new_min]:
                dist[new_min] = dist[u] + node.weight
                pred[new_min] = u
                q.decrease_key(new_min, dist[new_min])
        #overall complexity is O(elog(v) + vlog(v)), but since e dominates v
        #the complexity becomes O(elog(v))
        return (dist, pred)
        

#if __name__ == "__main__":
    #new_graph = Graph('ffile.txt')
    #new_graph.shallowest_spanning_tree()
    #new_graph.shortest_errand(0, 8, [1, 5, 8], [4, 6])
