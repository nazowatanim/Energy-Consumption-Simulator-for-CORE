To run the app please install dependencies of requirement.txt with command : sudo pip install -r requirement.txt
run command:python3 battery_simulator

#to get parameter with get method:
request: curl localhost:5000/emulate


#to change the single parameter with get method:
request: curl localhost:5000/emulate

#to change all the parameters
curl -d '{"recv":5, "sent":5,"ram":5, "cpu":5,"read":5, "write":5}' -H "Content-Type: application/json" -X POST http://localhost:5000/change_all



#request from different nodes: curl server_node_ip:5000/given_url