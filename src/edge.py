import copy
from abc import ABC, abstractmethod

class Edge(ABC):

    def __init__(self, ep1, ep2, **kwargs):
        self.endpoints = {ep1, ep2}
        self.__dict__.update(kwargs)
    
    def __iter__(self):
        return iter(self.endpoints)
    
    def __deepcopy__(self, memo):
        #https://stackoverflow.com/questions/1500718/what-is-the-right-way-to-override-the-copy-deepcopy-operations-on-an-object-in-p
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
    
    @abstractmethod
    def is_outgoing_from_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is an outgoing edge from the given vertex
        """
        pass
    
    @abstractmethod
    def is_incoming_to_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is an incoming edge to the given vertex
        """
        pass

    def _make_neighbors(self):
        """
        Add each endpoint to the neighbors record of the other
        """
        ep_1, ep_2 = self
        ep_1._addNeighbor(ep_2)
        ep_2._addNeighbor(ep_1)


    def get_adjacent_vertex(self, vertex):
        """
        Returns the vertex adjacent to the input vertex on the given edge
        """
        return list(other_vertex for other_vertex in self.endpoints if other_vertex != vertex)[0]

    def is_incident_to_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is incident to the given vertex
        """
        return vertex in self.endpoints

    

class UndirectedEdge(Edge):
    
    def __init__(self, endpoint1, endpoint2, **kwargs):
        self.endpoints = frozenset({endpoint1, endpoint2})
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        msg = 'UndirectedEdge({ep_1}, {ep_2})'
        ep_1, ep_2 = self.endpoints
        return msg.format(ep_1 = ep_1.id, ep_2 = ep_2.id)
       
    def is_outgoing_from_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is an outgoing edge from the given vertex
        """
        return self.is_incident_to_vertex(vertex)
    
    def is_incoming_to_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is an outgoing edge from the given vertex
        """
        return self.is_incident_to_vertex(vertex)


class DirectedEdge(Edge):
    
    def __init__(self, tail, head, **kwargs):
        self.endpoints = (tail, head)
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        msg = 'DirectedEdge(tail = {t_ID}, head = {h_ID})'
        return msg.format(t_ID = self.tail.id, h_ID = self.head.id)
    
    @property
    def tail(self):
        """
        Returns the tail node of the given edge
        """
        return self.endpoints[0]
    
    @property
    def head(self):
        """
        Returns the head node of the given edge
        """
        return self.endpoints[1]
    
    def is_outgoing_from_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is an outgoing edge from the given vertex
        """
        return vertex is self.tail

    def is_incoming_to_vertex(self, vertex):
        """
        Predicate function that returns true if an edge is an incoming edge to the given vertex
        """
        return vertex is self.head
