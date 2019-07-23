# Energy-Consumption-Simulator-for-CORE
This project aims to emulate battery of every nodes of CORE on user specification. Data can be retrieved from CORE GUI with REST API.Python Flask RESTful has been used for that.It will be deployed as selectable service in CORE and will be responsible to emulate battery consumption on disaster network.
To run the app please install dependencies of requirement.txt with command : sudo pip install -r requirement.txt
then run energy_simu.py

Conceptual Model
![model](https://user-images.githubusercontent.com/45766557/61692983-00ccca00-ad2f-11e9-9b18-efd9502070cb.jpg)

Application deployment in CORE as a service
![energy_consumption_service](https://user-images.githubusercontent.com/45766557/61693471-e8a97a80-ad2f-11e9-9a46-3d235921aebe.png)


Changing Network Route at different battery level with application
![change route](https://user-images.githubusercontent.com/45766557/61693568-1abadc80-ad30-11e9-9e04-7bccfe7040f4.png)

![chnage route at different](https://user-images.githubusercontent.com/45766557/61693666-46d65d80-ad30-11e9-9eea-460b0f7a0cfa.png)


Emulatng Current Battery and Energy Consumption at different nodes
![current battery](https://user-images.githubusercontent.com/45766557/61693816-8309be00-ad30-11e9-8025-4e7974ccb9e4.png)









