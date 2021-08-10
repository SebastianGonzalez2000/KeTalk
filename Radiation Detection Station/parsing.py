# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:20:08 2021

@author: sgonzalez
"""

import sys
import matplotlib.pyplot as plt
import numpy as np

IDX_START_SN = 5
IDX_END_SN = 21

IDX_START_STATUS = 4

IDX_START_START_SPECTRUM = 4
IDX_END_START_SPECTRUM = 5

IDX_START_END_SPECTRUM = 4
IDX_END_END_SPECTRUM = 6

IDX_START_SPECTRUM_READ = 5
IDX_END_SPECTRUM_READ = 5 + (1024*3) + 1

IDX_START_PARAM_NAMES = 9

IDX_START_WRITE_PARAM_VALS = 4

def parse_serial_number(sn):
	
	sn = sn.decode()[IDX_START_SN:IDX_END_SN]
	
	return sn

def parse_serial_number_status_baudrate_check(status):
	
	status = status[IDX_START_STATUS]
	
	return status

def parse_apply_settings(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Apply Settings: OK'
	else:
		print('Status: ', status)
		print('ERROR while applying settings...')
		sys.exit()

def parse_write_polarity(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to POLARITY Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing POLARITY value to memory...')
		sys.exit()
		
def parse_write_preamp_resettime(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to RESETINT Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing RESETINT value to memory...')
		sys.exit()
		
def parse_write_parset(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to PARSET Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing PARSET value to memory...')
		sys.exit()
		
def parse_write_genset(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to GENSET Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing GENSET value to memory...')
		sys.exit()
		
def parse_write_filter_parameters(status, param_name):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to ' + param_name + ' Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing' + param_name + ' value to memory...')
		sys.exit()
		
def parse_write_blfilter(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to BLFILTER Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing BLFILTER value to memory...')
		sys.exit()
		
def parse_write_gainTweak(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to GAINTWEAK Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing GAINTWEAK value to memory...')
		sys.exit()
		
def parse_write_switchedGain(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to SWGAIN Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing SWGAIN value to memory...')
		sys.exit()
		
def parse_write_digital_base_gain(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to DGAINBASE Parameter and DGAINBASEEXP Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing DGAINBASE and DGAINBASEEXP values to memory...')
		sys.exit()
		
def parse_write_binwidth(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to BINGRANULAR Parameter and BINMULTIPLE Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing BINGRANULAR and BINMULTIPLE values to memory...')
		sys.exit()
		
def parse_write_num_mca_channels(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to MCALEN Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing MCALEN value to memory...')
		sys.exit()
		
def parse_write_thresholds(status, param_name):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to ' + param_name + ' Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing' + param_name + ' value to memory...')
		sys.exit()

def parse_write_preset(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Writing to PRESET Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while writing PRESET value to memory...')
		sys.exit()	
		
def parse_save_parset(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Saving PARSET Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while saving PARSET value to memory...')
		sys.exit()
		
def parse_save_genset(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'Saving GENSET Parameter: OK'
	else:
		print('Status: ', status)
		print('ERROR while saving GENSET value to memory...')
		sys.exit()
		
def parse_change_baudrate(status):
	
	if status[IDX_START_STATUS] == 0:
		return True
	else:
		return False
	
def parse_get_board_information(board_info):
	
	pic_code_variant = board_info[5]
	pic_code_major_version = board_info[6]
	pic_code_minor_version = board_info[7]
	
	dsp_code_variant = board_info[8]
	dsp_code_major_version = board_info[9]
	dsp_code_minor_version = board_info[10]
	dsp_clock_speed = board_info[11]
	
	nFiPPI = board_info[13]
	
	FiPPI_decimation = board_info[22]
	FiPPI_version = board_info[23]
	FiPPI_variant = board_info[24]
	
	return [pic_code_variant, pic_code_major_version, pic_code_minor_version,
		 dsp_code_variant, dsp_code_major_version, dsp_code_minor_version,
		 dsp_clock_speed, nFiPPI, FiPPI_decimation, FiPPI_version, FiPPI_variant]


def parse_write_param_val(status):
	status = status[IDX_START_WRITE_PARAM_VALS]
	
	if status == 0:
		return 'OK'
	else:
		print('Status: ', status)
		print('ERROR while writing parameter value to memory...')
		sys.exit()

def parse_start_spectrum_read(status):
	
	status = status[IDX_START_START_SPECTRUM]
	
	if status == 0:
		return 'OK'
	else:
		print('ERROR while starting run')
		sys.exit()

def parse_end_spectrum_read(status):
	
	status = status[IDX_START_END_SPECTRUM]
	
	if status == 0:
		return 'OK'
	else:
		print('ERROR while starting run')
		sys.exit()

def parse_spectrum_read(spectrum):
	
	spectrum_arr = [0] * 1024
	
	spectrum = spectrum[IDX_START_SPECTRUM_READ:IDX_END_SPECTRUM_READ]
	
	idx = 0
	
	for i in list(range(0, 3072, 3)):
		
		low_byte = spectrum[i]
		mid_byte = spectrum[i+1]
		high_byte = spectrum[i+2]
		
		count_in_decimal = (low_byte) + ((16**2)*mid_byte) + ((16**4)*high_byte)
		
		spectrum_arr[idx] = count_in_decimal
		idx = idx + 1
	
	return spectrum_arr

def parse_read_run_statistics(stats):

	livetime = stats[5] \
			+ ((16**2)*stats[6]) \
			+ ((16**4)*stats[7]) \
			+ ((16**6)*stats[8]) \
			+ ((16**8)*stats[9]) \
			+ ((16**10)*stats[10])
			
	realtime = stats[11] \
			+ ((16**2)*stats[12]) \
			+ ((16**4)*stats[13]) \
			+ ((16**6)*stats[14]) \
			+ ((16**8)*stats[15]) \
			+ ((16**10)*stats[16]) 
			
	livetime = 500*livetime/(10**9)
	
	realtime = 500*realtime/(10**9)
			
	fastpeaks = stats[17] \
			+ ((16**2)*stats[18]) \
			+ ((16**4)*stats[19]) \
			+ ((16**6)*stats[20]) \
				
	output_events = stats[21] \
			+ ((16**2)*stats[22]) \
			+ ((16**4)*stats[23]) \
			+ ((16**6)*stats[24]) \
				
	underflows = stats[25] \
			+ ((16**2)*stats[26]) \
			+ ((16**4)*stats[27]) \
			+ ((16**6)*stats[28]) \
				
	overflows = stats[29] \
			+ ((16**2)*stats[30]) \
			+ ((16**4)*stats[31]) \
			+ ((16**6)*stats[32]) \
				
				
	icr = fastpeaks/livetime
	
	ocr = output_events / realtime
	
	energy_livetime = 0
	
	if icr != 0:
	
		energy_livetime = realtime * (ocr/icr)
	
	numstats = 0 #TODO: What is numstats?
	
	parsed_stats = [realtime, livetime, energy_livetime, fastpeaks, output_events, 
				 icr, ocr, underflows, overflows, numstats]
	
	return parsed_stats

def parse_param_val(val):
	
	val = val[5] + ((16**2)*val[6])
	
	return val

def parse_param_names(params):
	
	num_params = params[5] + ((16**2)*params[6])
	
	str_len = params[7] + ((16**2)*params[8])
	
	param_chars = params[IDX_START_PARAM_NAMES: IDX_START_PARAM_NAMES + str_len]
	
	param_names = [''] * num_params
	
	idx = 0
	
	for i in range(str_len):
		
		char = param_chars[i]
		
		if char == 0:
		
			idx = idx + 1
			continue
		
		else:
			param_names[idx] = param_names[idx] + chr(char)
	
	return param_names
