import unittest
from DiGraph import DiGraph as Graph
from GraphAlgo import GraphAlgo as Algo


class TestGraphAlgorithms(unittest.TestCase):

    def test_save_load(self):
        graph = Graph();
        for number in range(4):
            graph.add_node(number)
        for number in range(4):
            graph.add_edge(0, number, 1)
        algo = Algo(graph)
        self.assertTrue(algo.save_to_json("saved_graph"))
        self.assertFalse(algo.save_to_json(""))
        self.assertFalse(algo.load_from_json("python"))
        self.assertTrue(algo.load_from_json("saved_graph"))
        self.assertEqual(graph, algo.get_graph())

    def test_get_graph(self):
        graph = Graph();
        for number in range(10):
            graph.add_node(number)
        for number in range(10):
            graph.add_edge(0, number, 1)
        algo = Algo(graph)
        self.assertTrue(id(graph), id(algo.get_graph()))

    def test_connected_components_and_component(self):
        graph = Graph();
        for number in range(10):
            graph.add_node(number)
        for number in range(5):
            if number != 0:
                graph.add_edge(0, number, number)
                graph.add_edge(number, 0, number)
        for number in range(6, 10):
            if number != 6:
                graph.add_edge(6, number, number)
                graph.add_edge(number, 6, number)
        algo = Algo(graph)
        components = algo.connected_components()
        self.assertTrue(components.__contains__([0, 1, 2, 3, 4]))
        self.assertTrue(components.__contains__([6, 7, 8, 9]))
        self.assertTrue(components.__contains__([5]))
        component1 = algo.connected_component(0)
        component2 = algo.connected_component(6)
        component3 = algo.connected_component(5)
        self.assertEqual(component1, [0, 1, 2, 3, 4])
        self.assertEqual(component2, [6, 7, 8, 9])
        self.assertEqual(component3, [5])
        graph2 = Graph()
        algo.graph = graph2
        self.assertEqual([], algo.connected_components())

    def test_shortes_path(self):
        graph = Graph()
        for number in range(10):
            graph.add_node(number)
        for number in range(10):
            graph.add_edge(0, number, 5)
        for number in range(10):
            graph.add_edge(number, 0, 5)
        algo = Algo(graph)
        for number in range(9):
            self.assertNotEqual(float('inf'), algo.shortest_path(number, number + 1)[0])
        self.assertEqual(10, algo.shortest_path(1, 3)[0])
        graph.remove_edge(0,3)
        self.assertEqual(float('inf'),algo.shortest_path(1,3)[0])
        path = [4,0,2]
        path2 = algo.shortest_path(4,2)[1]
        self.assertTrue(path.__eq__(algo.shortest_path(4,2)[1]))
