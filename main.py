from itertools import permutations

import networkx as nx

G = []
H = []

G.append([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]])
H.append([[0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]])

G.append(
    [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0],
    ]
)
H.append(
    [
        [0, 1, 0, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0],
    ]
)

G.append([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]])
H.append([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]])

G.append(
    [
        [0, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 0],
    ]
)
H.append(
    [
        [0, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 0],
    ]
)

G.append([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]])
H.append(
    [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
    ]
)


def get_number_of_edges(graph: list[list[int]]):
    return sum(sum(row) for row in graph) // 2


def get_list_of_degrees(graph: list[list[int]]):
    return list(map(sum, graph))


def are_graphs_isomorphic(G: list[list[int]], H: list[list[int]]):

    # Number of vertexs
    if len(G) != len(H):
        return False

    # Number of edges
    edgesG = get_number_of_edges(graph=G)
    edgesH = get_number_of_edges(graph=H)
    if edgesG != edgesH:
        return False

    # Vertex degrees
    degreesG = get_list_of_degrees(graph=G)
    degreesH = get_list_of_degrees(graph=H)
    if sorted(degreesG) != sorted(degreesH):
        return False

    # Check every graph permutations
    for permutation in permutations(range(len(H))):
        if all(
            G[i][j] == H[permutation[i]][permutation[j]]
            for i in range(len(G))
            for j in G[i]
        ):
            return True

    return False


print("Isomorfismo:")
for g, h in zip(G, H):
    print(are_graphs_isomorphic(g, h))


# Get Jaccard similatiry of one node from G and one node from H
def jaccard_similarity(G, H, node1, node2):
    neighbors1 = set(G.neighbors(node1)) | {node1}
    neighbors2 = set(H.neighbors(node2)) | {node2}
    intersection = len(neighbors1 & neighbors2)
    union = len(neighbors1 | neighbors2)
    return intersection / union if union != 0 else 0


# Get Mean Jaccard Similatiry of G and H
def average_jaccard_similarity(G, H):
    total_similarity = 0
    count = 0
    for node1, node2 in zip(G.nodes(), H.nodes()):
        total_similarity += jaccard_similarity(G, H, node1, node2)
        count += 1
    return total_similarity / count if count else 0


# Permutate H and test all permutations to get the best similatiry
def best_similarity(G, H):
    best_similarity_score = 0

    for permutation in permutations(H.nodes()):
        H_permuted = nx.relabel_nodes(
            H,
            {
                old_label: new_label
                for old_label, new_label in zip(H.nodes(), permutation)
            },
        )

        current_similarity = average_jaccard_similarity(G, H_permuted)

        if current_similarity > best_similarity_score:
            best_similarity_score = current_similarity

    return True if best_similarity_score >= 0.75 else False


# Convert matrix to NetworkX graph object
def generate_graph(matrix: list[list[int]]):
    G = nx.Graph()
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if matrix[i][j] == 1:
                G.add_edge(i + 1, j + 1)
    return G


print("Similaridade:")
for g, h in zip(G, H):
    print(best_similarity(generate_graph(g), generate_graph(h)))
