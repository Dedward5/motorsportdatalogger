Install Guide

You will need

A Raspberry Pi https://thepihut.com/products/raspberry-pi-3-model-b
A SenseHat https://thepihut.com/products/raspberry-pi-sense-hat-astro-pi
A case like this one http://cpc.farnell.com/camdenboss/cbrpsh-blk/enclosure-for-raspberry-pi-sense/dp/SC13933
A usb flash disk/thumb drive
A noobs card for the OS etc like this https://thepihut.com/products/noobs-preinstalled-sd-card


Hardware and dependency setup

* Build up the Pi and SenseHat
* Run up the noobs card choosing the Raspian build and the other defaults
* Make sure your packages are up to date by running sudo apt-get update
* Install sense hat sudo apt-get install sense-hat
* Now Reboot

More help on sensehat is available here https://www.raspberrypi.org/documentation/hardware/sense-hat/README.md


Download my datalogger software from Github
* Logon to the pi and from terminal run git clone https://github.com/Dedward5/motorsportdatalogger.git



Setup the datalogger software to run on startup
Edit the rc.local file for example
sudo nano /etc/rc.local

Add the line at the end

sudo python3 /motorsportdatalogger/datalogger.py



Calibrating the compass (Magnatometer)
See https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=109064&p=750616#p810193

sudo apt-get install octave
cd
cp /usr/share/librtimulib-utils/RTEllipsoidFit ./ -a
cd RTEllipsoidFit
RTIMULibCal

Follow the on-screen instructions.
Refer to steps 8 to 19 in the original post.
In addition to those steps, you can also do the ellipsoid fit.

When you're done, copy the resulting RTIMULib.ini to /etc/ and remove the local copy in ~/.config/sense_hat/
CODE: SELECT ALL
rm ~/.config/sense_hat/RTIMULib.ini
sudo cp RTIMULib.ini /etc
