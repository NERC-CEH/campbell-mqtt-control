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
    client_id: 12345
    certificate_pem: 'certificate_filename.pem'
    public_key: 'public_filename.crt'
    private_key: 'private_filename.key'


Options
-------

Some options in the configuration file can be over-written by command-line switches.

For example:

`mqtt-control --client_id 54321 ls`

Will replace the client ID number set in the configuration file.

Note that these are options to `mqtt-control` and not to its sub-commands!

Settings
--------

All the settings visible through the "Device Configuration Utility" can be read or changed one by one with the `settings` topic.

There's a [full list of settings in the official documentation](https://help.campbellsci.com/CR1000X/Content/shared/Maintain/Advanced/settings-general.htm). There's also a script, `extract_settings.py` included in the repository, which collects the list from that page into a text file.

Get the value of a specific setting on the logger. 

`mqtt-control get [setting]`

For example,

`mqtt-control get PakBusAddress`

Set a given setting to a specific value:

`mqtt-control set [setting] [value]`

For example,

`mqtt-control set PakBusAddress 2`

See a list of all the setting names available to get or set:

`mqtt-control settings`


MQTT Configuration (not yet implemented)
----------------------------------------

Send an updated MQTT configuration value to the logger.

`mqtt-control config --name [setting] --value [value]`


Scripts
-------

`mqtt-control ls` - show a file listing

`mqtt-control rm --filename [file]` - delete a file

`mqtt-control put --url=[url] --filename=[filename]` - download the file from `url` and save it at the location `filename`. *"If successful, the program will be set to run now and run on power up and the data logger will restart and compile and run the program"*

Script control (not yet implemented)
------------------------------------

Optional extras, but nice if quick to implement:

`mqtt-control run filename.crx1` - run a program
`mqtt-control stop` - stop the currently running program

`mqtt-control getVar` - get the value of a script variable
`mqtt-control setVar` - set the value of a script variable

TODO
----

* x.509 certificate rotation, if possible (the `fileControl` interface could be used in an unintended way, but would result in a short downtime while the logger is not running a program)

