# Raceing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards


#### Libraries #####

import pygame
from pygame.locals import *
from sense_hat import SenseHat
from datetime import datetime


#### Functions ####

def get_sense_data():
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
  
  

#### Main Program ####

sense = SenseHat()

sense.show_message("Started", scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,255])

sense.clear()

pygame.init()
pygame.display.set_mode((640, 480))

# sense = SenseHat()
# sense.clear()

running = True

x = 0
y = 0
sense.set_pixel(x, y, 255, 255, 255)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            sense.set_pixel(x, y, 0, 0, 0)  # Black 0,0,0 means OFF

            if event.key == K_DOWN and y < 7:
                y = y + 1
            elif event.key == K_UP and y > 0:
                y = y - 1
            elif event.key == K_RIGHT and x < 7:
                x = x + 1
            elif event.key == K_LEFT and x > 0:
                x = x - 1

        sense.set_pixel(x, y, 255, 255, 255)
        if event.type == QUIT:
            running = False
            print("BYE")
