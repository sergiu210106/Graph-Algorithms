class Graph:
    def __init__(self, n : dict = {}):
        self.list_of_neighbours = n

    def add_vertex(self, name): # O(1)
        if name in self.list_of_neighbours:
            raise ValueError("Vertex already in Graph")
        self.list_of_neighbours[name] = []
    def add_edge(self, start_vertex, terminal_vertex): # O(1)
        if start_vertex not in self.list_of_neighbours or terminal_vertex not in self.list_of_neighbours:
            raise ValueError("Vertices do not exist in current graph")

        if terminal_vertex in self.list_of_neighbours[start_vertex]:
            raise ValueError("Edge already exists")

        self.list_of_neighbours[start_vertex].append(terminal_vertex)

    def remove_edge(self, start_vertex, terminal_vertex): # O(E)
        if start_vertex not in self.list_of_neighbours or terminal_vertex not in self.list_of_neighbours:
            raise ValueError("Vertices do not exist in current graph")
        if terminal_vertex not in self.list_of_neighbours[start_vertex]:
            raise ValueError("Edge does not exist")
        for i in range(len(self.list_of_neighbours[start_vertex])):
            if self.list_of_neighbours[start_vertex][i] == terminal_vertex:
                del self.list_of_neighbours[start_vertex][i]
                break

    def remove_vertex(self, vertex): # O(V+E)
        if vertex not in self.list_of_neighbours:
            raise ValueError("Vertex not in Graph")

        for key in self.list_of_neighbours.keys():
            if vertex in self.list_of_neighbours[key]:
                self.remove_edge(key, vertex)

        del self.list_of_neighbours[vertex]

    def get_v(self): # O(1)
        return len(self.list_of_neighbours.keys())

    def get_e(self): # O(V+E)
        result = 0
        for i in self.list_of_neighbours.values():
            result += len(i)
        return result

    def is_edge(self, start_vertex, terminal_vertex): # O(V+E)
        if start_vertex not in self.list_of_neighbours or terminal_vertex not in self.list_of_neighbours:
            raise ValueError("Vertices do not exist in current graph")
        return terminal_vertex in self.list_of_neighbours[start_vertex]

    def neighbours(self, vertex) -> list: # O(V)
        if vertex not in self.list_of_neighbours:
            raise ValueError("Vertex not in Graph")
        return list(self.list_of_neighbours[vertex])[:]

    def neighbours_v2(self, vertex): # Theta(1)
        if vertex not in self.list_of_neighbours:
            raise ValueError("Vertex not in Graph")
        return iter(self.list_of_neighbours[vertex])

    def inbound_neighbours(self, vertex): # O(V)
        ans = []
        for v in self.list_of_neighbours:
            if vertex in self.list_of_neighbours[v]:
                ans.append(v)
        return ans
    def get_vertices(self): # O(V)
        return list(self.list_of_neighbours.keys())[:]

    def __str__(self):
        s = "directed unweighted\n"
        for k in self.list_of_neighbours.keys():
            for o in self.list_of_neighbours[k]:
                s += f"{k} {o}\n"
            if not self.list_of_neighbours[k]:
                s+=f"{k}\n"
        return s