"""Module containing the PWM relay adapter logic."""

import time
import logging
import os

import RPi.GPIO as GPIO


logger = logging.getLogger(__name__)


class PWMRelayAdapter:
    """Adapter that takes a virtual GPIO input and drives a PWM relay."""

    def __init__(self, physical_pin: int, virtual_pin: int, pwm_freq: float = 50.0):
        self.physical_pin = physical_pin
        self.virtual_pin = virtual_pin
        self.pwm_freq = pwm_freq
        self._last_value = GPIO.LOW
        self._pwm = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.physical_pin, GPIO.OUT)
        GPIO.setup(self.virtual_pin, GPIO.OUT)

        self._pwm = GPIO.PWM(self.physical_pin, self.pwm_freq)
        self._pwm.start(5.0)
        time.sleep(1)
        self._pwm.ChangeDutyCycle(0.0)

    def run(self) -> None:
        """Begin listening on the virtual pin and drive the PWM relay.

        This method blocks until a KeyboardInterrupt is raised.
        """
        try:
            logger.info("Starting main loop, monitoring virtual pin %s", self.virtual_pin)
            while True:
                current = GPIO.input(self.virtual_pin)
                if current == self._last_value:
                    continue
                if current == GPIO.HIGH:
                    self._pwm.ChangeDutyCycle(10.0)
                else:
                    self._pwm.ChangeDutyCycle(0.0)
                self._last_value = current
                logger.info("Current relay value: %s", current)

        except KeyboardInterrupt:
            logger.info("Stopping due to keyboard interrupt")

        finally:
            if self._pwm:
                self._pwm.stop()
                del self._pwm

            GPIO.cleanup()


def _configure_logging() -> None:
    """Configure the package-wide logging settings.

    The default configuration writes INFO+ messages to stderr using a simple
    timestamped format.  When running under systemd the output will go into the
    journal automatically.  Consumers can override the level with the
    SOVA_RELAY_LOG_LEVEL environment variable if desired.
    """
    level = logging.getLevelName(
        os.getenv("SOVA_RELAY_LOG_LEVEL", "INFO")
    )
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def main() -> None:
    """Entry point when running as a script or module."""
    _configure_logging()
    adapter = PWMRelayAdapter(physical_pin=18, virtual_pin=17)
    adapter.run()


if __name__ == "__main__":
    main()