import subprocess
from wifi import MinimalWifiObservation
from typing import List


def scanAPs() -> List[MinimalWifiObservation]:
  try:
    # https://askubuntu.com/a/851253
    # https://people.freedesktop.org/~lkundrak/nm-docs/nmcli.html
    out = subprocess.check_output(["nmcli", "-t", "-m", "multiline", "-f", "SSID,BSSID,SIGNAL", "dev", "wifi", "list"], encoding="utf-8")
    # SSID:MajasInternets
    # BSSID:5C:E9:31:63:19:97
    # SIGNAL:87
    lines = out.strip().split('\n')
    obs: List[MinimalWifiObservation] = []
    while len(lines):
      ssid = lines.pop(0).replace("SSID:", "")
      mac_address = lines.pop(0).replace("BSSID:", "").lower()
      signal_str = lines.pop(0).replace("SIGNAL:", "")
      try:
        signal_strength = int(signal_str)
        obs.append(MinimalWifiObservation(macAddress=mac_address, signalStrength=signal_strength, ssid=ssid))
      except ValueError:
        pass

    print("locate", len(obs))
    for o in obs:
      print(o.macAddress, o.ssid.replace(" ", ""), o.signalStrength)
    return obs

  except Exception as e:
    print("Skenēšana neizdevās! Skeneris atbalsta tikai Linux sistēmu ar NetworkManager.", e)
    print("Ir iespējams izmantot sagatavotu sarkastu: https://github.com/Edgars-P/WifiClue/blob/main/example_ap_list.md")
    return []
