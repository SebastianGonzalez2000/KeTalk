# KeTalk

This repository contains the Main Control Station and the code for each individual Radiation Detection Station of a real-time radiaton detection system using Ketek Radiation Detector hardware. The Radiation Detection Station sends structured binary commands to the XIA chip board inside of the detector and receives binary responses through a socket connection. Commands include reading and writting Digital Signal Processing parameters and collecting spectrum reads. Each station receives radiation spectrum read data from the surroundings measured by the detector every second, that is later parsed into a radiation dose rate in nSv/hr.

Each radiation station communicates to the main control station over the internet to send the parsed dose rate and report any levels of radiation that are considered dangerously high. Both stations periodically record this information on a log file with a time stamp for later reference. 
