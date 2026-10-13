#!/usr/bin/env python3
"""
morse_reader.py — reads the letters the board sends over USB-Serial
and displays them live, one letter per line, in the order received.

Usage:
    python3 morse_reader.py            # tries to auto-detect the port
    python3 morse_reader.py /dev/ttyACM0
    python3 morse_reader.py COM5       # on Windows

Requires: pip install pyserial
"""

import sys
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("Requires the pyserial library: pip install pyserial")
    sys.exit(1)


def find_port():
    ports = list(list_ports.comports())
    if not ports:
        return None
    # prefer a port whose name/description suggests USB/ACM/ESP32
    for p in ports:
        desc = (p.description or "").lower()
        dev = (p.device or "").lower()
        if "usb" in desc or "acm" in dev or "esp" in desc:
            return p.device
    return ports[0].device


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else find_port()
    if not port:
        print("No serial port available. Plug in the board and specify the port manually:")
        print("  python3 morse_reader.py /dev/ttyACM0")
        sys.exit(1)

    print(f"Reading from {port} ...  (Ctrl+C to quit)")
    message = ""

    try:
        with serial.Serial(port, baudrate=115200, timeout=1) as ser:
            while True:
                line = ser.readline()
                if not line:
                    continue
                ch = line.decode(errors="replace").strip()
                if not ch:
                    continue
                message += ch
                print(f"[{time.strftime('%H:%M:%S')}]  letter: {ch}    message so far: {message}")
    except serial.SerialException as e:
        print(f"Could not open the port: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\nFinal message: {message}")


if __name__ == "__main__":
    main()
