import copy

class Vertex:

    def __init__(self, id, **kwargs):
        self.id = id
        self._neighbors = set()
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        msg = 'Vertex(id = {id})'
        return msg.format(id = self.id)
    
    def __deepcopy__(self, memo):
        #https://stackoverflow.com/questions/1500718/what-is-the-right-way-to-override-the-copy-deepcopy-operations-on-an-object-in-p
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
    
    @property
    def neighbors(self):
        """
        Returns a list of the given vertex's neighbors, those vertices that are adjacent to it.
        """
        return self._neighbors
    
    def _addNeighbor(self, other):
        """
        Adds the input vertex(other) to the neighbor list of the given vertex
        """
        self._neighbors.add(other)