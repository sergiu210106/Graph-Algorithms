from graph import Graph

def test_graph():
    # Create a new graph instance
    g = Graph()

    # Test adding vertices
    g.add_vertex("A")  # Theta(1)
    g.add_vertex("B")  # Theta(1)
    g.add_vertex("C")  # Theta(1)
    assert g.get_v() == 3
    assert set(g.get_vertices()) == {"A", "B", "C"}

    # Test adding edges
    g.add_edge("A", "B")  # Worst-case O(V+E)
    g.add_edge("B", "C")
    assert g.get_e() == 2
    assert g.is_edge("A", "B")
    assert g.is_edge("B", "C")
    assert not g.is_edge("A", "C")

    # Test the original neighbours function (returns a list copy)
    assert g.neighbours("A") == ["B"]
    assert g.neighbours("B") == ["C"]
    assert g.neighbours("C") == []

    # Test the new iterator-based neighbours_v2 function (Theta(1) for iterator creation)
    neighbors_iter_A = list(g.neighbours_v2("A"))
    neighbors_iter_B = list(g.neighbours_v2("B"))
    neighbors_iter_C = list(g.neighbours_v2("C"))
    assert neighbors_iter_A == ["B"]
    assert neighbors_iter_B == ["C"]
    assert neighbors_iter_C == []

    # Test inbound neighbours
    assert g.inbound_neighbours("C") == ["B"]
    assert g.inbound_neighbours("B") == ["A"]
    assert g.inbound_neighbours("A") == []

    # Test removing an edge
    g.remove_edge("A", "B")
    assert not g.is_edge("A", "B")
    assert g.get_e() == 1

    # Test removing a vertex (also removes associated edges)
    g.remove_vertex("B")
    assert g.get_v() == 2
    assert "B" not in g.get_vertices()
    assert g.get_e() == 0  # "B" was connected to "C", so edge count is now 0

    print("All tests passed!")


# Run the tests
if __name__ == '__main__':
    test_graph()
