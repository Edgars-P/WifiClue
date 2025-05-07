import math
from typing import List, Optional
import time
import json
import urllib.parse
import webbrowser

from hashtable import HashTable
from scanner import scanAPs
from wifi import LocationGuess, MinimalWifiObservation, WifiObservation


def makeLocationGuess(observations: List[MinimalWifiObservation]) -> LocationGuess:
  # TODO pārbaudīt visus observation
  # No visiem obervation ar zināmiem loc, atrast uztvērēja loc
  return LocationGuess(0, 0, 5, [])

type PosList =  List[List[float]]
def locGuessToPoly(loc: LocationGuess, points: int = 20) -> PosList:
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


# Globāls HashTable wifi punktiem
wifiTable = HashTable(32)

import csv

def importCsv(file_path: str):
  with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      timestamp = row['timestamp']
      latitude = float(row['latitude'])
      longitude = float(row['longitude'])
      macAddress = row['macAddress']
      signalStrength = int(row['signalStrength'])
      ssid = row['ssid']

      observation = WifiObservation(timestamp, latitude, longitude, macAddress, signalStrength, ssid)
      key = macAddress
      wifiTable.insert(key, observation)

  print("Datu bāze apstrādāta!")

def displayMap(points: List[WifiObservation], guess: Optional[LocationGuess]):
  geojson = {
    "type": "FeatureCollection",
    "features": []
  }
  # Pievieno katru wifi punktu kā GeoJSON feature lai tie rādas uz kartes
  for observation in points:
    feature = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [observation.longitude, observation.latitude]
      },
      "properties": {
        "mac": observation.macAddress,
        "ssid": observation.ssid,
        "signal": observation.signalStrength,
        "timestamp": observation.timestamp
      }
    }
    geojson["features"].append(feature)

  if guess:
    poly = locGuessToPoly(guess)
    geojson["features"].append({
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [poly],
        "type": "Polygon"
      }
    })
    geojson["features"].append(    {
      "type": "Feature",
      "properties": {
        "marker-size": "large",
        "marker-color": "#0f0"
      },
      "geometry": {
        "coordinates": [
          guess.longitude,
          guess.latitude
        ],
        "type": "Point"
      }
    })

  geojson_str = json.dumps(geojson)
  # https://stackoverflow.com/a/9345102
  url = f"http://geojson.io/#data=data:application/json,{urllib.parse.quote(geojson_str)}"
  print(url)
  webbrowser.open(url)

start = time.time()
importCsv("wifis.rtu.csv") # Todo - uztaisīt minimālu neostumbler at tikai RTU apkārtni
end = time.time()
print("Importa laiks:", end - start, "s")
# total: 13829
# Importa laiks: 0.826019287109375 s

# Parāda pirmos dažus observations lai redzētu vai dati ir pareizi importēti
def debugWifiStore():
  count = 500
  observations: List[WifiObservation] = []
  for key, observation in wifiTable:
    count -= 1
    if count < 0:
      break
    if count % 3 != 0:
      continue
    observations.append(observation)
    print(count)
  displayMap(observations, None)

def cliLoop():
  command = input(">").split(" ")

  match command:
    case ["locate", "scan"]:
      wifilist = scanAPs()
      guess = makeLocationGuess(wifilist)
      displayMap(guess.usedAPs, guess)
    case ["locate", count] if count.isdigit():
      print("TODO, ievadīt", count, "AP")
    case ["count"]:
      print("TODO saskaitīt datu bāzē salgabātus AP")
    case ["debugstore"]:
      debugWifiStore()
    case _:
      print("Komanta nav atpazīta!")
      print("Atbalstītas komandas: TODO")

while True:
  cliLoop()
