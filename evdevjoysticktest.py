#!/usr/bin/python HELLO world again

import sys
import time
from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes

print("Press Ctrl-C to quit")
time.sleep(1)

sense = SenseHat()
sense.clear()  # Blank the LED matrix

found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()
try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:  # key down
                print ("keydown")
            if event.value == 0:  # key up
                print ("key upppppppppppp")
except KeyboardInterrupt:
    sys.exit()
