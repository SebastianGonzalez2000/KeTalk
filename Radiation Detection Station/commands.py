# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:46:24 2021

@author: sgonzalez
"""

import sys

ESC = 0x1B

def get_bitwise_xor(in_buffer, num_chars):
	
	v = in_buffer[0]
	
	for i in range (num_chars-1):
		i = i + 1
		v = v^in_buffer[i]
	
	return v

def make_cmd(in_buffer, num_chars):
	
	wbuf = bytearray([ESC]) + bytearray(in_buffer) + bytearray([get_bitwise_xor(in_buffer, num_chars)])
		
	
	return num_chars+2, wbuf

def cmd_start_spectrum():
	
	cmd = 0x00
	n_data_1 = 0x01
	n_data_2 = 0x00
	data_1 = 0x01
	
	ibuf = [cmd, n_data_1, n_data_2, data_1]
	
	sz_pre = 4
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_end_spectrum():
	
	cmd = 0x01
	n_data_1 = 0x00
	n_data_2 = 0x00
	
	ibuf = [cmd, n_data_1, n_data_2]
	
	sz_pre = 3
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_read_spectrum():

        cmd = 0x02
        n_data_1 = 0x05
        n_data_2 = 0x00

        data_1 = 0x00
        data_2 = 0x00
        data_3 = 0x00
        data_4 = 0x04
        data_5 = 0x03

        ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4, data_5]

        sz_pre = 8

        sz_cmd, wbuf = make_cmd(ibuf, sz_pre)

        return sz_cmd, wbuf
	
def cmd_read_run_statistics():

        cmd = 0x06
        n_data_1 = 0x01
        n_data_2 = 0x00

        data_1 = 0x01

        ibuf = [cmd, n_data_1, n_data_2, data_1]

        sz_pre = 4

        sz_cmd, wbuf = make_cmd(ibuf, sz_pre)

        return sz_cmd, wbuf
	
def cmd_read_param_names():
	
	cmd = 0x42
	n_data_1 = 0x01
	n_data_2 = 0x00
	
	data_1 = 0x00
	
	ibuf = [cmd, n_data_1, n_data_2, data_1]
	
	sz_pre = 4
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_read_param_val(param_num):
	
	cmd = 0x45
	
	n_data_1 = 0x04
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = 0x01
	data_3 = param_num & 0xFF
	data_4 = (param_num >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4]
	
	sz_pre = 7
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_apply_settings():
	
	cmd = 0x9F
	
	n_data_1 = 0x00
	n_data_2 = 0x00
	
	ibuf = [cmd, n_data_1, n_data_2]
	
	sz_pre = 3
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_polarity(polarity):
	
	cmd = 0x87
	
	n_data_1 = 0x02
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = polarity
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2]
	
	sz_pre = 5
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_preamp_resettime(preamp_resettime):
	
	cmd = 0x8A
	
	n_data_1 = 0x02
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = preamp_resettime
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2]
	
	sz_pre = 5
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_parset(parset):
	
	cmd = 0x82
	
	n_data_1 = 0x02
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = parset
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2]
	
	sz_pre = 5
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_genset(genset):
	
	cmd = 0x83
	
	n_data_1 = 0x02
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = genset
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2]
	
	sz_pre = 5
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_filter_parameters(paramNum, filter_param):
	
	cmd = 0x8B
	
	n_data_1 = 0x04
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = paramNum
	data_3 = (filter_param) & 0xFF
	data_4 = (filter_param >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4]
	
	sz_pre = 7
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_blfilter(blfilter):
	
	cmd = 0x92
	
	n_data_1 = 0x03
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = (blfilter) & 0xFF
	data_3 = (blfilter >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3]
	
	sz_pre = 6
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_gainTweak(gainTweak):
	
	cmd = 0x91
	
	n_data_1 = 0x03
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = (gainTweak) & 0xFF
	data_3 = (gainTweak >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3]
	
	sz_pre = 6
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_switchedGain(switchedGain):
	
	cmd = 0x9B
	
	n_data_1 = 0x02
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = switchedGain
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2]
	
	sz_pre = 5
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_digital_base_gain(digBaseGain, digBaseGainExp):
	
	cmd = 0x9C
	
	n_data_1 = 0x04
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = (digBaseGain) & 0xFF
	data_3 = (digBaseGain >> 8) & 0xFF
	data_4 = (digBaseGainExp) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4]
	
	sz_pre = 7
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_binwidth(binGranular, binMultiple):
	
	cmd = 0x84
	
	n_data_1 = 0x03
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = binGranular
	data_3 = binMultiple
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3]
	
	sz_pre = 6
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_num_mca_channels(num_mca_channels, firstbin):
	
	cmd = 0x85
	
	n_data_1 = 0x05
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = (num_mca_channels) & 0xFF
	data_3 = (num_mca_channels >> 8) & 0xFF
	data_4 = (firstbin) & 0xFF
	data_5 = (firstbin >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4, data_5]
	
	sz_pre = 8
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_thresholds(threshold, filter_choice):
	
	cmd = 0x86
	
	n_data_1 = 0x04
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = filter_choice
	data_3 = (threshold) & 0xFF
	data_4 = (threshold >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4]
	
	sz_pre = 7
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_write_preset(preset, presetlen):
	
	steps500 = presetlen
	
	cmd = 0x07
	
	n_data_1 = 0x08
	n_data_2 = 0x00
	
	data_1 = 0x00
	data_2 = preset
	data_3 = (steps500) & 0xFF
	data_4 = (steps500 >> 8) & 0xFF
	data_5 = (steps500 >> 16) & 0xFF
	data_6 = (steps500 >> 24) & 0xFF
	data_7 = (steps500 >> 32) & 0xFF
	data_8 = (steps500 >> 40) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8]
	
	sz_pre = 11
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_save_parset(parset):
	
	cmd = 0x8D
	
	n_data_1 = 0x03
	n_data_2 = 0x00
	
	data_1 = parset
	data_2 = 0x55
	data_3 = 0xAA
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3]
	
	sz_pre = 6
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_save_genset(genset):
	
	cmd = 0x8F
	
	n_data_1 = 0x03
	n_data_2 = 0x00
	
	data_1 = genset
	data_2 = 0x55
	data_3 = 0xAA
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3]
	
	sz_pre = 6
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_change_baudrate(baudrate):
	
	save = 0x01
	
	baud_rate_idx = 0
	
	if baudrate == 57600:
		baud_rate_idx = 0
		
	elif baudrate == 115200:
		baud_rate_idx = 1
		
	elif baudrate == 230400:
		baud_rate_idx = 2
		
	elif baudrate == 460800:
		baud_rate_idx = 3
		
	elif baudrate == 921600:
		baud_rate_idx = 4
		
	else:
		print('Attempted to set invalid baudrate ' + str(baudrate))
		sys.exit(1)
	
	cmd = 0xFB
	
	n_data_1 = 0x02
	n_data_2 = 0x00
	
	data_1 = save
	data_2 = baud_rate_idx
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2]
	
	sz_pre = 5
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_get_board_information():
	
	cmd = 0x49
	n_data_1 = 0x00
	n_data_2 = 0x00
	
	ibuf = [cmd, n_data_1, n_data_2]
	
	sz_pre = 3
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf
	

def cmd_write_param_val(param_num, param_val):
	
	cmd = 0x45
	
	n_data_1 = 0x06
	n_data_2 = 0x00
	
	data_1 = 0x01
	data_2 = 0x01 # Number of words to write
	data_3 = param_num & 0xFF
	data_4 = (param_num >> 8) & 0xFF
	data_5 = (param_val) & 0xFF
	data_6 = (param_val >> 8) & 0xFF
	
	ibuf = [cmd, n_data_1, n_data_2, data_1, data_2, data_3, data_4, data_5, data_6]
	
	sz_pre = 9
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

def cmd_read_serial_number():
	
	cmd = 0x48
	n_data_1 = 0x00
	n_data_2 = 0x00
	
	ibuf = [cmd, n_data_1, n_data_2]
	
	sz_pre = 3
	
	sz_cmd, wbuf = make_cmd(ibuf, sz_pre)
	
	return sz_cmd, wbuf

