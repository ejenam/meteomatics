# meteomatics

## Introduction
This repo makes a request to the Meteomatics data api and returns the temperature, relative humidity and precipitation data withing given periods

## Getting Started
on the terminal run
make install to install the required libraries
make run to run the meteo.py file

use 
python meteo.py "2024-01-15T00:00:00Z--2024-01-18T00:00:00Z:PT1H" "t_2m:C,precip_1h:mm" "52.520551,13.461804" "username" "password"
to run the cli