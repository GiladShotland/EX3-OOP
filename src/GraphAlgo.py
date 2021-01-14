import math
from typing import List
from NodeInfo import NodeInfo
from GraphInterface import GraphInterface
from AlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph as Graph
from matplotlib import pyplot as plt
import random as rand
import queue
import json

identifier = 0


class GraphAlgo(GraphAlgoInterface):
    """This class represents a directed weighted graph."""

    def __init__(self, graph: GraphInterface = None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        loads the graph in JSON format to a file
        @param file_name: The path to the load file
        @return: True if the load was successful, False o.w.
        """
        try:
            with open(file_name, "r") as file:
                graph_dict = json.load(file)
                nodes = graph_dict.get("Nodes")
                edges = graph_dict.get("Edges")
                graph = Graph()
                tup = None
                for node_dict in nodes:
                    pos_string = node_dict.get("pos")
                    if pos_string is not None:
                        x = float(pos_string.split(",")[0])
                        y = float(pos_string.split(",")[1])
                        z = float(pos_string.split(",")[2])
                        tup = (x, y, z)

                    graph.add_node(node_dict.get("id"), tup)
                for edge_dict in edges:
                    src = edge_dict.get('src')
                    weight = edge_dict.get('w')
                    dest = edge_dict.get('dest')
                    graph.add_edge(src, dest, weight)
                self.graph = graph
                return True

        except IOError as e:
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            graph = self.get_graph()
            graph_dict = graph.as_dict()

            with open(file_name, "w") as file:
                json.dump(graph_dict, indent=4, fp=file)
            return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])

        """
        if self.get_graph() is None:
            return float('inf'), []
        if id1 not in self.get_graph().get_all_v() or id2 not in self.get_graph().get_all_v():
            return float('inf'), []
        if id1 == id2:
            return (0,[id1])
        destination_node = self.get_graph().get_all_v().get(id2)
        source_node = self.get_graph().get_all_v().get(id1)
        predecessors = self.dijkstra_algorithm(source_node)
        if destination_node.weight == -1:
            return float('inf'), []
        ans1 = destination_node.weight
        ans2 = [destination_node.key]
        destination_node = predecessors.get(destination_node.key)
        while destination_node.key != id1:
            ans2.append(destination_node.key)
            destination_node = predecessors.get(destination_node.key)
        ans2.append(destination_node.key)
        ans2.reverse()
        return ans1, ans2

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        if self.get_graph() is None:
            return []
        if id1 not in self.get_graph().get_all_v():
            return []
        reversed = self.reversed_graph()

        return self.bfs_twice(id1, {}, [], reversed)

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        Notes:
        If the graph is None the function return an empty list []
        """
        if self.get_graph() is None:
            return []
        total = {}
        ans = []
        reversed = self.reversed_graph()
        for id in self.get_graph().get_all_v():
            if id not in total:
                ans.append(self.bfs_twice(id, total, [], reversed))

        return ans

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        if self.get_graph() is not None:
            nodes_list = self.get_graph().get_all_v()
            no_positions = self.get_empty_pos_nodes()
            self.generate_positions(no_positions)
            dx = self.get_differentialx(nodes_list)
            extend_x = (dx[0] - dx[1]) / 10
            dy = self.get_differentialy(nodes_list)
            extend_y = (dy[0] - dy[1]) / 10
            plt.axis([dx[0] - extend_x * 12, dx[1] + extend_x * 12, dy[0] - extend_y * 12, dy[1] + extend_y * 12])

            for node_id in nodes_list:
                node = nodes_list.get(node_id)
                pos = node.pos

                plt.plot(pos[0], pos[1], 'bo')
                plt.annotate(text=f"{node.key}", xy=(pos[0] + 0.0002, pos[1] + 0.0002),
                             xytext=(pos[0] - 0.0002, pos[1] + 0.0002), color='darkcyan')

            for node_id in nodes_list:
                node = nodes_list.get(node_id)
                pos = node.pos

                for neighbor_id in node.out_edges:
                    neighbor = nodes_list.get(neighbor_id)
                    neigh_pos = neighbor.pos
                    distance = self.distance(pos,neigh_pos)
                    length = min([distance/10,0.001])
                    plt.annotate("", xy=(neigh_pos[0], neigh_pos[1]), xytext=(node.pos[0], node.pos[1]),
                                 arrowprops=dict(edgecolor='green', facecolor='black', arrowstyle='-|>'))

            plt.show()

    def dijkstra_algorithm(self, source):
        """
        dijksra's algorithm implementation
        :param source: node to start the traversal from
        :return: dictionary of predecessors of each node
        """
        visited = {}
        predecessors = {}
        nodes_queue = queue.PriorityQueue()
        for node in self.get_graph().get_all_v().values():
            node1 = NodeInfo(node)
            node.set_weight(-1)
            visited[node.key] = False
        source.set_weight(0)
        nodes_queue.put(source)
        while not nodes_queue.empty():
            current_node = nodes_queue.get()
            if visited.get(current_node.key) is False:
                for node_id in current_node.out_edges.keys():
                    node = self.get_graph().get_all_v().get(node_id)
                    distance = current_node.out_edges.get(node_id) + current_node.weight
                    if node.weight == -1 or distance < node.weight:
                        node.set_weight(distance)
                        predecessors[node.key] = current_node
                        nodes_queue.put(node)

            visited[current_node.key] = True

        return predecessors

    def bfs_twice(self, id: int, total, specific, reverse):
        """
        help method for the connected components
        :param id: node which the algorithm will find its SCC
        :param total: dictionary of nodes. if an SCC found for a node it will be on the dict
        :param specific: pointer for the list of the SCC
        :param reverse: transposed version of this graph
        :return: list
        """
        q = queue.Queue()
        nodes_list = self.get_graph().get_all_v()
        start = self.get_graph().get_all_v().get(id)
        saved_nodes, visited = {}, {}
        q.put(start)
        specific.append(start.get_key())
        while not q.empty():
            node = q.get()
            for neighbor_id in node.out_edges:
                neighbor = nodes_list.get(neighbor_id)
                if neighbor_id not in visited:
                    visited[neighbor_id] = True
                    saved_nodes[neighbor.get_key()] = True
                    q.put(neighbor)
        nodes_list = reverse.get_all_v()
        start = nodes_list.get(id)
        q.put(start)
        visited.clear()
        while not q.empty():
            node = q.get()
            for neighbor_id in node.out_edges:
                neighbor = nodes_list.get(neighbor_id)
                if neighbor_id not in visited:
                    visited[neighbor_id] = True
                    q.put(neighbor)
                    if saved_nodes.get(neighbor_id) is True:
                        total[neighbor_id] = True
                        specific.append(neighbor_id)
        specific = list(dict.fromkeys(specific))
        return specific

    def reversed_graph(self):
        """

        :return: transposed version of the graph
        """
        graph = self.get_graph()
        reveresed = Graph()
        for node_id in graph.get_all_v():
            node = self.get_graph().get_all_v().get(node_id)
            if node.pos is not None:
                reveresed.add_node(node.get_key(), node.pos)
            else:
                reveresed.add_node(node.get_key())
        for node_id in graph.get_all_v():
            node = self.get_graph().get_all_v().get(node_id)
            for key in node.out_edges.keys():
                reveresed.add_edge(key, node.get_key(), 0)
        return reveresed

    def get_empty_pos_nodes(self):
        """

        :return: list of nodes with no positions
        """
        ans = []
        nodes_list = self.get_graph().get_all_v()
        for node_id in nodes_list:
            node = nodes_list.get(node_id)
            if node.pos is None:
                ans.append(node)
        return ans

    def generate_positions(self, nodes: []):
        """
        generate random positions for the nodes
        :param nodes:
        :return:
        """
        x_min = 35.19
        x_max = 35.23
        y_min = 31.1
        y_max = 31.2
        amount = 1 if len(nodes) == 0 else len(nodes)
        dx = self.get_differentialx(self.get_graph().get_all_v())
        dy = self.get_differentialy(self.get_graph().get_all_v())
        if dx != (-math.inf,math.inf) and dy != (-math.inf,math.inf):
            x_max ,x_min =dx[0],dx[1]
            y_max,y_min = dy[0],dy[1]


        counter = 0
        for node in nodes:
            x_point = rand.uniform(x_min, x_max)
            y_point = rand.uniform(y_min, y_max)

            node.pos = (x_point, y_point, 0)
            counter += 1

    def get_differentialx(self, dict):
        max = -math.inf
        min = math.inf

        for node_key in dict.keys():
            node = dict.get(node_key)
            if node.pos is not None:
                x = node.pos[0]
                if max < x:
                    max = x
                if min > x:
                    min = x
        return (max, min)

    def get_differentialy(self, dict):
        max = -math.inf
        min = math.inf
        for node_key in dict.keys():
            node = dict.get(node_key)
            if node.pos is not None:
                y = node.pos[1]
                if max < y:
                    max = y
                if min > y:
                    min = y
        return (max, min)
    def distance(self, src,dst):
        dx = (dst[0] - src[0])**2
        dy = (dst[1] - src[1])**2
        return math.sqrt(dx+dy)

