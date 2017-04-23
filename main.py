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
split_horizon = open('split.txt', 'w')
poison_reverse = open('poison.txt', 'w')


print('####### BASIC IMPLEMENTATION #######')
#parse input
num_routers, routers = input_to_routers(file_routers)
changes = input_to_changes(file_changes, num_routers)
changes.sort(key = lambda c: c.time_step)

#main loop
iter_num = 0
converged = False
count_to_infinity = False


print("INITIAL TABLE")
print_iter_table(routers)

while (not converged or len(changes) > 0):
    for r in routers:
        if int(max(r.adjacencies, key = lambda adj: adj[1])[1]) >= 100:
            print("Count to infinity instability detected. Stopping iterations.")
            count_to_infinity = True
            break
    if count_to_infinity:
        break

    print("ITERATION " + str(iter_num))
    time.sleep(1) #delay for readability

    #apply changes when applicable
    while len(changes) > 0 and iter_num == int(changes[0].time_step):
        print("Applying change: " + str(changes[0]))
        changes[0].apply_change(routers)
        del changes[0]
        converged = False

    #initialize tables with adjacencies
    for router in routers:
        for adj in router.adjacencies:
            router.table[adj[0].name] = Advertisement(adj[0].name, adj[1], 1)

    #temp copy of every table in routers
    temp_tables = {r.name: copy.copy(r.table) for r in routers}
    for router in routers:
        for adj in router.adjacencies:
            table_to_use = temp_tables[adj[0].name]
            for advert in table_to_use:
                if advert in router.table:
                    new_cost = router.table[adj[0].name].cost + table_to_use[advert].cost
                    if router.table[advert].cost == -1 or new_cost < router.table[advert].cost:
                        router.table[advert].cost = new_cost
                        router.table[advert].next_hop = adj[0].name
                        if router.table[advert].total_hops == -1:
                            router.table[advert].total_hops = 1
                        else:
                            router.table[advert].total_hops = 1 + table_to_use[advert].total_hops

    print("UPDATED TABLE")
    print_iter_table(routers)

    #check if no updates were made
    tables = {r.name: r.table for r in routers}
    if tables == temp_tables:
        print("CONVERGED")
        converged = True

    if (mode == '1'):
        #append output per iteration
        basic.write('basic')
        pass

    iter_num += 1

#append final output
basic.write('final_output')

#print('####### SPLIT HORIZON IMPLEMENTATION #######')
#split_horizon.write('split output')
#print('####### POISON REVERSE OUTPUT #######')
#poison_reverse.write('poison output')
