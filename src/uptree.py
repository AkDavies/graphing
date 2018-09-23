import operator

class UpTree:

    def __init__(self):
        self.parent = None
        self._height  = 0
    
    def __iter__(self):
        yield self
        if self.parent is not None:
            yield from self.parent
    
    def find(self):
        for node in self:
            pass
        else:
            return node
    
    def union(self, other):
        self_root = self.find()
        other_root = other.find()
        #the new root should be the root in the tree with the lowest height
        dominant_tree, assimilating_tree = sorted((self_root, other_root), key = operator.attrgetter('_height'))
        assimilating_tree.parent = dominant_tree
        dominant_tree._height = max(dominant_tree._height, assimilating_tree._height + 1)