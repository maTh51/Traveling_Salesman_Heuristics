import math
import time
import sys

sys.path.append('../Constructive_Heuristic/')

import tp1

def calc_cost_bylist(tsp, way):
    cost = 0
    for x in range(0, (len(way)-1)):
        y = x + 1
        if tsp["EDGE_WEIGHT_TYPE"] == "EUC_2D":
            xd= tsp["CITIES"][(way[x]-1)][1]-tsp["CITIES"][(way[y]-1)][1]
            yd= tsp["CITIES"][(way[x]-1)][2]-tsp["CITIES"][(way[y]-1)][2]
            dij= int(round( math.sqrt( xd*xd + yd*yd)))

        elif tsp["EDGE_WEIGHT_TYPE"] == "ATT":
            xd= tsp["CITIES"][way[x]-1][1]-tsp["CITIES"][(way[y]-1)][1]
            yd= tsp["CITIES"][way[x]-1][2]-tsp["CITIES"][(way[y]-1)][2]
            dij= int(round(math.sqrt( (xd*xd + yd*yd)/10.0)))
        
        cost += dij

    return cost


def two_opt(tsp, way):
    best_way = way
    flag_improved = True
    while flag_improved:
        flag_improved = False
        for i in range(1, len(way)-2):
            for j in range(i+1, len(way)):
                if j-i == 1: 
                    continue
                new_way = way.copy()
                new_way[i:j] = way[j-1:i-1:-1]

                if calc_cost_bylist(tsp, new_way) < calc_cost_bylist(tsp, best_way):
                    best_way = new_way
                    break
                    # flag_improved = True

        way = best_way

    return best_way

def biuld_simple_path(path, way, start):
        for i in path:
            if i[0] == start:
                way.append(start)
                if i[1] == 1:
                    way.append(i[1])
                    break
                else:
                    biuld_simple_path(path, way, i[1])
        return way


if __name__ == "__main__":
    start_time = time.time()
    tsp, route, cost = tp1.get_tsp_path_cost()
    way = [1]
    way = biuld_simple_path(route, way, route[(len(route)-1)][1])
    best = two_opt(tsp, way)
    cost = calc_cost_bylist(tsp, best)
    print("Best route found: \n")
    print(best)
    print("\nTotal Cost: {}".format(cost))
    print("\n---tempo de exec: %s seconds ---" % round((time.time() - start_time), 3))
