import operator
import copy
import itertools

from src.graph import Graph
from src.uptree import UpTree

def mst_kruskal(graph):
    """
    Returns a minimum spanning tree of the input graph using Kruskal's algorithm
    """
    edge_set = graph.edge_set
    sortedEdges = sorted(edge_set, key = operator.attrgetter('weight'))
    component_membership = {vertex:UpTree() for vertex in set(itertools.chain.from_iterable(edge_set))}
    mst_edges = set()
    for edge in sortedEdges:
        ep_1, ep_2 = edge
        if component_membership[ep_1].find() != component_membership[ep_2].find():
            component_membership[ep_1].union(component_membership[ep_2])
            mst_edges.add(edge)
        if(len(mst_edges) == graph.size - 1):
                break
    
    #edges will now be referencing vertices with different object ids than those vertices in the vertexSet
    mst_edges = copy.deepcopy(mst_edges)
    mst_vertices = set(itertools.chain.from_iterable(mst_edges))
    for vertex in mst_vertices:
        vertex._neighbors.clear()
    return Graph._from_vertex_and_edge_sets(vertex_set = mst_vertices, edge_set = mst_edges)
    
