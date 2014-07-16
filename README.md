tides
=====

This is a collection of scripts which automate display of live NOAA water level measurements.

td.sh is a bash script to get the latest .png from NOAA and display it with linux fbi utility.

tides is a debian /etc/init.d script which can be used to start td.sh.  To enable td.sh on boot one needs to run update-rc.d

td.py does the same thing in python but may someday parse raw data, create it's own graphs and perhaps preform some analysis.
