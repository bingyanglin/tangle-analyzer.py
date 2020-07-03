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

23:39:23,906 INFO: Version: tangle-analyzer-alpha-v0.1.0

...

^C23:39:25,923 DEBUG: Received exit signal SIGINT...
23:39:25,923 DEBUG: Closing database connections
23:39:25,923 DEBUG: Cancelling 20 tasks
23:39:25,924 DEBUG: Shutting down ThreadPoolExecutor
23:39:25,924 DEBUG: Releasing 1 threads from executor
23:39:25,924 DEBUG: Flushing metrics
23:39:25,924 DEBUG: Successfully shutdown. Good bye~
```