from typing import List


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

# LocationGuess - Punkts kurā gala ierīce visticamāk atrodas
class LocationGuess:
  latitude: float
  longitude: float
  accuracy: float
  usedAPs: List[WifiObservation]
  def __init__(self, latitude: float, longitude: float, usedAPs: List[WifiObservation]):
    self.latitude = latitude
    self.longitude = longitude
    self.usedAPs = usedAPs
