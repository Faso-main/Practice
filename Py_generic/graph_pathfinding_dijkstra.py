import heapq

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]
    
    while heap:
        current_distance, current_vertex = heapq.heappop(heap)
        
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))
    
    return distances

weighted_graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 2, 'E': 5},
    'C': {'A': 4, 'F': 3},
    'D': {'B': 2},
    'E': {'B': 5, 'F': 1},
    'F': {'C': 3, 'E': 1}
}

print("Dijkstra's shortest paths:")
print(dijkstra(weighted_graph, 'A'))