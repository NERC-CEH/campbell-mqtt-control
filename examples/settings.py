import csv

import pandas as pd

import campbellcontrol.commands.commands as commands
from campbellcontrol.config import load_config
from campbellcontrol.connection.factory import get_command_handler, get_connection

# Assumes your MQTT base topic and endpoint are set in config.yaml
config = load_config()

if __name__ == '__main__':

    # Read an excel spreadsheet and filter for specific columns
    df = pd.read_excel('examples/logger_list.xlsx')
    df = df[['Station Name','UI ID']]

    client = get_connection(config)
    command_handler = get_command_handler(client)
    setting = 'MQTTEndpoint'

    found = []

    for idx, row in df.iterrows():
        # Ask the logger to send its setting value via MQTT
        command = commands.PublishSetting(config.topic, row['UI ID'])
        try:
            response = command_handler.send_command(command, 'MQTTEndpoint')
        except ConnectionError as err:
            print(err)

        if not response:
            print(f"Sorry, couldn't connect to {row['UI ID']}")
            continue

        if not response.get("success", False):
            print(f"Sorry, couldn't read a value for {setting}")
            continue

        setting = response["payload"].get("value", None)

        if setting:
            # The value comes back padded with whitespace
            setting = setting.strip()
            found.append([row['Station Name'], row['UI ID'], setting])

    # Export the results as CSV
    with open('out.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(found)


