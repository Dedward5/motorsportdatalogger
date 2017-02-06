#Understanding the data

The file is saved in the mount /media/usb (see the install_guide)

The filename is race_data_YYYYMMDD-HHMMSS.csv where the date/time is the date/time the logging was initialised (joystick pressed)

The file produced has the following headings

temp_h	temp_p	humidity	pressure	pitch	roll	yaw	mag_x	mag_y	mag_z	accel_x	accel_y	accel_z	gyro_x	gyro_y	gyro_z	timestamp

There relate to categories of:
* Environmental
* Magnetometer (Compass)
* Roll Pitch Yaw
* Accelerometers
* Gyros
* Timestamp


##Environmental

temp_h	temp_p	humidity	pressure	

Environmental data may or may not be very significant in motorsport data logging. Temperature may not be precise as the Pi will het up under its own power and also its reading an internal cabin temp in the car as opposed to say true air temp.
Pressure may be of interest as pressure can be used as a proxy measure of altitude, so for Hillclimbs thats "interesting", but it will only be relative over a short period of time due to atmospheric changes in pressure.


##Magnetometer

mag_x mag_y	mag_z	

Direction information may weel be of interest as it could help gauge track position over time. 


##Roll Pitch Yaw

pitch	roll	yaw	

This can indicate some interesting vehicle dynamics
Roll obviously shows the vehicle is rolling (hopefully not upside down) so could show how much the vehicle leans into a corner.
Pitch is how the front/back movement changes e.g. diving under breaking,
Yaw should be an indication of "drift" e..g where the orientation of the vehicle is not straight in the direction of dravel.



##Accelerometers

accel_x	accel_y	accel_z	

These are the most common sensors used in basic dataloggers including the iPhone based apps that you see. They show vehicle acceleration/deceleration (X axis), Cornering forces (Y asis). The Z axis may indicate vertical acceleration/deceleration so possibly and indication fo rate of ascent.

##Gyros

gyro_x	gyro_y	gyro_z	

Right now I have no idea what this might mean!


##Timestam

timestamp

This seems to be a timestamp in MS since the logger program has started. It should provide the X axis on any charts and be used to synchronise the charts with times provided by official time keeping. Currently its not starting at 0 for the loggs as I think its set at program start up (that needs changing)

