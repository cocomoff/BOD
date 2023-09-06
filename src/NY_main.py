import dill
import time
import pandas as pd
import networkx as nx
import numpy as np
from typing import Dict, Tuple
from heapq import heappop, heappush
import matplotlib.pyplot as plt
plt.style.use("ggplot")

def BOAstar(
    G: nx.Graph, start: int, goal: int, h: Dict[int, Tuple[int, int]], keys: Tuple[str] = ("c1", "c2")
) -> Dict[int, Tuple[int, int]]:
    sols = {n: [] for n in G.nodes()}
    g2min = {n: float("inf") for n in G.nodes()}

    K1, K2 = keys

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
        # print(f"{iteration} {xn_str} {pn_str} {gn} {fn} {g2min[n]}")

        if n == goal:
            continue

        for m in G.neighbors(n):
            gm = (gn[0] + G[n][m][K1], gn[1] + G[n][m][K2])
            fm = (gm[0] + h[m][0], gm[1] + h[m][1])
            new_node = (fm, gm, m, n)
            if gm[1] >= g2min[m] or fm[1] >= g2min[goal]:
                continue
            heappush(openlist, new_node)

    return sols[goal]


if __name__ == "__main__":
    # read G and instances (pair of (s, t))
    ts = time.time()
    G = dill.load(open("USA-road-NY-graph.dill", "rb"))
    instance = pd.read_csv("NY-instance.txt", names=["source", "dist"])
    t1 = time.time() - ts

    idx = 0
    instanceI = instance.iloc[idx]
    start = instanceI.source
    goal = instanceI.dist
    print(G.number_of_nodes(), G.number_of_edges(), "|", start, goal)

    # Compute consistent heuristic values
    # on each 'c1' or 'c2' dimension,
    # using standard dijkstra algorithms.
    key1 = "cost"
    key2 = "resource"
    ts = time.time()
    dist_k1 = nx.single_source_dijkstra_path_length(G, goal, weight=key1)
    dist_k2 = nx.single_source_dijkstra_path_length(G, goal, weight=key2)
    for n in G.nodes():
        if n not in dist_k1:
            dist_k1[n] = float("inf")
        if n not in dist_k2:
            dist_k2[n] = float("inf")

    # first 10 samples
    for (idn, n) in enumerate(G.nodes()):
        if idn >= 10:
            break
        print(n, dist_k1[n], dist_k2[n])

    # run BOA*
    ts = time.time()
    consistent_h = {n: (dist_k1[n], dist_k2[n]) for n in G.nodes()}
    t2 = time.time() - ts

    ts = time.time()
    sols = BOAstar(G, start, goal, consistent_h, keys=(key1, key2))
    t3 = time.time() - ts
    print(sols)

    print("Time1:", t1)
    print("Time2:", t2)
    print("Time3:", t3)
    

    # min dist with Key 1 and Key 2
    value1 = nx.dijkstra_path_length(G, start, goal, weight=key1)
    value2 = nx.dijkstra_path_length(G, start, goal, weight=key2)

    plot_x = np.array([sol[0] for sol in sols])
    plot_y = np.array([sol[1] for sol in sols])
    
    # plot (x; cost, y: resource)
    f = plt.figure(figsize=(4, 4))
    a = f.gca()
    a.axvline(x=value1, ls="--", lw=1, alpha=0.5)
    a.axhline(y=value2, ls="--", lw=1, alpha=0.5)
    a.scatter(plot_x, plot_y, marker="x", s=20, color="dodgerblue")
    a.set_xlabel(f"{key1}")
    a.set_ylabel(f"{key2}")
    plt.tight_layout()
    plt.savefig(f"instance{idx}.png")