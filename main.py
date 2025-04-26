from typing import Optional, List, Tuple, Iterator
import time


# WifiObservation - XYZ punkts kurā ir pamanīts WIFI AP
# SSID ir hashmap key, to nav nepieciešams glabāt
class WifiObservation:
  timestamp: str
  latitude: float
  longitude: float
  macAddress: str
  signalStrength: int
  def __init__(self, timestamp: str, latitude: float, longitude: float, macAddress: str, signalStrength: int, ssid: str):
    self.timestamp = timestamp
    self.latitude = latitude
    self.longitude = longitude
    self.macAddress = macAddress
    self.signalStrength = signalStrength

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
    while node != None and node.next != None:
      # Ja key eksistē, update value
      if node.key == k:
        node.value = v
        return
      node = node.next
    node.next = newNode

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
      key = f"{macAddress}:{ssid}"
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

printDb()
start = time.time()
importCsv("wifis.private.csv") # Todo - uztaisīt minimālu neostumbler at tikai RTU apkārtni
end = time.time()
printDb()
print("Importa laiks:", end - start, "s")
# total: 13829
# Importa laiks: 0.826019287109375 s
