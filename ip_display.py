#!/usr/bin/env python3

import time
import subprocess
import netifaces
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

def get_ip_address():
    """Get IP addresses from eth0 and wlan0 interfaces."""
    try:
        ips = []
        # Check common interface names
        for interface in ['eth0', 'wlan0']:
            try:
                if interface in netifaces.interfaces():
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        ip = addrs[netifaces.AF_INET][0]['addr']
                        if not ip.startswith('127.'):  # Skip loopback
                            ips.append(f"{interface}: {ip}")
            except Exception as e:
                print(f"Error getting {interface} IP: {e}")
                
        return ips if ips else ["No IP found"]
    except Exception as e:
        print(f"Error getting IP addresses: {e}")
        return ["Error"]

def main():
    # Initialize I2C
    print("Initializing I2C interface...")
    serial = i2c(port=1, address=0x3C)
    
    # Initialize the OLED display
    print("Initializing OLED display...")
    device = ssd1306(serial, width=128, height=32)
    
    # Use the default font
    font = ImageFont.load_default()
    
    print("Starting display loop...")
    try:
        while True:
            # Get IP addresses
            ips = get_ip_address()
            print(f"Current IPs: {ips}")
            
            # Draw on the display
            with canvas(device) as draw:
                y = 0
                for ip in ips[:2]:  # Show up to 2 IPs
                    draw.text((0, y), ip, font=font, fill="white")
                    y += 16
            
            # Wait before next update
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nCleaning up...")
        device.clear()
        print("Display cleared. Exiting.")

if __name__ == "__main__":
    try:
        print("Starting IP Display Program")
        # Install required package if not present
        subprocess.run(["pip3", "install", "netifaces"], check=True)
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
