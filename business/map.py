import data.map as map_data
from model.coordinate import Coordinate
from queue import PriorityQueue


def travel(start: Coordinate, end: Coordinate):
    # Priority Queue
    def pq_put(pq, dist, item):
        pq.append(item)
        i = len(pq) - 1
        while i > 0 and dist[pq[(i - 1) // 2]] > dist[pq[i]]:
            pq[(i - 1) // 2], pq[i] = pq[i], pq[(i - 1) // 2]
            i = (i - 1) // 2
    
    def pq_get(pq, dist):
        pq[0], pq[-1] = pq[-1], pq[0]
        result = pq.pop()
        i = 0
        while i * 2 + 1 < len(pq):
            j = i * 2 + 1
            if i * 2 + 2 < len(pq) and dist[pq[i * 2 + 2]] < dist[pq[j]]:
                j = i * 2 + 2
            if dist[pq[i]] > dist[pq[j]]:
                pq[i], pq[j] = pq[j], pq[i]
                i = j
            else:
                break
        return result

    # Dijkstra
    dist = {start: 0}
    parent = {}
    pq = [start]
    while len(pq) > 0:
        curr = pq_get(pq, dist)
        if curr == end:
            break
        for next, edge in map_data.get_edges(curr):
            d = dist[curr] + edge.fuel_cost
            if next not in dist or dist[next] > d:
                dist[next] = d
                parent[next] = (curr, edge)
                pq_put(pq, dist, next)
    
    if end not in dist:
        return False

    path = [(end, None)]
    curr = end
    while curr in parent:
        path.append(parent[curr])
        curr = parent[curr][0]
    path = path[::-1]

    for ((_, edge), (next, _)) in zip(path[:-1], path[1:]):
        map_data.execute_edge(next, edge)
    return True
