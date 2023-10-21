class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.edges = []
        self.neighbours = []


class Edge:
    def __init__(self, node1, node2, weight=1):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__(self) -> str:
        return str([self.node1, self.node2, self.weight])


class Graph:
    def __init__(self) -> None:
        self.nodes = []

    def create_node(self, value):
        node = Node(value)
        self.nodes.append(node)
        return node

    def delete_node(self, node):
        if node not in self.nodes:
            raise ValueError("Node not found in the graph.")
        for edge in node.edges:
            edge.node1.edges.remove(edge)
            edge.node2.edges.remove(edge)
        self.nodes.remove(node)

    def insert_edge(self, node1, node2, weight=1):
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Nodes not found in the graph.")
        edge = Edge(node1, node2, weight)
        node1.edges.append(edge)
        node2.edges.append(edge)
        if node1 not in node2.neighbours:
            node2.neighbours.append(node1)
        if node2 not in node1.neighbours:
            node1.neighbours.append(node2)

    def delete_edge(self, node1, node2):
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Nodes not found in the graph.")
        for edge1, edge2 in zip(node1.edges, node2.edges):
            if (edge1.node2 == node2 or edge1.node1 == node2) and (edge2.node1 == node1 or edge2.node2 == node1):
                node1.edges.remove(edge1)
                node2.edges.remove(edge2)

    def search_item(self, value):
        for node in self.nodes:
            if node.value == value:
                return node
        return None

    # def __str__(self) -> str:
    #     graph = {}
    #     for node in self.nodes:
    #         edges = []
    #         for edge in node.edges:
    #             edges.append((edge.node1.value, edge.node2.value, edge.weight))
    #         graph[node.value] = edges
    #     return str(graph)
