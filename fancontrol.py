#!/usr/bin/env python3

import logging
import re
import RPi.GPIO as GPIO
import subprocess
import time

# Source: https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    filename="/home/{username}/Logs/fancontrol.log",
    encoding="utf-8",
    level=logging.DEBUG
)

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
    try:
        command = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True)
        output = command.stdout.decode()
        match = re.search(r"\d+\.\d", output)
        return float(match.group())
    except (IndexError, TypeError, ValueError):
        logging.error("Could not parse the command output.")
        raise RuntimeError("Could not parse the command output.")


def main():
    """
    Get the core temperature and check if it's higher than the value
    specified in 'ON_THRESHOLD'. If the temperature is higher, turn on
    BCM17 for 120 seconds to cool down the Raspberry Pi 4 (Pi-hole).
    """
    try:
        temperature = get_temperature()
        if temperature >= ON_THRESHOLD:
            logging.info("Activating BCM17 to start the fan.")
            GPIO.output(17, 1)  # Activate BCM17 to start the fan.
            time.sleep(120)
    except (IndexError, TypeError, ValueError):
        logging.error("Could not check the temperature.")
        raise RuntimeError("Could not check the temperature.")


if __name__ == "__main__":
    main()
    GPIO.cleanup()  # BCM17 will be reset to its default setting.
