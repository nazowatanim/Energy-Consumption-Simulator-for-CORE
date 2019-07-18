#!/usr/bin/python
from data_aggregator import * 
from script import *
from tinydb import TinyDB, Query
import ConfigParser
import subprocess
import os,sys
import json
import   threading
db = TinyDB('db.json')
total_consumption_all=0
def process_parameter():
	'''processing data as configuration,calls run_shellscript.py to run script at different battery level'''
	'''process parameters with config.ini file parameters, as example: for rx 1000 byte consumes x% of battery.calculation:(recv*X)/1000'''
	try:
		#get aggregated parameters
		without_loop_rx,without_loop_tx,sum_cpu,sum_ram,sum_disk_read,sum_disk_write=aggregator()
		config = ConfigParser.ConfigParser()
		config.read('config.ini')
		#read all configuration
		recvd_byte = config.get('rx_tx', 'recvd')
		sent_byte = config.get('rx_tx', 'sent')
		cpu_percentage = config.get('cpu_ram', 'cpu')
		ram_percentage = config.get('cpu_ram', 'ram')
		disk_read= config.get('disk_rd_wrt', 'disk_rd')
		disk_write = config.get('disk_rd_wrt', 'disk_wrt')
		run_history = config.get('activate_history', 'activate')
		run_history=int(run_history)
		#process parameters and calculation
		consumption_byte_rx=abs(without_loop_rx*float(recvd_byte))/1000
		consumption_byte_tx=abs(without_loop_tx*float(sent_byte))/1000
		cpu_consumption=(sum_cpu*float(cpu_percentage))/1
		ram_consumption=(sum_ram*float(ram_percentage))/1
		disk_read_consumption=(sum_disk_read*float(disk_read))/1000
		disk_write_consumption=(sum_disk_write*float(disk_write))/1000
		disk_consumption=(disk_read_consumption+disk_write_consumption)*1000 #convert kbit to byte for disk read/write
		#printing individualconsumption in json
		consumption_json={'consumption_by_rx':consumption_byte_rx,'consumption_by_tx':consumption_byte_tx,'consumption_by_cpu':cpu_consumption,'consumption_by_ram':ram_consumption,'consumption_by_diskrd':disk_read_consumption*1000,'consumption_by_diskwrt':disk_write_consumption*1000}    
		consumption_dump=json.dumps(consumption_json)
		'''get total consumption adding all parameters'''
		global total_consumption_all
		total_consumption_all=consumption_byte_rx+consumption_byte_tx+cpu_consumption+ram_consumption+disk_consumption
		total_consumption_json={'total_consumption':total_consumption_all}
		total_consumption=json.dumps(total_consumption_json)
		battery=100-total_consumption_all
		f=open('battery.txt','w+')
		f.write(str(battery)+'\n')
		f.write(str(total_consumption_all))
		#calculation in mA
		#read config_ma
		config.read('config_ma.ini')
		recvd_byte_mA = config.get('rx_tx', 'recvd_mA')
		sent_byte_mA = config.get('rx_tx', 'sent_mA')
		cpu_percentage_mA = config.get('cpu_ram', 'cpu_mA')
		ram_percentage_mA = config.get('cpu_ram', 'ram_mA')
		disk_read_mA= config.get('disk_rd_wrt', 'disk_rd_mA')
		disk_write_mA = config.get('disk_rd_wrt', 'disk_wrt_mA')
		voltage=config.get('battery_specification', 'voltage')
		capacity=config.get('battery_specification', 'capacity')
		#calculate individual consumption in mA
		consumption_byte_recv_mA=abs(without_loop_rx*float(recvd_byte_mA))/1000
		consumption_byte_sent_mA=abs(without_loop_tx*float(sent_byte_mA))/1000
		cpu_consumption_mA=(sum_cpu*float(cpu_percentage_mA))/1
		ram_consumption_mA=(sum_ram*float(ram_percentage_mA))/1
		disk_read_consumption=(sum_disk_read*float(disk_read_mA))/1000
		disk_write_consumption=(sum_disk_write*float(disk_write_mA))/1000
		disk_consumption_mA=(disk_read_consumption+disk_write_consumption)*1000#kb TO BYTES
		#insert usage in db.json
		import datetime
		if run_history==1:
			try:
				present_time=str(datetime.datetime.now())
				dttime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				db.insert({'time':dttime,'total_rx': without_loop_rx,'total_tx':without_loop_tx,'cpu_usage':sum_cpu,'ram_usage':sum_ram,'disk_read_usage':sum_disk_read*1000,'disk_write_usage':sum_disk_write*1000,'consumption':total_consumption_all})
				#print(db.all())			
			except(KeyboardInterrupt,SystemExit):
				print('keyboardinterruption')
		#call script.py to run script at different battery level
		current_battery=battery_level(total_consumption_all)				
		#run process_parameter() every second
		threading.Timer(1.0,process_parameter).start()
		return total_consumption_all
	
	except(KeyboardInterrupt,SystemExit):
			print('keyboardinterruption')

process_parameter()
