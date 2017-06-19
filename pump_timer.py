#!/usr/bin/env python

import sdnotify
import pigpio
import time

WDOG_INTERVAL=15

# Specify rest time and pump duration, both in seconds
REST_TIME = 300
PUMP_DURATION = 20

# This is the broadcom pin identifier
PUMP_PIN = 22

def turn_on_pump():
    global pi
    print("Turning on")
    pi.write(PUMP_PIN, 1)
    pass

def turn_off_pump():
    global pi
    print("Turning off")
    pi.write(PUMP_PIN, 0)
    pass

def configure_gpio():
    pi = pigpio.pi()
    pi.set_mode(PUMP_PIN, pigpio.OUTPUT)
    return pi

def sleep(sleep_time):
    for intervals in range(int(sleep_time)/WDOG_INTERVAL):
        time.sleep(WDOG_INTERVAL)
        n.notify("WATCHDOG=1")
    return

if __name__ == "__main__":

    pi = configure_gpio()

    # We are a service, so set up notifications
    n = sdnotify.SystemdNotifier()
    n.notify("READY=1")

    while True:
        turn_on_pump()
        sleep(PUMP_DURATION)
        turn_off_pump()
        sleep(REST_TIME)
