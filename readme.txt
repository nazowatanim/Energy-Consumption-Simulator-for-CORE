# to install all the python modules run below command:
$ pip install -r requirements.txt
#run energy_simu.py



#in some machines tinydb shows error for Python version.
#it can be eliminated by installing tinydb from github(https://tinydb.readthedocs.io/en/latest/getting-started.html)



#http requests
#for retriving battery and current consumption
curl localhost:5000/emulate
#to change configuration
curl -d'{"rx":0.0001,"tx":0.0002,"cpu":0.00001,"ram":0.00001,"read":0.005, "write":0.03}' -H "Content-Type: application/json" -X POST http://localhost:5000/change_all
#to get consumption history
curl localhost:5000/history/10
