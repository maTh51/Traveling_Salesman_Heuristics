# Traveling_Salesman_Heuristics

Some implementations of heuristics and metaheuristcs of TSP for Heuristics and Metaheuristics class of UFMG.

## 1. Constructive Heuristic: 

Python implementation of Clarke-Wright savings heuristic. Hub node is the first of the file.

Example to compile: `python3 tp1.py ../TSP_instances/EUC_2D/st70.tsp`

## 2. VND: 

Python implementation of Variable Neighborhood Descent algorithm, using the 2-OPT algorithm to generate the neighborhood, and the solution of the constructive heurístic of tp1 (previous topic).

Example to compile: `python3 tp2.py ../TSP_instances/EUC_2D/st70.tsp`

The program uses the first better solution than the current in a neighborhood and go to another. To find the best solution in each neighborhood, just comment the line 42 and uncomment the 43 line in tp2.py (this generate better solutions, but some cases take a lot of time)

## 3. Metaehuristic:

Python implementation of GRASP metaheuristic, modifying the Clarke-Wright savings heuristic of part 1 to chose the edge to build the path randomy based on alpha (LRC process), and then using the 2-OPT algorithm of part 2 to find the local maximum. Total of 20 iterations.

Example to compile: `python3 tp3.py ../TSP_instances/EUC_2D/st70.tsp`

