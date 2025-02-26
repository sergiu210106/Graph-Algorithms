from graph import Graph


def test_graph():
    g = Graph()

    # Test adding vertices
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    assert g.get_v() == 3
    assert set(g.get_vertices()) == {"A", "B", "C"}

    # Test adding edges
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    assert g.get_e() == 2
    assert g.is_edge("A", "B")
    assert g.is_edge("B", "C")
    assert not g.is_edge("A", "C")

    # Test neighbours
    assert g.neighbours("A") == ["B"]
    assert g.neighbours("B") == ["C"]
    assert g.neighbours("C") == []

    # Test inbound neighbours
    assert g.inbound_neighbours("C") == ["B"]
    assert g.inbound_neighbours("B") == ["A"]
    assert g.inbound_neighbours("A") == []

    # Test removing edges
    g.remove_edge("A", "B")
    assert not g.is_edge("A", "B")
    assert g.get_e() == 1

    # Test removing vertices
    g.remove_vertex("B")
    assert g.get_v() == 2
    assert "B" not in g.get_vertices()
    assert g.get_e() == 0  # Since "B" was connected to "C"

    print("All tests passed!")


test_graph()