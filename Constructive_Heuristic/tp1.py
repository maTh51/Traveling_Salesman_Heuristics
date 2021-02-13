from collections import deque
import math
import time
import sys
from bisect import insort

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


def calc_tsp(tsp, savings):
    path = []
    rec_ar = []
    send_ar = []
    
    for i in range(1, len(savings)):
        if(
            (savings[-i][1] in send_ar) == False and 
            (savings[-i][2] in rec_ar) == False and
            find_cicle(path, savings[-i][2], savings[-i][1]) == False
        ):
            send_ar.append(savings[-i][1])
            rec_ar.append(savings[-i][2])
            path.append((savings[-i][1], savings[-i][2]))
                
        elif(
            (savings[-i][1] in rec_ar) == False and 
            (savings[-i][2] in send_ar) == False and
            find_cicle(path, savings[-i][1], savings[-i][2]) == False
        ):
            send_ar.append((savings[-i][2]))
            rec_ar.append(savings[-i][1])
            path.append((savings[-i][2], savings[-i][1]))

            
        if((len(rec_ar) + len(send_ar)) == (2*(tsp["DIMENSION"] - 2))):
            flag = True
            break

    if(flag == False):
        if(
            (savings[0][1] in send_ar) == False and 
            (savings[0][2] in rec_ar) == False and
            find_cicle(path, savings[-i][2], savings[-i][1]) == False
        ):
            send_ar.append(savings[0][1])
            rec_ar.append(savings[0][2])
            path.append((savings[-i][1], savings[-i][2]))
        elif(
            (savings[0][1] in rec_ar) == False and 
            (savings[0][2] in send_ar) == False and
            find_cicle(path, savings[-i][1], savings[-i][2]) == False
        ):
            send_ar.append(savings[0][2])
            rec_ar.append(savings[0][1])
            path.append((savings[-i][2], savings[-i][1]))

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

def get_tsp_path_cost():
    file_name = sys.argv[1]
    tsp, hub = read_tsp_file(file_name)
    save = calculate_savings(tsp, hub)
    route = calc_tsp(tsp, save)
    cost = calc_cost(tsp, route)
    
    return tsp, route, cost

if __name__ == "__main__":
    start_time = time.time()
    tsp, route, cost = get_tsp_path_cost()
    print("Formed route: \n")
    print(route)
    print("\nTotal Cost: {}".format(cost))
    print("\n---tempo de exec: %s seconds ---" % round((time.time() - start_time), 3))
