# BedRock Applications and Hardware Ecosystem

This repository serves as the official ecosystem and package registry for the BedRock systems programming language, specifically optimized for bare-metal deployment on the ESP32-C3 RISC-V architecture without any operating system or external runtime overhead.

## Overview

The applications and core libraries contained herein demonstrate the platform's architectural stability, memory management, and deterministic hardware control under direct boot execution. Every binary is synthesized purely by the BedRock compiler infrastructure, bypassing standard SDK bloat to achieve minimal binary footprint footprints.

## Repository Structure

- `core-libs/`: Core hardware drivers and system stabilization packages.
- `examples/`: Production-ready interactive applications on physical hardware.
- `tooling/`: Automation utilities for target-specific image encapsulation.

## Target Hardware Specifications

All binaries are compiled and packaged to match the hardware register map of the ESP32-C3 Super Mini SoC under the following memory layout constraints:

- **BASE Layout**: `0x42000008` (Offset to protect image headers)
- **STACK Pointer**: `0x3FC9F000` (DRAM Stack Address)
- **DATA Segment**: `0x3FC8F000` (Static Allocation Boundary)

## Build and Deployment

Compilation requires the native `brc3` driver. Image encapsulation is finalized using the target-specific direct boot packager to generate a valid hardware image.

```bash
# 1. Compile source code to raw machine instructions
brc3 main.br --target riscv -o raw_output.bin

# 2. Encapsulate into a valid direct boot hardware image
python3 pack_direct_boot.py raw_output.bin firmware_direct.bin

# 3. Flash directly to Sector 0 of the SPI Flash
python3 -m esptool --chip esp32c3 -p /dev/ttyACM0 write-flash --flash-mode dio --flash-freq 80m --flash-size 4MB 0x0 firmware_direct.bin
```

## License

This ecosystem and all included applications are open-source software licensed under the terms of the MIT License.
