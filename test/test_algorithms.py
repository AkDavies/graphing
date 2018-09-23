import unittest
import os

from src.graph import Graph
import src.algorithms.prim as prim

class test_algorithms(unittest.TestCase):
    def setUp(self):
        file_path = os.path.abspath("test/moderateGraph.json")
        self.moderate_graph = Graph.from_JSON(file_path)
    
    def test_dijkstra(self):
        pass
    
    def test_mst_prim(self):
        result_mst = prim.mst_prim(self.moderate_graph)
        self.assertIsInstance(result_mst, Graph)
        self.assertEqual(result_mst.order, self.moderate_graph.order)
        self.assertEqual(result_mst.size, self.moderate_graph.order - 1)