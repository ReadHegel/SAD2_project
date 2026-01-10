import networkx as nx


def dump_digraph(G, name: str = ""):
    print(f"=== GRAPH INFO {name}===")
    print(G)

    print("\n=== NODES ===")
    for n, a in G.nodes(data=True):
        print(n, a)

    print("\n=== EDGES ===")
    for u, v, a in G.edges(data=True):
        print(f"{u} -> {v}, {a}")

    print("\n=== IN / OUT DEGREE ===")
    print("IN :", dict(G.in_degree(weight="weight")))
    print("OUT:", dict(G.out_degree(weight="weight")))

    print("\n=== SCC ===")
    print(list(nx.strongly_connected_components(G)))


def validate(G1: nx.DiGraph, G2: nx.DiGraph):
    assert list(G1.nodes()) == list(G2.nodes())


def jaccard_weighted(G1: nx.DiGraph, G2: nx.DiGraph):
    validate(G1, G2)

    edges = set(G1.edges() | G2.edges())
    num = 0.0
    den = 0.0

    for u, v in edges:
        # Taka heura na ujemne krawędzie ?
        s1: set = G1[u][v].get("sign", {}) if G1.has_edge(u, v) else set()
        s2: set = G2[u][v].get("sign", {}) if G2.has_edge(u, v) else set()

        # print(G1[u][v].get("sign", {0}) if G1.has_edge(u, v) else "Noedge")
        # print(G2[u][v].get("sign", {0}) if G2.has_edge(u, v) else "Noedge")
        # print("__________________")

        num += len(s1 & s2) 
        den += len(s1 | s2)

    return num / den if den > 0 else 1.0


def jaccard(G1: nx.DiGraph, G2: nx.DiGraph):
    validate(G1, G2)

    edges = set(G1.edges() | G2.edges())
    num = 0.0
    den = 0.0

    for u, v in edges:
        w1 = 1 if G1.has_edge(u, v) else 0
        w2 = 1 if G2.has_edge(u, v) else 0

        num += min(w1, w2)
        den += max(w1, w2)

    return num / den if den > 0 else 1.0


GRAPH_METRICS = [jaccard_weighted, jaccard]
