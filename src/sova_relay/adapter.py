"""Module containing the PWM relay adapter logic."""

import time

import RPi.GPIO as GPIO


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
            while True:
                current = GPIO.input(self.virtual_pin)
                if current == self._last_value:
                    continue
                if current == GPIO.HIGH:
                    self._pwm.ChangeDutyCycle(10.0)
                else:
                    self._pwm.ChangeDutyCycle(0.0)
                self._last_value = current
                print(f"Current relay value: {current}")
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self._pwm.stop()
            GPIO.cleanup()


def main() -> None:
    """Entry point when running as a script or module."""
    adapter = PWMRelayAdapter(physical_pin=18, virtual_pin=17)
    adapter.run()


if __name__ == "__main__":
    main()