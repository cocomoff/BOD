import networkx as nx
from sample import generate_sample
from typing import Dict, Tuple
from heapq import heappop, heappush


def BOD(G: nx.DiGraph, start: int) -> Dict[int, Tuple[int, int]]:
    sols = {n: [] for n in G.nodes()}
    g2min = {n: float("inf") for n in G.nodes()}

    # Node: g(x), node, parent
    node = ((0, 0), start, None)
    openlist = []
    heappush(openlist, node)

    while openlist:
        gn, n, pn = heappop(openlist)

        if gn[1] >= g2min[n]:
            continue

        g2min[n] = gn[1]
        sols[n].append(gn)

        for m in G.neighbors(n):
            gm = (gn[0] + G[n][m]["c1"], gn[1] + G[n][m]["c2"])
            new_node = (gm, m, n)
            if gm[1] >= g2min[m]:
                continue
            heappush(openlist, new_node)

    return sols


if __name__ == "__main__":
    G = generate_sample()
    start = 0

    # Debug print
    # for u, v, data in G.edges(data=True):
    #     print(u, v, data)

    sols = BOD(G, start)
    print(sols)
