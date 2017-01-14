# Raceing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards


#### Libraries #####

import sys # revisit to see if needed
import time # revisit to see if needed

from sense_hat import SenseHat # for core sensehat functions
from datetime import datetime # for date and time functions

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

def joystick_push(event):
    global value
    if event.action=='pressed':
      value = (1, 0)[value]  
    print(event)
    print(value)
    
#### Main Program ####

print("Press Ctrl-C to quit")

time.sleep(1)

sense = SenseHat()

sense.clear()  # Blank the LED matrix
sense.show_message("Started", scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,255]) # Show some text on matrix
      
# Loop around looking for keyboard and things      
    
value = 0

sense.stick.direction_up = joystick_push

while True:
  print("Waiting.....")
  while value:
    print("logging")
     


