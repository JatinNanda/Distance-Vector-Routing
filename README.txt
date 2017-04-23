Daniel Ocano docano3@gatech.edu
Jatin Nanda jnanda3@gatech.edu
4/23/2017 - Distance Vector Routing

#### Files submitted ####
main.py - Main file to call in python 3.6, runs all 3 algorithms separately
utils.py - Supporting file to clarify the structure of main

routers.txt, changes.txt - necessary to generate the sample output file
basic.txt, split.txt, poison.txt
  - Sample output text file for the sample input files. These are produced with the boolean flag '1' for verbose output

#### Running the Code ####

To run main.py you will want to run python3.6.x
The usage is:
    python3 main.py routers.txt changes.txt flag

    routers.txt is the file with the router connection(graph) description, formatted as outlined in the assignment pdf.
    changes.txt is the file with the topological events to occur to the routers, formatted as outlined in the assignment pdf.
    flag is a binary flag, 0 or 1 as outlined in the assignment pdf.

    main.py then outputs to basic.txt, split.txt, and poison.txt, as outlined in the assignment pdf.

    *Note: There will be output to the console. That can be ignored as it is also present within the text files

#### Limitations/Things to note #####

High-Level Design:
  -Split-Horizon and Poison reverse, although taking slightly different approaches, WILL output the same result. This is based on the instructor in a Piazza post
  -Neither of these should result in a count-to-infinity problem, as we believe this was the point of the assignment. To accomplish this, we propagate deletion of edges until this holds true.
  -We noted that in one of the examples of count-to-infity, one of our paths went to a different part of the cycle. We believe this is acceptable behavior as it depends on which path is selected first.
  -Round number and convergence delay may be slightly different from your expected output. We feel as though this is a matter of implementation (when round numbers get incremented/loops break). They should still be very similar

Assumptions:
  -Our code has some structural limitations, based on the assignment PDF:
    -An edge cannot be added unless it was first removed from the graph.
    -Our code assumes that if a link is being deleted, it must exist. Otherwise, it WILL error out.
  -As a result, our storage structure for the advertisements is inflexible.
    -This way we didn't have to modify our storage size on the fly.
