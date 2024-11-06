
#!/usr/bin/env python3
import subprocess
import re
import socket

# Define the URL for the PHP endpoint
url = "https://faridfarahmand.net/EE465/checkipaddress.php"

def get_ip_address():
    """Get the IP address of the Raspberry Pi."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "No IP Found"
    finally:
        s.close()
    return ip_address

def get_mac_address():
    """Get the MAC address of the Raspberry Pi."""
    try:
        # Run ifconfig and search for MAC address
        ifconfig_result = subprocess.check_output("ifconfig", shell=True).decode()
        mac_address = re.search(r"ether ([\da-fA-F:]{17})", ifconfig_result).group(1)
    except Exception:
        mac_address = "No MAC Found"
    return mac_address

def send_ip_mac():
    """Send IP and MAC address to the PHP page."""
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    # Construct the curl command with actual IP and MAC addresses
    command = f'curl -X POST {url} -d "IpAddress={ip_address}" -d "MACAddress={mac_address}"'
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    send_ip_mac()
