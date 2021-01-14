import unittest
from DiGraph import DiGraph


class TestDiGraph(unittest.TestCase):
    def test_mc(self):
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        self.assertEqual(10, graph.get_mc())
        for number in range(0, 9):
            graph.add_edge(number, number + 1, number + 1)
        self.assertEqual(19, graph.get_mc())
        for number in range(0, 9):
            graph.add_edge(number, number + 1, 1)
        self.assertEqual(19, graph.get_mc())
        graph.remove_node(0)
        self.assertEqual(20,graph.get_mc())

    def test_v_size(self):
        graph = DiGraph()
        for number in range(6):
            graph.add_node(number)
        self.assertEqual(6, graph.v_size())
        for number in range(3):
            graph.remove_node(10 + number)

        self.assertEqual(6, graph.v_size())
        for number in range(3):
            graph.remove_node(number)
        self.assertEqual(3, graph.v_size())

    def test_edge_size(self):
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        for number in range(9):
            graph.add_edge(number, number + 1, number)
        self.assertEqual(9, graph.edge_size)
        graph.remove_node(2)
        self.assertEqual(7, graph.edge_size)
        for number in range(4):
            graph.remove_edge(5 + number, 6 + number)
        self.assertEqual(3, graph.edge_size)
        graph.remove_edge(30, 31)
        self.assertEqual(3, graph.edge_size)

    def test_get_all_v(self):
        graph = DiGraph()
        for number in range(1000):
            graph.add_node(number)
        dict = graph.get_all_v()
        for number in range(1000):
            node = dict.get(number)
            self.assertIsNotNone(node)

    def test_has_edge(self):
        vertices = 10
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        for source in range(10):
            for destination in range(10):
                if source != destination:
                    graph.add_edge(source, destination, 3)
        graph2 = DiGraph()
        for source in range(10):
            for destination in range(10):
                if source != destination:
                    self.assertTrue(graph.has_edge(source, destination))
                self.assertFalse(graph2.has_edge(source, destination))

    def test_add_edge(self):
        graph = DiGraph()
        self.assertFalse(graph.add_edge(0, 1, 1))
        graph.add_node(1)
        self.assertFalse(graph.add_edge(0, 1, 1))
        graph.add_node(0)
        self.assertTrue(graph.add_edge(0, 1, 1))
        self.assertFalse(graph.add_edge(0, 1, 2))

    def test_remove_node(self):
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        for number in range(1, 10):
            graph.add_edge(0, number, 1)
        self.assertEqual(10, graph.v_size())
        self.assertEqual(9, graph.e_size())
        graph.remove_node(9)
        self.assertEqual(9, graph.v_size())
        self.assertEqual(8, graph.e_size())
        graph.remove_node(0)
        self.assertEqual(8, graph.v_size())
        self.assertEqual(0, graph.e_size())
        graph.remove_node(9)
        self.assertEqual(8, graph.v_size())

    def test_remove_edge(self):
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        for number in range(1, 10):
            graph.add_edge(0, number, number + 1)
        self.assertTrue(graph.remove_edge(0, 1))
        self.assertEqual(8, graph.e_size())
        self.assertFalse(graph.remove_edge(0,0))
    def test_all_in_edges_of_node(self):
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        for number in range(1,10):
            graph.add_edge(0,number,number+1)
        ans = {1 : 2, 2 : 3, 3: 4 ,4 : 5 , 5:6 , 6:7, 7:8,8:9,9:10}
        self.assertEqual(ans,graph.all_out_edges_of_node(0))
        ans.pop(1)
        graph.remove_edge(0,1)
        self.assertEqual(ans,graph.all_out_edges_of_node(0))
        ans.clear()
        self.assertEqual(ans,graph.all_out_edges_of_node(1))
    def test_all_in_edges_of_node(self):
        graph = DiGraph()
        for number in range(10):
            graph.add_node(number)
        for number in range(1,10):
            graph.add_edge(number,0,number+1)
        ans = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10}
        self.assertEqual(ans,graph.all_in_edges_of_node(0))
        graph.remove_edge(1,0)
        ans.pop(1)
        self.assertEqual(ans,graph.all_in_edges_of_node(0))
        ans.clear()
        self.assertEqual(ans,graph.all_in_edges_of_node(1))