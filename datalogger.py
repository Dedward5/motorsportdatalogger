# Raceing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards

#### Loggin Settings #######

FILENAME = ""
WRITE_FREQUENCY = 50

#### Libraries #####

import sys # revisit to see if needed
import time # revisit to see if needed

from sense_hat import SenseHat # for core sensehat functions
from datetime import datetime # for date and time function

#### Functions ####

def log_data ():
  output_string = ",".join(str(value) for value in sense_data)
  batch_data.append(output_string)

def file_setup(filename):
  header  =["temp_h","temp_p","humidity","pressure",
  "pitch","roll","yaw",
  "mag_x","mag_y","mag_z",
  "accel_x","accel_y","accel_z",
  "gyro_x","gyro_y","gyro_z",
  "timestamp"]

  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

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

def joystick_push(event):# if stick is pressed toggle logging state by switching "value" 
    global value
    global running
    global filename
    start = time.time()
    
    if event.action=='released':
      value = (1, 0)[value]  
    print(event)
    print(value)
    if value == 1: # only create and setup the file if we are going to do logging
      filename = "../race_data_"+str(datetime.now())+".csv"
      file_setup(filename)    
    
    while event.action=='held':
      print("Button is Held")
      if time.time() > start + 5:
          print ("shutdown")
          value = 0
          running = 0       
        
        
      
#### Main Program ####

print("Press Ctrl-C to quit")

time.sleep(1)
sense = SenseHat()
batch_data= []

sense.clear()  # Blank the LED matrix
# sense.show_message("Started", scroll_speed=0.05, text_colour=[255,255,255], back_colour=[0,0,0]) # Show some text on matrix
    
# Loop around looking for keyboard and things      
    
value = 0
running = 1

sense.stick.direction_middle = joystick_push

while running:
  print("Running.....")

  sense.show_letter("R",text_colour=[0, 0, 0], back_colour=[255,0,0]) 
  
  while value: # When we are logging
    
    print ("Logging")
    sense.show_letter("L",text_colour=[0, 0, 0], back_colour=[0,255,0])     
    sense_data = get_sense_data()
    log_data()

    if len(batch_data) >= WRITE_FREQUENCY:
      print("Writing to file..")
      with open(filename,"a") as f:
          for line in batch_data:
              f.write(line + "\n")
          batch_data = []

#Once the above while loop ends its time to shutdown
print ("Shutting down the Pi") # Displays this on the main screen

killall python

