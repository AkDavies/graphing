import sys

def dijkstra(graph, startVertex):
    #create a record of unvisited vertices (at the start all but one of the vertices are unvisited)
    unvisited_vertices = graph.vertex_set
    #defaultdict with default value sys.maxsize
    distance_dict = {node:sys.maxsize for node in unvisited_vertices}
    distance_dict[graph[startVertex]] = 0
    while unvisited_vertices:
        closest_vertex = min(unvisited_vertices, key = distance_dict.get)
        outgoing_edges = graph._outgoing_edges(closest_vertex)
        for edge in outgoing_edges:
            adjacent_vertex = edge.get_adjacent_vertex(closest_vertex)
            if(distance_dict[closest_vertex] + edge.weight < distance_dict[adjacent_vertex]):
                distance_dict[adjacent_vertex] = distance_dict[closest_vertex] + edge.weight 
        unvisited_vertices.remove(closest_vertex)
    return distance_dict