import math
from typing import List
from wifi import LocationGuess


def locGuessToPoly(loc: LocationGuess, points: int = 20) -> List[List[float]]:
    R = 6371  #zemes radiuss km
    lat, lon = loc.latitude, loc.longitude
    accuracy = loc.accuracy / 1000  #parvers m uz km

    polygon = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        dlat = accuracy * math.cos(angle) / R
        dlon = accuracy * math.sin(angle) / (R * math.cos(math.radians(lat)))
        new_lat = lat + math.degrees(dlat)
        new_lon = lon + math.degrees(dlon)
        polygon.append([new_lon, new_lat])

    
    polygon.append(polygon[0])
    return polygon



if __name__ == "__main__":
    guess = LocationGuess(56.962267, 24.070821, 10.0, [])
    poly = locGuessToPoly(guess)
    print("Generated polygon:", poly)
