Adafruit Bluefruit LE Firmware
==============================

This repository contains firmware images for the Bluefruit LE family of boards from Adafruit Industries.

Current members of this board family include:

- **BLEFRIEND** Firmware (16KB SRAM parts):
  - [Bluefruit LE Friend V1](https://www.adafruit.com/product/2267) - Blue PCB
- **BLEFRIEND32** Firmware (32KB SRAM parts):
  - [Bluefruit LE Friend V2](https://www.adafruit.com/product/2267) - Black PCB
  - [Bluefruit LE UART Friend](https://www.adafruit.com/product/2479)
- **BLESPIFRIEND** Firmware:
  - [Bluefruit LE SPI Friend](https://www.adafruit.com/product/2633)
  - [Bluefruit LE Shield](https://www.adafruit.com/products/2746)
  - [Bluefruit LE Micro](https://www.adafruit.com/product/2661)
  - [Feather 32u4 Bluefruit LE](https://www.adafruit.com/product/2829)
  - [Feather M0 Bluefruit LE](https://www.adafruit.com/products/2995)

The firmware on your Bluefruit LE modules can be updated with the [on-board DFU bootloader](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/field-updates), using the latest firmare image from this repository for the update.

The Adafruit Bluefruit LE Connect app for [Android](https://play.google.com/store/apps/details?id=com.adafruit.bluefruit.le.connect&hl=en_US) or [iOS](https://itunes.apple.com/app/adafruit-bluefruit-le-connect/id830125974?mt=8) also enable over the air firmware updates using the files found in this repo.

# Firmware/Board Compatibility Chart

Firmware  | BLEFRIEND  | BLEFRIEND32 | BLESPIFRIEND
--------- | ---------- | ----------- | ------------
0.3.1     | Yes        | --          | --
0.4.7     | Yes        | --          | --
0.5.0     | Yes        | --          | --
0.6.2     | --         | Yes         | --
0.6.5     | --         | Yes         | Yes
0.6.6     | --         | Yes         | Yes
0.6.7     | --         | Yes         | Yes
0.7.0     | --         | Yes         | Yes

For the V1 (blue PCB) [Bluefruit LE Friend](https://www.adafruit.com/product/2267), which is based on the first generation 16KB SRAM nRF51822 parts, you **must use the 0.5.0 or lower series firmware**.

The 0.6.0+ series firmware only works with newer boards based on 32KB SRAM nrf51822 parts like the [Bluefruit LE UART Friend](https://www.adafruit.com/product/2479) or V2 of the Bluefruit LE Friend (black PCBs). The 0.6.0+ firmware won't boot on older 16KB SRAM parts.

If you are using the Bluefruit LE Connect apps from Adafruit to manage your firmware updates, it should take care of the version differences automatically.

# File Types

Each firmware version and board target folder (for example `0.6.7/blespifriend`) contains three files:

- `filename.hex` - The main firmware image, required for any firmware update.
- `filename_signature.hex` - This file contains the CRC check for the filename.hex file above, and is required when manually flashing firmware with a tool like [Adalink](https://github.com/adafruit/Adafruit_Adalink).  If the _signature.hex file containing the CRC check isn't flashed along with the main firmware image, the bootloader on the nRF51 will reject the firmware image and you will boot into DFU mode.  You only need this file when manually flashing firmware updates onto you Bluefruit LE module via AdaLink or a similar SWD debugger tools.  The CRC will automatically be calculate and written when doing over-the-air (OTA) updates.
- `filename_init.dat` - This file contains meta-data about the main firmware image in filename.hex, such as the required SoftDevice version and expected HW.  This file is required when performing over-the-air (OTA) updates, which is a two file process.
