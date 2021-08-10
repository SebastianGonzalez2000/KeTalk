# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:23:40 2021

This script is used to run as a Master that communicates to different
computer/detector units.

Uses Zero MQ to do simple socket-based communications

@author: Peter and Sebastian

"""

import ctypes
from ctypes import wintypes
import pathlib
import string
import numpy as np
import pandas as pd
import time
import csv
import os
import zmq

from scipy import interpolate as ip
#from multiprocessing import Process

verString  = '1.0.0'
PATH_REPORT = '//MTL-FS2/MTL-Engineering/Temp/Sebastian/KeTalk/master_record.csv'

def write_to_file(detector_id, detector_loc, dose_rate):
	
	report_time = time.asctime()
	
	row = [str(detector_id), str(detector_loc), str(dose_rate), report_time]
	
	try:
		with open(PATH_REPORT, 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(row)
	except Exception as e: 
		print('File error: {0}'.format( e ) )
		raise Exception( 'Terminating -- could not open detector CSV file for writing (is it open in Excel?)')
	
	return

def getListOfUnits(fileName):
	'''
	

	Returns
	-------
	None.

	'''
	# Set lines to None, do this to ensure the variable has full function scope.
	lines = None
	try:
		filePath = os.path.join( os.getcwd(), fileName )
		with open(filePath, 'r') as file:
			lines = file.readlines()
	except Exception as e: 
		print( e )
		raise Exception( 'EXIT SCRIPT: Failed while trying to get file that lists the IP addresses of all units' )
	
	
	# go through each line and strip out any leading and trailing spaces
	# Only add a line if it isn't blank
	# Better checking would verify that these are valid IP addresses; for the future.

	linesCleaned = []
	for line in lines:
		lineOut = line.strip()
		if len( lineOut ) > 0:
			linesCleaned.append( lineOut )
		
	return linesCleaned

def getConnections( context, ipList, usePortNum ):
	'''
	Parameters
	----------
	ipList : TYPE
		DESCRIPTION.
	usePortNum : TYPE
		DESCRIPTION.

	Returns
	-------
	None.
	'''
	# create an empty array of sockets, the size of the list of IP addresses
	sockets = [len( ipList )]
	pollers = [len( ipList )]
	
	for nIdx in range( 0, len( ipList ) ):
		ipAddr = ipList[nIdx]
		# Use try/catch exception handling to handle problems, e.g.,
		# the network might be down, the address is invalid, etc.
		# Not really handled here, but for the future
		try:
			# We are the client, we want to subscribe to a report
			sockets[nIdx] = context.socket( zmq.SUB )
			# subscribe to all 'filters', or all messages from this 'channel'
			sockets[nIdx].subscribe( '' )

			strTCP = 'tcp://{0}:{1}'.format( ipAddr, usePortNum )
			sockets[nIdx].connect( strTCP )
			pollers[nIdx] = zmq.Poller()
			pollers[nIdx].register(sockets[nIdx], zmq.POLLIN) # POLLIN for recv, POLLOUT for send
		except Exception as e: 
			print( e )
			raise Exception( 'EXIT SCRIPT: Failed while trying to talk to IP address ' + ipAddr )
		
	return sockets, pollers
	
def main():
	'''
	Radiation Detection Master that monitors units based on IP address.
	
	'''
	print( '---------------------------------------------' )
	print( 'Master Radiation Survey Application' )
	print( ' - version {0}'.format( verString ) )
	print( 'Minesense Technologies Ltd.')
	print( 'Copyright (C) 2021')
	print( 'All Rights Reserved.')
	print( '---------------------------------------------' )

	ipList = getListOfUnits( 'IPList.txt' )

	usePortNum = 5558
	context = zmq.Context()
	
	sockets, pollers = getConnections( context, ipList, usePortNum )
	while( True ):
		for nIdx in range( 0, len( ipList ) ):

			evts = pollers[nIdx].poll(1000) # wait *up to* one second for a message to arrive.
			if len( evts ) == 0:
				print( 'Nothing received' )
				# can do housekeeping in this part here
			else:
				message = sockets[nIdx].recv()
				
				# convert binary ASCII bytes to better string for display
				list_message = message.decode().split(",")
				detector_id = list_message[0]
				detector_loc = list_message[1]
				dose_rate = list_message[2]
				is_leakage = bool(list_message[3])
				
				if is_leakage:
					print("###!!! Detector {0} at Location {1}: RADIATION LEAK of {2} nSv/hr !!!###".format( detector_id, detector_loc, dose_rate ))
					write_to_file(detector_id, detector_loc, dose_rate)
					
				else:
					print("Detector {0} at Location {1}: radiation OK, {2} nSv/hr".format( detector_id, detector_loc, dose_rate ))
				
				#print(  'Received reply: {0}'.format( displayMessage) )
	
	
	print( '---------------------------------------------' )
	print( 'Master Application Finished.  Exiting.' )
	print( '---------------------------------------------' )
	
	
if __name__ == "__main__":
	 '''
	 '''
	 main()
