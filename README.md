## About

This tool is used to analyze tangle data.

It can be integrated with IOTA nodes and Chronicle nodes to perform online filtering, pattern matching, and graph building, with GUI.

Also this tool can be used for complicated analysis (e.g., search for a specific pattern in huge IOTA historical data.)

Note that operations those need to scan all transactions stored in the database can be **ONLY** performed offline. The reason is that the scan operation in database to get all historical transactions is time consuming and costly. A better alternative is to perform parallel processing to collect/analyze all the data in tangle. Here is an example: One needs to filter the transactions whose value is larger than 0 from 2017/1/1 to 2020/1/1, then the user needs to use the dmp file(s) as input(s).

## Tool Functionalities
- Filter all the historical data (off-line) or monitor the filtered new coming transactions by zmq event subscription from IOTA node (on-line)
  - Filtering: **Note that AND/OR logical operations can be used with the following filters together.**

    - `Transaction hash`: Identify the transactions which have a (set of) specific transaction hash(es), and identify the bundles which contain these transactions.

    - `address`: Identify the transactions those contain a (set of) specific address(es), and identify the bundles contain these transactions.

    - `value`: Identify the transactions which value is in a specific range, and identify the bundles contain these transactions.

    - `time`: Identify the transactions whose **`time`** is in a (set of) specific range(s), and identify the bundles contain these transactions. The rule of identifying the **`time`** in a transaction is: 
      - For the transactions with milestones `6000`, `13157`, `18675`, `61491`, `150354`, `216223`, `242662`, and `337541`, the timestamp is used directly. ([Historical data link](https://dbfiles.iota.org/?prefix=mainnet/history/))
      - For other milestones, the attachmentTimestamp will be used if it is not zero, else we use timestamp directly.

    - `bundle hash`: Identify the transactions which have a (set of) specific transaction hash(es), and identify the bundles which contain these transactions.

    - `tag`: Identify the transactions those contain a (set of) specific tag(s), and identify the bundles contain these transactions.

- Given a set of transactions and/or bundles, construct the corresponding transaction flow graph by connecting the input and out addresses.

- Monitor a set of addresses(es) and the identify the corresponding output addresses if new transactions are requested.

## Prerequisites

- Python 3.8+
- [PyOTA] https://github.com/iotaledger/iota.py

## User Configurations

- Use `config.toml` to configure the settings
- The following shows an configuration example
```yaml
# version details
[version]
name = "tangle-analyzer-alpha-v0.1.0"
service = "Tangle Analyzer"

# logger settings
[logger]
level = "INFO" # INFO, DEBUG, ERROR, WARNING, CRITICAL

# zmq settings
[zmq]
enable = "FALSE" # TURE or FALSE
node_ip = "tcp://zmq.iota.org:5556"
topic = "trytes"

# dmp file settings
[dmp]
enable = "TRUE" # TRUE or FALSE
input_folder = "dmp" # The historical dmp files from https://dbfiles.iota.org/?prefix=mainnet/history/
output_folder = "decoded_data"

# filter settings
# Note: blank list represents `no filtering` to the target field.
#       If a filter is set, then only transactions meet the filter conidtion will be reserved
[filters]
addresses = []
bundle = []
tag = []
transactions = []

# Setting for rlse:
#     'R' for start < time < end
#     'm' for time > start
#     'M' for time < end
#     'E' for time = start
#     'RE' for start <= time <= end
#     'mE' for time >= start
#     'ME' for time <= end
[[filters.time]]
    start = "20090101"
    end = "20200706"
    rlse = 'RE'

# Setting for rlsq:
#     'R' for min < value < max
#     'm' for value > min
#     'M' for value < max
#     'E' for value = min
#     'RE' for min <= value <= max
#     'mE' for value >= min
#     'ME' for value <= max
[[filters.value]]
    min = 0
    max = 100
    rlse = 'RE'
```

## How to run

`python main.py`


## Running Example

```
 $ python3 main.py 
  ______                  __        ___                __                     
 /_  __/___ _____  ____ _/ /__     /   |  ____  ____ _/ /_  ______  ___  _____
  / / / __ `/ __ \/ __ `/ / _ \   / /| | / __ \/ __ `/ / / / /_  / / _ \/ ___/
 / / / /_/ / / / / /_/ / /  __/  / ___ |/ / / / /_/ / / /_/ / / /_/  __/ /    
/_/  \__,_/_/ /_/\__, /_/\___/  /_/  |_/_/ /_/\__,_/_/\__, / /___/\___/_/     
                /____/                               /____/                   

22:57:19,222 INFO: Version: tangle-analyzer-alpha-v0.1.0
22:57:20,362 INFO: Received b'trytes 9999999999999'...
22:57:20,362 INFO: Received b'trytes 9999999999999'...
22:57:20,363 INFO: Start filtering...
22:57:20,363 INFO: Start filtering...
22:57:20,425 INFO: Received b'trytes SBYBCCKBEATBP'...
22:57:20,425 INFO: Start filtering...
22:57:20,425 INFO: Saved b'SBYBCCKBEATBPCADADTC'... into database
22:57:20,539 INFO: Received b'trytes 9999999999999'...
22:57:20,539 INFO: Received b'trytes BCDDPCADADXCB'...
22:57:20,539 INFO: Start filtering...
22:57:20,539 INFO: Saved b'99999999999999999999'... into database
22:57:20,539 INFO: Start filtering...
22:57:20,539 INFO: Saved b'BCDDPCADADXCBDVCEAKD'... into database
22:57:20,675 INFO: Received b'trytes BCDDPCADADXCB'...
22:57:20,676 INFO: Start filtering...
22:57:20,676 INFO: Saved b'BCDDPCADADXCBDVCEAKD'... into database
22:57:20,746 INFO: Received b'trytes RBCDFDBDTCHDE'...
22:57:20,747 INFO: Start filtering...
22:57:20,747 INFO: Saved b'RBCDFDBDTCHDEAUASAYA'... into database
^C22:57:20,777 INFO: Received exit signal SIGINT...
22:57:20,777 INFO: Closing database connections
22:57:20,777 INFO: Cancelling 8 tasks
22:57:20,777 INFO: Shutting down ThreadPoolExecutor
22:57:20,777 INFO: Releasing 1 threads from executor
22:57:20,777 INFO: Flushing metrics
22:57:20,778 INFO: Successfully shutdown. Good bye~
```