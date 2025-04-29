from typing import List

# Dati kurus var iegūt no wifi skanējuma, bez lokācijas datiem
class MinimalWifiObservation:
  ssid: str
  macAddress: str
  signalStrength: int
  def __init__(self, macAddress: str, signalStrength: int, ssid: str):
    self.macAddress = macAddress
    self.signalStrength = signalStrength
    self.ssid = ssid


# WifiObservation - XYZ punkts kurā ir pamanīts WIFI AP
class WifiObservation(MinimalWifiObservation):
  timestamp: str
  latitude: float
  longitude: float
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
