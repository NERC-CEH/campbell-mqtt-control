MQTT Settings File
==================

One of the MQTT command instructs the logger to download a binary settings file from a URL and apply settings from it to the logger. These are specifically MQTT settings, not general logger settings that are set with the SetSetting command.

When the command to update the MQTT settings is received, it instructs the logger to download a settings file. The logger then confirms that the file matches the format expected before iterating through each setting in the file and changing them to the new values. Any setting not in the file is ignored.

File Format
-----------

The  settings file is binary formatted with 3 components to it:

* A header byte indicating the file start. Must be 2 bytes (big-endian Most significant byte first (MSB)) equal to `0x0020`.
* A sequence of setting entries, repeating as necessary, consisting of:

    * 2 byte setting ID from `0x0001` to `0x0011`  (big-endian MSB first).
    * 4 byte length of the setting value (MSB first).
    * ASCII value of the settings. Must be equal to the setting length. For example changing the MQTT broker endpoint to "test.mosquitto.org" is a length of 18.

* A null byte indicating the file end. Must be null byte `0x0000` 
* Each byte of the file is written without newlines and without spaces.

Available Settings
------------------

There are 20 known settings that can be altered in the file and they are shown below:

.. list-table::
   :widths: auto
   :header-rows: 1

   * - Setting
     - Identifier
   * - Account ID
     - 1 (0x0001)
   * - Private key
     - 2 (0x0002)
   * - Public certificate
     - 3 (0x0003)
   * - Root certificate authority
     - 4 (0x0004)
   * - Endpoint
     - 5 (0x0005)
   * - Port number
     - 6 (0x0006)
   * - Username
     - 7 (0x0007)
   * - Password
     - 8 (0x0008)
   * - Keep alive time
     - 9 (0x0009)
   * - Client ID
     - 10 (0x000A)
   * - Last will topic
     - 11 (0x000B)
   * - Last will message
     - 12 (0x000C)
   * - Last will QoS
     - 13 (0x000D)
   * - Last will message retained by broker
     - 14 (0x000E)
   * - Enable TLS in data logger
     - 15 (0x000F)
   * - Base MQTT topic
     - 16 (0x0010)
   * - State publish interval
     - 18 (0x0012)
   * - Status info publish interval
     - 19 (0x0013)
   * - MQTT connect with clean session
     - 20 (0x0014)

Example Building of File
------------------------

The following code block writes a settings file with 2 settings added:

.. code:: python

    from struct import pack

    # Open a file for writing in binary mode
    with open("mqtt.bin", "wb") as f:

        # Write the header byte
        f.write(pack(">H", 0x0020))

        # Write a setting to change (changing the endpoint)
        f.write(pack(">HH", 0x0005, 18) + b"test.mosquitto.org")

        # Write another setting to change (changing the port)
        f.write(pack(">HH", 0x0006, 4) + b"1883")

        # Write the null byte
        f.write(b"\x00")

For the first setting, the enpoint has ID `0x0005` and new value "test.mosquitto.org" has 18 characters. For the second, the ID is `0x0006` and the value 1883 has 4 characters.

.. warning::
    In the example implementation above, setting string values works well for the endpoint, but setting numeric values doesn't. Further testing is needed to figure out how to write the file for numeric setting values. There is possibly some specifity needed for the byte length of a numeric value.
