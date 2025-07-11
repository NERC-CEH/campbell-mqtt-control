# Campbell MQTT Command and Control

[![tests badge](https://github.com/NERC-CEH/campbell-mqtt-control/actions/workflows/pipeline.yml/badge.svg)](https://github.com/NERC-CEH/campbell-mqtt-control/actions)
[![docs badge](https://img.shields.io/badge/Documentation-blue)](https://nerc-ceh.github.io/campbell-mqtt-control/)

This project allows you to control Campbell data loggers remotely via MQTT messages. MQTT is a popular protocol for sending short messages back and forth to Internet of Things (IoT) devices. Campbell Scientific provide a [supported MQTT interface](https://help.campbellsci.com/CR1000X/Content/shared/Communication/mqtt/mqtt-command-control.htm) for updating scripts and changing settings. This package helps to do remote administration in a way that can be automated.

* `campbellcontrol` python library
* `mqtt-control` command-line interface

## How Does it Work?

The loggers connect to the MQTT server and listen for messages sent to special _topics_. 
Topics look like file paths, or links. By sending a small "payload" in the JSON format

 This app wraps around this feature by handling connections to a MQTT broker and sending payloads to the special topics that the loggers are subscribed to, then listening to a response to evaluate the success or failure.
When connected over MQTT, the loggers subscribe and publish to a couple of select topics:

* `<base_topic>/cc/<serial_number>/<command_name>`: Logger subscribes to this topic to listen for MQTT commands.
* `<base_topic>/cr/<serial_number>/<command_name>`: Logger publishes to this topic to return data relating to a previous command request
* `<base_topic>/state/<serial_number>/`: Logger reports changes to the state. Often has messages while processing a command

For example: Deleting a file on the logger remotely. In a logger with serial number `1234` and using base topic `my/logger`.

* The logger subscribes to topic `my/logger/cc/1234/fileControl`. When a payload is received on this topic, it triggers the logger to delete a file specified in the payload
* Success is published on topic `/my/logger/cr/1234/fileControl`.

The Python code wraps this logic by publishing commands and subscribing to the response topic.

## What's implemented here

* [Command classes](src/campbellcontrol/commands/commands.py) for generating relevant topics and response handlers that support all commands available in the MQTT API.
* [Client classes](src/campbellcontrol/connection/interface.py) for connecting to an MQTT broker via [Paho](src/campbellcontrol/connection/generic.py) or [AWS]((src/campbellcontrol/connection/aws.py))
* [Command Handlers](src/campbellcontrol/control.py) for submitting commands through an MQTT broker and awaiting the response.

## Example python usage

The example below connects to the public MQTT broker and sends a command instructing a datalogger to delete a file called `myfile.CR1X`.
```python
from campbellcontrol.control import PahoCommandHandler
from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.commands.commands import DeleteFile

base_topic = "cs/v2"
serial = "1234"
file_to_delete = "myfile.CR1X"

# Create a MQTT client using Paho
client = PahoConnection("test.mosquitto.org", 1883)

# Instanticating a command handler
command_handler = PahoCommandHandler(client)

# Create a command targeted to the desired logger
command = commands.DeleteFile(base_topic, serial)

# Send the command and wait for a response
response = command_handler.send_command(command, file_to_delete)

print(response)
```

## Example commandline usage 

Get help on the application and see all options:

```
$ mqtt-control --help
_  _  __  ___ ___    ____ ____ __ _ ___ ____ ____ _
|\/| [_,]  |   |  -- |___ [__] | \|  |  |--< [__] |___

:
Usage: mqtt-control [OPTIONS] COMMAND [ARGS]...

Options:
  --config PATH
  --client_id TEXT
  --device_id TEXT
  --help            Show this message and exit.

Commands:
  get       Get the value of a setting on the logger.
  getvar    Get the value of a script variable on the logger.
  ls        Read and print the list of files on the logger
  put       Upload a file at {URL} to a file named {filename} on the logger
  reboot    Reboot the logger! Use with caution
  rm        Delete a named file off the datalogger
  set       Update a setting on the logger
  settings  Shows all the settings which you can reset with this tool.
  setvar    Update a script variable on the logger.
```

Download a script file from a URL, save it on the logger with a specific filename, and try to reboot and run it:

```
mqtt-control --device_id 12345 --filename test.cr1x --url https://github.com/NERC-CEH/campbell-mqtt-control/blob/main/tests/data/logger-quiet.CR1X
```

Update one of the settings values:

```
mqtt-control --device_id 12345 set PakBusAddress 2 
```

For more detail on the commandline interface, please see the [documentation site](https://nerc-ceh.github.io/campbell-mqtt-control/)

## Getting Started 

It's best to create a python virtual environment for each project. We currently require python version 3.12 or above, but can try to change that.

```
python -m venv .venv
```

Install the package. This will also install the `mqtt-control` commandline client.
```
pip install -e .
```

### Configuration

A file called `config.yaml` needs to be present in your current working directory. It looks like this. The `topic` should be set to the same value that is configured as the `MQTT base topic` in the Campbell logger.

```
topic: 'cs/v2'
broker: 'Mosquitto'
client_id: 12345
server: test.mosquitto.org
port: 1883
```


### AWS authentication

We've developed this to work with either a generic MQTT implementation using the [Eclipse Paho](https://pypi.org/project/paho-mqtt/) client and the [Mosquitto](https://mosquitto.org/) server, or an Amazon Web Services specific implementation using the [aws-crt-python](https://github.com/awslabs/aws-crt-python) library and AWS's IoT Core MQTT service. 

The certificate root are only needed if you are doing mTLS authentication to an MQTT server running on the secure port 8883. We don't currently support WebSocket authentication on port 443.

```
topic: 'cs/v2'
broker: 'AWS'
client_id: 12345
server: [this is the AWS IoT core endpoint URL]
port: 8883
certificate_root: 'CARoot.pem'
public_key: 'public_filename.crt'
private_key: 'private_filename.key'
```

If you've had to manually configure a Campbell logger to add TLS certificates, this is the same pair that you would upload to the device with a client like PC400. 

## Development

### Using the Githooks

From the root directory of the repo, run:

```
git config --local core.hooksPath .githooks/
```

This will set this repo up to use the git hooks in the `.githooks/` directory. The hook runs `ruff format --check` and `ruff check` to prevent commits that are not formatted correctly or have errors. The hook intentionally does not alter the files, but informs the user which command to run.

### Installing the package

This package is configured to use optional dependencies based on what you are doing with the code.

As a user, you would install the code with only the dependencies needed to run it:

```
pip install .
```

To work on the docs:

```
pip install -e .[docs]
```

To work on tests:

```
pip install -e .[tests]
```

To run the linter and githook:

```
pip install -e .[lint]
```

The docs, tests, and linter packages can be installed together with:

```
pip install -e .[dev]
```

### Building Docs Locally

The documentation is driven by [Sphinx](https://www.sphinx-doc.org/) an industry standard for documentation with a healthy userbase and lots of add-ons. It uses `sphinx-apidoc` to generate API documentation for the codebase from Python docstrings.

To run `sphinx-apidoc` run:

```
# Install your package with optional dependencies for docs
pip install -e .[docs]

cd docs
make apidoc
```

This will populate `./docs/sources/...` with `*.rst` files for each Python module, which may be included into the documentation.

Documentation can then be built locally by running `make html`, or found on the [GitHub Deployment](https://nerc-ceh.github.io/campbell-mqtt-control).

### Run the Tests

To run the tests run:

```
#Install package with optional dependencies for testing
pip install -e .[test]

pytest
```

To run the hardware integration tests, you need a Campbell logger configured to allow connection to an MQTT broker on the topic `cs/v2`. Please see the docs for more info about setting up and testing this. The `-m` switch here is the marker for optional hardware tests.

`py.test -vs -m hardware -serial ABCDEF`

Options

```
--serial Serial number of the logger, configurable
--server Address of the MQTT broker to use for testing
```

### Automatic Versioning

This codebase is set up using [autosemver](https://autosemver.readthedocs.io/en/latest/usage.html#) a tool that uses git commit history to calculate the package version. Each time you make a commit, it increments the patch version by 1. You can increment by:

* Normal commit. Use for bugfixes and small updates
    * Increments patch version: `x.x.5 -> x.x.6`
* Commit starts with `* NEW:`. Use for new features
    * Increments minor version `x.1.x -> x.2.x`
* Commit starts with `* INCOMPATIBLE:`. Use for API breaking changes
    * Increments major version `2.x.x -> 3.x.x`
