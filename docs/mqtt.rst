

MQTT 
====

General overview of MQTT interaction with the Campbell Logger including connection to the public test instance at Mosquitto

`Campbell MQTT documentation <https://help.campbellsci.com/CR300/Content/shared/Communication/mqtt/mqtt-command-control.htm>`_
We can use MQTT to remotely communicate with dataloggers that are in the field - update their settings, their scripts, and potentially even do operating system upgrades and rotate certificates.


Mosquitto test instance
-----------------------

`test.mosquitto.org <https://test.mosquitto.org/>`_ is a publically available MQTT broker (accepts messages and publishes them) that we have been using for testing. It's a service from the Mosquitto open source project and a) has no guarantees of uptime and b) all traffic is publically visible.

In the even that you're seeing unexpected connection failures, try `mosquitto_sub` to check whether it's handling any traffic at all:

`mosquitto_sub <https://mosquitto.org/man/mosquitto_sub-1.html>`_

Download the tarball abd build from source:

.. code:: bash

    sudo apt install cmake libssl-dev libcjson-dev
    make; sudo make install
    sudo /sbin/ldconfig

Listener
--------

`listener.py` is a utility for testing and debugging.

It connects to an MQTT server and listens and prints to `stdout` all the traffic relating to MQTT control of Campbell dataloggers on the `cs/v2` topic. 

`python listener.py -s test.mosquitto.org -c 12345`

Options:

- `-c  / --client` - serial number of the datalogger
- `-s / --server`- MQTT server to connect to 
- `-p / --port` - port on the MQTT server to use. default 1883

  

Running in docker 
-----------------

`Mosquitto docker image <https://hub.docker.com/_/eclipse-mosquitto/>`_ useful for testing MQTT logger control on a local network.


`docker run -it -p 1883:1883 -v "$PWD/mosquitto:/mosquitto/config" eclipse-mosquitto`

We provide a docker `compose.yml` file and basic mosquitto configuration to simplify this. 

`Install docker-compose standalone <https://docs.docker.com/compose/install/standalone/>`_ if needed. (If running in `podman`, this should work with the `podman compose` wrapper too.) 

In the project root, run:

`docker-compose up` 


TODO
----

* Could add info with screenshots on configuring specific models for MQTT connection

