Adafruit Bluefruit LE Firmware
==============================

This repository contains firmware images for the Bluefruit LE family of boards from Adafruit Industries.

Current members of this board family include:

- [Bluefruit LE Friend](https://www.adafruit.com/product/2267)
- [Bluefruit LE UART Friend](https://www.adafruit.com/product/2479)

The firmware on your Bluefruit LE modules can be updated with the [on-board DFU bootloader](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/field-updates), using the latest firmare image from this repository for the update.

The Adafruit Bluefruit LE Connect app for [Android](https://play.google.com/store/apps/details?id=com.adafruit.bluefruit.le.connect&hl=en_US) or [iOS](https://itunes.apple.com/app/adafruit-bluefruit-le-connect/id830125974?mt=8) also enable over the air firmware updates using the files found in this repo.

# Important Note

For the [Bluefruit LE Friend](https://www.adafruit.com/product/2267), whiched is based on the first generation 16KB SRAM nRF51822, you **must use the 0.5.0 or lower series firmware**.

The 0.6.0+ series firmware only works with newer boards based on 32KB SRAM nrf51822 parts like the [Bluefruit LE UART Friend](https://www.adafruit.com/product/2479). The 0.6.0+ firmware won't boot on older 16KB SRAM parts.

The 16KB SRAM Bluefruit LE Friend board should normally be updated with the .hex file located here: https://github.com/adafruit/Adafruit_BluefruitLE_Firmware/tree/master/0.5.0/blefriend

If you are using the Bluefruit LE Connect apps from Adafruit to manage your firmware updates, it should take care of the version differences automatically.
