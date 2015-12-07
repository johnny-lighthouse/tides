tides
=====

This is a collection of scripts which automate display of live NOAA water level measurements.

td.sh is a bash script to get the latest .png from NOAA and display it with linux fbi utility.

tides is a debian /etc/init.d script which can be used to start td.sh.  To enable td.sh on boot one needs to run update-rc.d

td.py does the same thing in python but may someday parse raw data, create it's own graphs and perhaps preform some analysis.

NB, By default the Pi blanks it screen after inactivity.  To turn this function off, add to /etc/rc.local:

sh -c 'setterm -blank 0 -powersave off -powerdown 0 < /dev/console > /dev/console 2>&1'
