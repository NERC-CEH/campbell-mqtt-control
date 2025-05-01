# OS
Successful download/install
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/OS b'{"url": "https://www.campbellsci.com/download?dl=dlf&dlid=612&as=3244F814-10DD-47CB-AAE11B7C582972A0&au=167227"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"OS file download"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"Flashing OS"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"OS update"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online"}'
```
Failed download/install
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/OS b'{"url": "fakeurl"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"OS file download"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"OS file download"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"OS file download"}'
cs/v2/cr/QU8Q-9JTY-HVP8/OS b'{"error":"OS Download Failed"}'
```

# Program  Download
Success (Success means that a response from a server is received even if it's a 404 page)
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/program b'{"url": "https://www.campbellsci.com/testfile.crb", "fileName": "testfile.crb"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"Program file download"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"Loading program"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online"}'
cs/v2/cr/QU8Q-9JTY-HVP8/program b'{"success":"Program loaded successfully"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online"}'
```

Failed
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/program b'{"url": "sdfsdfs/testfile.crb", "fileName": "testfile2.crb"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"Program file download"}'
cs/v2/cr/QU8Q-9JTY-HVP8/program b'{"error":"Program download failed"}'
```

# MQTT Config
Bad server
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig b'{"url": "sdfsdfs/testfile.crb"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"MQTT config file download"}'
cs/v2/cr/QU8Q-9JTY-HVP8/mqttConfig b'{"error":"MQTT Config file download failed, code: 0"}'
```

Bad file
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig b'{"url": "https://www.campbellsci.com/testfile.crb"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"MQTT config file download"}'
cs/v2/cr/QU8Q-9JTY-HVP8/mqttConfig b'{"error":"MQTT Config file parse failed"}'
```

Good File
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig b'{"url": "https://raw.githubusercontent.com/NERC-CEH/campbell-mqtt-control/refs/heads/feature/commands/logger"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"MQTT config file download"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"Loading MQTT Configuration"}'
cs/v2/cr/QU8Q-9JTY-HVP8/mqttConfig b'{"success":"MQTT configuration file loaded"}'
```

# Edit Constant
No constant table
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/editConst b'{"const1": "12"}'
cs/v2/cr/QU8Q-9JTY-HVP8/editConst b'{"error":"No constant table to edit"}'
```
Constant not present in table
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/editConst b'{"const1": "12"}'
cs/v2/cr/QU8Q-9JTY-HVP8/editConst b'{"success":"No constant table changes"}'
```

Successful change
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/editConst b'{"const1": "12"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"Changed constants, recompiling"}'
cs/v2/cr/QU8Q-9JTY-HVP8/editConst b'{"success":"Editing constants succeeded"}'
```

# Reboot
Success
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/reboot b'{"action": "reboot"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"Reboot command"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online"}'
cs/v2/cr/QU8Q-9JTY-HVP8/reboot b'{"success":"Reboot complete"}'
```

# File Control
## List
Success
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "list"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"drive":"CPU:","clientID":"CR1000X_70681","fileList":["TemplateExample.CR1X","CPU_hacked-milo-script 1.CR1X","OS.obj","testfile.crb"
```
Invalid drive
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "list", "drive": "USR"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"error":"Directory \'USR:\' does not exist"}'
```
## Delete
Success
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "delete", "fileName": "testfile.crb"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"success":"File deleted"}'
```
File doesn't exist or wrong drive used
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "delete", "fileName": "testfile.crb"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"error":"File does not exist"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"error":"File delete failed"}'
```

## Stop
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "stop"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"Stopping program"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"success":"Program stopped"}'
```

## Run
Valid file given
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "run", "fileName": "TemplateExample.CR1X"}'
cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"offline","reason":"Running program"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"success":"Program running"}'
```

Invalid file or bad argument given
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/fileControl b'{"action": "run", "filename": "TemplateExample.CR1X"}'
cs/v2/cr/QU8Q-9JTY-HVP8/fileControl b'{"error":"File does not exist"}'
```

# Settings
Setting (with apply=true)
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/setting b'{"action": "set", "name": "PakBusAddress", "value": "3", "apply": "true"}'
cs/v2/cr/QU8Q-9JTY-HVP8/setting b'{"success":"Settings applied, no reboot required"}'
```
Invalid setting
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/setting b'{"action": "set", "name": "abc", "value": "3", "apply": "true"}'
cs/v2/cr/QU8Q-9JTY-HVP8/setting b'{"error":"Invalid setting: abc"}'
```
## Apply
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/setting b'{"action": "apply", "apply": "true"}'
cs/v2/cr/QU8Q-9JTY-HVP8/setting b'{"success":"Settings applied, no reboot required"}'
```

## Publish
Success
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/setting b'{"action": "publish", "name": "EthernetPower"}'
cs/v2/cr/QU8Q-9JTY-HVP8/setting b'{"setting":"EthernetPower","value":"2"}'
```
Invalid
```bash
cs/v2/cc/QU8Q-9JTY-HVP8/setting b'{"action": "publish", "name": "EthernetPowder"}'
cs/v2/cr/QU8Q-9JTY-HVP8/setting b'{"error":"Invalid setting: EthernetPowder"}'
```
# Historic Data
Success
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/historicData b'{"table": "Table1", "start": "2025-04-01T03:16:51", "end": "2025-05-01T10:16:51"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/historicData/Table1/cj b'{"head": {"transaction": 0,"signature": 52815,"environment":  {"station_name":  "70681","table_name":  "Table1","model":  "CR1000X","serial_no":  "70681","os_version":  "CR1000X.Std.08.01","prog_name":  "CPU:CPU_hacked-milo-script 1.CR1X"},"fields":  [{"name":  "BattV","type":  "xsd:float","units":  "Volts","process":  "Smp","settable":  false},{"name":  "PTemp_C","type":  "xsd:float","units":  "Deg C","process":  "Smp","settable":  false}]},"data": []}'
```
Table doesn't exist
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/historicData b'{"table": "publish", "start": "2025-05-01T03:16:51", "end": "2025-05-01T03:16:51"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/historicData b'{"error":"Historic Data: Table does not exist!"}'
```
# Set Variable
Successful. Sucess doesn't imply that the variable was set. If the type is FLOAT, it can't be set to a STRING
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/setVar b'{"name": "VarOne", "value": "1.2"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/setVar b'{"success":"Set variable succeeded"}'
```

Variable doesn't exist
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/setVar b'{"name": "VarOne", "value": "1.2"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/setVar b'{"error":"Set variable failed"}'
```

# Get Variable
Success
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/setVar b'{"name": "VarOne", "value": "1.2"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/setVar b'{"success":"Set variable succeeded"}'
```
Variable doesn't exist
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/getVar b'{"name": "VarTwo"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/getVar b'{"error":"Invalid field: VarTwo"}'
```

# Talk Thru
Illegal port
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/talkThru b'{"comPort": "ComU6", "outString": "heyyo"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/talkThru b'{"response":"Illegal ComPort"}'
```

Closed port
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/talkThru b'{"comPort": "ComC1", "outString": "heyyo"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/talkThru b'{"response":"ComPort must be open to use MQTT Talk Thru"}'
```