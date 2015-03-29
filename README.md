Adafruit Bluefruit LE Firmware
==============================

This repository contains firmware images for the Bluefruit LE family of boards from Adafruit Industries.

Current members of this board family include:

- [Bluefruit LE Friend](https://www.adafruit.com/product/2267)

The firmware on your Bluefruit LE modules can be updated with the [on-board DFU bootloader](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/field-updates), using the latest firmare image from this repository for the update.

# Important Note

For the [BLEFriend](https://www.adafruit.com/product/2267) currently in the store, you **must use the 0.5.0 or lower series firmware**.  The 0.6.0+ series firmware only works with new, unreleased parts with 32KB SRAM and won't boot on older 16KB SRAM parts.

The BLEFriend boards should normally be updated with the .hex file located here: vhttps://github.com/adafruit/Adafruit_BluefruitLE_Firmware/tree/master/0.5.0/blefriend
