Command-line interface 
======================

We provide a command-line interface to the library. You can use this from your PC to update the settings on a remote Campbell device. We plan to provide a way to do this inside Amazon Web Services without having to install the tool or create certificates.

_Note, this document is speculative as it's not implemented yet!


Quickstart
----------

`pip install -e .` - this will install the CLI 

Authentication
--------------

Create certificates for testing using the AWS console or the `aws` commandline interface.

- `Create AWS IoT client certificates <https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-create.html>`_

Configuration
-------------

The base `topic` for sending messages and the `broker` client library type will use these defaults if not set out in the JSON format config file:

.. code:: bash

    topic: cs/v2
    broker: AWS


.. code:: bash
    
    topic: 'cs/v2'
    broker: 'AWS'
    serial: 12345
    certificate_pem: 'certificate_filename.pem'
    public_key: 'public_filename.key'
    private_key: 'private_filename.key'

Settings
--------

All the settings visible through the "Device Configuration Utility" can be read or changed one by one with the `settings` topic.
*Note: need to infer a canonical list of names for use in the `set` topic, the `Campbell docs <https://help.campbellsci.com/CR300/Content/shared/Communication/mqtt/mqtt-command-control.htm>`_* don't spell them out.

`mqtt-control get [setting]`

Get the value of a specific setting on the logger.

`mqtt-control get --help`

See a list of all the settings available to get or set 

Note: `MQTT settings <https://github.com/NERC-CEH/campbell-mqtt-control/blob/main/src/mqttconfig/README.md>`_ binary format specifically for configuring the MQTT settings all at once.

`mqtt-control set [setting]`

Scripts
-------

`mqtt-control list` - show a file listing
`mqtt-control rm` - delete a file

`mqtt-control download --url=[url] --filename=[filename]` - download the file from `url` and save it at the location `filename`. *"If successful, the program will be set to run now and run on power up and the data logger will restart and compile and run the program"*

Script control
--------------

Optional extras, but nice if quick to implement:

`mqtt-control run filename.crx1` - run a program
`mqtt-control stop` - stop the currently running program

`mqtt-control getVar` - get the value of a script variable
`mqtt-control setVar` - set the value of a script variable

TODO
----

* x.509 certificate rotation, if possible (not clear from the API docs whether it is)

