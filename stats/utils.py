import random
from math import sin, cos, sqrt, atan2, radians

def calculateDistance(coords1, coords2):
    # radius of earth in km
    radius_earth = 6373.0

    lat1 = radians(coords1[0])
    lon1 = radians(coords1[1])
    lat2 = radians(coords2[0])
    lon2 = radians(coords2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius_earth * c

    return distance

def transports(distance):
    transport = None
    tsp = None
    percent = None
    if distance < 2:
        tsp = ["marche", "voiture", "métro", "autres"]
        percent = [65, 20, 10, 5]
    elif distance < 5:
        tsp = ["marche", "voiture", "métro", "autres"]
        percent = [8, 40, 45, 7]
    elif distance < 10:
        tsp = ["voiture", "métro", "autres"]
        percent = [50, 45, 5]
    elif distance < 20:
        tsp = ["voiture", "métro", "train", "autres"]
        percent = [65, 25, 5, 5]
    elif distance < 30:
        tsp = ["voiture", "métro", "train", "autres"]
        percent = [65, 5, 37, 3]
    
    elif distance < 50:
        tsp = ["voiture", "train", "autres"]
        percent = [52, 45, 3]
    else:
        tsp = ["voiture", "train", "autres"]
        percent = [45, 50, 5]

    transport = choicePercent(tsp, percent)

    return transport[0]  

def choicePercent(data,weights):
    choice = random.choices(data, weights=weights, k=1)
    return choice