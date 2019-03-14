import psutil
import json
import os
import threading
from config_1 import recvd_byte,sent_byte,cpu_percentage,ram_percentage,disk_byte
import pandas as pd
import  math

'''test function reads the data of components and convert this t necessary Dataframe for extraction like pandas'''
def test():
    '''read data rx tx from psutil net_io_counters,take only recv and sent byte and subtract loop'''
    net = psutil.net_io_counters(pernic=True)
    interface='lo' 
    a=obj=net.get(interface)
    p=obj.bytes_recv                 #getting the loopback recv byte                    
    q=obj.bytes_sent                 #getting the loopback sent byte
    loopback=p+q                            #add bytes_sent and recv
    #print (t)
    rx_tx = []
    #j = []
    for k, v in net.items():
    	x1={"bytes_recv":v.bytes_recv,"bytes_sent":v.bytes_sent}                 #getting the bytes recv_sent parameter from 'net' 	
    	y1=json.dumps(x1)
    	rx_tx.append(y1)             #append rx_tx for all ethernets
    #print(l)
    '''takes shell input 'ps aux' and extract the cpu ram parameter only'''
    output_lines = [s.split() for s in os.popen("ps aux").read().splitlines()]   #shell input of 'ps aux'
    df=pd.DataFrame(output_lines)   #convert this to datframe
    df1= (df.iloc[1:,2])            #starts from row 1 and take only CPU column
    df2= (df.iloc[1:,3])            #starts from row 1 and take only RAM column
    '''takes shell input 'pidstat -dl' and extract the process usage disk_read_write parameter'''
    output_lines2=[s.split() for s in os.popen("pidstat -dl").read().splitlines()]
    df_disc=pd.DataFrame(output_lines2)
    df3=(df_disc.iloc[3:,3])        #take read_to_disc parameter column only
    df4=(df_disc.iloc[3:,4])        ##take write_to_disc parameter column only     
    return net,rx_tx,loopback,df1,df2,df3,df4

#------------------------####################----------------------------------------
from flask import Flask,request
app=Flask(__name__)
total_consumption=0
def process():
    '''add RX TX bytes nd subtract loopback'''
    net,l,loopback,df1,df2,df3,df4=test()
    rx= []      #recv_byte     
    for k, v in net.items():
        x3=(v.bytes_recv)
        rx.append(x3)
    total_rx=math.fsum(rx)             #add byte_recv of all ethernets
    #print(total_rx)
    tx= []      #sent_byte            
    for k, v in net.items():
        x3=(v.bytes_recv)
        rx.append(x3)
    total_tx=math.fsum(tx)              #add sent_byte of all ethernets
    without_loop_recv=total_rx-loopback #subtract loopback from total recv_bytes
    consumption_byte_recv=abs(without_loop_recv)/recvd_byte
    #print(without_byte_recv)
    without_loop_sent=total_tx-loopback #subtract loopback from total sent_bytes
    consumption_byte_sent=abs(without_loop_sent)/sent_byte 
    #print(consumption_byte_sent)
    '''take the shell command and extract cpu,ram,harddisk parameters'''
    #------gets  read_write parameter of PID and add all
    sum_sda_write=0 
    sum_sda_read=0
    for i in df3:
        i=float(i)
        sum_sda_write=sum_sda_write+i   #add all the write_to_disk for all processes
    #print(sum_sda_write)
    for i in df4:
        i=float(i)
        sum_sda_read=sum_sda_read+i
    #print(sum_sda_read)
    #--------getscpu/ram usage of processes and add all
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
    disk_consumption=((sum_sda_write/disk_byte)+(sum_sda_read/disk_byte))*1000 #convert kbit to bytes
    cpu_consumption=(sum_cpu/cpu_percentage)
    ram_consumption=(sum_ram/ram_percentage)
    #print(disk_consumption)
    #print(sum_sda_write)
    #print(sum_sda_read)
    global total_consumption
    total_consumption_all_parameters=consumption_byte_recv+consumption_byte_sent+cpu_consumption+ram_consumption+disk_consumption
    total_consumption_all={'total_consumption':consumption_byte_recv+consumption_byte_sent+cpu_consumption+ram_consumption+disk_consumption}#to jsonify
    #threading.Timer(1.0,process).start()
    total_consumption=json.dumps(total_consumption_all)
    current_battery_level={'current_battery':100-total_consumption_all_parameters}
    current_battery=json.dumps(current_battery_level)
    return total_consumption,current_battery #total_consumption_all#cpu_consumption,ram_consumption,total_consumption
 #-------------------------######----------------------------------------       
#process()
@app.route('/')
def test_server():
    return 'server is running'
@app.route('/emulate',methods=['GET'])
def battery_emulator():
    total_consumption,current_battery=process()
    #current_battery_level={'current_battry':100-total_consumption_all}
    #current_battery=json.dumps(current_battery_level)
    threading.Timer(1.0,battery_emulator).start()
    return str(total_consumption)+str(current_battery)

#battery_emulator()
'''to test the parameters'''

if __name__ == '__main__':
    app.run(host='0.0.0.0')








'''
       
    sum=0
    for i in p:
    	sum+=i
    total=sum-t
    print ("consumption",abs(total))

    #CPU usage

    output_lines = [s.split() for s in os.popen("ps aux").read().splitlines()]
    #print (output_lines)
    df=pd.DataFrame(output_lines)
    print (df)
    total1=df.sum(axis=1)
    print(total1)
    #print (df.iloc[:,0:2])


'''
#test()