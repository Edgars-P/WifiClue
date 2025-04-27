from typing import Optional, List, Tuple, Iterator
import time
import json
import urllib.parse
import webbrowser


# WifiObservation - XYZ punkts kurā ir pamanīts WIFI AP
class WifiObservation:
  timestamp: str
  latitude: float
  longitude: float
  macAddress: str
  signalStrength: int
  ssid: str
  def __init__(self, timestamp: str, latitude: float, longitude: float, macAddress: str, signalStrength: int, ssid: str):
    self.timestamp = timestamp
    self.latitude = latitude
    self.longitude = longitude
    self.macAddress = macAddress
    self.signalStrength = signalStrength
    self.ssid = ssid

class LocationGuess:
  latitude: float
  longitude: float
  accuracy: float
  usedAPs: List[WifiObservation]
  def __init__(self, latitude: float, longitude: float, usedAPs: List[WifiObservation]):
    self.latitude = latitude
    self.longitude = longitude
    self.usedAPs = usedAPs


class Node:
  key: str
  value: WifiObservation
  next: Optional['Node']
  def __init__(self, k: str, v: WifiObservation):
    self.key = k
    self.value = v
    self.next = None

# Hastable implementācija no https://github.com/rtudip/de0918-pt-03-Edgars-P/
# Pievienoti tipi lai vieglāk strādāt
class HashTable:
  store: List[Optional[Node]] = []
  slots: int = 0
  def __init__(self, slots: int):
    self.store = []
    self.slots = slots
    # Aizpilda visus slots ar None
    for i in range(slots):
      self.store.append(None)

  # Pārtaisa key par slot index
  def _keyToIndex(self, k: str) -> int:
    return hash(k) % self.slots

  def insert(self, k: str, v: WifiObservation) -> None:
    slot = self._keyToIndex(k)
    node = self.store[slot]
    newNode = Node(k, v)
    if node == None:
      self.store[slot] = newNode
      return

    prev = node
    while node != None:
      # Ja key eksistē un signāls ir stiprāks, update value
      # Teorētiski labākais veids būtu meklēt wifi avotu apstrādājot vairākus punktus
      # bet ja ir pietiekami observations vajadzētu pietikt
      if node.key == k:
        if node.value.signalStrength > v.signalStrength:
          node.value = v
        return
      prev = node
      node = node.next
    prev.next = newNode

  def find(self, k: str) -> Optional[WifiObservation]:
    slot = self._keyToIndex(k)
    node = self.store[slot]
    while node != None:
      if node.key == k:
        return node.value
      node = node.next
    return None

  def __contains__(self, k: str) -> bool:
    return self.find(k) != None

  def remove(self, k: str) -> None:
    slot = self._keyToIndex(k)
    node = self.store[slot]
    prev = None
    while node != None:
      if node.key == k:
        if prev:
          # Ja ir vidū vai beigās, izņem un salīmē ar next
          prev.next = node.next
        else:
          # Ja ir sākumā, ieliek nākamo kā slot
          self.store[slot] = node.next
        return
      prev = node
      node = node.next

  def __iter__(self) -> Iterator:
    self.currentSlot = 0
    self.currentNode = self.store[0]
    return self

  def __next__(self) -> Tuple[str, WifiObservation]:
    # Ja ir currentNode, iet cauri visiem node šajā slot
    if self.currentNode:
      node = self.currentNode
      self.currentNode = self.currentNode.next
      return (node.key, node.value)
    # Ja nav currentNode (baidzās vai neeksistē), iet uz nāk slot
    if self.currentSlot < len(self.store) -1:
      self.currentSlot += 1
      self.currentNode = self.store[self.currentSlot]
      return self.__next__()
    # Ja nav currentNode un nav slot, beigas
    raise StopIteration

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

# Tests - Vai var nolasīt geoclue failu

def printDb():
  count = 0
  for key, observation in wifiTable:
    mac = observation.macAddress
    # Extract SSID from the key
    ssid = key
    lat = observation.latitude
    lon = observation.longitude
    signal = observation.signalStrength

    print(f"{count+1}. MAC: {mac} | SSID: {ssid} | Position: ({lat:.6f}, {lon:.6f}) | Signal: {signal} dBm")
    count += 1

  print(f"total: {count}")

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

debugWifiStore()
