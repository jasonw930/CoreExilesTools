class Coordinate:
    # (system, planet, None, None) means we are undocked in system and orbiting planet
    # (system, planet, port, None) means we are on planet and docked at port, port is same as planet for NPC ports
    # (system, planet, port, building) means we are docked at port and inside building
    def __init__(self, system=None, planet=None, port=None, building=None):
      self.system = system
      self.planet = planet
      self.port = port
      self.building = building
    
    def __key(self):
        return (self.system, self.planet, self.port, self.building)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.__key() == other.__key()
        return NotImplemented
    
    def is_jump_gate_nexus(self):
        return \
            self.system is not None and \
            self.planet == 'Jump Gate Nexus' and \
            self.port == 'Jump Gate Nexus' and \
            self.building is None  
    
    def is_orbiting(self):
        return \
            self.system is not None and \
            self.planet is not None and \
            self.port is None and \
            self.building is None

    def is_docked(self):
        return \
            self.system is not None and \
            self.planet is not None and \
            self.port is not None and \
            self.building is None
    
    def is_in_building(self):
        return \
            self.system is not None and \
            self.planet is not None and \
            self.port is not None and \
            self.building is not None 
