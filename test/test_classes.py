import os
import unittest

import hypothesis.strategies as st
from hypothesis import given

from src.edge import Edge, UndirectedEdge
from src.graph import Graph
from src.vertex import Vertex


class TestVertex(unittest.TestCase):
    
    @given(id = st.text(), kwargs = st.dictionaries(keys = st.text(),
                                                            values = st.text()
                                            )
    )
    def test_constructor(self, id, kwargs):
        self.assertIsInstance(Vertex(id, **kwargs), Vertex)
    
    def test_representation(self):
        pass

class TestEdge(unittest.TestCase):
    def setUp(self):
        self.v1 = Vertex(id = "1")
        self.v2 = Vertex(id = "2")
        self.properties = {'weight': 10, 'color': 'blue'}
        self.testEdge = UndirectedEdge(self.v1, self.v2, **self.properties)
    
    def test_constructor(self):
        self.assertIsInstance(UndirectedEdge(self.v1, self.v2, **self.properties),
                              UndirectedEdge
        )
    
    def test_representation(self):
        pass

class TestGraph(unittest.TestCase):
    def setUp(self):
        file_path = os.path.abspath("test/moderateGraph.json")
        self.moderate_graph = Graph.from_JSON(file_path)
  
    def test_constructor(self):
        self.assertIsInstance(self.moderate_graph, Graph)
    
    def test_getitem(self):
        self.assertIsInstance(self.moderate_graph["0"], Vertex)
    
    def test_contains(self):
        self.assertIn(self.moderate_graph["0"], self.moderate_graph)
    
    def test_vertex_set(self):
        self.assertTrue(all(vertex in self.moderate_graph for vertex in self.moderate_graph.vertex_set))
    
    def test_edge_set(self):
        self.assertTrue(all(edge in self.moderate_graph for edge in self.moderate_graph.edge_set))
    
    def test_addEdge(self):
        initial_size = self.moderate_graph.size
        self.assertTrue({"0","1"} in self.moderate_graph)
        self.assertTrue({"1","2"} in self.moderate_graph)
        self.assertFalse({"1","8"} in self.moderate_graph)

        self.moderate_graph.add_edge("1","8")

        self.assertTrue({"1","8"} in self.moderate_graph)
        self.assertEqual(self.moderate_graph.size, initial_size + 1)
    
    def test_addVertex(self):
        initial_order = self.moderate_graph.order
        self.assertFalse("9" in self.moderate_graph)

        self.moderate_graph.add_vertex("9", weight = 5, color = 'blue')
        
        self.assertTrue("9" in self.moderate_graph)
        self.assertTrue(self.moderate_graph["9"].weight == 5)
        self.assertTrue(self.moderate_graph["9"].color == 'blue')
        self.assertEqual(self.moderate_graph.order, initial_order + 1)

    #should add tests for the empty graph
    def test_order(self):
        """
        Returns the order of a graph, its number of vertices
        """
        self.assertEqual(self.moderate_graph.order, 9)

    # should add tests for the empty graph
    def test_size(self):
        """
        Returns the size of a graph, its number of edges
        """
        self.assertEqual(self.moderate_graph.size, 14)
    
    
    def test_populateNeighbors(self):
        self.assertTrue(self.moderate_graph["1"] in self.moderate_graph["0"].neighbors)
        self.assertTrue(self.moderate_graph["7"] in self.moderate_graph["0"].neighbors)
        self.assertTrue(self.moderate_graph["3"] in self.moderate_graph["4"].neighbors)
        self.assertTrue(self.moderate_graph["5"] in self.moderate_graph["4"].neighbors)

if __name__ == "__main__":
    unittest.main()
