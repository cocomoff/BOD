import networkx as nx
from sample import generate_sample
from typing import Dict, Tuple, List
from heapq import heappop, heappush


def BOD(G: nx.DiGraph, start: int) -> Dict[int, List[Tuple[Tuple[int, int], int]]]:
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
        sols[n].append((gn, pn))

        for m in G.neighbors(n):
            gm = (gn[0] + G[n][m]["c1"], gn[1] + G[n][m]["c2"])
            new_node = (gm, m, n)
            if gm[1] >= g2min[m]:
                continue
            heappush(openlist, new_node)

    return sols


def trace(G, sols, start: int, goal: int) -> List[List[int]]:
    print(sols)

    paths = []

    def _intrace(cost, n, goal):
        path = [goal]
        node = n
        cost_n = [cost[0], cost[1]]
        while node is not None:
            new_cost_n = [cost_n[0], cost_n[1]]
            cost_edge = [G[node][path[-1]]["c1"], G[node][path[-1]]["c2"]]
            rev_cost = (new_cost_n[0] - cost_edge[0], new_cost_n[1] - cost_edge[1])
            path.append(node)

            target_node = None
            for elem in sols[node]:
                if elem[0] == rev_cost:
                    target_node = elem[1]

            if target_node is None:
                break

            cost_n[:] = rev_cost
            node = target_node

        path.reverse()
        return path

    for cost, p in sols[goal]:
        path = _intrace(cost, p, goal)
        paths.append((path, cost))

    return paths


if __name__ == "__main__":
    G = generate_sample()
    start = 0
    goal = 5

    sols = BOD(G, start)
    paths = trace(G, sols, start, goal)
    for path, cost in paths:
        print(path, cost)
