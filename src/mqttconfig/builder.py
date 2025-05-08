from struct import pack

with open("mqtt.bin", "wb") as f:
    # Write the header
    f.write(pack(">H", 0x0020))
    f.write(pack(">HH", 0x0005, 18) + b"test.mosquitto.org")
    f.write(b"\x00")
