def input_to_routers(filename):
    num_routers = None
    routers = []
    edges = []
    with open(filename) as f:
        inputs = f.readlines()
        for i, line in enumerate(inputs):
            if (i == 0):
                num_routers = int(line)
            else:
                line = line.split(' ')
                #parse router ids
                router_a = Router(line[0], num_routers)
                router_b = Router(line[1], num_routers)
                #add adjacencies
                if router_a in routers:
                    routers[routers.index(router_a)].adjacencies.append(router_b)
                else:
                    router_a.adjacencies.append(router_b)
                    routers.append(router_a)

                if router_b in routers:
                    routers[routers.index(router_b)].adjacencies.append(router_a)
                else:
                    router_b.adjacencies.append(router_a)
                    routers.append(router_b)

                #make edge
                edges.append(Edge(router_a, router_b, line[2]))
    return (num_routers, routers, edges)


def input_to_changes(filename, num_routers):
    changes = []
    with open(filename) as f:
        inputs = f.readlines()
        for line in inputs:
            line = line.split(' ')
            time_step = line[0]
            router_a = Router(line[1], num_routers)
            router_b = Router(line[2], num_routers)
            edge = Edge(router_a, router_b, line[3])
            changes.append(Change(time_step, edge))
    return changes

class Router():
    def __init__(self, name, total_routers):
        self.name = name
        self.adjacencies = []
        self.table = {}

    def print_adjacencies(self):
        return str(self.adjacencies)

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name

class Edge():
    def __init__(self, router_a, router_b, cost):
        self.router_a = router_a
        self.router_b = router_b
        self.cost = int(cost)

    def __repr__(self):
        return str(self.router_a) + "->" + str(self.router_b) + " COST: " + str(self.cost)

    def __eq__(self, other):
        return (self.router_a == other.router_a) and (self.router_b == other.router_b)

class Change():
    def __init__(self, time_step, edge):
        self.time_step = time_step
        self.edge = edge

    def apply_change(self, routers, edges):
        if self.edge in edges:
            ind = edges.index(self.edge)
            edges[ind].cost = self.edge.cost
            #delete edge
            if (self.edge.cost) == -1:
                del edges[ind]
        else:
            edges.append(self.edge)
        return edges

    def __repr__(self):
        return "TIME: " + str(self.time_step) + " EDGE:" + str(self.edge)

