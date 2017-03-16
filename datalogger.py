# Racing car data logger for SenseHat equipped Raspberry Pi
# By David Edwards (Dedward5)
#
# Find the project on GitHUb at https://github.com/Dedward5/motorsportdatalogger

from sense_hat import SenseHat # for core sensehat functions #import this first so we can use sense hat display

sense = SenseHat()

sense.show_letter("s",text_colour=[0, 0, 0], back_colour=[255,0,0])  # prints ! on the matrix to indicate "starting up"

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
usb_mic_installed = configparser.get('video_options', 'usb_mic')
do_video_preview = configparser.get('video_options', 'video_preview')


print ("Datalogger started")
print ("Configuration settings")
print ("Pi camera option = ",pi_camera_installed) # display the camera option setting on screen as a debug helper
print ("Pi camera vertical flip  = ",pi_camera_vertical_flip) # display the camera option setting on screen as a debug he$
print ("Pi camera horizontal flip  = ",pi_camera_horizontal_flip) # display the camera option setting on screen as a debug he$
print ("Overlay sense data on video = ",do_overlay_sensedata) # display the config option for video overlay of sense data
print ("Overlay GPS data on video = ",do_overlay_gpsdata) # display the config option for the video overlay of GPS data
print ("GPS installed = ",usb_gps_installed) # display the config option for the USB BPS
print ("USB Microphone = ", usb_mic_installed) 
# print ("Video Preview =", do_video_preview)  

FILENAME = ""
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

	from gps3.agps3threaded import AGPS3mechanism
	agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
	agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
	agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second


# import dependencies for Audio Recording
import subprocess



############################################ Functions ############################################

def file_setup(filename): # setup the CSV headers using the right options for any add-ons like GPS
  header  =["timestamp",
  "accel_x","accel_y","accel_z",
  "pitch","roll","yaw",
  "mag_x","mag_y","mag_z",
  "gyro_x","gyro_y","gyro_z",
  "temp_h","temp_p","humidity","pressure"]
  if usb_gps_installed == "yes":
  	header += "alt","lat","lon","speed"

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
  
  sense_overlay_data = time.strftime("%H:%M:%S %d/%m/%Y") + " Accel " + str(round(y,2)) + " Corner " + str(round(x,2))
 
  # print(sense_overlay_data)  #prints the overlay data on the screen, left to aid debugging if needed

  return sense_data

def get_gps_data (): #function that gets the GPS data
	global gps_overlay_data
	gps_data=[]

	lat = format(agps_thread.data_stream.lat)
	lon = format(agps_thread.data_stream.lon)
	speed = format(agps_thread.data_stream.speed)
	alt = format(agps_thread.data_stream.alt)	
	sense_data.extend([alt,lat,lon,speed])
	gps_overlay_data = " Alt = "  + alt + " KPH = " + speed
	print("GPS Data", gps_overlay_data)  #prints the overlay data on the screen, left to aid debugging if need
  	
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
	global record_process
	sense.show_letter("L",text_colour=[0, 0, 0], back_colour=[0,255,0])
	filename =  "/media/usb/race_data_"+time.strftime("%Y%m%d-%H%M%S")+".csv"
	file_setup(filename)
	if pi_camera_installed == "yes":
		camera.start_preview(alpha=200)
		camera.start_recording("/media/usb/race_video_"+time.strftime("%Y%m%d-%H%M%S")+".h264")   # starts the camera recording 
	if usb_mic_installed == "yes":	
		arecord_cmd = "arecord -D plughw:1 -f cd /media/usb/race_audio"+time.strftime("%Y%m%d-%H%M%S")+".wav"
		record_process = subprocess.Popen("exec " + arecord_cmd,stdout=subprocess.PIPE, shell=True)


def log_data ():
	output_string = ",".join(str(value) for value in sense_data)
	gps_output_string = ",".join(gps_data)
	output_string += gps_output_string
	batch_data.append(output_string)
  
def video_overlay ():
	if do_overlay_sensedata == "yes": 
#		camera.annotate_background = True
		if do_overlay_gpsdata == "yes":
			# print ("Annotate Sense + GPS")     
			camera.annotate_text = sense_overlay_data+gps_overlay_data
		else:	
			# print("Annotate Sense data only, no GPS")
			camera.annotate_text = sense_overlay_data		
	else:
		print("Overlay disabled")
        
def stop_logging ():
	print("Logging stopped, still ready") # prints to the main screen

	sense.show_letter("R",text_colour=[0, 0, 0], back_colour=[255,181,7]) 
	if pi_camera_installed == "yes":
		camera.stop_preview()
		camera.stop_recording() # stops the camera from recording
	if usb_mic_installed =="yes":
		record_process.kill()
		  	
	
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

  
