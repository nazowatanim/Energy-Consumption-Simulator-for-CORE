import psutil
#from  energy import process
import json
import os
import pandas as pd
import math
import threading

def testing_parameters():
    net = psutil.net_io_counters(pernic=True)#retrieves network info like ip,packet,rx,tx,mac etc
    interface='lo'
    a=obj=net.get(interface)
    p=obj.bytes_recv
    q=obj.bytes_sent
    t=p+q
    #print (t)
    l = []
    j = []
    #p= []
    #RX/TX parameter
    for k, v in net.items():
    	x1={"bytes_recv":v.bytes_recv,"bytes_sent":v.bytes_sent}    	
    	y1=json.dumps(x1)
    	l.append(y1)
    output_lines = [s.split() for s in os.popen("ps aux").read().splitlines()]
    df=pd.DataFrame(output_lines)
    df1= (df.iloc[1:,2])#starts from row 1 and take only CPU column
    df2= (df.iloc[1:,3])#starts from row 1 and take only RAM column
    output_lines2=[s.split() for s in os.popen("iostat -x | grep sda").read().splitlines()]
    df_disc=pd.DataFrame(output_lines2)
   # return net,l,j,t,output_lines,df,df_disc
    df3=(df_disc.iloc[0:,3])#take 'write to disc' parameter column only
    df4=(df_disc.iloc[0:,4])
    #print(l)
    sum_cpu=0
    sum_ram=0
    sum_sda_write=0
    sum_sda_read=0
    for i in df1:
        i=float(i)
        sum_cpu=sum_cpu+i
    #print(sum_cpu)
    for i in df2:
        i=float(i)
        sum_ram=sum_ram+i
    #print(sum_write_to_disc)
    for i in df3:
        i=float(i)
        sum_sda_write=sum_sda_write+i
    #print(sum_read_from_disc)
    for i in df4:
        i=float(i)
        sum_sda_read=sum_sda_read+i

    #print(l)
    p= []
    for k, v in net.items():
        x3=(v.bytes_recv)#+v.bytes_sent)
        p.append(x3)
    total=math.fsum(p)
    print ('recv',p)
    q= []
    for k, v in net.items():
        x4=(v.bytes_sent)#+v.bytes_sent)
        q.append(x4)
    total1=math.fsum(q)
    print(q)
    without_loop={"bytes_recv_sent_without_loop":total-t} 
    without_loop2={"bytes_recv_sent_without_loop":total1-t} 
    y2=json.dumps(without_loop) 
    #-------------test parameters----------
    #print(l) #with loop
    #print(y2)
    #print('{"cpu_usage:"',sum_cpu,'}')
    #print('{"ram_usage:"',sum_ram,'}')
    #print('{"disc_write":',sum_sda_write,'}')
    #print('{"disc_read":',sum_sda_read,'}')
    #print(sum_sda_read)
    print(without_loop)
    print(without_loop2)
    threading.Timer(1.0,testing_parameters).start()
testing_parameters()