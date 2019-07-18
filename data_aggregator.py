#!/usr/bin/python
import psutil
import json
import os
import threading
import pandas as pd
import  math
import pdb

'''aggreagtor() aggregates the parameter from CORE node.It can read six parameters:rx,tx,cpu,ram,disk read write from node'''
def aggregator(): 
    try:
        net = psutil.net_io_counters(pernic=True) #takes the network configuration parameters like ifconfig
        interface='lo' #loopback interface
        take_loopback=obj=net.get(interface)          
        loopback_recv=obj.bytes_recv #extract the loopback recv byte from net_io_counters                  
        loopback_sent=obj.bytes_sent  #extract  the loopback sent byte  from net_io_counters 
    	loop_json_rx={"loopback_rx":loopback_recv}
    	rx_loop_dump=json.dumps(loop_json_rx)#dumping in json
    	loop_json_tx={"loopback_tx":loopback_sent}
    	tx_loop_dump=json.dumps(loop_json_tx)
    	#print (rx_loop_dump)
    	#print (tx_loop_dump)
        
        '''get rx bytes  of all ethernets and sum it '''
        rx_byte= []      #recv_byte     
        for k, v in net.items():
            byte_recv=(v.bytes_recv)
            rx_byte.append(byte_recv) #append all ethernet byte recv parameter in a list
        total_rx=math.fsum(rx_byte) #get total of all recv bytes from the list       
        global without_loop_rx
        without_loop_rx=abs(total_rx-loopback_recv) #subtract loopback from rx-get rx bytes without loopback
        '''dumping in json'''
        rx_json={"total_bytes_rx":total_rx,'rx_without_loopback':without_loop_rx}
        rx_dump=json.dumps(rx_json)
        #print(rx_dump)
        '''get tx byte  of all ethernets and sum it '''
        tx_byte= []      #recv_byte     
        for k, v in net.items():
            byte_sent=(v.bytes_sent)
            tx_byte.append(byte_sent) #append all ethernet byte sent parameter in a list
        total_tx=math.fsum(tx_byte) #get total of all sent bytes from the list      
        global without_loop_tx
        without_loop_tx=abs(total_tx-loopback_sent) #subtract loopback from tx
        '''dumping in json'''
        tx_json={"total_bytes_tx":total_tx,'tx_without_loopback':without_loop_tx}
        tx_dump=json.dumps(tx_json)
        #print(tx_dump)

        '''takes shell input 'ps aux' and extract the cpu ram column'''
        output_lines = [s.split() for s in os.popen("ps aux").read().splitlines()] #shell input of 'ps aux'
        #print('output ps_aux',output_lines)
        df=pd.DataFrame(output_lines)   #convert this to dataframe to extract desired column
        df_cpu= (df.iloc[1:,2])  #starts from row 1 and takes only CPU column
        df_ram= (df.iloc[1:,3])  #starts from row 1 and takes only RAM column
        global sum_cpu
        sum_cpu=0
        global sum_ram
        sum_ram=0
        for i in df_cpu:
            i=float(i)
            sum_cpu=sum_cpu+i #sum of all cpu usage
        for i in df_ram:
             i=float(i)
             sum_ram=sum_ram+i#sum of all ram usage
        cpu_ram_json={'cpu_total_usage':sum_cpu,'ram_total_usage':sum_ram}
        cpu_ram_dump=json.dumps(cpu_ram_json)
        #print(cpu_ram_dump)
        '''takes shell input 'pidstat -dl' and extract the process usage disk_read_write parameter'''
        output_lines2=[s.split() for s in os.popen("pidstat -dl").read().splitlines()]
        df_disc=pd.DataFrame(output_lines2)
        df_read_disc=(df_disc.iloc[3:,4])   #take read_to_disc parameter column only
        df_write_disc=(df_disc.iloc[3:,5])  #take write_to_disc parameter column only 
        global sum_disk_read
        sum_disk_read=0
        global sum_disk_write
        sum_disk_write=0
        for i in df_read_disc:
            i=float(i)
            sum_disk_read=sum_disk_read+i #total usage by adding all bytes of extracted column
        for i in df_write_disc:
            i=float(i)
            sum_disk_write=sum_disk_write+i
        disk_json={'disk_read':sum_disk_read,'disk_write':sum_disk_write}
        disk_dump=json.dumps(disk_json)
        return without_loop_rx,without_loop_tx,sum_cpu,sum_ram,sum_disk_read,sum_disk_write
    except(KeyboardInterrupt,SystemExit):
            print('keyboardinterruption')



#aggregator()
