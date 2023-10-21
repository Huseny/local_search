from collections import defaultdict, deque
from graph import Graph, Node
import math


class Search:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def BFS(self, startNode: Node, target: Node):
        queue = deque()
        queue.append(startNode)
        visited = {startNode: None}

        while queue:
            node = queue.popleft()
            neighbours = node.neighbours

            if node == target:
                break

            for neigh in neighbours:
                if neigh not in visited:
                    queue.append(neigh)
                    visited[neigh] = node

        cur_node = target
        path = deque([target.value["name"]])
        while cur_node != startNode:
            cur_node = visited[cur_node]
            path.appendleft(cur_node.value["name"])
        return list(path)

    def DFS(self, startNode: Node, target: Node, visited=set(),
            path=[]):
        visited.add(startNode)
        path.append(startNode.value['name'])
        if startNode == target:
            return path
        for neighbour in startNode.neighbours:
            if neighbour not in visited:
                result = self.DFS(neighbour, target, visited, path)
                if result:
                    return result
        path.pop()
        return None

    def UCS(self, startNode: Node, target: Node):
        visited = set()
        current = deque([(0, [startNode])])

        while current:
            cost, path = current.popleft()
            node = path[-1]

            if node == target:
                real_path = []
                for point in path:
                    real_path.append(point.value["name"])
                return (cost, real_path)

            if node not in visited:
                visited.add(node)
                i = 0
                for neighbor in node.neighbours:
                    edge_cost = node.edges[0].weight
                    if neighbor not in visited:
                        new_cost = cost + edge_cost
                        new_path = path + [neighbor]
                        current.append((new_cost, new_path))
                current = deque(sorted(current, key=lambda x: x[0]))

        return []

    def iterative_deepening(self, startNode: Node, target: Node):
        depth_limit = 0
        while True:
            visited = defaultdict(bool)
            path = []
            result, path = self.__helper_iter(
                startNode, target, 0, depth_limit, visited, path)
            if result:
                return depth_limit, path
            else:
                depth_limit += 1

    def bi_directional(self, startNode: Node, target: Node):
        start_queue = [startNode]
        target_queue = [target]
        start_visited = {startNode}
        target_visited = {target}
        start_parent = {}
        target_parent = {}

        while start_queue or target_queue:
            if start_queue:
                curr = start_queue.pop(0)

                if curr == target or curr in target_visited:
                    return self.__path_for_bi_directional(startNode, start_parent, target_parent, curr)

                for neighbor in curr.neighbours:
                    if neighbor not in start_visited:
                        start_visited.add(neighbor)
                        start_parent[neighbor] = curr
                        start_queue.append(neighbor)

            if target_queue:
                curr = target_queue.pop(0)

                if curr == startNode or curr in start_visited:
                    return self.__path_for_bi_directional(startNode, start_parent, target_parent, curr)

                for neighbor in curr.neighbours:
                    if neighbor not in target_visited:
                        target_visited.add(neighbor)
                        target_parent[neighbor] = curr
                        target_queue.append(neighbor)

        return None

    def Astar(self, start, target, heuristic=None):
        queue = [(start, [])]
        visited = set()
        if not heuristic:
            heuristic = self.__manhattan_distance

        while queue:
            curr, path = queue.pop(0)

            if curr == target:
                return path + [curr.value['name']]

            if curr not in visited:
                visited.add(curr)
                neighbours = curr.neighbours

                neighbours.sort(key=lambda x: heuristic(
                    x, target) + self.__get_cost(x, curr))

                for neighbor in neighbours:
                    queue.append((neighbor, path + [curr.value['name']]))

        return None

    def __helper_iter(self, node: Node, target: Node, depth: int, depth_limit: int, visited=defaultdict(bool), path=[]):
        visited[node] = True
        path.append(node.value['name'])
        if node == target:
            return True, path

        if depth == depth_limit:
            path.pop()
            return False, path
        for neighbor in node.neighbours:
            if not visited[neighbor]:
                result, path = self.__helper_iter(
                    neighbor, target, depth + 1, depth_limit, visited, path)
                if result:
                    return True, path

        path.pop()
        return False, path

    def __path_for_bi_directional(self, startNode: Node, start_parent: dict, target_parent: dict, common_node: Node):
        path = []
        curr = common_node

        while curr in start_parent:
            path.insert(0, curr.value['name'])
            curr = start_parent[curr]

        curr = common_node

        while curr in target_parent:
            curr = target_parent[curr]
            path.append(curr.value['name'])
        path.insert(0, startNode.value['name'])

        return path

    def __get_cost(self, cur, child):
        for i in cur.edges:
            if i in child.edges:
                return i.weight

    def __manhattan_distance(self, node, target):
        lat1_rad = math.radians(float(node.value['Latitude']))
        lon1_rad = math.radians(float(node.value['Longitude']))
        lat2_rad = math.radians(float(target.value['Latitude']))
        lon2_rad = math.radians(float(target.value['Longitude']))

        x1 = math.cos(lat1_rad) * math.cos(lon1_rad)
        y1 = math.cos(lat1_rad) * math.sin(lon1_rad)
        x2 = math.cos(lat2_rad) * math.cos(lon2_rad)
        y2 = math.cos(lat2_rad) * math.sin(lon2_rad)

        distance = abs(x1 - x2) + abs(y1 - y2)

        distance_km = distance * 6371.0

        return distance_km

    def __euclidean_distance(self, node, target):
        lat1_rad = math.radians(float(node.value['Latitude']))
        lon1_rad = math.radians(float(node.value['Longitude']))
        lat2_rad = math.radians(float(target.value['Latitude']))
        lon2_rad = math.radians(float(target.value['Longitude']))

        x1 = math.cos(lat1_rad) * math.cos(lon1_rad)
        y1 = math.cos(lat1_rad) * math.sin(lon1_rad)
        z1 = math.sin(lat1_rad)
        x2 = math.cos(lat2_rad) * math.cos(lon2_rad)
        y2 = math.cos(lat2_rad) * math.sin(lon2_rad)
        z2 = math.sin(lat2_rad)

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

        distance_km = distance * 6371.0

        return distance_km
