import networkx as nx


def generate_sample() -> nx.DiGraph:
    g = nx.DiGraph()
    g.add_nodes_from(range(6))

    edges = [
        # from, to, c1, c2
        (0, 1, 1, 1),
        (0, 2, 1, 5),
        (0, 3, 1, 1),
        (1, 2, 1, 2),
        (1, 4, 4, 8),
        (1, 5, 7, 5),
        (2, 5, 2, 4),
        (3, 2, 2, 1),
        (3, 5, 5, 7),
        (5, 4, 3, 2),
    ]

    for u, v, c1, c2 in edges:
        g.add_edge(u, v, c1=c1, c2=c2)

    return g
