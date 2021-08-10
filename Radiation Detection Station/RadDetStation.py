# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:33:51 2021

@author: Peter and Sebastian
"""


import socket
import pathlib
import string
import numpy as np
import pandas as pd
import datetime
import time
import csv
import sys
import os
import zmq

from scipy import interpolate as ip

import commands
import parsing


verString  = '1.0.1'

PUBPORT_NUMBER = 5558
SEND_PERIOD_MSEC = 10000
EXPECTED_BAUD_RATE = 921600
IP_ADDR = '192.168.1.89' # This IP Address depends on the BrainBox used on each unit
PORT = 9001

XIA_SUCCESS = 0 # The routine succeeded

MD_DEBUG = 4
MD_IO_PRI_NORMAL = 0
MD_IO_PRI_HIGH = 1

DETECTOR_ID = 12345
DETECTOR_LOC = 'Lab'


SZ_BUF_RET = 4096
SZ_BUF_RET_SN = 36
SZ_BUF_RET_START_SPECTRUM = 8
SZ_BUF_RET_END_SPECTRUM = 6
SZ_BUF_RET_READ_SPECTRUM = 5+(3*1024)+1
SZ_BUF_RET_READ_RUN_STATS = 34

CLEAR_MCA = 0
RESUME_MCA = 1
RUN_ACTIVE = 0
NUM_BINS_MCA = 1024
CAL_PEAK_1 = 287
CAL_PEAK_2 = 780
ENERGY_FEKA = 6.4
ENERGY_MOKA = 17.48
XTAL_MULT = 1
PATH_RECORD = './data/detector_record.csv'
PATH_LEAK = './data/leakage_report.csv'

COLS_1 = ["DataType", "LoopCounter", "Channel", "RowOK", "ERR_TAKE", "ERR_TEMP",
		   "ERR_SPEC", "ERR_STAT", "Timebase", "Calibration Peak 1", "Calibration Peak 2",
		   "Laser Height", "kV Feedback", "uA Feedback", "Emitter Temperature",
		   "Detector Temperature", "Serial Number", "Detector Timestamp", "Live Time",
		   "Real Time", "Energy Live Time", "Input Counts", "output Counts",
		   "Input Count Rate", "Output Count Rate", "Undershoot", "Overshoot",
		   "TotalSpecSum"]

COLS_2 = ["Health Code", "PICStatus", "DSPBootStatus", "RunState", "DSPBusy",
		  "DSPRunError", "EchoValid"]

DOSE_RATE_THRESHOLD = 200000
LEAK_ENTRY = 'Radiation Leak'

'''
Creates a leak record csv file on the path specified by PATH_LEAK. Function should only be called
if the specified path does not contain said file already.
'''
def create_leak_record():
	
	values = {'time':[], 'Input Count Rate':[], 'Dose Rate':[], 'Entry Type':[]}
	
	file = pd.DataFrame(values)		
	file.set_index('time')
	
	file.to_csv(PATH_LEAK, index=False)
	
	print('The file has been created at ' + PATH_LEAK)
	
	return


'''
Creates a record csv file on the path specified by PATH_RECORD. Function should only be called
if the specified path does not contain said file already.
'''
def create_record_file():
	
	values_1 = {
	         "DataType":[],
			 "LoopCounter":[],
			 "Channel":[],
			 "RowOK":[],
			 "ERR_TAKE":[],
			 "ERR_TEMP":[],
			 "ERR_SPEC":[],
			 "ERR_STAT":[],
			 "Timebase":[],
			 "Calibration Peak 1":[],
			 "Calibration Peak 2":[],
			 "Laser Height":[],
			 "kV Feedback":[],
			 "uA Feedback":[],
			 "Emitter Temperature":[],
			 "Detector Temperature":[],
			 "Serial Number":[],
			 "Detector Timestamp":[],
			 "Live Time":[],
			 "Real Time":[],
			 "Energy Live Time":[],
			 "Input Counts":[],
			 "output Counts":[],
			 "Input Count Rate":[],
			 "Output Count Rate":[],
			 "Undershoot":[],
			 "Overshoot":[],
			 "TotalSpecSum":[]}
	
	values_bins = {}
	
	
	for i in list(range(1024)):
		temp_bins = {'Bin'+str(i):[]}
		values_bins.update(temp_bins)
	
		
	values_2 = {"Health Code":[],
			    "PICStatus":[],
				"DSPBootStatus":[],
				"RunState":[],
				"DSPBusy":[],
				"DSPRunError":[],
				"EchoValid":[]}
	
	values = {}
	values.update(values_1)
	values.update(values_bins)
	values.update(values_2)
	
	file = pd.DataFrame(values)		
	file.set_index('LoopCounter')
	
	file.to_csv(PATH_RECORD, index=False)
	
	print('The file has been created at ' + PATH_RECORD)
	
	return

'''
Interpolate the mass attenuation coefficient for the given energies
using a Spline derived from the mappings found at: 

https://physics.nist.gov/PhysRefData/XrayMassCoef/tab3.html

Params:

energy_arr: array of length len(mca) representing all energy values in the spectrum
element: Flag conveying which element (Oxygen, Carbon, Hydrogen, Nitrogen) the program is
dealing with to correctly interpolate mu values for the corresponding mapping
'''
def get_mass_att_coefs(energy_arr, element):
	
	energies = [0, 0.001, 0.0015, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05 ]
	
	#===============Oxygen===============
	if (element == 'O'):
		mus_O = [4*4590, 4590, 1549, 694.9, 217.1, 93.15, 47.9, 27.7, 11.63, 5.952, 1.836, 0.8651, 0.3779, 0.2585, 0.2132 ]
		Spline = ip.interp1d(energies, mus_O)
		mus = Spline(np.array([energy_arr]))
	
	#===============Carbon===============
	elif (element == 'C'):
		mus_C = [4*2211, 2211, 700.2, 302.6, 90.33, 37.78, 19.12, 10.95, 4.576, 2.373, 0.8071, 0.4420, 0.2562, 0.2076, 0.1871 ]
		Spline = ip.interp1d(energies, mus_C)
		mus = Spline(np.array([energy_arr]))
	
	#===============Hydrogen===============
	elif (element == 'H'):
		mus_H = [4*7.217, 7.217, 2.148, 1.059, 0.5612, 0.4546, 0.4193, 0.4042, 0.3914, 0.3854, 0.3764, 0.3695, 0.3570, 0.3458, 0.3355 ]
		Spline = ip.interp1d(energies, mus_H)
		mus = Spline(np.array([energy_arr]))
	
	#===============Nitrogen===============
	elif (element == 'N'):
		mus_N = [4*3311, 3311, 1083, 476.9, 145.6, 61.66, 31.44, 18.09, 7.562, 3.879, 1.236, 0.6178, 0.3066, 0.2288, 0.1980 ]
		Spline = ip.interp1d(energies, mus_N)
		mus = Spline(np.array([energy_arr]))
	
	return mus
	
'''
Retunrs the slope and intercept for the conversion from bin number
to energy in KeV

Params:

peak_1: Bin number for the FeKa peak
peak 2: Bin number for the MoKa peak
'''
def get_energies(peak_1, peak_2):
	
	slope = (ENERGY_MOKA - ENERGY_FEKA)/(peak_2 - peak_1)
	intercept = ENERGY_MOKA - (slope * peak_2)
	
	return slope, intercept
	
'''
For a given detector measurement, the spectrum recorded and the Input Count rate
are used to calculate the dose rate using an ICRU Sphere model.

Params:

icr: Input Count rate in counts per second
mca: array containing spectrum measured by the detector
'''
def parse_to_dose(icr, mca):
	
	
	slope, intercept = get_energies(CAL_PEAK_1, CAL_PEAK_2)
	
	dose = 0
	d = 1
	area_mm2 = 51
	area_cm2 = area_mm2/100
	
	#Density composition of the ICRU sphere model in g/cm^3
	density_O = 0.762
	density_C = 0.111
	density_H = 0.101
	density_N = 0.026
	
	xBins = np.arange(0, len(mca))
	energies_KeV = (slope * xBins)+intercept
	
	# Ignore unphysical negative energies
	mask = energies_KeV < 0
	energies_KeV[mask] = 0.0
	
	energies_MeV = energies_KeV/1000
	energies_eV = energies_KeV*1000
	fund_charge = 1.602*(10**(-19))
	
	fluxes = mca/area_cm2
	
	
	mass_att_coefs_O = get_mass_att_coefs(energies_MeV, 'O')
	mass_att_coefs_C = get_mass_att_coefs(energies_MeV, 'C')
	mass_att_coefs_H = get_mass_att_coefs(energies_MeV, 'H')
	mass_att_coefs_N = get_mass_att_coefs(energies_MeV, 'N')
	
	exponent_O = (-1) * mass_att_coefs_O * density_O * d
	exponent_C = (-1) * mass_att_coefs_C * density_C * d
	exponent_H = (-1) * mass_att_coefs_H * density_H * d
	exponent_N = (-1) * mass_att_coefs_N * density_N * d
	
	#Calculation of the absorption contribution of each element
	# new_dose(in J/g*s) = fundamental_charge*E(eV)*flux_array*mu_array*exp(-mu*density*d)
	# new_dose(in J/kg*s) = new_dose*1000
	# new_dose(in J/kg*hr == Sv/hr) = new_dose(in J/kg*s)*3600
	# new_dose(in nSv/hr) = new_dose(in Sv/hr)*(10**9)
	new_doses_O = energies_eV*fund_charge*fluxes*mass_att_coefs_O*1000*3600*(10**9)*(1-np.exp(exponent_O))
	new_doses_C = energies_eV*fund_charge*fluxes*mass_att_coefs_C*1000*3600*(10**9)*(1-np.exp(exponent_C))
	new_doses_H = energies_eV*fund_charge*fluxes*mass_att_coefs_H*1000*3600*(10**9)*(1-np.exp(exponent_H))
	new_doses_N = energies_eV*fund_charge*fluxes*mass_att_coefs_N*1000*3600*(10**9)*(1-np.exp(exponent_N))
	
	dose += np.sum(new_doses_O)
	dose += np.sum(new_doses_C)
	dose += np.sum(new_doses_H)
	dose += np.sum(new_doses_N)
	
	return dose

'''
Returns list of column labels for the detector record csv file
'''
def get_columns():
	
	columns = COLS_1 + ['Bin{0}'.format( x ) for x in range( NUM_BINS_MCA )] + COLS_2

	return columns

'''
Write a new leak entry when dose rate surpasses the dose rate safety threshold to 
the csv file found at PATH_LEAK.

params:

path: path to the leak record csv file
time: time in string format Day Mon Date Hour:Min:Sec Year
icr: Input Count Rate in counts per second
dose_rate: calculated dose rate from ICRU Sphere model in nSv/hr
entry_type: string indicating the type of report being recorded (e.g. 'radiation leak)
'''
def write_to_leak_file(path, time, icr, dose_rate, entry_type):
	row = [str(time), str(icr), str(dose_rate), entry_type]
	
	# could put try/except around this also
	with open(path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(row)
	
'''
Write a new measurement entry from the detector to the csv file at PATH_RECORD

params:

path: path to csv record file
mca: array containing spectrum measured by detector
statistics: statistics collected from XIA Board in the detector
next_loop_counter: sequential index of the current measurement
'''
def write_to_file(path, mca, statistics, next_loop_counter):
	

	rt = statistics[0]
	lt = statistics[1]
	elt = statistics[2]
	trig = statistics[3]
	evts = statistics[4]
	icr = statistics[5]
	ocr = statistics[6]
	under = statistics[7]
	over = statistics[8]
	numstats = statistics[9]
	
	row = [0, next_loop_counter, 0, 0, 0, 0, 0, 0, 0, CAL_PEAK_1, CAL_PEAK_2, 
		   0, 0, 0, 0, 0, 0, 0, lt, rt, elt,
		   trig, evts, icr, ocr, 
		   under, over, np.array( mca ).sum() ]
	
	row += mca.tolist()
		
	row += [0, 0, 0, 0, 0, 0, 0]
	
	# convert row of numbers to string before writing to file
	row = [str(round(x, 4)) for x in row]
	
	try:
		with open(path, 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(row)
	except Exception as e: 
		print('File error: {0}'.format( e ) )
		raise Exception( 'Terminating -- could not open detector CSV file for writing (is it open in Excel?)')
	
	
	
def start_spectrum_read(socket):
	sz_cmd, wbuf = commands.cmd_start_spectrum()
	socket.send(wbuf)
	wait_time_rx_tx(6,40)
	msg = socket.recv(SZ_BUF_RET_START_SPECTRUM)
	parsed_msg = parsing.parse_start_spectrum_read(msg)
	
	return parsed_msg

def end_spectrum_read(socket):
	sz_cmd, wbuf = commands.cmd_end_spectrum()
	socket.send(wbuf)
	wait_time_rx_tx(6,40)
	msg = socket.recv(SZ_BUF_RET_END_SPECTRUM)
	parsed_msg = parsing.parse_end_spectrum_read(msg)
	
	return parsed_msg

def read_spectrum_run(socket):
	sz_cmd, wbuf = commands.cmd_read_spectrum()
	socket.send(wbuf)
	wait_time_rx_tx(6,3300)
	msg = socket.recv(SZ_BUF_RET_READ_SPECTRUM)
	parsed_msg = parsing.parse_spectrum_read(msg)
		
	return parsed_msg

def read_run_statistics(socket):
	sz_cmd, wbuf = commands.cmd_read_run_statistics()
	socket.send(wbuf)
	wait_time_rx_tx(6,1000)
	msg = socket.recv(SZ_BUF_RET_READ_RUN_STATS)
	parsed_msg = parsing.parse_read_run_statistics(msg)
		
	return parsed_msg


'''
Loop a few times to read radiation measurement from detector
'''
def readLoop(det_socket):

	# Set up the Zero MQ queue 
	# The detector is a 'server' that is publishing 'messages'
	context = zmq.Context()
	socket = context.socket( zmq.PUB )
	try:
		socket.bind("tcp://*:%s" % PUBPORT_NUMBER)
	except Exception as e:
		print( e )
		print( 'If you are getting this exception, the socket is already open.')
		print( 'You should close the app (or command window) or possibly just')
		print( 'wait for it to stop on its own.')
		sys.exit('Stopping script - socket address in use')
	
	print ( "Running ZMQ pub/sub server on port: {0}".format( PUBPORT_NUMBER )) 
		
	
	try:
		file = pd.read_csv(PATH_RECORD)
		
		if (file.empty):
			next_loop_counter = 0
		else:
			next_loop_counter = file['LoopCounter'].iloc[-1] + 1
	except:
		print('Creating record file...')
		create_record_file()
		next_loop_counter = 0


	bOK = True
	#for nLoops in range( 0, 100 ):
	
	doSendMessage = False
	messageToSend = 'Nothing'
	# we set up start time with a time that will be so old that it will trigger a 
	# timeout and thus an update message on the first loop
	startTime = datetime.datetime.today() - datetime.timedelta(days=3)

	# we want this loop to run forever
	nLoops = 0
	while( True ):
		
		nLoops += 1
		
		parsed_msg = start_spectrum_read(det_socket)
		
		if parsed_msg != 'OK':
			print('ERROR WHILE STARTING SPECTRUM READ')
			sys.exit(1)
		
		time.sleep( 1 )
		
		parsed_msg = end_spectrum_read(det_socket)
		
		if parsed_msg != 'OK':
			print('ERROR WHILE ENDING SPECTRUM READ')
			sys.exit(1)
			
		mca = read_spectrum_run(det_socket)
		
		mca = np.array(mca)
			
		statistics = read_run_statistics(det_socket)

		rt = statistics[0]
		lt = statistics[1]
		elt = statistics[2]
		trig = statistics[3]
		evts = statistics[4]
		icr = statistics[5]
		ocr = statistics[6]
		under = statistics[7]
		over = statistics[8]
		numstats = statistics[9]
		
		dose_rate = round(parse_to_dose(icr, mca), 4)
		
		corrected_mca = np.zeros(len(mca))
		
		if (ocr != 0):
			corrected_mca = mca * (icr/ocr)
	
		
		strOut = '\nLoop #{0}'.format( nLoops )
		strOut += '\nRealtime={0:.3f}'.format( rt)
		strOut += '  Livetime={0:.3f}'.format( lt )
		strOut += '  Events={0:.3f}'.format( evts )
		strOut += '  ICR={0:.3f}  OCR={1:.3f}'.format( icr, ocr )
		strOut += '\n#######################'
		strOut += '\nDose rate: ' + str(dose_rate) + ' nSv/hr'
		strOut += '\n#######################'
		
		print( strOut  )

		write_to_file(PATH_RECORD, mca, statistics, next_loop_counter)
		next_loop_counter = next_loop_counter + 1
		
		
		is_leakage = dose_rate > DOSE_RATE_THRESHOLD
		
		messageToSend = "{0},{1},{2:.3f},{3}".format( DETECTOR_ID, DETECTOR_LOC, dose_rate, str(is_leakage) )

		if (is_leakage):
			print('\n##################################################')
			print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			print('\n##################################################')
			
			print('\n#####################WARNING######################')
			
			print('\nRADIATION LEAK DETECTED. Dose rate measurement:')
			print('\n' + str(dose_rate) + ' nSv/hr')
			
			print('\n#####################WARNING######################')
			
			print('\n##################################################')
			print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			print('\n##################################################')
			
			time_of_leakage = str(time.asctime())
			
			try:
				file = pd.read_csv(PATH_LEAK)
				
			except (IOError, OSError) as e:
				print( e )
				print('Creating record file...')
				create_leak_record()
				
			write_to_leak_file(PATH_LEAK, time_of_leakage, round(icr, 4), dose_rate, LEAK_ENTRY)
			
			doSendMessage = True
			#messageToSend = "###!!! Detector {0} at Location {1}: RADIATION LEAK of {2:.3f} nSv/hr !!!###".format( DETECTOR_ID, DETECTOR_LOC,dose_rate )
			

			# TODO: Add warning sound or maybe time the duration of leakage
		else:
			# there was no leak, but send a value every XX seconds just to 
			# indicate that everything is working fine
			
			# get the current time
			currTime = datetime.datetime.now()
			
			# determine the elapsed time since the previous time a message was sent
			elapsed_msec = 1000 * (currTime - startTime).total_seconds()
			
			if elapsed_msec > SEND_PERIOD_MSEC:
				#messageToSend = "Detector {0} at Location {1}: radiation OK, {2:.3f} nSv/hr".format( DETECTOR_ID, DETECTOR_LOC, dose_rate )
				doSendMessage = True
				startTime = datetime.datetime.now()
		
		
		# after each round through the infinite while loop, check to see if we
		# should send a message.  If so, send the message and reset 
		# the 'doSendMessage' flag to False
		if doSendMessage:
			socket.send( messageToSend.encode( 'ascii' ) )
			doSendMessage = False


	return bOK

'''
Opens a socket and connects it to the BrainBox IP Address
to test baud rates
'''
def get_test_connection(ip_addr):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	
	BB_IP_ADDR = ip_addr
        
	s.connect((BB_IP_ADDR, PORT))
	
	return s

'''
Returns for how long should the system wait for every character
sent or received in communication in microseconds
'''
def get_char_delay_usec():
	
	t_per_char_sec = 10.0/EXPECTED_BAUD_RATE
	t_per_char_usec = 1000000 * t_per_char_sec
	return t_per_char_usec

'''
Waiting time for the command and response bytes to be
sent and received by client and detector
'''
def wait_time_rx_tx(num_chars_send, num_chars_response):
	char_delay = get_char_delay_usec() / (100000*XTAL_MULT)
	delay_chars = num_chars_send + num_chars_response
	
	time.sleep(delay_chars*char_delay)
	
'''
Close the Socket used for the connection with the Detector
'''
def close_connection(s):
	s.close()

'''
Sends a request to the detector to get the Serial Number
and receives a response that will be parsed to check if
the program was able to correctly speak to it at baudrate
'''
def check_is_good_baud_rate(socket, baudrate):
	
	sz_cmd, wbuf = commands.cmd_read_serial_number()

	socket.send(wbuf)
	
	
	wait_time_rx_tx(6, 33)
	
	try:
		msg = socket.recv(SZ_BUF_RET_SN)
		print('ABLE TO TALK TO DETECTOR AT BAUDRATE OF ' + str(baudrate))
		parsed_msg = parsing.parse_serial_number_status_baudrate_check(msg)
		
		if parsed_msg == 0:
			return True
		
		else:
			print('FAILED TO RECEIVE STATUS OK FROM DETECTOR')
			print(parsed_msg)
			return False
		
	except Exception as e:
		print(e)
		print('FAILED TO CONNECT TO DETECTOR AT BAUDRATE ' + str(baudrate))
		pass

def connect_cycle_bauds(ip_addr):
	
	BB_IP_ADDR = ip_addr
	
	baud_rates = [ 
			   921600,
			   115200,
			   460800, 
			   230400, 
			   57600]
	
	for i in range(len(baud_rates)):
		test_baud_rate = baud_rates[i]
		
		
		cmd = 'python Setting.py {0} {1}'.format(BB_IP_ADDR, test_baud_rate)
		os.system(cmd)
		
		
		print('#############################################################')
		print('Please wait 5 seconds for the Brainbox to adjust to {} baud...'.format(test_baud_rate))
		print('#############################################################')
		time.sleep(5)
		test_socket = get_test_connection(ip_addr)
		print('###')
		is_good_bRate = check_is_good_baud_rate(test_socket, test_baud_rate)
		print('###')
		close_connection(test_socket)
		
		if is_good_bRate:
			return test_baud_rate
	
	print('COULD NOT COMMUNICATE WITH DETECTOR AT ANY BAUDRATE.')
	print('CHECK CONNECTION.')
	print('Exiting application...')
	sys.exit(1)
	

'''
Sends a request to the detector asking it to change
its baudrate to the given baudrate
'''
def change_detector_baudrate(socket, baudrate):
	
	sz_cmd, wbuf = commands.cmd_change_baudrate(baudrate)

	socket.send(wbuf)
	
	wait_time_rx_tx(6, 33)
	
	msg = socket.recv(SZ_BUF_RET_SN)
	parsed_msg = parsing.parse_change_baudrate(msg)
	return parsed_msg
	
'''
Changes the detector baudrate to the standard value of EXPECTED_BAUD_RATE
'''
def switch_to_correct_baudrate(current_br, ip_addr):
	
	BB_IP_ADDR = ip_addr
	
	temp_socket = get_test_connection(BB_IP_ADDR)
	print('###')
	bOK = change_detector_baudrate(temp_socket, EXPECTED_BAUD_RATE)
	print('###')
	close_connection(temp_socket)
	
	if bOK:
		print('Successfully changed the Detector Baudrate to ' + str(EXPECTED_BAUD_RATE))
	else:
		print('Could not change the detector Baudrate to ' + str(EXPECTED_BAUD_RATE))
	
'''
Opens a socket and connects it to the BrainBox IP Address
at the specified port 9001
'''
def get_connection(ip_addr):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	BB_IP_ADDR = ip_addr
        
	s.connect((BB_IP_ADDR, PORT))
	
	return s

'''
Requests the DPP Board information
'''
def get_board_information(socket):
	
	board_info_labels = ['PIC code variant', 'PIC code major version', 
					  'PIC code minor version', 'DSP code variant', 
					  'DSP code major version', 'DSP code minor version',
					  'DSP clock speed', 'Number of FPGA Configs',
					  'FPGA Index 0 decimation', 'FPGA Index 0 version',
					  'FPGA Index 0 variant']
	
	sz_cmd, wbuf = commands.cmd_get_board_information()
	socket.send(wbuf)
	
	wait_time_rx_tx(6,3100)
	
	msg = socket.recv(SZ_BUF_RET)
	parsed_msg = parsing.parse_get_board_information(msg)
	
	return parsed_msg
	
def main():
	'''
	Radiation Detection Program that constantly measures the level of radiation in the room
	as a dose rate in nSv/hr. The computer needs to be connected to a detector with the power
	on so that said detector can measure counts from its surroundings.
	You can call the program on the terminal like this:	
	
	python CommLib.py
	
	'''
	print( '---------------------------------------------' )
	print( 'Detector Radiation Survey Test Application' )
	print( ' - version {0}'.format( verString ) )
	print( 'Minesense Technologies Ltd.')
	print( 'Copyright (C) 2021')
	print( 'All Rights Reserved.')
	print( '---------------------------------------------' )
	
	'''
	current_baud_rate = connect_cycle_bauds(IP_ADDR)
	
	if current_baud_rate is not EXPECTED_BAUD_RATE:
	
		switch_to_correct_baudrate(current_baud_rate, IP_ADDR)
		
	'''
	
	s = get_connection(IP_ADDR)
	
	buffer = get_board_information(s)
	

	print( 'PIC version: {0} Var {1}.{2}'.format( int(buffer[0]), int(buffer[1]), int(buffer[2]) ) )
	print( 'DSP variant: {0} Var {1}.{2}'.format( int(buffer[3]), int(buffer[4]), int(buffer[5]) ) )
	print( 'DSP clock speed: {0} MHz'.format( int( buffer[6] ) ) )

	readLoop( s )
	
	print( '---------------------------------------------' )
	print( 'Detector Application Finished.  Exiting.' )
	print( '---------------------------------------------' )
	
	
if __name__ == "__main__":
	 '''
	 '''
	 main()
