#retrieve and display graph of current tide state.

import subprocess

while True:

     try:

          subprocess.call(["wget", "http://tidesandcurrents.noaa.gov/ports/plots/8545240_wl_24.png"])

          subprocess.call(["fbi", "-noverbose", "-t", "360", "-1", "8545240_wl_24.png"])

          subprocess.call(["rm", "8545240_wl_24.png"])


     except KeyboardInterrupt:

          from sys import exit

          exit()

