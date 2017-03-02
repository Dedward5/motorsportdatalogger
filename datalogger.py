# Racing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards (Dedward5)
#
# Find the project on GitHUb at https://github.com/Dedward5/motorsportdatalogger


####################################### Configuration and  Settings ###############################

import configparser

configparser = configparser.RawConfigParser()   
configparser.read("options.cfg")

pi_camera_installed = configparser.get('video_options', 'pi_camera')
pi_camera_vertical_flip = configparser.get('video_options', 'flip_pi_vertical')
pi_camera_horizontal_flip = configparser.get('video_options', 'flip_pi_horizontal')

print ("Datalogger started")
print ("Configuration settings")
print ("Pi camera option = ",pi_camera_installed) # display the camera option setting on screen as a debug helper
print ("Pi camera vertical flip  = ",pi_camera_vertical_flip) # display the camera option setting on screen as a debug he$
print ("Pi camera horizontal flip  = ",pi_camera_horizontal_flip) # display the camera option setting on screen as a debug he$


FILENAME = ""
WRITE_FREQUENCY = 50

############################################ Libraries ############################################

import sys # revisit to see if needed
import os # used for the shutdown
import time # used for time functions

# Import and setup the camera if camera option set in config file

if pi_camera_installed == "yes":
	from picamera import PiCamera
	camera = PiCamera()
	if pi_camera_vertical_flip == "yes": 
		camera.vflip = True
	if pi_camera_horizontal_flip == "yes":
		camera.hflip = True

from sense_hat import SenseHat # for core sensehat functions
from datetime import datetime # for date and time function

############################################ Functions ############################################

def log_data ():
  output_string = ",".join(str(value) for value in sense_data)
  batch_data.append(output_string)

def file_setup(filename):
  header  =["timestamp",
  "accel_x","accel_y","accel_z",
  "pitch","roll","yaw",
  "mag_x","mag_y","mag_z",
  "gyro_x","gyro_y","gyro_z",
  "temp_h","temp_p","humidity","pressure"]

  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

def get_sense_data(): # Main function to get all the sense data
  sense_data=[]

  sense_data.append(datetime.now())

  acc = sense.get_accelerometer_raw()
  x = acc["x"]
  y = acc["y"]
  z = acc["z"]
  sense_data.extend([x,y,z])

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

  gyro = sense.get_gyroscope_raw()
  gyro_x = gyro["x"]
  gyro_y = gyro["y"]
  gyro_z = gyro["z"]
  sense_data.extend([gyro_x,gyro_y,gyro_z])

  sense_data.append(sense.get_temperature_from_humidity())
  sense_data.append(sense.get_temperature_from_pressure())
  sense_data.append(sense.get_humidity())
  sense_data.append(sense.get_pressure())



  return sense_data

def joystick_push(event): # if stick is pressed toggle logging state by switching "value" 
	global value
	global running
	# global filename
	start = time.time()
	if event.action=='released':
		time.sleep(0.5) #wait half a second to reduce button bounce
		value = (1, 0)[value] 
		if value == 1:
			start_logging() 
		else:
			stop_logging()	
    
	while event.action=='held':
		print("Button is held")
		if time.time() > start + 4:
			shutdown_pi()       
        
def start_logging ():	
	print ("Logging started")
	global filename
	sense.show_letter("L",text_colour=[0, 0, 0], back_colour=[0,255,0])
	filename = "/media/usb/race_data_"+time.strftime("%Y%m%d-%H%M%S")+".csv"
	file_setup(filename)
	if pi_camera_installed == "yes":
		camera.start_recording("/media/usb/race_video_"+time.strftime("%Y%m%d-%H%M%S")+".h264")   # starts the camera recording 

        
def stop_logging ():
	print("Logging stopped, still ready") # prints to the main screen
	sense.show_letter("R",text_colour=[0, 0, 0], back_colour=[255,0,0]) 
	if pi_camera_installed == "yes":
		camera.stop_recording() # stops the camera from recording
  		
def shutdown_pi ():
	print ("Shutting down the Pi") # displays this on the main screen
	sense.show_message("Shutting down the Pi", scroll_speed=0.02, text_colour=[255,255,255], back_colour=[0,0,0]) # show this text on the matrix
	sense.clear()  # blank the LED matrix
	os.system('shutdown now -h') # call the OS command to shutdown	 		
      
################################################# Main Program #####################################

print("Press Ctrl-C to quit")

sense = SenseHat()
batch_data= [] # creates an empty list called batch_data 
sense.clear()  # blank the LED matrix  
sense.show_letter("R",text_colour=[0, 0, 0], back_colour=[255,0,0])  # prints R on the matrix to indicate "Ready"
sense.stick.direction_middle = joystick_push  #call the callback (function) joystick_push if pressed at any time including in a loop
 
value = 0 

running = 1

print("Ready") # prints to the main screen

while running: # Loop around until CRTL-C keyboard interrupt   
 
	# print(".")  prints to the main screen after "Ready" not the postion of the comma
  
	while value: # When we are logging
		sense_data = get_sense_data()
		log_data()
		if len(batch_data) >= WRITE_FREQUENCY:
			print("Writing to file")
			with open(filename,"a") as f:
				for line in batch_data:
					f.write(line + "\n")
				batch_data = []

  
