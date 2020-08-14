"""
== FIT2004: Assignment 4 - Graphs ==

Author: Dania Ismadi
Student ID: 30990971
"""
import math


class Graph:
    """
    A class for a connected, undirected and simple graph.

    == Attributes ==
    vertices:   (list) a list of vertices in this graph
    """

    def __init__(self, gfile):
        """
        Initialise a new connected, undirected and simple graph with vertices
        outlined in gfile.

        :precondition:          - gfile is the name of a valid file
                                - input in gfile is always valid
                                - first line in gfile contains a single
                                integer n, which is the number of vertices in
                                the graph
                                - each following line in gfile consists of 3
                                integers separated by spaces
                                - the first two integers are vertex IDs (in the
                                range [0, n-1]) and the third is the weight of
                                that edge (must be non-negative)
                                - every edge of the graph will be represented
                                by exactly one line in gfile

        :param gfile:           (str) name of a file containing information
                                about the graph

        :time complexity:       Best Case: O(V), where V is the number of
                                vertices in the graph. This occurs when
                                there are no edges in the graph. The function
                                will initialise V vertices but no edges
                                which will take O(V) time.

                                Worst Case: O(V^2), where V is the number of
                                vertices in the graph. This occurs when each
                                vertex has an edge to every other vertex
                                in the graph, i.e., each vertex has V edges.
                                Thus, there will be at most V^2 edges in this
                                graph. Therefore the for loop will iterate
                                at most V^2 + 1 times since there will be at
                                most V^2 + 1 lines in the file, including the
                                line of the file that represents the number of
                                vertices in the graph. Initialising all
                                the vertices in the graph takes O(V) time.
                                Thus, the total time complexity is O(V + V^2)
                                which is O(V^2).

        :space complexity:      O(V^2), where V is the number of vertices in
                                the graph. The input uses O(V^2) space as
                                there are at most V^2 edges in a graph and the
                                auxiliary space complexity of this function
                                is O(V^2), giving a space complexity of O(V^2).

        :aux space complexity:  O(V^2), where V is the number of vertices
                                in the graph. This function initialises
                                a V new vertices. Each vertex uses at most
                                O(V) space when the vertex has an edge to
                                every other vertex in the graph. Thus, the
                                auxiliary space complexity is O(V^2).
        """
        # open the file
        f = open(gfile, "r")
        # read the file
        file = f.readlines()

        line_count = 0
        for line in file:
            if line_count == 0:
                # initialise all vertices in graph
                num_vertices = int(line.strip())
                self.vertices = []
                for i in range(num_vertices):
                    self.vertices.append(Vertex(i))
            else:
                # add edges
                edge = line.split()
                # convert to integers
                for i in range(len(edge)):
                    edge[i] = int(edge[i])
                self.add_directed_edge(edge[0], edge[1], edge[2])
                self.add_directed_edge(edge[1], edge[0], edge[2])
            line_count += 1

        # close the file
        f.close()

    def add_directed_edge(self, u, v, weight):
        """
        Add directed edge from u to v with weight.

        :precondition:          weight is non-negative
        :param u:               (int) the id of the vertex that is the origin
                                of this edge
        :param v:               (int) the id of the vertex that is the
                                destination of this edge
        :param weight:          (int) the weight of this edge

        :time complexity:       O(1). Initialising a new edge, accessing the
                                vertex from self.vertices and adding
                                a new edge to this vertex takes constant time.

        :space complexity:      O(1). This function uses constant space. This
                                is because the input uses constant space and
                                the auxiliary space complexity is constant.

        :aux space complexity:  O(1). Initialising a new edge uses constant
                                space, thus, this function uses constant space.

        :return:                None
        """
        # add u to v
        curr_edge = Edge(u, v, weight)
        curr_vertex = self.vertices[u]
        curr_vertex.add_edge(curr_edge)

    def shallowest_spanning_tree(self):
        """
        Find the spanning tree which minimises the number of edges in this
        graph and return the vertex ID of the root and the height of this tree.

        :precondition:          ignore edge weights

        :time complexity:       Best Case: O(V^3), where V is the number of
                                vertices in the graph. This is the same as
                                the worst case, see below.

                                Worst Case: O(V^3), where V is the number of
                                vertices in the graph. Creating the matrix,
                                adj_matrix, takes O(V^2) time. Initialising
                                the depth_array takes O(V) time. Initialising
                                the adj_matrix takes O(V^2) time. Updating the
                                adj_matrix for the appropriate values takes
                                O(V^3) time. Updating depth_arr with appropriate
                                values takes O(V^2) time. Finally, returning
                                the required values takes O(2V) time. Combining
                                everything together, this gives us a time
                                complexity of O(V^3).

        :space complexity:      O(V^2), where V is the number of vertices
                                in the graph. This is because this function
                                has an auxiliary space complexity of O(V^2).

        :aux space complexity:  O(V^2), where V is the number of vertices in
                                the graph. This is because the V by V matrix,
                                adj_matrix, is initialised.

        :return:                (tup) a tuple where the first item is the
                                vertex of ID of the root which gives the
                                shallowest spanning tree and the second item
                                is an integer representing the height
                                of the shallowest spanning tree
        """

        # create adjacency matrix
        # O(V^2).
        adj_matrix = [[]] * len(self.vertices)
        for i in range(len(adj_matrix)):
            adj_matrix[i] = [math.inf] * len(self.vertices)

        # initialise array of V size corresponding to each vertex (depth)
        # O(V).
        depth_arr = [None] * len(self.vertices)

        # fill edges (0 for diagonal, inf for edges that do not exist and 1
        # for edges that exist
        # O(V^2).
        for i in range(len(adj_matrix)):
            adj_matrix[i][i] = 0
            # loop through vertex connections and set to 1
            for edge in self.vertices[i].edges:
                vertex_id = self.vertices[edge.v].id
                adj_matrix[i][vertex_id] = 1

        # go through each column and find each shortest distance (if there is
        # a minimum)
        # O(V^3).
        for k in range(len(self.vertices)):
            for i in range(len(self.vertices)):
                for j in range(len(self.vertices)):
                    adj_matrix[i][j] = min(adj_matrix[i][j],
                                           adj_matrix[i][k] + adj_matrix[k][j])

        # update depth array
        # O(V^2).
        for k in range(len(self.vertices)):
            depth_arr[k] = max(adj_matrix[k])

        # return minimum depth from depth array and the index it's at
        # which corresponds to the vertex ID
        # O(V)
        return depth_arr.index(min(depth_arr)), min(depth_arr)

    def shortest_errand(self, home, destination, ice_locs, ice_cream_locs):
        """
        Return the length of the shortest walk from home to destination with
        stopping at an ice location and ice cream location, in this order, in
        between home to destination.

        :precondition:              home, destination, the IDs in ice_locs and
                                    the IDs in ice_cream_locs are valid
                                    vertex IDs in this graph. ice_locs and
                                    ice_cream_locs contain at least one
                                    vertex ID.

        :param home:                (int) vertex ID of source
        :param destination:         (int) vertex ID of destination
        :param ice_locs:            (list) IDs of vertices that represent ice
                                    locations
        :param ice_cream_locs:      (list) IDs of vertices that represent ice
                                    cream locations

        :time complexity:           Best Case: O(E(log(V))), where E is the
                                    number of edges in the graph and V is
                                    the number of vertices in the graph. This
                                    is the same as the worst case, see below.

                                    Worst Case: O(E(log(V))), where E is the
                                    number of edges in the graph and V is the
                                    number of vertices in the graph. The
                                    analysis is below.

                                    Pre-processing the graph takes O(V + E)
                                    time. Initialising the MinHeap takes O(V)
                                    time. Thus, this part has a total time
                                    complexity of O(V + E).

                                    The while loop will run at most in O(V)
                                    time since each vertex will not be added
                                    back to the heap once it has been served.
                                    Within the while loop, the call to serve()
                                    will take O(log(V)) at the worst case. Thus,
                                    this part has a total time complexity of
                                    O(V(logV)).

                                    In total, the while loop will go through
                                    all the edges in this graph and add to
                                    or update the heap accordingly. Adding to
                                    or updating the heap has a time complexity
                                    of O(log(V)). Thus, the total time
                                    complexity for this part is O(E(log(V)).

                                    Backtracking to find the path and creating
                                    the final path list takes at most O(V)
                                    time since the length of the path is at most
                                    3V. Finally, resetting the graph takes
                                    O(V) time. Thus, the total time complexity
                                    for this part is O(V).

                                    Combining everything together, we get
                                    O(V + E + V(log(V)) + E(log(V)) + V).
                                    Considering that when the graph is
                                    dense, E is at most V^2 and thus, V < E,
                                    we then arrive at the final time complexity
                                    of O(E(log(V)).

        :space complexity:          O(V), where V is the number of vertices
                                    in the graph. The inputs, ice_locs and
                                    ice_cream_locs, uses at most O(V) space
                                    each. The auxiliary space complexity of
                                    this function is O(V). Thus, the space
                                    complexity is O(V).

        :aux space complexity:      O(V), where V is the number of vertices in
                                    the graph. This is because the final
                                    path list uses at most O(V) space since
                                    the length of the path is at most 3V. Also,
                                    the size of the heap is at most O(V).

        :return:                    (tuple) a tuple where the first item
                                    is the length of the shortest walk you
                                    have found and the second item is a list
                                    of vertices in this walk
        """

        if len(self.vertices) <= 0:
            # graph is empty
            return 0, []

        n = len(self.vertices)

        # pre process graph
        # O(V + E)
        self._pre_process(ice_locs, ice_cream_locs)

        # set home (source) distance to 0
        self.vertices[home].distance = 0

        # initialise min_heap
        # O(V) bounded by O(E)
        heap = MinHeap(len(self.vertices))
        # add to min heap
        self.vertices[home].discovered = True
        heap.add(self.vertices[home])

        final_destination = destination + (2*n)
        curr_vertex = None
        # O(V) bounded by O(E)
        while len(heap) > 0:
            # serve current vertex
            # O(log(V))
            curr_vertex = heap.serve()
            curr_vertex.visited = True

            # if current vertex served is destination, break out of loop
            if curr_vertex.id == final_destination:
                break

            # O(V)
            for edge in curr_vertex.edges:
                # find the next vertex
                next_vertex = self.vertices[edge.v]

                # if have not discovered vertex, relax edge and add to heap
                if not next_vertex.discovered:
                    # relax edge
                    next_vertex.discovered = True
                    next_vertex.distance = curr_vertex.distance + edge.weight
                    next_vertex.previous = curr_vertex

                    # add to heap
                    # O(log(V))
                    heap.add(next_vertex)
                # have discovered vertex, but not yet finalised
                elif not next_vertex.visited:
                    # if a shorter distance is found, change it
                    new_distance = curr_vertex.distance + edge.weight
                    if next_vertex.distance > new_distance:
                        # update distance
                        next_vertex.distance = new_distance
                        next_vertex.previous = curr_vertex

                        # update heap
                        # O(log(V))
                        heap.update(next_vertex.pos_in_heap)

        # implement backtracking

        # curr_vertex will always be not none because there is always at least
        # one vertex served
        assert curr_vertex is not None
        # curr_vertex will always be equal to the id of the final destination
        assert curr_vertex.id == final_destination

        final_distance = curr_vertex.distance
        # unprocessed path
        pre_path = []

        # bounded by O(3V)
        while curr_vertex is not None:
            curr_vertex_id = curr_vertex.id

            # vertex is in ice_cream layer, convert vertex id back
            # to original id
            if curr_vertex_id >= 2*n:
                curr_vertex_id = curr_vertex_id - (2*n)
            # vertex is in ice layer, convert vertex id back to original id
            elif curr_vertex_id >= n:
                curr_vertex_id = curr_vertex_id - n

            pre_path.append(curr_vertex_id)
            curr_vertex = curr_vertex.previous

        # process path for return
        # delete duplicates and reverse path
        # bounded by O(3V)
        final_path = []
        for i in range(len(pre_path) - 1, -1, -1):
            if i == 0 or pre_path[i] != pre_path[i-1]:
                final_path.append(pre_path[i])

        # reset graph
        # O(V) bounded by O(E)
        self._reset(ice_locs, n)

        return final_distance, final_path

    def _reset(self, ice_locs, n):
        """
        Reset the graph to its original state after running shortest_errand().

        :param ice_locs:        (list) the IDs of the vertices that are ice
        :param n:               (int) the number of vertices in the original
                                graph

        :time complexity:       Best and Worst Case: O(V), where V is the
                                number of vertices in the graph. Initialising
                                the list, vertices, takes O(V) time. The
                                second for loop runs at most O(V) time and
                                pop() takes constant time. The third for loop
                                runs at most O(V) time and updating the
                                attributes in each vertex is constant. Thus,
                                the time complexity of this function is O(V).

        :space complexity:      O(V), where V is the number of vertices in
                                the original graph. The input, ice_locs,
                                is uses at most O(V) space and this function
                                uses O(V) space. Therefore, the total space
                                complexity is O(V).

        :aux space complexity:  O(V), where V is the number of vertices in
                                the original graph. This is because the list,
                                vertices, is initialised and is at most of
                                size V.

        :return:
        """

        # O(V)
        vertices = []
        for i in range(n):
            vertices.append(self.vertices[i])
        self.vertices = vertices

        for vertex_id in ice_locs:
            # newly added edges to ice layer will be at the last position always
            self.vertices[vertex_id].edges.pop()

        # reset all vertex attributes
        for vertex in self.vertices:
            vertex.distance = math.inf
            vertex.previous = None
            vertex.pos_in_heap = None
            vertex.visited = False
            vertex.discovered = False

    def _pre_process(self, ice_locs, ice_cream_locs):
        """
        Pre-process the graph for shortest_errand() by adding new vertices
        and creating the appropriate links between ice and ice cream locations
        in the graph.

        :param ice_locs:        (list) the IDs of the vertices that are ice
        :param ice_cream_locs:  (list) the IDs of the vertices that are ice
                                creams

        :time complexity:       Best and Worst Case: O(V + E), where V is the
                                number of vertices in the graph and E is the
                                number of edges in the graph. The analysis is
                                provided below.

                                Creating the new vertices takes O(V) time.
                                Adding the appropriate edges in the new
                                vertices takes O(E) time. Adding the
                                appropriate links between ice locations
                                takes at most O(V) time when every vertex is
                                in the graph is ice. Adding the appropriate
                                links between ice cream locations take at most
                                O(V) time when every vertex in the graph
                                is an ice cream. Thus, the total time
                                complexity is O(V + E).

        :space complexity:      O(V). The inputs, ice and ice_locs, uses
                                O(V) space each and this function uses constant
                                auxiliary space. Thus, the total space
                                complexity is O(V).

        :aux space complexity:  O(1). This function uses constant auxiliary
                                space.

        :return:                None
        """

        n = len(self.vertices)

        # create new vertices
        for i in range(2*n):
            old_vertex = self.vertices[i]
            new_vertex = Vertex(old_vertex.id + n)
            self.vertices.append(new_vertex)

        # add edges in ice and ice cream layer
        for i in range(n):
            for edge in self.vertices[i].edges:
                for j in range(1, 3):
                    new_u = edge.u + j*n
                    new_v = edge.v + j*n
                    self.add_directed_edge(new_u, new_v, edge.weight)

        # add ice and ice cream links
        for ice in ice_locs:
            self.add_directed_edge(ice, ice+n, 0)
            self.add_directed_edge(ice+n, ice, 0)

        for ice_cream in ice_cream_locs:
            self.add_directed_edge(ice_cream+n, ice_cream+(2*n), 0)
            self.add_directed_edge(ice_cream+(2*n), ice_cream+n, 0)


class Vertex:
    """
    A class for the vertex of a graph.

    == Attributes ==
    id:             the identifier of this vertex
    edges:          the edges of this vertex
    distance:       the distance between this vertex and the source vertex
    visited:        True if this vertex has been visited in the path, otherwise
                    False
    discovered:     True if this vertex has been discovered in the path,
                    otherwise False
    pos_in_heap:    the position of this vertex in the min heap
    previous:       the previous vertex that was visited before this vertex
                    was visited
    """

    def __init__(self, id):
        """
        Initialise a new vertex with id.

        :param id:  (int) the id of this vertex

        :time complexity:       O(1). Initialising all the variables takes
                                constant time.

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.
        """
        # vertex id
        self.id = id
        # edges of this vertex
        self.edges = []

        # distance
        self.distance = math.inf

        # have visited
        self.visited = False

        # have discovered
        self.discovered = False

        # position in heap
        self.pos_in_heap = None

        # backtracking
        self.previous = None

    def __eq__(self, other):
        """
        Return True if this vertex is the same as other, otherwise return
        False.

        :param other:           the other object to compare this vertex to

        :time complexity:       O(1). Comparison takes constant time.

        :space complexity:      O(1). This function uses constant space.

        :aux space complexity:  O(1). This function uses constant space.

        :return:                (bool) Return True if this vertex is equal to
                                other, otherwise return False.
        """
        if type(self) != type(other):
            return False

        return self.id == other.id

    def add_edge(self, edge):
        """
        Add edge to this vertex.

        :param edge:            (Edge) the edge to add

        :time complexity:       O(1). Appending to the end of the self.edges
                                list takes O(1) time.

        :space complexity:      O(1). This function uses constant space

        :aux space complexity:  O(1). This function uses constant space.

        :return:                None
        """
        self.edges.append(edge)


class Edge:
    """
    A class for an edge of a graph.

    == Attributes ==
    u:      (int) represents the vertex that is the origin of this edge
    v:      (int) represents the vertex that is the destination of this edge
    weight: (int) the weight of this edge
    """

    def __init__(self, u: int, v: int, weight: int):
        """
        Initialise a new edge coming from vertex u to vertex v with weight.

        :param u:               (int) represents the vertex that is the origin
                                of this edge
        :param v:               (int) represents the vertex that is the
                                destination of this edge
        :param weight:          (int) the weight of this edge

        :time complexity:       O(1). This function takes constant time
                                to initialise all variables.

        :space complexity:      O(1). This function uses constant input and
                                auxiliary space.

        :aux space complexity:  O(1). This function uses constant auxiliary
                                space.
        """
        # vertex from
        self.u = u
        # vertex to
        self.v = v
        self.weight = weight


class MinHeap:
    """
    A class for Min Heap.

    == Attributes ==
    array:      (list) an array that contains the contents of this min heap
    counter:    (int) the number of items in this heap
    """

    def __init__(self, size):
        """
        Initialise a new min heap with size.

        :param size:            (int) the maximum number of items that
                                this min heap can hold

        :time complexity:       Best and Worst Case: O(N), where N is size.
                                It takes O(N) time to initialise the array of
                                size N.

        :space complexity:      O(N), where N is size. This is because
                                the input is of constant size and this function
                                has an auxiliary space complexity of O(N).

        :aux space complexity:  O(N), where N is size. This is because
                                array is initialised to a size of N.
        """
        # indices start at 1
        # e.g., need an array of 11 cells if our heap has 10 elements
        self.array = [None] * (size + 1)

        # how many items are stored
        self.counter = 0

    def is_empty(self):
        """
        Return True if heap is empty, False otherwise.

        :time complexity:       Best and Worst Case: O(1). The comparison
                                takes constant time.

        :space complexity:      O(1). This function uses constant space.

        :aux space complexity:  O(1). This function uses constant space.

        :return:                (bool) True if heap is empty and False
                                otherwise.
        """

        return self.counter == 0

    def __len__(self):
        """
        Return the number of items in the heap.

        :time complexity:       Best and Worst Case: O(1). Returning
                                self.counter takes constant time.

        :space complexity:      O(1). This function uses constant space.

        :aux space complexity:  O(1). This function uses constant space.

        :return:                (int) length of the heap
        """
        return self.counter

    def is_full(self):
        """
        Return True if heap is full, otherwise return False.

        :time complexity:       Best and Worst Case: O(1). Comparison takes
                                constant time.

        :space complexity:      O(1). This function uses constant space.

        :aux space complexity:  O(1). This function uses constant space.

        :return:                (bool) True if heap is full and False otherwise.
        """
        # length of the array is one more than the max size of heap
        return self.counter + 1 == len(self.array)

    def swap(self, i, j):
        """
        Swap the vertices at index i and index j in the heap and update the
        pos_in_heap attribute in the corresponding vertices.

        :param i:               (int) vertex to swap at index i
        :param j:               (int) vertex to swap at index j

        :time complexity:       Best and Worst Case: O(1). Accessing and
                                assigning the vertices in the array and
                                updating the attribute takes constant time.

        :space complexity:      O(1). This function uses constant space.

        :aux space complexity:  O(1). This function uses constant space.

        :return:                None
        """

        # update vertex positions in heap
        self.array[i].pos_in_heap = j
        self.array[j].pos_in_heap = i

        # swap elements
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def rise(self, k):
        """
        Rise element at position k.

        :param k:               (int) index of the vertex to rise

        :time complexity:       Best Case: O(1). This occurs when the vertex
                                at position k in this heap is already in the
                                correct position. The while loop condition
                                will be False and the function will return.

                                Worst Case: O(log(N)), where N is the number of
                                items in the heap. This occurs when k is N
                                and the vertex at position k is the smallest
                                in this heap. The while loop will iterate at
                                most log(N) times because k decreases by a
                                factor of 2 at each iteration of the while loop
                                and the while loop will terminate when k <= 1.
                                The element will be risen all the way to
                                the top.

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.

        :return:                (int) the new index of the vertex that has
                                been risen
        """

        # k > 1 means that k has a parent
        # self.array[k][0] < self.array[k//2][0] means that the key of parent
        # is larger than the element at k
        # rise until the parent is less than or equal to the element at k

        while k > 1 and self.array[k].distance < self.array[k//2].distance:
            # swap element with parent because parent is larger
            self.swap(k, k//2)
            # update index k with the position of the parent
            # k now represents where the element is currently at
            k = k // 2

        # update final vertex position in heap
        self.array[k].pos_in_heap = k
        return k

    def smallest_child(self, k):
        """
        Returns the position of the smallest child of the element at position
        k.

        :precondition:          2k <= self.counter (k has at least one child)

        :param k:               (int) the index of the element to analyse

        :time complexity:       Best and Worst Case: O(1). Accessing and
                                comparing the elements at the appropriate
                                positions take constant time.

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.

        :return:                (int) position of the smallest child of k
        """

        # 2*k == self.counter: check that k only has one child, if yes,
        # then just return this child's index
        # self.array[2*k][0] < self.array[2*k + 1]: the left child is smaller
        # than the right child
        if 2*k == self.counter \
                or self.array[2*k].distance < self.array[2*k + 1].distance:
            return 2*k
        else:
            # return the index of the right child if right child is less than
            # the left child
            return 2*k + 1

    def sink(self, k):
        """
        Sink the element at position k to the correct position in the heap.

        :param k:               (int) the position of the element to sink

        :time complexity:       Best Case: O(1). This occurs when the
                                element at position k is already in the
                                correct position. The while loop will break
                                early and the function will return.

                                Worst Case: O(log(N)), where N is the number of
                                items in the heap. This occurs when k = 1 and
                                the element at position 1 is the largest item
                                in this heap. The while loop will iterate
                                at most O(log(N)) times because at each
                                iteration, the k increases by a factor of 2
                                and the while loop will terminate when
                                k > N/2. The element will be sunk all
                                the way to the bottom.

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.

        :return:                (int) the new position of the element that
                                was sunk
        """

        # while k has at least one child
        while 2*k <= self.counter:
            # find the smallest child of k
            child = self.smallest_child(k)

            # if the key of element k is smaller or equal to its smallest child,
            # then the element at k is already at the right position
            if self.array[k].distance <= self.array[child].distance:
                # break out of loop
                break

            # otherwise, swap index of child with index of k to sink
            self.swap(child, k)

            # update the index of k with the index of child
            k = child

        # update final vertex of position in heap
        self.array[k].pos_in_heap = k
        return k

    def add(self, vertex):
        """
        Add the element to the heap.

        :param vertex:          (Vertex) vertex to add to the heap

        :time complexity:       Best Case: O(1). This occurs when the element
                                is larger or equal to the parent so you just
                                add to the back to the array.

                                Worst Case: O(log(N)), where N is the number of
                                items in the array. This occurs when the vertex
                                added is the smallest in the heap. Then, when
                                this function calls rise(), the vertex will
                                be risen all the way to the top. This will cost
                                O(log(N)).

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.

        :return:                (int) the new position of the vertex added
        """

        if self.is_full():
            raise Exception("Heap is full!")

        # increment counter
        self.counter += 1
        self.array[self.counter] = vertex

        # set vertex's position in heap
        vertex.pos_in_heap = self.counter

        k = self.rise(self.counter)

        return k

    def serve(self):
        """
        Return the smallest element in the heap and serve (delete) it from the
        heap.

        :time complexity:       Best Case: O(1). This occurs when the element
                                at the last position in the heap is the next
                                smallest element in the heap. Then, the elements
                                after the serve are already in the correct
                                position and the call to sink() will cost O(1).

                                Worst Case: O(log(N)), where N is the number of
                                items in the array. This occurs when the element
                                at the last position in the heap is the largest
                                in the heap. Then, the element that the smallest
                                element was swapped with will sink all the
                                way to the bottom after the serve. Thus, the
                                call to sink() will cost O(log(N)).

        :space complexity:      O(1). This function takes constant time.

        :aux space complexity:  O(1). This function takes constant time.

        :return:                (Vertex) the smallest vertex in the heap
        """

        # swap the root with the last element in the heap
        smallest_el = self.array[1]
        self.swap(1, self.counter)

        # set position of vertex served to None
        self.array[self.counter].pos_in_heap = None

        # decrease the counter
        self.counter -= 1
        # sink the element at the first index to the appropriate position
        if self.counter > 0:
            self.sink(1)

        return smallest_el

    def get_vertex(self, k):
        """
        Return the vertex at position k.

        :param k:               (int) the position of the vertex in the heap

        :time complexity:       O(1). Accessing the element at position k
                                takes constant time.

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.

        :return:                (Vertex) the vertex at position k
        """

        return self.array[k]

    def update(self, k):
        """
        Update the vertex at position k to the appropriate position.

        :param k:               (int) the position of the vertex in the heap
                                to update

        :time complexity:       Best Case: O(1). This occurs when the
                                vertex at position k is already in the correct
                                position. Then, the call to rise() and sink()
                                will cost O(1).

                                Worst Case: O(log(N)), where N is the number
                                of items in the heap. This can occur when the
                                vertex at position k is either at the last
                                position of the heap and is updated to be
                                the smallest item in the heap. Then, the
                                call to rise() will cost O(log(N)). This can
                                also occur when the vertex at position k is
                                at the first position of the heap and is
                                updated to be the largest item in the heap,
                                Then, the call to sink() will cost O(log(N)).

        :space complexity:      O(1). This function takes constant space.

        :aux space complexity:  O(1). This function takes constant space.

        :return:                None
        """

        if k <= self.counter:
            # rise and sink
            self.rise(k)
            self.sink(k)
