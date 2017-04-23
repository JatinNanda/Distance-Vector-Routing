import sys
import copy
import time
from utils import *

if len(sys.argv) < 4:
    print("Please supply all the arguments!")
    sys.exit(0)

#retrieve command line arguments
file_routers = sys.argv[1]
file_changes = sys.argv[2]
mode = sys.argv[3]


#output files
basic = open('basic.txt', 'w')
split = open('split.txt', 'w')
poison_reverse = open('poison.txt', 'w')


print('####### BASIC IMPLEMENTATION #######')
#parse input
num_routers, routers = input_to_routers(file_routers)
changes = input_to_changes(file_changes, num_routers)
changes.sort(key = lambda c: c.time_step)

#main loop
iter_num = 1
converged = False
count_to_infinity = False
last_table = None
last_event = 0
convergence_delay = None



while (not converged or len(changes) > 0):
    print("ITERATION " + str(iter_num))
    #time.sleep(1) #delay for readability

    #First check for count to infinity
    for r in routers:
        for advert in r.table:
            if r.table[advert].total_hops > 100:
                print("Count to infinity instability detected. Stopping iterations.")
                count_to_infinity = True
                break
        if count_to_infinity:
            break
    if count_to_infinity:
        convergence_delay = "N/A"
        break

    #apply changes when applicable
    while len(changes) > 0 and iter_num == int(changes[0].time_step):
        print("Applying change: " + str(changes[0]))
        changes[0].apply_change(routers)
        last_event = changes[0].time_step
        del changes[0]
        converged = False

    #temporary storage for the iteration
    temp_tables = {r.name: copy.deepcopy(r.table) for r in routers}

    #update tables
    for router in routers:
        table_of_router = temp_tables[router.name]
        for advert in table_of_router:
            if table_of_router[advert].next_hop != -1:
                table_of_adj = temp_tables[table_of_router[advert].next_hop]
                if table_of_router[advert].cost != -1 and table_of_adj[advert].cost != -1 and table_of_router[advert].cost != 0:
                    new_cost = table_of_router[advert].cost + table_of_adj[advert].cost
                    router.table[advert].total_hops = 1 + table_of_adj[advert].total_hops
                    router.table[advert].cost = new_cost

    #temporary storage for the iteration
    temp_tables = {r.name: copy.deepcopy(r.table) for r in routers}

    for router in routers:
        table_of_router = temp_tables[router.name]
        for adj in router.adjacencies:
            table_of_adj = temp_tables[adj[0].name]
            #get advertisements from adjacencies
            for advert in table_of_adj:
                if table_of_router[adj[0].name].cost != -1 and table_of_adj[advert].cost != -1:
                    new_cost = table_of_router[adj[0].name].cost + table_of_adj[advert].cost
                    if table_of_router[advert].cost == -1 or new_cost < table_of_router[advert].cost:
                        router.table[advert].cost = new_cost
                        router.table[advert].next_hop = adj[0].name
                        router.table[advert].total_hops = 1 + table_of_adj[advert].total_hops

            #see if direct adjacency is better (initial setup or based on a change)
            if router.table[adj[0].name].cost == -1 or router.table[adj[0].name].cost > adj[1]:
                router.table[adj[0].name] = Advertisement(adj[0].name, adj[1], 1)
                for r in routers:
                    if r.name == adj[0].name:
                        r.table[router.name] = Advertisement(router.name, adj[1], 1)

    table = print_iter_table(routers)
    if table == last_table:
        print("CONVERGED")
        converged = True
    print(print_iter_table(routers))
    last_table = table


    if (mode == '1'):
        #append output per iteration
        basic.write('Round Number: ' + str(iter_num) + '\n')
        basic.write(print_iter_table(routers) + '\n')
        pass

    iter_num += 1
if convergence_delay is None:
    convergence_delay = iter_num - last_event
print("Convergence Delay: " + str(convergence_delay))

#append final output
if mode == '0':
    basic.write('Round Number: ' + str(iter_num - 1) + '\n')
    basic.write(print_iter_table(routers) + '\n')
basic.write('Convergence Delay: ' + str(convergence_delay))

print('####### SPLIT HORIZON IMPLEMENTATION #######')
#parse input
num_routers, routers = input_to_routers(file_routers)
changes = input_to_changes(file_changes, num_routers)
changes.sort(key = lambda c: c.time_step)

#main loop
iter_num = 1
converged = False
count_to_infinity = False
last_table = None
last_event = 0
convergence_delay = None



while (not converged or len(changes) > 0):
    print("ITERATION " + str(iter_num))
    #time.sleep(1) #delay for readability

    #First check for count to infinity
    for r in routers:
        for advert in r.table:
            if r.table[advert].total_hops > 100:
                print("Count to infinity instability detected. Stopping iterations.")
                count_to_infinity = True
                break
        if count_to_infinity:
            break
    if count_to_infinity:
        convergence_delay = "N/A"
        break

    #apply changes when applicable
    while len(changes) > 0 and iter_num == int(changes[0].time_step):
        print("Applying change: " + str(changes[0]))
        changes[0].apply_change(routers)
        last_event = changes[0].time_step
        del changes[0]
        converged = False

    #temporary storage for the iteration
    temp_tables = {r.name: copy.deepcopy(r.table) for r in routers}

    #update tables
    for router in routers:
        table_of_router = temp_tables[router.name]
        for advert in table_of_router:
            if table_of_router[advert].next_hop != -1:
                table_of_adj = temp_tables[table_of_router[advert].next_hop]
                if table_of_router[advert].cost != -1 and table_of_adj[advert].cost != -1 and table_of_router[advert].cost != 0:
                    new_cost = table_of_router[advert].cost + table_of_adj[advert].cost
                    router.table[advert].total_hops = 1 + table_of_adj[advert].total_hops
                    router.table[advert].cost = new_cost

    #temporary storage for the iteration
    temp_tables = {r.name: copy.deepcopy(r.table) for r in routers}

    for router in routers:
        table_of_router = temp_tables[router.name]
        for adj in router.adjacencies:
            table_of_adj = temp_tables[adj[0].name]
            #get advertisements from adjacencies
            for advert in table_of_adj:
                if table_of_router[adj[0].name].cost != -1 and table_of_adj[advert].cost != -1:
                    if table_of_adj[advert].next_hop != router.name:
                        new_cost = table_of_router[adj[0].name].cost + table_of_adj[advert].cost
                        if table_of_router[advert].cost == -1 or new_cost < table_of_router[advert].cost:
                            router.table[advert].cost = new_cost
                            router.table[advert].next_hop = adj[0].name
                            router.table[advert].total_hops = 1 + table_of_adj[advert].total_hops

            #see if direct adjacency is better (initial setup or based on a change)
            if router.table[adj[0].name].cost == -1 or router.table[adj[0].name].cost > adj[1]:
                router.table[adj[0].name] = Advertisement(adj[0].name, adj[1], 1)
                for r in routers:
                    if r.name == adj[0].name:
                        r.table[router.name] = Advertisement(router.name, adj[1], 1)

    table = print_iter_table(routers)
    if table == last_table:
        print("CONVERGED")
        converged = True
    print(print_iter_table(routers))
    last_table = table


    if (mode == '1'):
        #append output per iteration
        split.write('Round Number: ' + str(iter_num) + '\n')
        split.write(print_iter_table(routers) + '\n')
        pass

    iter_num += 1
if convergence_delay is None:
    convergence_delay = iter_num - last_event
print("Convergence Delay: " + str(convergence_delay))

#append final output
if mode == '0':
    split.write('Round Number: ' + str(iter_num - 1) + '\n')
    split.write(print_iter_table(routers) + '\n')
split.write('Convergence Delay: ' + str(convergence_delay))

print('####### POISON REVERSE OUTPUT #######')
#parse input
num_routers, routers = input_to_routers(file_routers)
changes = input_to_changes(file_changes, num_routers)
changes.sort(key = lambda c: c.time_step)

#main loop
iter_num = 1
converged = False
count_to_infinity = False
last_table = None
last_event = 0
convergence_delay = None



while (not converged or len(changes) > 0):
    print("ITERATION " + str(iter_num))
    #time.sleep(1) #delay for readability

    #First check for count to infinity
    for r in routers:
        for advert in r.table:
            if r.table[advert].total_hops > 100:
                print("Count to infinity instability detected. Stopping iterations.")
                count_to_infinity = True
                break
        if count_to_infinity:
            break
    if count_to_infinity:
        convergence_delay = "N/A"
        break

    #apply changes when applicable
    while len(changes) > 0 and iter_num == int(changes[0].time_step):
        print("Applying change: " + str(changes[0]))
        changes[0].apply_change(routers)
        last_event = changes[0].time_step
        del changes[0]
        converged = False

    #temporary storage for the iteration
    temp_tables = {r.name: copy.deepcopy(r.table) for r in routers}

    #update tables
    for router in routers:
        table_of_router = temp_tables[router.name]
        for advert in table_of_router:
            if table_of_router[advert].next_hop != -1:
                table_of_adj = temp_tables[table_of_router[advert].next_hop]
                if table_of_router[advert].cost != -1 and table_of_adj[advert].cost != -1 and table_of_router[advert].cost != 0:
                    new_cost = table_of_router[advert].cost + table_of_adj[advert].cost
                    router.table[advert].total_hops = 1 + table_of_adj[advert].total_hops
                    router.table[advert].cost = new_cost

    #temporary storage for the iteration
    temp_tables = {r.name: copy.deepcopy(r.table) for r in routers}

    for router in routers:
        table_of_router = temp_tables[router.name]
        for adj in router.adjacencies:
            table_of_adj = temp_tables[adj[0].name]
            #get advertisements from adjacencies
            for advert in table_of_adj:
                if table_of_router[adj[0].name].cost != -1 and table_of_adj[advert].cost != -1:
                    if table_of_adj[advert].next_hop != router.name:
                        new_cost = table_of_router[adj[0].name].cost + table_of_adj[advert].cost
                        if table_of_router[advert].cost == -1 or new_cost < table_of_router[advert].cost:
                            router.table[advert].cost = new_cost
                            router.table[advert].next_hop = adj[0].name
                            router.table[advert].total_hops = 1 + table_of_adj[advert].total_hops

            #see if direct adjacency is better (initial setup or based on a change)
            if router.table[adj[0].name].cost == -1 or router.table[adj[0].name].cost > adj[1]:
                router.table[adj[0].name] = Advertisement(adj[0].name, adj[1], 1)
                for r in routers:
                    if r.name == adj[0].name:
                        r.table[router.name] = Advertisement(router.name, adj[1], 1)

    table = print_iter_table(routers)
    if table == last_table:
        print("CONVERGED")
        converged = True
    print(print_iter_table(routers))
    last_table = table


    if (mode == '1'):
        #append output per iteration
        poison_reverse.write('Round Number: ' + str(iter_num) + '\n')
        poison_reverse.write(print_iter_table(routers) + '\n')
        pass

    iter_num += 1
if convergence_delay is None:
    convergence_delay = iter_num - last_event
print("Convergence Delay: " + str(convergence_delay))

#append final output
if mode == '0':
    poison_reverse.write('Round Number: ' + str(iter_num - 1) + '\n')
    poison_reverse.write(print_iter_table(routers) + '\n')
poison_reverse.write('Convergence Delay: ' + str(convergence_delay))

