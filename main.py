import sys
import time
from utils import *

if len(sys.argv) < 4:
    print("Please supply all the arguments!")
    sys.exit(0)

#retrieve command line arguments
file_routers = sys.argv[1]
file_changes = sys.argv[2]
mode = sys.argv[3]


#parse input
num_routers, routers, edges = input_to_routers(file_routers)
changes = input_to_changes(file_changes, num_routers)
changes.sort(key = lambda c: c.time_step)

#print statement examples
print("NUM ROUTERS:" + str(num_routers))
print("ROUTERS:")
for r in routers:
    print(r)
    print(r.adjacencies)
print("EDGES:")
for e in edges:
    print(e)
print("CHANGES:")
for c in changes:
    print(c)

#output files
basic = open('basic.txt', 'w')
split_horizon = open('split.txt', 'w')
poison_reverse = open('poison.txt', 'w')

#main loop
iter_num = 0
converged = False
while (not converged):
    if max(edges, key = lambda e : e.cost).cost >= 100:
        print("Count to infinity instability detected. Stopping iterations.")
        break

    print("ITERATION " + str(iter_num))
    time.sleep(1) #delay for readability

    #apply changes when applicable
    if len(changes) > 0 and iter_num == int(changes[0].time_step):
        print("Applying change: " + str(changes[0]))
        changes[0].apply_change(routers, edges)
        del changes[0]

    #code for basic protocol


    #code for split horizon


    #code for split horizon with poison reverse

    if (mode == '1'):
        #append output per iteration
        #basic.write('basic')
        #split_horizon.write('split')
        #poison_reverse.write('poison')
        pass

    iter_num += 1

#final output appending
