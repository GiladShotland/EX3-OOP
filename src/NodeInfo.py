class NodeInfo:
    """This class represents a single node in a directed weighted graph"""

    def __init__(self, key: int, pos: tuple = None, weight: float = -1):
        self.key = key
        self.in_edges = {}
        self.out_edges = {}
        self.weight = weight
        self.tag = (-1, -1)
        self.pos = pos

    def get_key(self) -> int:
        """

        :return: id of the graph
        """

        return self.key

    def add_in_edge(self, source_id: int, weight: float = 0):
        """
        add an edge going into the nod
        :param source_id: source of the edge
        :param weight: weight of the edge
        :return:None
        """
        self.in_edges[source_id] = weight

    def add_out_edge(self, dest_id: int, weight: float = 0):
        """
        add an edge going out of the nod
        :param dest_id: destination of the edge
        :param weight: weight of the edge
        :return:None
        """
        self.out_edges[dest_id] = weight

    def remove_in_edge(self, source_id: int) -> None:
        """
        remove an edge going into the node
        :param source_id: source of the edge
        :return: None
        """
        self.in_edges.pop(source_id, None)

    def remove_out_edge(self, dest_id: int):
        """
        remove an edge going into the node
        :param source_id: source of the edge
        :return: None
        """
        self.in_edges.pop(dest_id, None)

    def set_weight(self, weight: float) -> None:
        """
        update the weight of the node
        :param weight: weight of the node
        :return: None
        """
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def encoder(self):
        ans = {}
        if self.pos is None:
            ans["pos"] = None
        else:
            ans["pos"] = str(self.pos[0]) + "," + str(self.pos[1]) + "," + str(self.pos[2])

        ans["id"] = self.get_key()

        return ans

    def __eq__(self, other):
        if self.get_key() != other.get_key():
            return False
        if self.pos != other.pos:
            return False
        return self.out_edges.__eq__(other.out_edges) and self.in_edges.__eq__(other.in_edges)
    def __repr__(self):
        return f"{self.key}: |edges out|: {len(self.out_edges)} |edges in|: {len(self.in_edges)}"