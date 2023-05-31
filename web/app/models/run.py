import pywifi
import time

def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()  # Create a PyWiFi object
    iface = wifi.interfaces()[0]  # Get the first available network interface

    iface.disconnect()  # Disconnect from any existing Wi-Fi connection
    time.sleep(1)

    profile = pywifi.Profile()  # Create a new Wi-Fi profile
    profile.ssid = ssid  # Set the SSID (Wi-Fi network name)
    profile.auth = pywifi.const.AUTH_ALG_OPEN  # Set the authentication algorithm

    # Set the encryption type and password (comment out if the network is not password-protected)
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()  # Remove all existing profiles
    temp_profile = iface.add_network_profile(profile)  # Add the new profile

    iface.connect(temp_profile)  # Connect to the network
    time.sleep(5)  # Wait for the connection to establish

    if iface.status() == pywifi.const.IFACE_CONNECTED:  # Check if connection is successful
        print("Connected to Wi-Fi!")
        return True
    else:
        return False

# Usage
ssid = "espWifi2"
password = "0123456789A"
connect_to_wifi(ssid, password)
