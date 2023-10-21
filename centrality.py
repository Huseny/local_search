from searches import Search


class Centrality:
    def __init__(self, graph):
        self.graph = graph

    def compute_degree(self):
        degrees = {}
        for node in self.graph.nodes:
            degrees[node.value["name"]] = len(node.neighbours)
        return degrees

    def closeness(self):
        closeness_scores = {}
        n = len(self.graph.nodes) - 1

        for node in self.graph.nodes:
            total_shortest_path_distance = 0
            for another_node in self.graph.nodes:
                if another_node is node:
                    continue
                total_shortest_path_distance += Search(
                    self.graph).UCS(node, another_node)[0]

            closeness_scores[node.value["name"]] = (
                n / total_shortest_path_distance) if total_shortest_path_distance > 0 else 0
        return closeness_scores

    def eigenvector(self):
        centrality_scores = {node.value["name"]: 1 for node in self.graph.nodes}
        tolerance = 1e-6
        for i in range(100):  # 100 will be the maximum number of iterations allowed
            prev_scores = centrality_scores.copy()
            for node in self.graph.nodes:
                neighbours = node.neighbours
                score = sum(centrality_scores[neighbour.value["name"]]
                            for neighbour in neighbours)
                centrality_scores[node.value["name"]] = score

            norm_factor = sum(
                score ** 2 for score in centrality_scores.values()) ** 0.5
            centrality_scores = {
                node: score / norm_factor for node, score in centrality_scores.items()}

            if all(abs(prev_scores[node.value["name"]] - centrality_scores[node.value["name"]]) < tolerance for node in self.graph.nodes):
                break

        return centrality_scores

    def betweenness(self):
        betweenness_values = {node.value["name"]: 0 for node in self.graph.nodes}

        for source in self.graph.nodes:
            distance = {}
            for node in self.graph.nodes:
                distance[node] = Search(self.graph).UCS(source, node)[0]

            sigma = {node: 0 for node in self.graph.nodes}
            sigma[source] = 1
            sorted_nodes = sorted(
                distance, key=lambda x: distance[x], reverse=True)

            for node in sorted_nodes:
                if node is not source:
                    for main in node.neighbours:
                        if distance[main] == distance[node] + 1:
                            sigma[node] += sigma[main]

                    delta = 0
                    for sub in node.neighbours:
                        if distance[sub] == distance[node] + 1:
                            if sigma[node] != 0:
                                delta += (sigma[sub] / sigma[node]) * \
                                    (1 + betweenness_values[sub.value["name"]])
                betweenness_values[node.value["name"]] += delta

        factor = len(self.graph.nodes) * (len(self.graph.nodes) - 1) / 2
        for node in betweenness_values.keys():
            betweenness_values[node] /= factor

        return betweenness_values

    def page_rank(self):
        pagerank = {node.value["name"]: 1 /
                    len(self.graph.nodes) for node in self.graph.nodes}
        tolerance = 1e-6

        for i in range(100):
            new_pagerank = {node.value["name"]: 0 for node in self.graph.nodes}
            for node in self.graph.nodes:
                for neighbour in node.neighbours:
                    num_of_edges = len(neighbour.neighbours)

                    if num_of_edges > 0:
                        # the code calculates the contribution of the outgoing edges of a neighbouring node
                        #  to the PageRank score of the current node.
                        # 0.85 is the dumping factor
                        contribution = 0.85 * \
                            pagerank[neighbour.value["name"]] / num_of_edges
                        new_pagerank[node.value["name"]] += contribution

                # after we calculate the contributions of neighboring nodes to the PageRank
                # score of the current node, we also need to add a damping factor to the score.
                # the following code do that
                new_pagerank[node.value["name"]] += (1 - 0.85) / \
                    len(self.graph.nodes)

            norm = sum(abs(pagerank[node.value["name"]] - new_pagerank[node.value["name"]])
                       for node in self.graph.nodes)

            if norm < tolerance:
                break

            pagerank = new_pagerank
        return pagerank

    def katz(self):
        alpha = 0.1
        beta = 1
        tolerance = 1e-6
        katz = {node.value["name"]: 0 for node in self.graph.nodes}

        # This formula ensures that the sum of Katz centrality values is
        # bounded and prevents the values from exploding or going to zero.
        constant = 1 / \
            max(beta, abs(
                1-alpha*max([len(node.neighbours) for node in self.graph.nodes])))

        for i in range(100):
            new_katz = {node.value["name"]: 0 for node in self.graph.nodes}

            for node in self.graph.nodes:
                for neighbour in node.neighbours:
                    path_length = Search(self.graph).UCS(node, neighbour)[0]

                    if path_length > 0:
                        # this formula is used to calculate the contribution of the neighboring node
                        #  to the Katz centrality score of the current node.
                        contribution = alpha * \
                            (beta ** path_length) * \
                            katz[neighbour.value["name"]]
                        new_katz[node.value["name"]] += contribution

                new_katz[node.value["name"]] += constant

            norm = sum(abs(katz[node.value["name"]] -
                       new_katz[node.value["name"]]) for node in self.graph.nodes)
            if norm < tolerance:
                break

            katz = new_katz

        # This will scale all Katz centrality values to the range between 0 and 1,
        # with the node having the highest Katz centrality value having a value of 1.
        max_katz = max(katz.values())
        normalized_katz = {
            node.value["name"]: katz[node.value["name"]] / max_katz for node in self.graph.nodes}
        return normalized_katz
