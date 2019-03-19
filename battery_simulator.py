import psutil
import json
import os
import threading
import pandas as pd
from configuration import * #import parametrs=recvd_byte,sent_byte,cpu_percentage,ram_percentage,disk_read,disk_write,pidno,interval,stop_pid
import  math
import subprocess

'''read data rx tx,cpu,ram,disk read/write of CORE nodes'''
def test(): 
    net = psutil.net_io_counters(pernic=True)
    interface='lo' 
    take_loopback=obj=net.get(interface)
    loopback_recv=obj.bytes_recv    #getting the loopback recv byte                    
    loopback_sent=obj.bytes_sent    #getting the loopback sent byte
    loopback=loopback_recv+loopback_sent                            #add bytes_sent and recv
    #print (t)
    rx_tx = []   
    for k, v in net.items():
    	x1={"bytes_recv":v.bytes_recv,"bytes_sent":v.bytes_sent}  #getting the bytes recv_sent parameter from 'net' 	
    	y1=json.dumps(x1)
    	rx_tx.append(y1)   #append rx_tx for all ethernets
    #print(l)

    '''takes shell input 'ps aux' and extract the cpu ram parameter only'''
    output_lines = [s.split() for s in os.popen("ps aux").read().splitlines()]   #shell input of 'ps aux'
    #print(output_lines[1:])
    df=pd.DataFrame(output_lines)   #convert this to dataframe to extract desired column
    df1= (df.iloc[1:,2])            #starts from row 1 and take only CPU column
    df2= (df.iloc[1:,3])            #starts from row 1 and take only RAM column

    '''takes shell input 'pidstat -dl' and extract the process usage disk_read_write parameter'''
    output_lines2=[s.split() for s in os.popen("pidstat -dl").read().splitlines()]
    df_disc=pd.DataFrame(output_lines2)
    df3=(df_disc.iloc[3:,3])        #take read_to_disc parameter column only
    df4=(df_disc.iloc[3:,4])        #take write_to_disc parameter column only     
    return net,rx_tx,loopback,df1,df2,df3,df4

#test()
def process_parameter(rx,tx,cpu,ram,read,write):
	'''takes the parameter from test() function and process it with configuration file parametres:rx,tx,cpu,ram,diskread/write'''
	net,l,loopback,df1,df2,df3,df4=test()

	'''calculates rx_byte of all ethernets of all CORE nodes and get the toal rx'''
	rx_byte= []      #recv_byte     
	for k, v in net.items():
		x3=(v.bytes_recv)
		rx_byte.append(x3)
	total_rx=math.fsum(rx_byte)  #add rx_byte of all ethernets
	#print(total_rx)
	without_loop_recv=total_rx-loopback
	#print(without_loop_recv)
	consumption_byte_recv=abs(without_loop_recv)/rx
	#print(consumption_byte_recv)

	'''calculates rx_byte of all ethernets of all CORE nodes and get the toal rx'''
	tx_byte= [] 
	for k, v in net.items():
		x3=(v.bytes_sent)
		tx_byte.append(x3)
	total_tx=math.fsum(tx_byte)   #add tx_byte of all ethernets
	#print(total_tx)
	without_loop_sent=total_tx-loopback
	#print(without_loop_sent)
	consumption_byte_sent=abs(without_loop_sent)/tx 
	#print(consumption_byte_sent)

	'''extracts ram_cpu percentage of the all processes'''
	sum_cpu=0
	sum_ram=0
	for i in df1:
		i=float(i)
		sum_cpu=sum_cpu+i
	#print(sum_cpu)
	for i in df2:
		 i=float(i)
		 sum_ram=sum_ram+i
	#print(sum_ram)

	'''extracts disk read/write parameters and convert it from kbit to byte'''	
	sum_disk_read=0
	sum_disk_write=0
	for i in df3:
		i=float(i)
		sum_disk_read=sum_disk_read+i
	#print(sum_disk_read)
	for i in df4:
		i=float(i)
		sum_disk_write=sum_disk_write+i
	#print(sum_disk_write)

	'''consumption by ram,cpu,disk'''
	cpu_consumption=sum_cpu/cpu
	ram_consumption=sum_ram/ram
	disk_read_consumption=sum_disk_read/read
	disk_write_consumption=sum_disk_write/write
	disk_consumption=(disk_read_consumption+disk_write_consumption)*1000 #convert kbit to byte for disk read/write

	'''total consumption'''
	global total_consumption_all
	total_consumption_all=consumption_byte_recv+consumption_byte_sent+cpu_consumption+ram_consumption+disk_consumption
	total_consumption_json={'total_consumption':total_consumption_all}
	global total_consumption
	total_consumption=json.dumps(total_consumption_json)

	#print(total_consumption)

	'''current_battery_level'''
	current_battery_json={'current_battery':100-total_consumption_all}
	global current_battery
	current_battery=json.dumps(current_battery_json)
	#print(current_battery)
	#return total_consumption
	max_pid = [s.split() for s in os.popen("ps -eo pid --sort=-%mem | head -n 2").read().splitlines()]
	df=pd.DataFrame(max_pid)
	df_pid= (df.iloc[1:,0])
	pid_no=0
	for i in df_pid:
		i=int(i)#change string to int
		pid_no=i
	print(pid_no)
	process=psutil.Process(pid_no)
	print(process.name())

	'''kill highest consuming pid if stop_pid is True''' 
	#process_parameter(rx,tx,cpu,ram,read,write)
	if stop_pid==True and total_consumption_all>70:
		kill_pid=subprocess.call(['kill',str(rx)],shell=True)
#process_parameter(recvd_byte,sent_byte,cpu_percentage,ram_percentage,disk_read,disk_write)



'''http request to get the total_consumption,current battery with GET,POST methods'''
from flask import Flask,request
app=Flask(__name__)
@app.route('/')
def test_server():
    return 'server is running'

'''total consumption and current battery level'''
@app.route('/emulate',methods=['GET'])
def battery_emulator():
	process_parameter(recvd_byte,sent_byte,cpu_percentage,ram_percentage,disk_read,disk_write)#calculates total_consumption with configuration specification
	return str(total_consumption)+'   '+str(current_battery)+'    '


'''change a single parameter'''
@app.route('/parameters/<change>/<int:parameter>',methods=['GET'])
def change_parameter(change,parameter):
	new_recv_byte=recvd_byte
	new_sent_byte=sent_byte
	new_cpu=cpu_percentage
	new_ram=ram_percentage
	new_read=disk_read
	new_write=disk_write
	'''only rx/tx is tested'''#need to add other parameters also
	if change=='rx':
		new_recv_byte=parameter
		process_parameter(new_recv_byte,new_sent_byte,new_cpu,new_ram,new_read,new_write)
		return str(total_consumption)+'   '+str(current_battery)+'   '
	if change=='tx':
		new_byte_recv=parameter
		process_parameter(new_recv_byte,new_sent_byte,new_cpu,new_ram,new_read,new_write)
		return str(total_consumption)+'    '+str(current_battery)+'   '
	#process_parameter(new_recv_byte,new_sent_byte,new_cpu,new_ram,new_read,new_write)
	#return str(total_consumption)+'/n'+str(current_battery)+'/n'+'recv'+str(new_recv_byte)+'sent'+str(new_sent_byte)

'''change all parameters with POST method'''
@app.route('/change_all',methods=['POST'])
def change_all_parameters():
	data=request.get_json()
	changed_recv_byte=int(data['recv'])
	changed_sent_byte=int(data['sent'])
	changed_cpu=int(data['cpu'])
	changed_ram=int(data['ram'])
	changed_read=int(data['read'])
	changed_write=int(data['write'])
	process_parameter(changed_recv_byte,changed_sent_byte,changed_cpu,changed_ram,changed_read,changed_write)
	return str(total_consumption)+'    '+str(current_battery)+'   '

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')