import networkx as nx
import dill
import numpy as np
import os.path


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


def generate_sample_undirected() -> nx.Graph:
    g = nx.Graph()
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


def new_york() -> nx.Graph:
    G = dill.load(open("USA-road-NY-graph.dill", "rb"))
    # for id, (u, v, data) in enumerate(G.edges(data=True)):
    #     print(id, u, v, data)
    #     if id >= 10:
    #         break
    print(G.number_of_nodes(), G.number_of_edges())

    # samples
    if not os.path.exists("NY-instance.txt"):
        N = G.number_of_nodes()
        candidates = []
        while len(candidates) < 10:
            n1, n2 = np.random.randint(N, size=2)
            if n1 == n2:
                n1, n2 = np.random.randint(N, size=2)
            if n1 >= n2:
                n1, n2 = n2, n1

            l1 = nx.shortest_path_length(G, n1, n2, weight="resource")
            l2 = nx.shortest_path_length(G, n1, n2, weight="time")
            if l1 <= 300_000:
                print(n1, n2, l1, l2)
                candidates.append((n1, n2))
        with open("NY-instance.txt", "w") as fp:
            for n1, n2 in candidates:
                fp.write(f"{n1},{n2}\n")

    return G


if __name__ == "__main__":
    new_york()
