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
        
        
        output_rx_wmn=[s.split() for s in os.popen("iw dev wlan0 station dump | grep 'rx bytes'").read().splitlines()]
        df1=pd.DataFrame(output_rx_wmn)
        df_rx= (df1.iloc[0:,2]) 
        rx=[]
        for i in df_rx:
            i=float(i)
            sum=rx.append(i)
        total_rx=math.fsum(rx)
        output_tx_wmn=[s.split() for s in os.popen("iw dev wlan0 station dump | grep 'tx bytes'").read().splitlines()]
        df2=pd.DataFrame(output_tx_wmn)
        df_tx= (df2.iloc[0:,2]) 
        tx=[]
        for i in df_tx:
            i=float(i)
            sum=tx.append(i)
        total_tx=math.fsum(tx)

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
        return total_rx, total_tx,sum_cpu,sum_ram,sum_disk_read,sum_disk_write
    except(KeyboardInterrupt,SystemExit):
            print('keyboardinterruption')



#aggregator()
