# Python Project Template

[![tests badge](https://github.com/NERC-CEH/campbell-mqtt-control/actions/workflows/pipeline.yml/badge.svg)](https://github.com/NERC-CEH/campbell-mqtt-control/actions)
[![docs badge](https://img.shields.io/badge/Documentation-blue)](https://nerc-ceh.github.io/campbell-mqtt-control/)

This is a Python project that allows you to command Campbell data loggers remotely via MQTT messages. This is done by sending specific JSON payloads to special topics that the loggers subscribe to when communicating over MQTT. This app wraps around this feature by handling connections to a MQTT broker and sending payloads to the special topics that the loggers are subscribed to, then listening to a response to evaluate the success or failure.

## How Does it Work?

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

## A Simple Workflow
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
## Getting Started For Devs

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

`py.test -vs -m hardware -c ABCDEF`

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
