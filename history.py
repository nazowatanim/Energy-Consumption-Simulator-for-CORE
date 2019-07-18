import threading
from tinydb import TinyDB, Query
#from data_aggregator import*
import datetime
import pandas as pd
#import threading
import ConfigParser
import os
db = TinyDB('db.json')
	#global values_of_cpu


def db_read():
			'''read config.ini with userdefined interval to extract history and then this interval is used to get the list of last usages from db.json'''
			try:
				config = ConfigParser.ConfigParser()
				config.read('config.ini')				
				get_history = config.get('activate_history', 'history')
				all_history=int(get_history)
				
				##get rx avg
				rx_list=(list(list(db))[-all_history:])#get the usage based on interval
				rx_to_dataframe=pd.DataFrame(rx_list)# convert to dataframe
				df_rx= (rx_to_dataframe.iloc[-all_history:]) # extract column from dataframe
				length_rx=len(rx_list)
				values_of_rx=rx_to_dataframe['total_rx'].values[-length_rx:]#extract 'total_tx' from all parameters
				rx=sum(values_of_rx)
				rx_avg=rx/len(values_of_rx)	
				##get tx avg
				tx_list=(list(list(db))[-all_history:])
				tx_to_dataframe=pd.DataFrame(tx_list)
				df_cpu= (tx_to_dataframe.iloc[-all_history:])
				length_tx=len(tx_list)
				values_of_tx=tx_to_dataframe['total_tx'].values[-length_tx:]
				tx=sum(values_of_tx)
				tx_avg=tx/len(values_of_tx)
				##get cpu
				cpu_list=(list(list(db))[-all_history:])
				cpu_to_dataframe=pd.DataFrame(cpu_list)
				df_cpu= (cpu_to_dataframe.iloc[-all_history:])
				length_cpu=len(cpu_list)
				values_of_cpu=cpu_to_dataframe['cpu_usage'].values[-length_cpu:]
				#print('cpu_values',values_of_cpu)
				a=sum(values_of_cpu)
				cpu_avg=a/len(values_of_cpu)	
				last_time_cpu=df_cpu['time'].values[-(all_history-(all_history-1)):]
				start_time_cpu=df_cpu['time'].values[-all_history]
				
				#get ram avg
				ram_list=(list(list(db))[-all_history:])
				ram_to_dataframe=pd.DataFrame(ram_list)
				df_ram= (ram_to_dataframe.iloc[-all_history:])
				length_ram=len(ram_list)
				values_of_ram=ram_to_dataframe['ram_usage'].values[-length_ram:]
				#print('ram_values',values_of_ram)
				ram_sum=sum(values_of_ram)
				ram_avg=ram_sum/len(values_of_ram)	
				##get disk read
				read_list=(list(list(db))[-all_history:])
				read_to_dataframe=pd.DataFrame(read_list)
				df_read= (read_to_dataframe.iloc[-all_history:])
				length_read=len(read_list)
				values_of_read=read_to_dataframe['disk_read_usage'].values[-length_read:]
				read_sum=sum(values_of_read)
				read_avg=read_sum/len(values_of_read)
				##get disk write
				write_list=(list(list(db))[-all_history:])
				write_to_dataframe=pd.DataFrame(write_list)
				df_write= (write_to_dataframe.iloc[-all_history:])
				length_write=len(write_list)
				values_of_write=write_to_dataframe['disk_write_usage'].values[-length_write:]
				write_sum=sum(values_of_write)
				write_avg=write_sum/len(values_of_write)

				'''battery_consumption history'''
				consumption_list=(list(list(db))[-all_history:])
				consumption_to_dataframe=pd.DataFrame(consumption_list)
				df_consumption= (consumption_to_dataframe.iloc[-all_history:])
				#print('df',df_cpu)
				length_consumption=len(consumption_list)
				#print('con_len',length_consumption)
				values_of_consumption=consumption_to_dataframe['consumption'].values[-length_consumption:]
				#print('consumption_values',values_of_consumption)
				consumption_sum=sum(values_of_consumption)
				consumption_avg=consumption_sum/len(values_of_ram)	
				#print('avg_cpu_usage',cpu_avg)
				last_time=df_consumption['time'].values[-(all_history-(all_history-1)):]
				last_time_consumption=df_consumption['time'].values[-(all_history)]
				
				recv=('avg_rx',rx_avg)
				sent=('avg_tx',tx_avg)
				cpu=('avg_cpu',cpu_avg)
				ram=('avg_ram',ram_avg)
				dk1=('avg_disk_read',read_avg)
				dk2=('avg_disk_write',write_avg)
				cons=('avg_consumption',consumption_avg)
				time=('start',start_time_cpu,'end',last_time_cpu)
				#summary_consumption_usage=('summary_of_consumption_usage:',consumption_avg)#start_time_consumption,'end:',last_time_consumption,'avg_consumption_usage:',consumption_avg)
				print(recv)
				print(sent)
				print(cpu)
				print(ram)
				print(dk1)
				print(dk2)
				print(cons)
				print(time)
				#save in summary_history.txt
				f=open('summary_history.txt','w+')
				f.write(str(recv)+'\n')
				f.write(str(sent)+'\n')
				f.write(str(cpu)+'\n')
				f.write(str(ram)+'\n')
				f.write(str(dk1)+'\n')
				f.write(str(dk2)+'\n')
				f.write(str(cons)+'\n')
				f.write(str(time)+'\n')
				threading.Timer(1.0,db_read).start()

			except(KeyboardInterrupt,SystemExit):
				print('keyboardinterruption')	



#db_update()
#db_read()
