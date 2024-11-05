# Getting Started

### 1. Working Directory

In this working [eventgen](./) folder.

### 2. Configuration

Configure your seetings under [config.json](config.json). There are four important options to configure:

| Option | Description | Format |
| ------ | ----------- | ------ |
| sourcetype | The classification for the data | Change the URL option for `oracle_audit` to support your desired choice. 
| output_size | The amount of data to send | KB, MB and GB |
| time_range | Period of time to distribute the data | m, h, d |
| format | The format to send the data | xml, json |

Here is an example of the configuration to generate 10KB of data over a 20 minute period. 

```json
{
  "samples": "samples/audit_log.txt",
  "webhook_url": "https://ingest.us1.sentinelone.net/services/collector/raw?sourcetype=oracle_audit",
  "output_size": "10KB",
  "time_range": "20m",
  "format": "xml"
}
```

### 3. API Key

Express your Log Access Key with an environment variable. This key must provide `Write` permissions to your desired SentinelOne Site.

```bash
export AUTH_TOKEN="******HOVWe_Yf"
```

### 4. Run the generator

```bash
python3 eventgen.py
```


At the moment we output some simple messages to indicate action. The events are shipped over the period of time you indicate in the configuration. For the configuration above, you may see a number of messages like these:

```bash
Data successfully sent. Status code: 200
Sent 1 events, 359 bytes in 0 minute(s).
Data successfully sent. Status code: 200
Sent 2 events, 753 bytes in 0 minute(s).
...
...
Data successfully sent. Status code: 200
Sent 28 events, 9885 bytes in 17 minute(s).
Data successfully sent. Status code: 200
Sent 29 events, 10244 bytes in 19 minute(s).
```
