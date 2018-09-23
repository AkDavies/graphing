import copy
import operator
import sys
import itertools
from collections import defaultdict

from src.graph import Graph

def mst_prim(graph):
    """
    Returns a minimum spanning tree (MST) of the input graph using Prim's algorithm
    """
    mst_edges = set()

    unincluded_vertices = graph.vertex_set
    optimal_connecting_edge = {vertex:None for vertex in unincluded_vertices}
    optimal_connecting_distance = {vertex:sys.maxsize for vertex in unincluded_vertices}
    initial_vertex = unincluded_vertices.pop()
    #assumes no parallel edges
    for edge in graph._outgoing_edges(initial_vertex):
        adjacent_vertex = edge.get_adjacent_vertex(initial_vertex)
        if edge.weight < optimal_connecting_distance[adjacent_vertex]:
            optimal_connecting_edge[adjacent_vertex] = edge
            optimal_connecting_distance[adjacent_vertex] = edge.weight
    while unincluded_vertices:
        new_vertex = min(unincluded_vertices, key = optimal_connecting_distance.get)
        new_edge = optimal_connecting_edge.get(new_vertex)
        mst_edges.add(new_edge)
        for edge in graph._outgoing_edges(new_vertex):
            adjacent_vertex = edge.get_adjacent_vertex(new_vertex)
            if edge.weight < optimal_connecting_distance[adjacent_vertex]:
                optimal_connecting_edge[adjacent_vertex] = edge
                optimal_connecting_distance[adjacent_vertex] = edge.weight
        unincluded_vertices.remove(new_vertex)
    mst_edges = copy.deepcopy(mst_edges)
    mst_vertices = set(itertools.chain.from_iterable(mst_edges))
    #still need to clear old neighbors from vertices
    for vertex in mst_vertices:
        vertex._neighbors.clear()
    return Graph._from_vertex_and_edge_sets(vertex_set = mst_vertices, edge_set = mst_edges)

