# Racing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards (Dedward5)
#
# Find the project on GitHUb at https://github.com/Dedward5/motorsportdatalogger

from sense_hat import SenseHat # for core sensehat functions #import this first so we can use sense hat display

sense.show_letter("!",text_colour=[0, 0, 0], back_colour=[255,0,0])  # prints ! on the matrix to indicate "starting up"

####################################### Configuration and  Settings ###############################

import configparser

configparser = configparser.RawConfigParser()   
configparser.read("options.cfg")

pi_camera_installed = configparser.get('video_options', 'pi_camera')
pi_camera_vertical_flip = configparser.get('video_options', 'flip_pi_vertical')
pi_camera_horizontal_flip = configparser.get('video_options', 'flip_pi_horizontal')
do_overlay_sensedata = configparser.get('video_options', 'overlay_sense_data')
do_overlay_gpsdata = configparser.get('video_options', 'overlay_gps_data')
chosen_path =  configparser.get('general_options', 'file_path')
usb_gps_installed = configparser.get('gps_options', 'usb_gps')


print ("Datalogger started")
print ("Configuration settings")
print ("Pi camera option = ",pi_camera_installed) # display the camera option setting on screen as a debug helper
print ("Pi camera vertical flip  = ",pi_camera_vertical_flip) # display the camera option setting on screen as a debug he$
print ("Pi camera horizontal flip  = ",pi_camera_horizontal_flip) # display the camera option setting on screen as a debug he$
print ("Overlay sense data on video = ",do_overlay_sensedata) # display the config option for video overlay of sense data
print ("Overlay GPS data on video = ",do_overlay_gpsdata) # display the config option for the video overlay of GPS data
print (" GPS installed = ",usb_gps_installed) # display the config option for the USB BPS

# FILENAME = ""
WRITE_FREQUENCY = 50

############################################ Libraries ############################################

import sys # revisit to see if needed
import os # used for the shutdown
import time # used for time functions

from datetime import datetime # for date and time function

# Import and setup the camera if camera option set in config file

if pi_camera_installed == "yes":
	from picamera import PiCamera
	camera = PiCamera()
	if pi_camera_vertical_flip == "yes": 
		camera.vflip = True
	if pi_camera_horizontal_flip == "yes":
		camera.hflip = True
		
# Import and setup the GPS if GPS option set in the config file		
if usb_gps_installed == "yes":
	from gps3 import gps3
	gps_socket = gps3.GPSDSocket()
	data_stream = gps3.DataStream()
	gps_socket.connect()
	gps_socket.watch()

############################################ Functions ############################################

def file_setup(filename): # setup the CSV headers using the right options for any add-ons like GPS
  header  =["timestamp",
  "accel_x","accel_y","accel_z",
  "pitch","roll","yaw",
  "mag_x","mag_y","mag_z",
  "gyro_x","gyro_y","gyro_z",
  "temp_h","temp_p","humidity","pressure"]
  if usb_gps_installed == "yes":
  	header.extend[,"alt","lat","lon","speed"]

  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

def get_sense_data(): # Main function to get all the sense data
  global sense_overlay_data
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
  
  sense_overlay_data = time.strftime("%H:%M:%S %d/%m/%Y") + " Acceleration " + str(round(y,2)) + " Cornering " + str(round(x,2))
 
  # print(sense_overlay_data)  #prints the overlay data on the screen, left to aid debugging if needed

  return sense_data

def get_gps_data (): #function that gets the GPS data
	global gps_overlay_data
	gps_data=[]
	
	data_stream.unpack(new_data)
    alt = data_stream.TPV['alt'])
    lat = data_stream.TPV['lat'])
    lon  = data_stream.TPV['lon'])
    speed = data_stream.TPV['speed'])

	sense_data.extend([alt,lat,lon,speed])
	
	gps_overlay_data = " Altitude = " , str(round(alt,2)), " Speed = " , str(round(speed,2))

	print(gps_overlay_data)  #prints the overlay data on the screen, left to aid debugging if need
  	
  	return gps_data
  
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
		sense.show_letter("H",text_colour=[0, 0, 0], back_colour=[255,181,7])  # prints H on the matrix to indicate held
		if time.time() > start + 4:
			shutdown_pi()       
        
def start_logging ():	
	print ("Logging started, press joystick button to stop")
	global filename
	sense.show_letter("L",text_colour=[0, 0, 0], back_colour=[0,255,0])
	filename = chosen_path + "/race_data_"+time.strftime("%Y%m%d-%H%M%S")+".csv"
	file_setup(filename)
	if pi_camera_installed == "yes":
		camera.start_recording(chosen_path + "/race_video_"+time.strftime("%Y%m%d-%H%M%S")+".h264")   # starts the camera recording 

def log_data ():
	output_string = ",".join(str(value) for value in sense_data)
	output_string.append = ",".join(str(value) for value in gps_data)
	batch_data.append(output_string)
  
def video_overlay ():
	if do_overlay_sensedata == "yes": 
		print ("overlay Sense data")
		camera.annotate_background = True
		camera.annotate_text = sense_overlay_data	
		
	if do_overlay_gpsdata == "yes":
		camera.annotate_text = gps_overlay_data
        
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
sense.show_letter("R",text_colour=[0, 0, 0], back_colour=[255,181,7])  # prints R on the matrix to indicate "Ready"

sense.stick.direction_middle = joystick_push  #call the callback (function) joystick_push if pressed at any time including in a loop
 
value = 0 

running = 1

print("Ready, press sensehat jostick to start logging") # prints to the main screen

while running: # Loop around until CRTL-C keyboard interrupt   
 
	# print(".")  prints to the main screen after "Ready" not the postion of the comma
  
	while value: # When we are logging
		sense_data = get_sense_data()
		gps_data = get_gps_data()
		log_data()
		video_overlay()

		if len(batch_data) >= WRITE_FREQUENCY:
			print("Writing to file")
			with open(filename,"a") as f:
				for line in batch_data:
					f.write(line + "\n")
				batch_data = []

  
