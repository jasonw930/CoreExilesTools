from functools import reduce


class CoreExilesMap:
    def add_system(self, system, nodes, ashar):
        self.systems.append(system)
        self.graph[system] = nodes
        self.ashar[system] = ashar

    def __init__(self):
        self.systems = ["Kelsey", "Ethan", "Feris", "Farpoint 1", "Farpoint 2",
                        "Franklyn", "Antioch", "Hexham", "Lorat", "Drakos", "Fieron",
                        "Grantham", "Palham", "Descarte", "Bedlam"]
        self.graph = {}
        self.ashar = {}

        self.add_system("Kelsey", [("Ethan", 5), ("Franklyn", 5), ("Antioch", 5), ("Lorat", 7), ("Grantham", 5)],
                        [("Cinq Port", "Cinq Port", 50)])

        self.add_system("Ethan", [("Kelsey", 5), ("Feris", 5)],
                        [("Meltram", "Pedra Branca", 50)])

        self.add_system("Feris", [("Ethan", 5), ("Farpoint 1", 2)],
                        [("New Orion", "IQ Academy", 50), ("Starbase-51", "Starbase-51", 50)])

        self.add_system("Farpoint 1", [("Feris", 2), ("Farpoint 2", 2)],
                        [])

        self.add_system("Farpoint 2", [("Farpoint 1", 2)],
                        [])

        self.add_system("Franklyn", [("Kelsey", 5)],
                        [("Port Ross", "Port Ross", 50)])

        self.add_system("Antioch", [("Kelsey", 5), ("Hexham", 7)],
                        [("Graninis", "Graninis", 50)])

        self.add_system("Hexham", [("Antioch", 7)],
                        [])

        self.add_system("Lorat", [("Kelsey", 7), ("Drakos", 5)],
                        [("Wimbourne", "Unimatrix 001", 37)])

        self.add_system("Drakos", [("Lorat", 5), ("Fieron", 3)],
                        [])

        self.add_system("Fieron", [("Drakos", 3), ("Descarte", 7)],
                        [("Welling", "Welling", 50)])

        self.add_system("Grantham", [("Kelsey", 5), ("Palham", 5)],
                        [("Beltaine", "mentlsplace", 10)])

        self.add_system("Palham", [("Grantham", 5), ("Descarte", 4)],
                        [("Wolsley", "Mysfits", 10)])

        self.add_system("Descarte", [("Palham", 4), ("Fieron", 7), ("Bedlam", 5)],
                        [("San Ferran", "San Ferran", 50), ("San Miguel", "San Miguel", 50), ("Daphine", "Shipwreck Island", 50)])

        self.add_system("Bedlam", [("Descarte", 5)],
                        [])

    def dist_and_path(self, start, end):
        dist = {start: 0}
        parent = {}
        q = [start]
        while len(q) > 0:
            cur = q[0]
            del q[0]
            for node, weight in self.graph[cur]:
                if node not in dist or dist[node] > dist[cur] + weight:
                    dist[node] = dist[cur] + weight
                    parent[node] = cur
                    q.append(node)
            q.sort(key=lambda a: dist[a])
        path = []
        cur = end
        while cur != start:
            path.append(cur)
            cur = parent[cur]
        return dist[end], list(reversed(path))

    def nearest_ashar(self, start, start_planet, start_location):
        # return nearness, dist, path, planet, location, cost
        # Same Location
        if start_location in [i[1] for i in self.ashar[start]]:
            return 0, 0, [], start_planet, start_location, 0
        # Same Planet
        if start_planet in [i[0] for i in self.ashar[start]]:
            planet, location, cost = reduce(lambda a, b: a if a[2] <= b[2] else b, [i for i in self.ashar[start] if i[0] == start_planet])
            return 1, 0, [], start_planet, location, cost
        # Same System
        if len(self.ashar[start]) > 0:
            planet, location, cost = reduce(lambda a, b: a if a[2] <= b[2] else b, self.ashar[start])
            return 2, 0, [], planet, location, cost
        # Different System
        else:
            dist = {start: 0}
            parent = {}
            q = [start]
            while len(q) > 0:
                cur = q[0]
                del q[0]
                for node, weight in self.graph[cur]:
                    if node not in dist or dist[node] > dist[cur] + weight:
                        dist[node] = dist[cur] + weight
                        parent[node] = cur
                        q.append(node)
                q.sort(key=lambda a: dist[a])
            dist = sorted([(k, dist[k]) for k in dist], key=lambda a: a[1])
            while len(self.ashar[dist[0][0]]) == 0:
                del dist[0]
            while dist[-1][1] != dist[0][1]:
                del dist[-1]
            system, planet, location, cost = "---", "---", "---", 9999999999
            for s, d in dist:
                for a_planet, a_location, a_cost in self.ashar[s]:
                    if a_cost < cost:
                        system, planet, location, cost = s, a_planet, a_location, a_cost
            path = []
            cur = system
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            return 3, dist[0][1], list(reversed(path)), planet, location, cost
