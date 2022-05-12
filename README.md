# FanControl
A Python script for controlling a Raspberry Pi 4 fan based on temperature measurements

## Source
This is the guide: https://howchoo.com/pi/add-raspberry-pi-4-cooling-fan.

## Modifications
* Add a diode across the fan to protect the Raspberry Pi 4.
* Changed the script to use RPi.GPIO and regex.
* Clean up the set ports after the script finishes.

## How to connect the transistor
If you follow the guide mentioned above, be sure to check how you connect your transistor. I used a 2N2222, which is recommended in the guide, but the schematic shows the wrong connection to the board. The emitter needs to be connected to the ground of the Raspberry Pi and the collector needs to be connected to the ground of the fan.

Use your search engine to look up the pinout. This is the one I used: https://lampatronics.com/product/2n2222-transistor40v-600ma-npn/.
Because it's an NPN-transistor, it will work as shown in the guide, but not as efficiently.
