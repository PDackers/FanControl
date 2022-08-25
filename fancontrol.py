#!/usr/bin/env python3

import re
import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BCM)  # Make use of the BCM-notation.
GPIO.setup(17, GPIO.OUT, initial=0)  # Initially, set BCM17 to output and off.
ON_THRESHOLD = 53.0  # (degrees Celsius) Fan starts at or above this temperature.


def get_temperature():
    """
    Get the core temperature.
    Run a subprocess to get the core temperature and parse the output.
    Raises a 'RuntimeError' if the response cannot be parsed.
    Returns a 'float' with the core temperature in degrees Celsius.
    """
    command = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True)
    output = command.stdout.decode()
    match = re.search(r"\d+\.\d", output)
    try:
        return float(match.group())
    except (IndexError, TypeError, ValueError):
        raise RuntimeError("Could not parse temperature output.")


def main():
    """
    Get the core temperature and check if it's higher than the value
    specified in 'ON_THRESHOLD'. If the temperature is higher, turn on
    BCM17 for 120 seconds to cool down the Raspberry Pi 4 (Pi-hole).
    """
    temperature = get_temperature()
    try:
        if temperature >= ON_THRESHOLD:
            GPIO.output(17, 1)  # Activate BCM17 to start the fan.
            time.sleep(120)
    except (IndexError, TypeError, ValueError):
        raise RuntimeError("Could not check the temperature.")


if __name__ == "__main__":
    main()
    GPIO.cleanup()  # BCM17 will be reset to its default setting.
