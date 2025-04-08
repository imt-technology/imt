import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG1 = 23
ECHO1 = 24
TRIG2 = 27
ECHO2 = 22
METAL_DETECTOR_PIN = 17

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO pins for ultrasonic sensor 1
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

# Setup GPIO pins for ultrasonic sensor 2
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

# Setup GPIO pin for metal detector
GPIO.setup(METAL_DETECTOR_PIN, GPIO.IN, pull_down_up=GPIO.PUD_DOWN) # Use pull-down resistor

def measure_distance(trig_pin, echo_pin):
    # Send a short HIGH pulse to the trigger pin
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    pulse_start = time.time()
    pulse_end = time.time()

    # Wait for the echo pin to go HIGH
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    # Wait for the echo pin to go LOW
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance_cm = (pulse_duration * 34300) / 2  # Speed of sound approx. 343 m/s
    return distance_cm
