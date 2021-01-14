from GraphInterface import GraphInterface
from NodeInfo import NodeInfo


class DiGraph(GraphInterface):
    """This  class represents a directed weighted graph."""
    def __init__(self):
        self.nodes_list = {}
        self.mc = 0
        self.edge_size = 0

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.edge_size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair  (key, node_data)
        """
        return self.nodes_list

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.nodes_list)

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (key, weight)
         """
        return self.nodes_list.get(id1).in_edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair (key,
        weight)
        """
        return self.nodes_list.get(id1).out_edges

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        if the node id does not exists the function will do nothing
        """
        if node_id in self.nodes_list:
            keysin = []
            for destination_node in self.all_out_edges_of_node(node_id).keys():
                keysin.append(destination_node)
            for key in keysin:
                self.remove_edge(node_id, key)
                self.mc -= 1
            keysout = []
            for source_node in self.all_in_edges_of_node(node_id).keys():
                keysout.append(source_node)
            for key in keysout:
                self.remove_edge(key, node_id)
                self.mc -= 1
            self.get_all_v().pop(node_id)
            self.mc += 1
            return True

        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id not in self.nodes_list:
            self.nodes_list[node_id] = NodeInfo(node_id, pos)
            self.mc += 1
            return True

        return False

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 not in self.nodes_list or id2 not in self.nodes_list:
            return False
        if self.has_edge(id1, id2) is True:
            return False

        source = self.nodes_list.get(id1)
        destination = self.nodes_list.get(id2)
        source.add_out_edge(id2, weight)
        destination.add_in_edge(id1, weight)
        self.mc += 1
        self.edge_size += 1
        return True


    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        If such an edge does not exists the function will do nothing
        """
        if node_id1 not in self.nodes_list or node_id2 not in self.nodes_list:
            return False
        if node_id1 in self.all_in_edges_of_node(node_id2).keys() is False:
            return False
        if node_id1 == node_id2:
            return False
        self.all_in_edges_of_node(node_id2).pop(node_id1)
        self.all_out_edges_of_node(node_id1).pop(node_id2)
        self.edge_size -= 1
        self.mc += 1

        return True

    def has_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.nodes_list or node_id2 not in self.nodes_list:
            return False
        if node_id2 not in self.all_out_edges_of_node(node_id1):
            return False
        if node_id1 not in self.all_in_edges_of_node(node_id2):
            return False
        return True

    def as_dict(self):
        list_of_nodes = []
        list_of_edges = []
        for key in self.get_all_v():
            node = self.get_all_v().get(key)
            list_of_nodes.append(node.encoder())
            for dst in self.all_out_edges_of_node(key):
                encoded_edge = {"src": key, "w": self.all_out_edges_of_node(key).get(dst), "dest": dst}
                list_of_edges.append(encoded_edge)

        ans = {"Edges": list_of_edges, "Nodes": list_of_nodes}
        return ans

    def __repr__(self):
        ans = "Graph: "
        ans += "|V|=" + str(self.v_size()) + " , |E|=" + str(self.edge_size)
        return ans

    def __eq__(self, other):
        return self.nodes_list.__eq__(other.nodes_list)
