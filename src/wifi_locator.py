import subprocess
import platform
import re
from wifi import WifiObservation
from main import makeLocationGuess, displayMap


def get_wifi_list() -> list:
    system = platform.system()
    wifi_list = []

    try:
        if system == "Windows":
            # Windows: Get Wi-Fi list
            output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], encoding="utf-8")
            wifi_list = re.findall(r"SSID\s*:\s*(.*)\n.*?Signal\s*:\s*(\d+)%.*?BSSID\s*:\s*([\w:]+)", output, re.DOTALL)
        elif system == "Linux":
            # Linux: Get Wi-Fi list
            output = subprocess.check_output(["nmcli", "dev", "wifi"], encoding="utf-8")
            wifi_list = re.findall(r"(\S+)\s+Infra\s+\S+\s+(\d+)\s+(\S+)", output)
        elif system == "Darwin":
            # macOS: Get Wi-Fi list
            output = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], encoding="utf-8")
            wifi_list = re.findall(r"(\S+)\s+([\-\d]+)\s+([\w:]+)", output)
        else:
            print("Unsupported OS")
            return []
    except subprocess.CalledProcessError:
        print("Failed to retrieve Wi-Fi list.")
        return []

    return wifi_list


def find_location_from_wifi():
    wifi_list = get_wifi_list()
    if not wifi_list:
        print("No Wi-Fi networks found.")
        return

    observations = []
    for ssid, signal, mac in wifi_list:
        observation = WifiObservation("", 0.0, 0.0, mac, int(signal), ssid)
        observations.append(observation)

    guess = makeLocationGuess(observations)
    displayMap(observations, guess)


if __name__ == "__main__":
    find_location_from_wifi()
