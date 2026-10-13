#!/usr/bin/env python3
"""
pack_direct_boot.py
Prepends the ESP32-C3 "Direct Boot" magic header (8 bytes) before your
BedRock compiler's raw binary output, so the ROM bootloader skips the
normal ESP-IDF image format and jumps straight to your code.

Usage:
    python3 pack_direct_boot.py raw_output.bin flashable.bin
"""

import sys

MAGIC = bytes([0x1D, 0x04, 0xDB, 0xAE, 0x1D, 0x04, 0xDB, 0xAE])

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 pack_direct_boot.py <input_raw.bin> <output_flashable.bin>")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    with open(input_path, "rb") as f:
        code = f.read()

    with open(output_path, "wb") as f:
        f.write(MAGIC)
        f.write(code)

    print(f"Wrote {len(MAGIC) + len(code)} bytes to {output_path}")
    print("First real instruction is at flash offset 8 (matches `root BASE = 0x42000008;`)")

if __name__ == "__main__":
    main()
