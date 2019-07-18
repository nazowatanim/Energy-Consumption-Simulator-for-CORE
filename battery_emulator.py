#!/usr/bin/python
from data_processor import *
from history import *
from flask import Flask,request,Response
app = Flask(__name__)

#testing server
@app.route('/')
def test_server():
	return 'server is running.....'#+hostname+socket.gethostbyname(hostname)

'''get current battery level,highest usage cpu/ram-PID by GET request'''
@app.route('/emulate',methods=['GET'])
def battery_emulator():
	try:
		#total_consumption_all=process_parameter()
		#calcualte current battery
		#current_battery=100-total_consumption_all
		#if current_battery<0:
			#current_battery=0
			#get high consuming CPU RAM
		f=open('battery.txt')
		lines=f.readlines()
		#return str(lines)
		consumption_json={'total consumption':lines[1],'current_battery':lines[0]}

		max_pid_cpu = [s.split() for s in os.popen("ps -eo pid,user,%cpu --sort=-%cpu | head -n 4").read().splitlines()]#get get highest CPU consuming PID
		max_pid_ram= [s.split() for s in os.popen("ps -eo pid,user,%mem --sort=-%mem | head -n 4").read().splitlines()]#get get highest RAM consuming PID
		 
		cpu_json={'max_cpu_usage_pid':max_pid_cpu}
		ram_json={'max_ram_usage_pid':max_pid_ram} 
		return str(consumption_json)+'\n'+str(cpu_json)+'\n' +str(ram_json)+'\n'
	except requests.exceptions.HTTPError:
			pass

'''change all parameters by POST request'''
@app.route('/change_all',methods=['POST'])
def change_all_parameters():
	data=request.get_json()
	#get parameters from user sent by POST request
	changed_rx_byte=float(data['rx'])
	changed_tx_byte=float(data['tx'])
	changed_cpu=float(data['cpu'])
	changed_ram=float(data['ram'])
	changed_read=float(data['read'])
	changed_write=float(data['write'])
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	#set the parameters got from user in config.ini
	config.set('rx_tx','recvd',str(changed_rx_byte))
	config.set('rx_tx','sent',str(changed_tx_byte))
	config.set('cpu_ram','cpu',str(changed_cpu))
	config.set('cpu_ram','ram',str(changed_ram))
	config.set('disk_rd_wrt','disk_rd',str(changed_read))
	config.set('disk_rd_wrt','disk_wrt',str(changed_write))
	with open('config.ini','w') as configfile:
		config.write(configfile)
	configfile.close()
	return str('changed')

'''get summary of history'''
@app.route('/history/<int:id>',methods=['GET'])
def get_consumption_history(id):
	try:
		config = ConfigParser.ConfigParser()
		config.read('config.ini')
		config.set('activate_history','history',str(id))
		with open('config.ini','w') as configfile:
			config.write(configfile)
		configfile.close()	
		db_read()	
		#time.sleep(1)
		#read history from summary_history.txt
		f=open('summary_history.txt')
		lines=f.readlines()
		return str(lines)#str(lines[0])+str(lines[1])+str(lines[2])+str(lines[3])+str(lines[4])+str(lines[5])+str(lines[6])+str(lines[7])
	except(KeyboardInterrupt,SystemExit):
			print('keyboardinterruption')


