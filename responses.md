## OS
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

## Program  Download
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

## MQTT Config
Bad server
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig b'{"url": "sdfsdfs/testfile.crb"}'
INFO:root:cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"MQTT config file download"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/mqttConfig b'{"error":"MQTT Config file download failed, code: 0"}'
```

Bad file
```bash
INFO:root:cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig b'{"url": "https://www.campbellsci.com/testfile.crb"}'
INFO:root:cs/v2/state/QU8Q-9JTY-HVP8/ b'{"clientId":"CR1000X_70681","state":"online","fileTransfer":"MQTT config file download"}'
INFO:root:cs/v2/cr/QU8Q-9JTY-HVP8/mqttConfig b'{"error":"MQTT Config file parse failed"}'
```