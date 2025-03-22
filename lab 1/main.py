import unittest
from graph import Graph  # Ensure the Graph class is imported correctly

class TestGraph(unittest.TestCase):

    def setUp(self):
        # Create four variants of graphs for testing:
        # 1. Directed Unweighted
        self.du_graph = Graph(directed=True, weighted=False)
        # 2. Undirected Unweighted
        self.uu_graph = Graph(directed=False, weighted=False)
        # 3. Directed Weighted
        self.dw_graph = Graph(directed=True, weighted=True)
        # 4. Undirected Weighted
        self.uw_graph = Graph(directed=False, weighted=True)

        # Add vertices to all graphs.
        for g in [self.du_graph, self.uu_graph, self.dw_graph, self.uw_graph]:
            for vertex in ["A", "B", "C", "D"]:
                g.add_vertex(vertex)

    def test_add_vertex(self):
        self.du_graph.add_vertex("E")
        self.assertIn("E", self.du_graph.get_vertices())
        with self.assertRaises(ValueError):
            self.du_graph.add_vertex("A")  # Duplicate vertex

    def test_add_edge_unweighted_directed(self):
        self.du_graph.add_edge("A", "B")
        self.assertTrue(self.du_graph.is_edge("A", "B"))
        self.assertFalse(self.du_graph.is_edge("B", "A"))

    def test_add_edge_unweighted_undirected(self):
        self.uu_graph.add_edge("A", "B")
        self.assertTrue(self.uu_graph.is_edge("A", "B"))
        self.assertTrue(self.uu_graph.is_edge("B", "A"))

    def test_add_edge_weighted_directed(self):
        self.dw_graph.add_edge("A", "B", weight=5)
        self.assertTrue(self.dw_graph.is_edge("A", "B"))
        self.assertEqual(self.dw_graph.get_weight("A", "B"), 5)
        self.assertFalse(self.dw_graph.is_edge("B", "A"))
        with self.assertRaises(ValueError):
            self.dw_graph.add_edge("A", "B", weight=5)  # Duplicate

    def test_add_edge_weighted_undirected(self):
        self.uw_graph.add_edge("A", "B", weight=3)
        self.assertTrue(self.uw_graph.is_edge("A", "B"))
        self.assertTrue(self.uw_graph.is_edge("B", "A"))
        self.assertEqual(self.uw_graph.get_weight("A", "B"), 3)
        self.assertEqual(self.uw_graph.get_weight("B", "A"), 3)

    def test_remove_edge_unweighted(self):
        self.uu_graph.add_edge("A", "B")
        self.uu_graph.remove_edge("A", "B")
        self.assertFalse(self.uu_graph.is_edge("A", "B"))
        self.assertFalse(self.uu_graph.is_edge("B", "A"))
        with self.assertRaises(ValueError):
            self.uu_graph.remove_edge("A", "B")

    def test_remove_edge_weighted(self):
        self.uw_graph.add_edge("A", "B", weight=7)
        self.uw_graph.remove_edge("A", "B")
        self.assertFalse(self.uw_graph.is_edge("A", "B"))
        self.assertFalse(self.uw_graph.is_edge("B", "A"))
        with self.assertRaises(ValueError):
            self.uw_graph.remove_edge("A", "B")

    def test_remove_vertex(self):
        self.du_graph.add_edge("A", "B")
        self.du_graph.add_edge("C", "A")
        self.du_graph.remove_vertex("A")
        self.assertNotIn("A", self.du_graph.get_vertices())
        for vertex in self.du_graph.get_vertices():
            self.assertNotIn("A", self.du_graph.neighbours(vertex))
        with self.assertRaises(ValueError):
            self.du_graph.remove_vertex("Z")

    def test_get_v_and_get_e(self):
        self.du_graph.add_edge("A", "B")
        self.du_graph.add_edge("B", "C")
        self.assertEqual(self.du_graph.get_v(), 4)
        self.assertEqual(self.du_graph.get_e(), 2)

    def test_neighbours_and_inbound(self):
        self.du_graph.add_edge("A", "B")
        self.du_graph.add_edge("C", "B")
        self.assertEqual(set(self.du_graph.neighbours("A")), {"B"})
        self.assertEqual(set(self.du_graph.inbound_neighbours("B")), {"A", "C"})

    def test_set_and_get_weight(self):
        self.dw_graph.add_edge("A", "B", weight=2)
        self.dw_graph.set_weight("A", "B", 10)
        self.assertEqual(self.dw_graph.get_weight("A", "B"), 10)
        self.uw_graph.add_edge("A", "B", weight=4)
        self.uw_graph.set_weight("A", "B", 8)
        self.assertEqual(self.uw_graph.get_weight("B", "A"), 8)
        with self.assertRaises(ValueError):
            self.du_graph.set_weight("A", "B", 5)  # Unweighted graph

    def test_change_if_weighted(self):
        self.uu_graph.add_edge("A", "B")
        self.uu_graph.change_if_weighted(True)
        self.assertTrue(self.uu_graph.weighted)
        nbs = self.uu_graph.neighbours("A")
        self.assertTrue(any(isinstance(e, tuple) and e[0] == "B" for e in nbs))
        self.uu_graph.change_if_weighted(False)
        self.assertFalse(self.uu_graph.weighted)
        nbs = self.uu_graph.neighbours("A")
        self.assertTrue("B" in nbs)

    def test_change_if_directed(self):
        self.du_graph.add_edge("A", "B")
        self.assertFalse(self.du_graph.is_edge("B", "A"))
        self.du_graph.change_if_directed(False)
        self.assertTrue(self.du_graph.is_edge("A", "B"))
        self.assertTrue(self.du_graph.is_edge("B", "A"))
        self.du_graph.change_if_directed(True)
        self.assertTrue(self.du_graph.is_edge("A", "B"))
        self.assertTrue(self.du_graph.is_edge("B", "A"))

    def test_BFS_iterator(self):
        # Build a simple graph:
        # A -> B, A -> C, B -> D, C -> D
        self.du_graph.add_edge("A", "B")
        self.du_graph.add_edge("A", "C")
        self.du_graph.add_edge("B", "D")
        self.du_graph.add_edge("C", "D")
        bfs = self.du_graph.BFS_iter("A")
        result = []
        for vertex, dist in bfs:
            result.append((vertex, dist))
        # Expected order: A (0), B (1), C (1), D (2)
        self.assertEqual(result, [("A", 0), ("B", 1), ("C", 1), ("D", 2)])

    def test_DFS_iterator(self):
        # Build a simple graph:
        # A -> B, A -> C, B -> D, C -> D
        self.du_graph.add_edge("A", "B")
        self.du_graph.add_edge("A", "C")
        self.du_graph.add_edge("B", "D")
        self.du_graph.add_edge("C", "D")
        dfs = self.du_graph.DFS_iter("A")
        result = []
        for vertex, depth in dfs:
            result.append((vertex, depth))
        # DFS order may vary. Check that all vertices are visited.
        vertices_visited = set(v for v, _ in result)
        self.assertEqual(vertices_visited, {"A", "B", "C", "D"})

    def test_str_output(self):
        self.dw_graph.add_edge("A", "B", weight=5)
        output = str(self.dw_graph)
        self.assertIn("directed weighted", output)
        self.assertIn("A B (weight: 5)", output)

if __name__ == "__main__":
    unittest.main()
