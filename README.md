## About

This tool is used to analyze tangle data.

It can be integrated with IOTA nodes and Chrnoicle nodes to perform online filtering, patern matching, and garph building, with GUI.

Also this tool supports complicated analysis (e.g., search for a specific pattern in huge IOTA historical data.)

Note that operations those need to scan all transactions stored in the database can be **ONLY** performed offline. The reason is that the scan operation in database to get all historical transactions is time consuming and/or costly. A better alternative is to perfom parallel processing to collect/analyze all the data in tangle. Here is an example: One needs to filter the transactions whose value is larger than 0 from 2017/1/1 to 2020/1/1, then he/she needs to use the dmp files as the tool's inputs.

## Tool Features

- Support input streams from dmp files, IOTA nodes, and chronicle nodes
- Graph automatic construction
- Efficient traversal of transaction flows in tangle
- Efficent filting for different criterions and patterns
- Support GUI

## Prerequisites

- Python 3.6+
- [PyOTA] https://github.com/iotaledger/iota.py

## Installation

TODO

## Getting started

TODO

## Tool Usage

TODO