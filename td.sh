#!/bin/bash


FILE=8545240_wl_24.png

URL=http://tidesandcurrents.noaa.gov/ports/plots/


while true

do

		# we have to rm first, otherwise the file might not get removed if loop was not completed on previous pass.
		# -f tests for existence of file

	if [ -f $FILE ]

		then rm $FILE
		
		fi


	wget $URL$FILE


		# fbi is a utility to display an image with the framebuffer in a text terminal without using X windows
		# -t 360 is the time to display each image (it can do slidshows of multiple images)
		# -1 indicates how many times to loop through the slidshow.  we want just once around for our one image

	fbi -noverbose -t 360 -1 $FILE


		# $? contains the exit status of the last command which was executed
		# -ne is a 'not equal' comparison
		# in this case $? refers to the return status of fbi, if we exited fbi via interupt then we want to stop the loop.

        if [ $? -ne 0 ]

	        then exit

		fi
done
