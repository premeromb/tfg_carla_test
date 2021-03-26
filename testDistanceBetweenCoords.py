import math

def distanceBetweenCoords(lat1, lon1, lat2, lon2):
    rad=math.pi/180
    dlat=lat2-lat1
    dlon=lon2-lon1
    R=6372.795477598
    a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia=2*R*math.asin(math.sqrt(a))
    return distancia

coord1 = [39.479230, -6.339492]
coord2 = [39.480316, -6.344431]

print(distanceBetweenCoords(0, 0, coord2[0], coord2[1]))