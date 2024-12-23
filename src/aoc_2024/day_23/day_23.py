from collections import defaultdict

from common.input import get_data_file, get_lines

EXAMPLE = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def find_t_triangles(graph: dict[str, set]) -> set:
    triangles = set()
    for node_a in graph:
        for node_b in [node for node in graph[node_a] if node > node_a]:
            for node_c in [node for node in (graph[node_b] & graph[node_a]) if node > node_b]:
                if node_a[0] == "t" or node_b[0] == "t" or node_c[0] == "t":
                    triangles.add(tuple(sorted((node_a, node_b, node_c))))
    return triangles


def find_cliques(graph: dict[str, set], current_clique: set, potential_nodes: set, excluded: set, cliques: list):
    if not potential_nodes and not excluded:
        cliques.append(current_clique)
        return
    for node in list(potential_nodes):
        find_cliques(
            graph,
            current_clique.union({node}),
            potential_nodes.intersection(graph[node]),
            excluded.intersection(graph[node]),
            cliques,
        )
        potential_nodes.remove(node)
        excluded.add(node)


def build_graph(data: str) -> dict[str, set]:
    graph = defaultdict(set)
    connections = get_lines(data)
    for connection in connections:
        a_node, b_node = connection.split("-")
        graph[a_node].add(b_node)
        graph[b_node].add(a_node)
    return graph


def find_lan_party(data: str, biggest: bool) -> int | str:
    graph = build_graph(data)
    if not biggest:
        triangles = find_t_triangles(graph)
        return len(triangles)
    cliques = []
    find_cliques(graph, set(), set(graph.keys()), set(), cliques)
    largest_clique = sorted(list(max(cliques, key=len)))
    return ",".join(largest_clique)


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    return find_lan_party(source, part_b)
