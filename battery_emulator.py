import psutil
from  energy import process
import json
import os
import pandas as pd
import threading

from flask import Flask,request
app=Flask(__name__)

@app.route('/')
def test_server():
	return 'server is running'
@app.route('/emulate',methods=['GET'])
def battery_emulator():
	total_consumption=process()
	#print(total_consumption,'%')
	return str(total_consumption)#('current battery:',100-total_consumption,'%')
	#threading.Timer(1.0,battery_emulator).start()



#battery_emulator()
'''to test the parameters'''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
