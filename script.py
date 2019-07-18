#!/usr/bin/python
'''this script is responsible to run scripts at battery levels defined in config.ini'''
import threading
import ConfigParser
import os
config = ConfigParser.ConfigParser()
config.read('config.ini')
#read battery level from config.ini
battery_level1=config.get('battery_lev', 'battery_1')
battery_level2=config.get('battery_lev', 'battery_2')
battery_script1=config.get('battery_lev', 'script_1')
battery_script2=config.get('battery_lev', 'script_2')
battery_level3=config.get('battery_lev', 'battery_3')
battery_script3=config.get('battery_lev', 'script_3')
battery_level1=float(battery_level1)
battery_level2=float(battery_level2)
battery_level3=float(battery_level3)
#set some conditional variable
x = 0 
trigger1 = 0
trigger2=0
trigger3=0
def battery_3():
	#run script_3 if battery_level3 condition matches	
	cmd='chmod 777 '+battery_script3#enable permission
	os.system(cmd)
	print('running '+battery_script3+'.....')
	script_run='./'+battery_script3
	p=os.popen(script_run).read()

def battery_2():
	#run script_3 if battery_level3 condition matches
	cmd='chmod 777 '+battery_script2
	os.system(cmd)
	print('running '+battery_script2+'.....')
	script_run='./'+battery_script2
	p=os.popen(script_run).read()


def battery_1():
	##run script_3 if battery_level3 condition matches
	print('script_name '+battery_script1+'......')
	script_run='./'+battery_script1	
	p=os.popen(script_run).read()		
	print(p)

def battery_level(consumption):
	current_battery=100-consumption# get current battery level
	print('current_battery',current_battery)
	try:
		global trigger3
		global trigger2
		global trigger1
		if trigger3 == 0: 
			if current_battery<=battery_level3 and current_battery>battery_level2:
				battery_3()
				trigger3 += 1
		if trigger2 == 0:
			if current_battery<=battery_level2 and current_battery>battery_level1:
				battery_2()
				trigger2 += 1
			#print(trigger)
		if trigger1==0:
			if current_battery<=battery_level1 and current_battery>0:
				battery_1()
				trigger1 += 1
		return current_battery

	except(KeyboardInterrupt,SystemExit):
			print('keyboardinterruption')


#battery_level()
 


