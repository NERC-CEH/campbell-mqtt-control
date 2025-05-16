

MQTT 
====

General overview of MQTT interaction with the Campbell Logger including connection to the public test instance at Mosquitto

Mosquitto test instance
-----------------------

https://test.mosquitto.org/

mosquitto_sub

Download the tarball

sudo apt install cmake libssl-dev libcjson-dev
make; sudo make install
sudo /sbin/ldconfig

https://mosquitto.org/man/mosquitto_sub-1.html

Running in docker 
-----------------

https://hub.docker.com/_/eclipse-mosquitto/


`docker run -it -p 1883:1883 -v "$PWD/mosquitto:/mosquitto/config" eclipse-mosquitto`

OR

https://docs.docker.com/compose/install/standalone/

then in the project root

`docker-compose up` 




