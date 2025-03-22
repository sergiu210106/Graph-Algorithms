class Graph:
    def __init__(self, n: dict = None, directed=True, weighted=False):
        self.list_of_neighbours = n if n is not None else {}
        self.directed = directed
        self.weighted = weighted

    def add_vertex(self, name):  # Theta(1)
        if name in self.list_of_neighbours:
            raise ValueError("Vertex already in Graph")
        self.list_of_neighbours[name] = []

    def add_edge(self, start_vertex, terminal_vertex, weight=0):  # Theta(1)
        if start_vertex not in self.list_of_neighbours or terminal_vertex not in self.list_of_neighbours:
            raise ValueError("Vertices do not exist in current graph")

        edge = (terminal_vertex, weight) if self.weighted else terminal_vertex
        reversed_edge = (start_vertex, weight) if self.weighted else start_vertex

        if self.weighted:
            if any(e[0] == terminal_vertex for e in self.list_of_neighbours[start_vertex]):
                raise ValueError("Edge already exists")
        else:
            if edge in self.list_of_neighbours[start_vertex]:
                raise ValueError("Edge already exists")

        self.list_of_neighbours[start_vertex].append(edge)

        if not self.directed:
            if self.weighted:
                if not any(e[0] == start_vertex for e in self.list_of_neighbours[terminal_vertex]):
                    self.list_of_neighbours[terminal_vertex].append(reversed_edge)
            else:
                if reversed_edge not in self.list_of_neighbours[terminal_vertex]:
                    self.list_of_neighbours[terminal_vertex].append(reversed_edge)

    def remove_edge(self, start_vertex, terminal_vertex):  # O(E/V)
        if start_vertex not in self.list_of_neighbours or terminal_vertex not in self.list_of_neighbours:
            raise ValueError("Vertices do not exist in current graph")

        def remove_single_edge(from_vertex, to_vertex):
            if self.weighted:
                for e in self.list_of_neighbours[from_vertex]:
                    if e[0] == to_vertex:
                        self.list_of_neighbours[from_vertex].remove(e)
                        return
                raise ValueError("Edge does not exist")
            else:
                try:
                    self.list_of_neighbours[from_vertex].remove(to_vertex)
                except ValueError:
                    raise ValueError("Edge does not exist")

        remove_single_edge(start_vertex, terminal_vertex)
        if not self.directed:
            remove_single_edge(terminal_vertex, start_vertex)

    def remove_vertex(self, vertex):  # O(V+E)
        if vertex not in self.list_of_neighbours:
            raise ValueError("Vertex does not exist in current graph")

        for key in list(self.list_of_neighbours.keys()):
            if self.weighted:
                self.list_of_neighbours[key] = [e for e in self.list_of_neighbours[key] if e[0] != vertex]
            else:
                if vertex in self.list_of_neighbours[key]:
                    self.list_of_neighbours[key].remove(vertex)

        del self.list_of_neighbours[vertex]

    def get_v(self):  # O(1)
        return len(self.list_of_neighbours.keys())

    def get_e(self):  # Theta(V)
        result = 0
        for i in self.list_of_neighbours.values():
            result += len(i)
        return result

    def is_edge(self, start_vertex, terminal_vertex):  # O(E/V)
        if start_vertex not in self.list_of_neighbours or terminal_vertex not in self.list_of_neighbours:
            raise ValueError("Vertices do not exist in current graph")
        if self.weighted:
            exists = any(e[0] == terminal_vertex for e in self.list_of_neighbours[start_vertex])
            if not self.directed:
                exists = exists and any(e[0] == start_vertex for e in self.list_of_neighbours[terminal_vertex])
            return exists
        else:
            if self.directed:
                return terminal_vertex in self.list_of_neighbours[start_vertex]
            else:
                return (terminal_vertex in self.list_of_neighbours[start_vertex] and
                        start_vertex in self.list_of_neighbours[terminal_vertex])

    def neighbours(self, vertex) -> list:  # O(V)
        if vertex not in self.list_of_neighbours:
            raise ValueError("Vertex not in Graph")
        return list(self.list_of_neighbours[vertex])[:]

    def neighbours_v2(self, vertex):  # Theta(1)
        if vertex not in self.list_of_neighbours:
            raise ValueError("Vertex not in Graph")
        return iter(self.list_of_neighbours[vertex])

    def inbound_neighbours(self, vertex):  # O(V+E)
        if not self.directed:
            return self.neighbours(vertex)
        ans = []
        for v in self.list_of_neighbours:
            if self.weighted:
                if any(e[0] == vertex for e in self.list_of_neighbours[v]):
                    ans.append(v)
            else:
                if vertex in self.list_of_neighbours[v]:
                    ans.append(v)
        return ans

    def get_vertices(self):  # O(V)
        return list(self.list_of_neighbours.keys())[:]

    def change_if_directed(self, option: bool):
        if self.directed == option:
            return

        if option:
            # Converting from undirected to directed
            for u in self.list_of_neighbours:
                for v in self.list_of_neighbours[u]:
                    if self.weighted:
                        if not any(e[0] == u for e in self.list_of_neighbours[v]):
                            self.list_of_neighbours[v].append((u, v[1] if isinstance(v, tuple) else 0))
                    else:
                        if u not in self.list_of_neighbours[v]:
                            self.list_of_neighbours[v].append(u)
            self.directed = True
        else:
            # Converting from directed to undirected
            for u in self.list_of_neighbours:
                for v in self.list_of_neighbours[u]:
                    if self.weighted:
                        if not any(e[0] == u for e in self.list_of_neighbours[v]):
                            self.list_of_neighbours[v].append((u, v[1] if isinstance(v, tuple) else 0))
                    else:
                        if u not in self.list_of_neighbours[v]:
                            self.list_of_neighbours[v].append(u)
            self.directed = False

            for u in self.list_of_neighbours:
                if self.weighted:
                    unique = {}
                    for e in self.list_of_neighbours[u]:
                        unique[e[0]] = e
                    self.list_of_neighbours[u] = list(unique.values())
                else:
                    self.list_of_neighbours[u] = list(set(self.list_of_neighbours[u]))

    def get_weight(self, start_vertex, terminal_vertex):
        if not self.weighted:
            raise ValueError("Graph is not weighted")
        if start_vertex not in self.list_of_neighbours:
            raise ValueError("Start vertex does not exist")
        for edge in self.list_of_neighbours[start_vertex]:
            if isinstance(edge, tuple) and edge[0] == terminal_vertex:
                return edge[1]
        raise ValueError("Edge does not exist")

    def set_weight(self, start_vertex, terminal_vertex, weight):
        if not self.weighted:
            raise ValueError("Graph is not weighted")
        if start_vertex not in self.list_of_neighbours:
            raise ValueError("Start vertex does not exist")
        updated = False
        for idx, edge in enumerate(self.list_of_neighbours[start_vertex]):
            if edge[0] == terminal_vertex:
                self.list_of_neighbours[start_vertex][idx] = (terminal_vertex, weight)
                updated = True
                break
        if not updated:
            raise ValueError("Edge does not exist")
        if not self.directed:
            updated = False
            for idx, edge in enumerate(self.list_of_neighbours[terminal_vertex]):
                if edge[0] == start_vertex:
                    self.list_of_neighbours[terminal_vertex][idx] = (start_vertex, weight)
                    updated = True
                    break
            if not updated:
                raise ValueError("Reverse edge does not exist")

    def change_if_weighted(self, option: bool):
        if self.weighted == option:
            return
        if option:
            # Convert from unweighted to weighted
            for vertex in self.list_of_neighbours:
                new_list = []
                for edge in self.list_of_neighbours[vertex]:
                    new_list.append((edge, 0))
                self.list_of_neighbours[vertex] = new_list
        else:
            # Convert from weighted to unweighted
            for vertex in self.list_of_neighbours:
                new_list = []
                for edge in self.list_of_neighbours[vertex]:
                    if isinstance(edge, tuple):
                        new_list.append(edge[0])
                    else:
                        new_list.append(edge)
                self.list_of_neighbours[vertex] = new_list
        self.weighted = option

    def __str__(self):
        s = ("directed weighted\n" if self.directed and self.weighted else
             "directed unweighted\n" if self.directed else
             "undirected weighted\n" if self.weighted else
             "undirected unweighted\n")
        for k in self.list_of_neighbours.keys():
            for edge in self.list_of_neighbours[k]:
                if self.weighted:
                    s += f"{k} {edge[0]} (weight: {edge[1]})\n"
                else:
                    s += f"{k} {edge}\n"
            if not self.list_of_neighbours[k]:
                s += f"{k}\n"
        return s

        # ============================
        # BFS and DFS Iterator Methods
        # ============================

    def BFS_iter(self, start_vertex):
        return BFSIterator(self, start_vertex)

    def DFS_iter(self, start_vertex):
        return DFSIterator(self, start_vertex)

    # Iterator classes for BFS and DFS

class BFSIterator:
    def __init__(self, graph, start_vertex):
        if start_vertex not in graph.list_of_neighbours:
            raise ValueError("Start vertex not in graph")
        self.graph = graph
        self.queue = [(start_vertex, 0)]  # (vertex, distance)
        self.visited = {start_vertex}

    def __iter__(self):
        return self

    def __next__(self):
        if not self.queue:
            raise StopIteration
        current, dist = self.queue.pop(0)

        for neighbor in self.graph.list_of_neighbours[current]:
            nb = neighbor[0] if self.graph.weighted else neighbor
            if nb not in self.visited:
                self.visited.add(nb)
                self.queue.append((nb, dist + 1))
        return (current, dist)

class DFSIterator:
    def __init__(self, graph, start_vertex):
        if start_vertex not in graph.list_of_neighbours:
            raise ValueError("Start vertex not in graph")
        self.graph = graph
        self.stack = [(start_vertex, 0)]  # (vertex, depth)
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            current, depth = self.stack.pop()
            if current in self.visited:
                continue
            self.visited.add(current)
            neighbors = list(self.graph.list_of_neighbours[current])
            for neighbor in neighbors:
                nb = neighbor[0] if self.graph.weighted else neighbor
                if nb not in self.visited:
                    self.stack.append((nb, depth + 1))
            return (current, depth)
        raise StopIteration
