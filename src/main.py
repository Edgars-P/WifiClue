from typing import List
import time
import json
import urllib.parse
import webbrowser

from hashtable import HashTable
from wifi import LocationGuess, WifiObservation


type PosList =  List[List[float]]
def locGuessToPoly(loc: LocationGuess) -> PosList:
  # TODO izveidot apli no LocationGuess X, Y un accuracy
  return [
    [
      24.070821008499877,
      56.9622676862144
    ],
    [
      24.060788695396667,
      56.95994178583996
    ],
    [
      24.0602261357825,
      56.94912827703811
    ],
    [
      24.0775717238582,
      56.93693055648515
    ],
    [
      24.096370590934953,
      56.94276141126227
    ],
    [
      24.104152665584053,
      56.95219625786467
    ],
    [
      24.089432355703906,
      56.96137312632811
    ],
    [
      24.070821008499877,
      56.9622676862144
    ]
  ]

def makeLocationGuess(observations: List[WifiObservation]) -> LocationGuess:
  # TODO
  return LocationGuess(0, 0, [])


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

def displayMap(points: List[WifiObservation]):
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

  geojson_str = json.dumps(geojson)
  # https://stackoverflow.com/a/9345102
  url = f"http://geojson.io/#data=data:application/json,{urllib.parse.quote(geojson_str)}"
  webbrowser.open(url)

start = time.time()
importCsv("wifis.private.csv") # Todo - uztaisīt minimālu neostumbler at tikai RTU apkārtni
end = time.time()
print("Importa laiks:", end - start, "s")
# total: 13829
# Importa laiks: 0.826019287109375 s

# Parāda pirmos dažus observations lai redzētu vai dati ir pareizi importēti
def debugWifiStore():
  count = 5
  observations: List[WifiObservation] = []
  for key, observation in wifiTable:
    if count < 0:
      break
    observations.append(observation)
    print(count)
    count -= 1
  displayMap(observations)

def cliLoop():
  command = input(">").split(" ")

  match command:
    case ["locate", "scan"]:
      print("TODO skanēt netālus AP un no tiem atrast loc")
    case ["locate", count]:
      print("TODO, ievadīt", count, "AP")
    case ["count"]:
      print("TODO saskaitīt datu bāzē salgabātus AP")

while True:
  cliLoop()
