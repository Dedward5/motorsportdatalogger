# Raceing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards


#### Libraries #####

import sys # revisit to see if needed
import time # revisit to see if needed

from sense_hat import SenseHat # for core sensehat functions
from datetime import datetime # for date and time functions
from evdev import InputDevice, list_devices, ecodes # needed for joystick 

#### Functions ####

def get_sense_data(): # Main function to get all the sense data
  sense_data=[]

  sense_data.append(sense.get_temperature_from_humidity())
  sense_data.append(sense.get_temperature_from_pressure())
  sense_data.append(sense.get_humidity())
  sense_data.append(sense.get_pressure())
  
  o = sense.get_orientation()
  yaw = o["yaw"]
  pitch = o["pitch"]
  roll = o["roll"]
  sense_data.extend([pitch,roll,yaw])

  mag = sense.get_compass_raw()
  mag_x = mag["x"]
  mag_y = mag["y"]
  mag_z = mag["z"]
  sense_data.extend([mag_x,mag_y,mag_z])

  acc = sense.get_accelerometer_raw()
  x = acc["x"]
  y = acc["y"]
  z = acc["z"]
  sense_data.extend([x,y,z])

  gyro = sense.get_gyroscope_raw()
  gyro_x = gyro["x"]
  gyro_y = gyro["y"]
  gyro_z = gyro["z"]
  sense_data.extend([gyro_x,gyro_y,gyro_z])

  sense_data.append(datetime.now())

  return sense_data
  
def run_log(): # funtion to pick up joystick input
  value = 0
  value = (1, 0)[value]  
  try:
    for event in dev.read_loop():
      sense.show_message("Logging", scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,255]) # Show some text on matrix
      if event.type == ecodes.EV_KEY:
          if event.code == ecodes.KEY_ENTER and event.value == 1:
            print("Logging stopped")
  except KeyboardInterrupt:
          sys.exit()
  return value 
  
  
#### Main Program ####

print("Press Ctrl-C to quit")
time.sleep(1)

sense = SenseHat()

sense.clear()  # Blank the LED matrix
sense.show_message("Started", scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,255]) # Show some text on matrix

# Check to see if the sense hat joystick is there and set it up as an input device

found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()

logging = False    
    
# Loop around looking for keyboard and things      
    
value = 0
  
while True:

  print (run_log)
  

    
    
