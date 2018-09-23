import json
import itertools
import sys
from src.vertex import Vertex
from src.edge import (Edge, DirectedEdge, UndirectedEdge)


class Graph:
    #initializer takes a collection of namedTuples for vertices that contains the vertex id and any additional properties,
    #and a collection of edges represented as tuples where each element is a vertex id

    def __init__(self, ids = None, edges = None, properties = None):
        self._vertex_set = dict()
        self._edge_set = {'DirectedEdges': dict(), 'UndirectedEdges': dict()}
    
    def __repr__(self):
        msg = "Vertices: {vertices}, Edges: {edges}"
        return msg.format(vertices = self.vertex_set.__repr__(), edges = self.edge_set.__repr__())
    
    def __getitem__(self, key):
        return self._vertex_set.get(key)
    
    def __contains__(self, key):
        val = False
        if isinstance(key, Vertex):
            val = key in self.vertex_set
        elif isinstance(key, Edge):
            val = key in self.edge_set
        # "key is provided as a tuple of vertex ids"
        else:
            #if key is a tuple => checking for a directed edge
            if isinstance(key, tuple):
                val = key in self._edge_set['DirectedEdges']
            #if key is a frozenset => checking for an undirected edge
            elif isinstance(key, set) or isinstance(key, frozenset):
                val = frozenset(key) in self._edge_set['UndirectedEdges']
            #otherwise key should be a string => checking for a vertex
            else:
                val = key in self._vertex_set
        return val
    
    #should have a singular method to populate neighbors in the edge class
    def _populateNeighbors(self):
        """
        Populates the neighbors attribute for every Vertex in the Graph
        """
        for edge in self.edge_set:
            edge._make_neighbors()
            
    @property
    def vertex_set(self):
        """
        Returns the vertex_set of the given Graph
        """
        return set(self._vertex_set.values())
    
    @property
    def edge_set(self):
        return set(itertools.chain(
                                    self._edge_set['UndirectedEdges'].values(),
                                    self._edge_set['DirectedEdges'].values()
                    )
                )

    @property
    def order(self):
        return len(self.vertex_set)

    @property
    def size(self):
        return len(self.edge_set)

    def add_edge(self, vertex_1, vertex_2, directed = False, **properties):
        if vertex_1 not in self or vertex_2 not in self:
            raise Exception("Attempted to add an edge whose endpoints are not all in the selected graph.")
        vertex_1 = self._vertex_set.get(vertex_1)
        vertex_2 = self._vertex_set.get(vertex_2)
        if directed:
            edge = DirectedEdge(vertex_1, vertex_2, **properties)
            self._add_DirectedEdge(edge)
        else:
            edge = UndirectedEdge(vertex_1, vertex_2, **properties)
            self._add_UndirectedEdge(edge)

    
    def add_vertex(self, id, **properties):       
        #check that a Vertex with this id is not already in the graph
        if id in self.vertex_set:
            raise Exception("A Vertex with this ID already exists in the graph.")
        else:
            newVertex = Vertex(id, **properties)
            self._add_vertex(newVertex)
    
    
    def _add_vertex(self, vertex):
        self._vertex_set[vertex.id] = vertex
    
    def _add_edge(self, edge):
        if isinstance(edge, UndirectedEdge):
            self._add_UndirectedEdge(edge)
        elif isinstance(edge, DirectedEdge):
            self._add_DirectedEdge(edge)
        else:
            raise Exception("Attempted to add unsupported Edge type")
        
    def _add_neighbors(self, edge):
        ep_1, ep_2 = edge.endpoints
        ep_1.neighbors.add(ep_2)
        ep_2.neighbors.add(ep_1)
    
    def _add_UndirectedEdge(self, edge):
        try:
            ep_1, ep_2 = edge.endpoints
            endpoints = frozenset({ep_1.id, ep_2.id})
            self._edge_set['UndirectedEdges'][endpoints] = edge
        except:
            raise Exception("Failure attempting to add UndirectedEdge")
        self._add_neighbors(edge)

    def _add_DirectedEdge(self, edge):
        try:
            ep_1, ep_2 = edge.endpoints
            endpoints = frozenset({ep_1.id, ep_2.id})
            self._edge_set['DirectedEdges'][endpoints] = edge
        except:
            raise Exception("Failure attempting to add DirectedEdge")
        self._add_neighbors(edge)

    #Need to clean up API to differentiate between vertex/edge_set as an actual set of vertices/edges
    # and the implementation of the abstraction of the vertex/edge_set 
    @classmethod
    def _from_vertex_and_edge_sets(cls, vertex_set, edge_set):
        graph = cls()
        for vertex in vertex_set:
            graph._add_vertex(vertex)
        for edge in edge_set:
            graph._add_edge(edge)
        return graph

    @classmethod
    def from_JSON(cls, file_path):
        with open(file_path) as file:
            json_data = json.load(file)
            # graph_properties = json_data["properties"]

            graph_vertex_set = json_data["vertex_set"]           
            temp_vertex_set = dict()
            for vertex in graph_vertex_set:
                vertex_name = vertex["name"]
                temp_vertex_set[vertex_name] = Vertex(id = vertex_name, **vertex["properties"])

            graph_edge_set = json_data["edge_set"]
            temp_edge_set = {'DirectedEdges': dict(), 'UndirectedEdges': dict()}
            for edge in graph_edge_set:
                if edge["directed"]:
                    endpoints = tuple(edge["endpoints"])
                    tail, head = endpoints
                    tail = temp_vertex_set.get(tail)
                    head = temp_vertex_set.get(head)
                    temp_edge_set['DirectedEdges'][endpoints] =  DirectedEdge(tail, head, **edge["properties"])
                elif not edge["directed"]:
                    endpoints = frozenset(edge["endpoints"])
                    endVertices = (temp_vertex_set.get(point) for point in endpoints)
                    temp_edge_set['UndirectedEdges'][endpoints] = UndirectedEdge(*endVertices, **edge["properties"])
                else:
                    raise Exception("All Edges must have a boolean-valued 'directed' field.")
        return Graph._from_vertex_and_edge_sets(
                                            temp_vertex_set.values(),
                                            itertools.chain(
                                                            temp_edge_set['DirectedEdges'].values(),
                                                            temp_edge_set['UndirectedEdges'].values()
                                            )
            )


    
    def _outgoing_edges(self, vertex):
        """
        Returns a iterable/collection of all the outgoing edges from a given vertex in the selected graph
        """
        #can build up list of adjacent edges by using the neighbors set
        return (edge for edge in self.edge_set if edge.is_outgoing_from_vertex(vertex))
    
    def _incoming_edges(self, vertex):
        """
        Returns a iterable/collection of all the incoming edges from a given vertex in the selected graph
        """
        return (edge for edge in self.edge_set if edge.is_incoming_to_vertex(vertex))
