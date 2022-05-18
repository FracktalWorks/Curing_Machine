import RPi.GPIO as GPIO
import time

# map SSR channel to GPIO output
channel_1 = 19
channel_2 = 16
channel_3 = 26
channel_4 = 20
channel_5 = 21

def setup():
    """setup GPIOs"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel_1, GPIO.OUT)
    GPIO.setup(channel_2, GPIO.OUT)
    GPIO.setup(channel_3, GPIO.OUT)
    GPIO.setup(channel_4, GPIO.OUT)
    GPIO.setup(channel_5, GPIO.OUT)


def units_on(one,two,three,four,five):
    """turn units on"""
    print('units on')
    GPIO.output(one, GPIO.HIGH)
    GPIO.output(two, GPIO.HIGH)
    GPIO.output(three, GPIO.HIGH)
    GPIO.output(four, GPIO.HIGH)
    GPIO.output(five, GPIO.HIGH)


def units_off(one,two,three,four,five):
    """turn units off"""
    print('units off')
    GPIO.output(one, GPIO.LOW)
    GPIO.output(two, GPIO.LOW)
    GPIO.output(three, GPIO.LOW)
    GPIO.output(four, GPIO.LOW)
    GPIO.output(five, GPIO.LOW)


if __name__ == '__main__':
    try:
        setup()
        units_on(channel_1,channel_2,channel_3,channel_4,channel_5)
        time.sleep(5)
        units_off(channel_1,channel_2,channel_3,channel_4,channel_5)
        time.sleep(2)
        GPIO.cleanup()
    except KeyboardInterrupt: # exit gracefully
        units_off(channel_1,channel_2,channel_3,channel_4,channel_5)
        GPIO.cleanup()