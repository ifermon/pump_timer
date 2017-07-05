#!/usr/bin/env python

import sdnotify
import pigpio
import time
import sys
import argparse

WDOG_INTERVAL=15

# Specify rest time and pump duration, both in seconds
REST_TIME = 300
PUMP_DURATION = 15

# This is the broadcom pin identifier
PUMP_PIN = 22

def log(msg):
    print(msg)
    sys.stdout.flush()
    return

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-run", action="store_true", help="Run pump manually")
    return parser.parse_args()

def turn_on_pump():
    global pi
    log("Turning on")
    pi.write(PUMP_PIN, 1)
    return

def turn_off_pump():
    global pi
    log("Turning off")
    pi.write(PUMP_PIN, 0)
    return

def configure_gpio():
    pi = pigpio.pi()
    pi.set_mode(PUMP_PIN, pigpio.OUTPUT)
    return pi

def sleep(sleep_time):
    log("Sleeping for {} seconds".format(sleep_time))
    for intervals in range(int(sleep_time)/WDOG_INTERVAL):
        time.sleep(WDOG_INTERVAL)
        if n:
            n.notify("WATCHDOG=1")
    return

if __name__ == "__main__":

    pi = configure_gpio()

    args = parse_command_line()

    if args.run:
        log("Running pump manually")
        turn_on_pump()
        sleep(PUMP_DURATION)
        turn_off_pump()
        sys.exit(0)

    # We are a service, so set up notifications
    n = sdnotify.SystemdNotifier()
    n.notify("READY=1")

    while True:
        turn_on_pump()
        sleep(PUMP_DURATION)
        turn_off_pump()
        sleep(REST_TIME)
