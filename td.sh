while true;

do

	if [ -f 8545240_wl_24.png ];

	then rm 8545240_wl_24.png;
		
	fi

	wget http://tidesandcurrents.noaa.gov/ports/plots/8545240_wl_24.png

 	if [ $? -ne 0 ]

	then exit

	else fbi -noverbose -t 360 -1 8545240_wl_24.png

        fi

        if [ $? -ne 0 ]

        then exit

	fi
done
