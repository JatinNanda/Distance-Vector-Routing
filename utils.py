def input_to_routers(filename):
    num_routers = None
    routers = []
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
                edge_cost = int(line[2])
                #add adjacencies
                if router_a in routers:
                    routers[routers.index(router_a)].adjacencies.append((router_b, edge_cost))
                else:
                    router_a.adjacencies.append((router_b, edge_cost))
                    routers.append(router_a)

                if router_b in routers:
                    routers[routers.index(router_b)].adjacencies.append((router_a, edge_cost))
                else:
                    router_b.adjacencies.append((router_a, edge_cost))
                    routers.append(router_b)

    return (num_routers, routers)


def input_to_changes(filename, num_routers):
    changes = []
    with open(filename) as f:
        inputs = f.readlines()
        for line in inputs:
            line = line.split(' ')
            time_step = int(line[0])
            router_a = Router(line[1], num_routers)
            router_b = Router(line[2], num_routers)
            cost = int(line[3])
            changes.append(Change(time_step, router_a, router_b, cost))
    return changes

def print_iter_table(routers):
    table = ''
    for r in routers:
        table += str(r.name) + ' | '
        for advert in r.table:
            table += str(r.table[advert]) + ' |'
        table += '\n'
    print(table)



class Router():
    def __init__(self, name, total_routers):
        self.name = name
        self.adjacencies = []
        self.table = self.init_table(total_routers)

    def init_table(self, total_routers):
        table = {}
        for i in range(total_routers):
            if i+1 is not int(self.name):
                table[str(i+1)] = Advertisement(0, -1, -1)
            else:
                table[str(i+1)] = Advertisement(self.name, 0, 0)
        return table

    def print_table(self):
        table = ''
        for entry in self.table:
            table += str(self.name) + "->" + str(entry) + " " + (str(self.table[entry]) + "\n")
        return table

    def print_adjacencies(self):
        return str(self.adjacencies)

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return int(self.name)


class Change():
    def __init__(self, time_step, router_a, router_b, cost):
        self.time_step = time_step
        self.router_a = router_a
        self.router_b = router_b
        self.cost = cost

    def apply_change(self, routers):
        #update routers and adjacencies
        router_a = [r for r in routers if r == self.router_a][0]
        router_b = [r for r in routers if r == self.router_b][0]

        #deleting edge, get rid of adjacencies
        if int(self.cost) == -1:
            print("DELETING EDGE")
            b_cost = dict(router_a.adjacencies)[router_b]
            del router_a.adjacencies[router_a.adjacencies.index((router_b, b_cost))]
            a_cost = dict(router_b.adjacencies)[router_a]
            del router_b.adjacencies[router_b.adjacencies.index((router_a, a_cost))]
            self.cost = -1
        #new edge
        elif self.router_b not in dict(router_a.adjacencies):
            print("ADDING NEW EDGE")
            router_a.adjacencies.append((router_b, self.cost))
            router_b.adjacencies.append((router_a, self.cost))
        #existing edge
        else:
            a_cost = dict(router_b.adjacencies)[router_a]
            b_cost = dict(router_a.adjacencies)[router_b]
            del router_a.adjacencies[router_a.adjacencies.index((router_b, b_cost))]
            del router_b.adjacencies[router_b.adjacencies.index((router_a, a_cost))]
            router_a.adjacencies.append((router_b, self.cost))
            router_b.adjacencies.append((router_a, self.cost))

        #update in the routing tables
        if router_a.table[router_b.name].cost > self.cost:
            router_a.table[router_b.name].cost = self.cost
            router_a.table[router_b.name].next_hop = self.router_b
            router_a.table[router_b.name].total_hops = 1

        if router_b.table[router_a.name].cost > self.cost:
            router_b.table[router_a.name].cost = self.cost
            router_b.table[router_a.name].next_hop = self.router_a
            router_b.table[router_a.name].total_hops = 1

    def __repr__(self):
        return "TIME: " + str(self.time_step) + " EDGE:" + str(self.router_a) + "->" + str(self.router_b) + " COST: " + str(self.cost)

class Advertisement():
    def __init__(self, next_hop, cost, total_hops):
        self.next_hop = next_hop
        self.cost = int(cost)
        self.total_hops = total_hops

    def __repr__(self):
        return str(self.next_hop) + "," + str(self.total_hops) + ": " + str(self.cost)
