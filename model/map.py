from typing import Iterator, Tuple
from model.coordinate import Coordinate
from model.edge import Edge


class Map:
    def __init__(self):
        self.system_graph = {}
        self.system_planets = {}
        self.planet_ports = {}
        self.port_buildings = {}
    
    def insert_system_connection(self, system1, system2, fuel_cost):
        if system1 not in self.system_graph:
            self.system_graph[system1] = []
            self.insert_system_planet(system1, 'Jump Gate Nexus')
            self.insert_planet_port(system1, 'Jump Gate Nexus', 'Jump Gate Nexus', 50)
        self.system_graph[system1].append((system2, fuel_cost))

        if system2 not in self.system_graph:
            self.system_graph[system2] = []
            self.insert_system_planet(system2, 'Jump Gate Nexus')
            self.insert_planet_port(system2, 'Jump Gate Nexus', 'Jump Gate Nexus', 50)
        self.system_graph[system2].append((system1, fuel_cost))

    def insert_system_connections(self, system1, systems_and_fuel_costs):
        for system2, fuel_cost in systems_and_fuel_costs:
            self.insert_system_connection(system1, system2, fuel_cost)
    
    def insert_system_planet(self, system, planet):
        if system not in self.system_planets:
            self.system_planets[system] = []
        self.system_planets[system].append(planet)
    
    def insert_planet_port(self, system, planet, port, credit_cost):
        if (system, planet) not in self.planet_ports:
            self.planet_ports[(system, planet)] = []
        self.planet_ports[(system, planet)].append((port, credit_cost))
    
    def insert_port_building(self, system, planet, port, building):
        if (system, planet, port) not in self.port_buildings:
            self.port_buildings[(system, planet, port)] = []
        self.port_buildings[(system, planet, port)].append(building)
    
    def get_edges(self, start: Coordinate) -> Iterator[Tuple[Coordinate, Edge]]:
        if start.is_jump_gate_nexus():
            for (system, fuel_cost) in self.system_graph.get(start.system, []):
                yield (Coordinate(system, 'Jump Gate Nexus', 'Jump Gate Nexus'), Edge(Edge.INTER_SYSTEM, fuel_cost, 0))
        
        if start.is_orbiting():
            for planet in self.system_planets.get(start.system, []):
                if planet == start.planet:
                    continue
                yield (Coordinate(start.system, planet, None, None), Edge(Edge.INTER_PLANET, 1, 0))
            
            for (port, credit_cost) in self.planet_ports.get((start.system, start.planet), []):
                yield (Coordinate(start.system, start.planet, port, None), Edge(Edge.DOCK_PORT, 0, credit_cost))
        
        if start.is_docked():
            yield (Coordinate(start.system, start.planet, None, None), Edge(Edge.UNDOCK_PORT, 0, 0))

            for building in self.port_buildings.get((start.system, start.planet, start.port), []):
                yield (Coordinate(start.system, start.planet, start.port, building), Edge(Edge.ENTER_BUILDING, 0, 0))
        
        if start.is_in_building():
            yield (Coordinate(start.system, start.planet, start.port, None), Edge(Edge.EXIT_BUILDING, 0, 0))

    
    def get_edge(self, start, end):
        return next((end_edge[1] for end_edge in self.get_edges(start) if end_edge[0] == end), None)
