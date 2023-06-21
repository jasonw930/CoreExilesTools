class Edge:
    INTER_SYSTEM = 0
    INTER_PLANET = 1
    DOCK_PORT = 2
    UNDOCK_PORT = 3
    ENTER_BUILDING = 4
    EXIT_BUILDING = 5


    def __init__(self, action, fuel_cost, credit_cost):
        self.action = action
        self.fuel_cost = fuel_cost
        self.credit_cost = credit_cost

    def __key(self):
        return (self.action, self.fuel_cost, self.credit_cost)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.__key() == other.__key()
        return NotImplemented
