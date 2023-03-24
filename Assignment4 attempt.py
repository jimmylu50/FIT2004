import math

class adj_node:
    def __init__(self,data = None):
        self.vertex = data
        self.next = None
        self.size = 1

class min_heap:
    def __init__(self, length, start):
        self.queue = [math.inf] * length
        self.min_extract = 0
        self.size = length
        self.s = start
        self.queue[start] = 0
        self.pos = []
        for i in range(length):
            self.pos.append(i)
        
    def swap(self, i, j):
        self.queue[i], self.queue[j] = self.queue[j], self.queue[i]

    def swap_pos(self, i, j):
        self.pos[i], self.pos[j] = self.pos[j], self.pos[i]

    def is_not_empty(self):
        return self.min_extract != self.size
        #return self.size != 0

    def is_leaf(self, pos):
        return pos >= self.size//2 and pos <= self.size

    def heapify(self, index):
        new_index = index
        left = 2*index + 1
        right = 2*index + 2
        """
        if left < self.size and self.queue[left] < self.queue[new_index]: 
            new_index = left 
  
        if right < self.size and self.queue[right] < self.queue[new_index]: 
            new_index = right

        if new_index != index: 
  
            self.pos[self.queue[new_index]] = index 
            self.pos[self.queue[index]] = new_index 

            self.swap(new_index, index) 
  
            self.heapify(new_index) 
        """
        if left <= self.size and right <= self.size:
            if self.queue[index] > self.queue[left] or self.queue[index] > self.queue[right]:
                if self.queue[left] < self.queue[right]:
                    self.swap(index, left)
                    self.swap_pos(index, left)
                    self.heapify(left)
                else:
                    self.swap(index, right)
                    self.swap_pos(index, right)
                    self.heapify(right)
        elif left <= self.size:
            if self.queue[index] > self.queue[left]:
                self.swap(index, left)
                self.swap_pos(index, left)
                self.heapify(left)
        elif right <= self.size:
            if self.queue[index] > self.queue[right]:
                self.swap(index, right)
                self.swap_pos(index, right)
                self.heapify(right)
        
        
    def decrease_key(self, v, dist):
        i = self.pos[v]
        self.queue[i] = dist
        while i > 0 and self.queue[i] < self.queue[i//2]:
            self.swap(i, i//2)
            self.swap_pos(i, i//2)
            i = i//2

    def pop_min(self):
        if self.is_not_empty() == False:
            return
        #self.heapify(self.min_extract)
        root = self.pos[self.min_extract]
        #print('s' + str(self.min_extract))
        #self.swap(0, self.size-1)
        #self.queue.pop(-1)
        #self.swap_pos(0, self.size-1)
        #self.pos.pop(-1)
        self.size -= 1
        self.min_extract += 1
        return root


class Graph:
    def __init__(self, gfile):
        numbers = '0123456789'
        self.adj_tab = []
        f = open(gfile, 'r')
        f1 = f.readlines()
        self.length = int(f1[0])
        self.adj_list = [None] * self.length
        for i in range(self.length):
            self.adj_tab.append([])
            for j in range(self.length):
                self.adj_tab[i].append(math.inf)
        for i in range(1, len(f1)):
            new_edge = f1[i]
            index, numbers = 0, 0
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
        for i in range(len(self.adj_tab)):
            for j in range(len(self.adj_tab[i])):
                if self.adj_tab[i][j] != math.inf:
                    node = adj_node(j)
                    node.next = self.adj_list[i]
                    self.adj_list[i] = node

    def shallowest_spanning_tree(self):
        new_tab = []
        for i in range(self.length):
            new_tab.append([])
            for j in range(self.length):
                if i == j:
                    new_tab[i].append(0)
                elif self.adj_tab[i][j] != math.inf:
                    new_tab[i].append(1)
                else:
                    new_tab[i].append(math.inf)
        for k in range(self.length):
            for i in range(self.length):
                for j in range(self.length):
                    new_tab[i][j] = min(new_tab[i][j], new_tab[i][k] + new_tab[k][j])
        shallow_vert, shallow_dist = 0, max(new_tab[0])
        for i in range(len(new_tab)):
            new_dist = max(new_tab[i])
            if new_dist < shallow_dist:
                shallow_dist = new_dist
                shallow_vert = i
        print((shallow_vert, shallow_dist))
            
    def shortest_errand(self, home, dest, ice_locs, ice_cream_locs):
        pass

    def dijkstra(self, s):
        dist = [math.inf] * self.length
        pred = [None] * self.length
        dist[s] = 0
        q = min_heap(self.length, s)
        while q.is_not_empty:
            if q.min_extract == q.size:
                break
            u = q.pop_min()
            print(u)
            node = self.adj_list[u]
            if node == None:
                break
            while node.next != None:
                new_min = node.vertex
                if dist[u] + self.adj_tab[u][new_min] < dist[new_min] and new_min != u:
                    dist[new_min] = dist[u] + self.adj_tab[u][new_min]
                    pred[new_min] = u
                    print(q.queue)
                    print(q.pos)
                    print((new_min, dist[new_min]))
                    q.decrease_key(new_min, dist[new_min])
                    print(q.queue)
                    print(q.pos)
                node = node.next
            new_min = node.vertex
            if dist[u] + self.adj_tab[u][new_min] < dist[new_min] and new_min != u:
                dist[new_min] = dist[u] + self.adj_tab[u][new_min]
                pred[new_min] = u
                print((new_min, dist[new_min]))
                q.decrease_key(new_min, dist[new_min])
                print(q.queue)
                print(q.pos)
        return (dist, pred)
        

if __name__ == "__main__":
    new_graph = Graph('dfile.txt')
    #new_graph.shallowest_spanning_tree()
    #new_graph.shortest_errand(0, 8, [1,5,8], [4,6])
    #print(new_graph.dijkstra(0))
