while true;

	do

		if [ -f 8545240_wl_24.png ];

			then rm 8545240_wl_24.png;
		
			fi

		wget http://tidesandcurrents.noaa.gov/ports/plots/8545240_wl_24.png

		fbi -noverbose -t 360 -1 8545240_wl_24.png

		done
