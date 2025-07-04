import math
from typing import List, Optional
import time
import json
import urllib.parse
import webbrowser
import random

from hashtable import HashTable
from scanner import scanAPs
from wifi import LocationGuess, MinimalWifiObservation, WifiObservation


def makeLocationGuess(observations: List[MinimalWifiObservation]) -> LocationGuess:
  # Svērts vidējais no visiem loc, izmantojot signāla jaudu
  stren = 0
  lat = 0
  lon = 0
  rad = 0.0
  usedAps: List[WifiObservation] = []
  for ap in observations:
    fullap = wifiTable.find(ap.macAddress.lower())
    # print(ap.macAddress.lower(), ap.ssid, fullap)
    if not fullap:
      continue
    stren += ap.signalStrength
    lat += fullap.latitude * ap.signalStrength
    lon += fullap.longitude * ap.signalStrength
    # print(rad, fullap.radius)
    rad = (rad + fullap.radius) / 2
    usedAps.append(fullap)
  # print(lat, lon, stren)
  if not stren:
    print("Nevarēja noteikt atrašanās vietu!")
    return LocationGuess(0, 0, 999, [])
  print("Atrasta atrašanās vieta izmantojot", len(usedAps), "/", len(observations), "wifi punktus")
  return LocationGuess(lat/stren, lon/stren, rad, usedAps)

type PosList =  List[List[float]]
def locGuessToPoly(loc: LocationGuess | WifiObservation, points: int = 20) -> PosList:
    radius_deg = 0
    if isinstance(loc, LocationGuess):
      radius_deg = loc.accuracy
    else:
      radius_deg = loc.radius
    #print(radius_deg)
    polygon = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        # * 0.5 Salabo projekciju jo zeme ir zeme
        # Nestrādās citās valstīs
        # TODO ja kaut kad komercializēsim :P
        offsetla = radius_deg * math.cos(angle) * 0.5
        offsetlo = radius_deg * math.sin(angle)
        new_lat = loc.latitude + offsetla
        new_lon = loc.longitude + offsetlo
        polygon.append([new_lon, new_lat])
    polygon.append(polygon[0]) # Atkal pirmails lai aizvērtu
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

      ex = wifiTable.find(macAddress)

      if not ex:
        observation = WifiObservation(timestamp, latitude, longitude, macAddress, signalStrength, ssid, 0)
        wifiTable.insert(macAddress, observation)
        continue

      newlat = (latitude+ex.latitude)/2
      newlong = (longitude+ex.longitude)/2
      rad = math.sqrt(
         ((latitude - newlat) * 2) ** 2
         + ((longitude - newlong) * 2) ** 2
      )
      # print("rad", rad)
      observation = WifiObservation(
        timestamp,
        (latitude+ex.latitude)/2,
        (longitude+ex.longitude)/2,
        macAddress,
        signalStrength,
        ssid,
        max(rad, ex.radius)
      )
      wifiTable.insert(macAddress, observation)

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
        # "type": "Polygon",
        # "coordinates": [locGuessToPoly(observation, 16)]
        "type": "Point",
        "coordinates": [
          # Izkliedē punktus lai vieglāk redzēt kartē
          observation.longitude + ((random.random() - 0.5) * 0.00001),
          observation.latitude + ((random.random() - 0.5) * 0.00001)
        ],
      },
      "properties": {
        "mac": observation.macAddress,
        "ssid": observation.ssid,
        "signal": observation.signalStrength,
        "timestamp": observation.timestamp,
        "radius": observation.radius
      }
    }
    geojson["features"].append(feature)

  if guess:
    poly = locGuessToPoly(guess)
    geojson["features"].append({
      "type": "Feature",
      "properties": {
        "stroke": "darkgreen",
        "fill": "green",
      },
      "geometry": {
        "coordinates": [poly],
        "type": "Polygon"
      }
    })
    geojson["features"].append({
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
    if count % 5 != 0:
      continue
    observations.append(observation)
    print(count)
  displayMap(observations, None)

def cliLoop():
  try:
    command = input(">").split(" ")
  except:
    exit()

  match command:
    case ["locate", "scan"]:
      wifilist = scanAPs()
      guess = makeLocationGuess(wifilist)
      displayMap(guess.usedAPs, guess)
    case ["locate", count] if count.isdigit():
      wifilist: List[MinimalWifiObservation] = []
      for i in range(int(count)):
        i = input().split(" ")
        mac = i[0].lower()
        ssid = i[1]
        stren = i[2] or 1
        wifilist.append(MinimalWifiObservation(mac, int(stren), ssid))
      guess = makeLocationGuess(wifilist)
      displayMap(guess.usedAPs, guess)

    # case ["count"]:
    #   print("TODO saskaitīt datu bāzē salgabātus AP")
    case ["dump"]:
      debugWifiStore()
    case _:
      print("Komanta nav atpazīta!")
      print("Atbalstītas komandas:\n locate scan\n locate (n)\n dump")

print("Laipni lūgti WifiClue programmā!")
print("Lūdzu ievadiet komantu vai ielīmējiet sarkastu no https://github.com/Edgars-P/WifiClue/blob/main/example_ap_list.md")
while True:
  cliLoop()
