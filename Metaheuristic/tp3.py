from collections import deque
import math
import time
import sys
from bisect import insort
import random

def minimal_tsp():
    return { "NAME"             : ""
            ,"TYPE"             : None 
            ,"COMMENT"          : ""
            ,"DIMENSION"        : None
            ,"EDGE_WEIGHT_TYPE" : None
            ,"CITIES"           : []}


def scan_tsp_file(tsp,tspfile):
    for line in tspfile:
        words   = deque(line.split())
        keyword = words.popleft().strip(": ")

        if keyword == "COMMENT":
            tsp["COMMENT"] += " ".join(words).strip(": ")
        elif keyword == "NAME":
            tsp["NAME"] = " ".join(words).strip(": ")
        elif keyword == "TYPE":
            tsp["TYPE"] = " ".join(words).strip(": ")
        elif keyword == "DIMENSION":
            tsp["DIMENSION"] = int(" ".join(words).strip(": "))
        elif keyword == "EDGE_WEIGHT_TYPE":
            tsp["EDGE_WEIGHT_TYPE"] = " ".join(words).strip(": ")
        elif keyword == "NODE_COORD_SECTION":
            break

def read_cities(tsp,tspfile):
    dist_hub = []
    for n in range(1, tsp["DIMENSION"] + 1):
        line  = tspfile.readline()
        words = deque(line.split())
        tsp["CITIES"].append(
            (float(words.popleft()), float(words.popleft()), float(words.popleft()))
        )
        if tsp["CITIES"][n-1][0] != 1:
            if tsp["EDGE_WEIGHT_TYPE"] == "EUC_2D":
                xd= tsp["CITIES"][0][1]-tsp["CITIES"][n-1][1]
                yd= tsp["CITIES"][0][2]-tsp["CITIES"][n-1][2]
                dij= int(round( math.sqrt( xd*xd + yd*yd)))

            elif tsp["EDGE_WEIGHT_TYPE"] == "ATT":
                xd= tsp["CITIES"][0][1]-tsp["CITIES"][n-1][1]
                yd= tsp["CITIES"][0][2]-tsp["CITIES"][n-1][2]
                dij= int(round(math.sqrt( (xd*xd + yd*yd)/10.0)))
                
            dist_hub.append(
                (tsp["CITIES"][n-1][0], dij)
            )
            
    return dist_hub

def calculate_savings(tsp, dist_hub):
    savings = []
    for i in range(2, tsp["DIMENSION"]+1):
        for j in range(i+1, tsp["DIMENSION"]+1):
            if tsp["EDGE_WEIGHT_TYPE"] == "EUC_2D":
                xd= tsp["CITIES"][(i-1)][1]-tsp["CITIES"][(j-1)][1]
                yd= tsp["CITIES"][(i-1)][2]-tsp["CITIES"][(j-1)][2]
                dij= int(round( math.sqrt( xd*xd + yd*yd)))

            elif tsp["EDGE_WEIGHT_TYPE"] == "ATT":
                xd= tsp["CITIES"][i-1][1]-tsp["CITIES"][(j-1)][1]
                yd= tsp["CITIES"][i-1][2]-tsp["CITIES"][(j-1)][2]
                dij= int(round(math.sqrt( (xd*xd + yd*yd)/10.0)))


            ans = dist_hub[i-2][1] + dist_hub[(j-2)][1] - dij
            insort(savings, (ans, i, j))

    return savings

def find_cicle(path, beg, fin):
    for item in path:
        if item[0] == beg:
            if item[1] == fin:
                return True
            else:
                return find_cicle(path, item[1], fin)
    
    return False


def calc_grasp_tsp(tsp, savings, alpha):
    path = []
    rec_ar = []
    send_ar = []
    grasp = []

    while(((len(rec_ar) + len(send_ar)) < (2*(tsp["DIMENSION"] - 2))) and (len(savings) > 0)):
        if(savings[0][0] < 0):
            c_e = savings[-1][0] - alpha*(savings[-1][0] + savings[0][0])
        else:
            c_e = savings[-1][0] - alpha*(savings[-1][0] - savings[0][0])
        
        if savings[-1][0] < 0:
            c_e = savings[-5][0]

        grasp.clear()

        for i in range(0, len(savings)):
            if(savings[i][0] >= c_e):
                grasp.append((savings[i], i))

        chosen = random.choice(grasp)

        if(
            (chosen[0][1] in send_ar) == False and 
            (chosen[0][2] in rec_ar) == False and
            find_cicle(path, chosen[0][2], chosen[0][1]) == False
        ):
            send_ar.append(chosen[0][1])
            rec_ar.append(chosen[0][2])
            path.append((chosen[0][1], chosen[0][2]))
                
        elif(
            (chosen[0][1] in rec_ar) == False and 
            (chosen[0][2] in send_ar) == False and
            find_cicle(path, chosen[0][1], chosen[0][2]) == False
        ):
            send_ar.append((chosen[0][2]))
            rec_ar.append(chosen[0][1])
            path.append((chosen[0][2], chosen[0][1]))

        del savings[chosen[1]]

    for i in range(2, tsp["DIMENSION"]):
        if((i in send_ar) == False):
            for j in range(2, tsp["DIMENSION"]):
                if((j in rec_ar) == False):
                    path.append((i,1))
                    path.append((1,j))
                    
    return path

def calc_cost(tsp, path):
    cost = 0
    for x,y in path:
        if tsp["EDGE_WEIGHT_TYPE"] == "EUC_2D":
            xd= tsp["CITIES"][(x-1)][1]-tsp["CITIES"][(y-1)][1]
            yd= tsp["CITIES"][(x-1)][2]-tsp["CITIES"][(y-1)][2]
            dij= int(round( math.sqrt( xd*xd + yd*yd)))

        elif tsp["EDGE_WEIGHT_TYPE"] == "ATT":
            xd= tsp["CITIES"][x-1][1]-tsp["CITIES"][(y-1)][1]
            yd= tsp["CITIES"][x-1][2]-tsp["CITIES"][(y-1)][2]
            dij= int(round(math.sqrt( (xd*xd + yd*yd)/10.0)))
        
        cost += dij

    return cost

def read_tsp_file(file_name):
    file = open(file_name,'r')
    tsp = minimal_tsp()
    scan_tsp_file(tsp, file)
    hub = read_cities(tsp, file)
    file.close()
    return tsp,hub

def get_grasp_tsp_path_cost(alpha):
    file_name = sys.argv[1]
    tsp, hub = read_tsp_file(file_name)
    save = calculate_savings(tsp, hub)
    route = calc_grasp_tsp(tsp, save, alpha)
    cost = calc_cost(tsp, route)
    return tsp, route, cost

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

                #para não calcular toda a lista desnecessariamente
                if ((calc_cost_bylist(tsp, new_way[i-1:i+1]) + calc_cost_bylist(tsp, new_way[j-1:j+1])) < (calc_cost_bylist(tsp, best_way[i-1:i+1]) + calc_cost_bylist(tsp, best_way[j-1:j+1]))):
                # if calc_cost_bylist(tsp, new_way) < calc_cost_bylist(tsp, best_way):
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
    best = -1 
    cost = -1
    for x in range(10):
        tsp, route, cost_aux = get_grasp_tsp_path_cost(0.05)
        way = [1]
        way = biuld_simple_path(route, way, route[(len(route)-1)][1])
        best_aux = two_opt(tsp, way)
        cost_aux = calc_cost_bylist(tsp, best_aux)

        if(((cost_aux < cost) or (cost == -1)) and len(way) == ((len(route)) + 1)):
            cost = cost_aux
            best = best_aux

    print("Best route found: \n")
    print(best)
    print("\nTotal Cost: {}".format(cost))
    print("\n---tempo de exec: %s seconds ---" % round((time.time() - start_time), 3))