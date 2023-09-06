import networkx as nx
from sample import generate_sample
from typing import Dict, Tuple
from heapq import heappop, heappush


def BOAstar(
    G: nx.DiGraph, start: int, goal: int, h: Dict[int, Tuple[int, int]]
) -> Dict[int, Tuple[int, int]]:
    sols = {n: [] for n in G.nodes()}
    g2min = {n: float("inf") for n in G.nodes()}

    # Node: f(x), g(x), node, parent
    node = ((h[start][0], h[start][1]), (0, 0), start, None)
    openlist = []
    heappush(openlist, node)

    iteration = 0
    while openlist:
        iteration += 1
        fn, gn, n, pn = heappop(openlist)

        if gn[1] >= g2min[n] or fn[1] >= g2min[goal]:
            continue

        g2min[n] = gn[1]
        sols[n].append(gn)

        xn_str = f"x{n}"
        pn_str = "null" if pn is None else f"x{pn}"
        print(f"{iteration} {xn_str} {pn_str} {gn} {fn} {g2min[n]}")

        if n == goal:
            continue

        for m in G.neighbors(n):
            gm = (gn[0] + G[n][m]["c1"], gn[1] + G[n][m]["c2"])
            fm = (gm[0] + h[m][0], gm[1] + h[m][1])
            new_node = (fm, gm, m, n)
            if gm[1] >= g2min[m] or fm[1] >= g2min[goal]:
                continue
            heappush(openlist, new_node)

    return sols[goal]


if __name__ == "__main__":
    G = generate_sample()
    Gr = G.reverse()
    start = 0
    goal = 5

    # Debug print
    # for u, v, data in G.edges(data=True):
    #     print(u, v, data)

    # Compute consistent heuristic values
    # on each 'c1' or 'c2' dimension,
    # using standard dijkstra algorithms.
    dist_c1 = nx.single_source_dijkstra_path_length(Gr, goal, weight="c1")
    dist_c2 = nx.single_source_dijkstra_path_length(Gr, goal, weight="c2")
    for n in G.nodes():
        if n not in dist_c1:
            dist_c1[n] = float("inf")
        if n not in dist_c2:
            dist_c2[n] = float("inf")

    print()
    print("-----------------------")
    print("- computed heuristics -")
    consistent_h = {n: (dist_c1[n], dist_c2[n]) for n in G.nodes()}
    consistent_h[1] = (3, 6)
    for n in G.nodes():
        print(n, consistent_h[n])
    print("-----------------------")
    print()

    sols = BOAstar(G, start, goal, consistent_h)
    print(sols)
