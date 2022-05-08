#!/usr/bin/env python3

import re
import subprocess
import syslog

from gpiozero import OutputDevice

ON_THRESHOLD = 50  # (degrees Celsius) Fan starts at this temperature.
OFF_THRESHOLD = 40  # (degress Celsius) Fan stops at this temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.


def get_temp():
    """
    Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises a 'RuntimeError' if response cannot be parsed.
    Returns a 'float' with the core temperature in degrees Celsius.
    """
    command = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True)
    output = command.stdout.decode()
    match = re.search(r"\d+\.\d", output)

    try:
        return float(match.group())
    except (IndexError, TypeError, ValueError):
        raise RuntimeError("Could not parse temperature output.")


if __name__ == "__main__":
    # Validate the 'on' and 'off' thresholds.
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError("OFF_THRESHOLD must be less than ON_THRESHOLD.")

    fan = OutputDevice(GPIO_PIN)
    temp = get_temp()

    try:
        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running. Note: 'fan.value' returns either 0 or 1.
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()
            syslog.syslog("Fan started")
        # Stop the fan if the fan is running and the temperature has dropped
        # to or below the 'off' threshold.
        elif fan.value and temp < OFF_THRESHOLD:
            fan.off()
            syslog.syslog("Fan stopped")
    except (IndexError, TypeError, ValueError):
        raise RuntimeError("Could not start or stop the fan.")
