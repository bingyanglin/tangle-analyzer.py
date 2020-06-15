## About

This tool is used to analyze tangle data.

It can be integrated with IOTA nodes and Chrnoicle nodes to perform online filtering, patern matching, and garph building, with GUI.

Also this tool can be used for complicated analysis (e.g., search for a specific pattern in huge IOTA historical data.)

Note that operations those need to scan all transactions stored in the database can be **ONLY** performed offline. The reason is that the scan operation in database to get all historical transactions is time consuming and costly. A better alternative is to perform parallel processing to collect/analyze all the data in tangle. Here is an example: One needs to filter the transactions whose value is larger than 0 from 2017/1/1 to 2020/1/1, then the user needs to use the dmp file(s) as input(s).

## Tool Functionalities
- Filter all the historical data (off-line) or monitor the filtered new coming transactions by zmq event subscription from IOTA node (on-line)
  - Filtering: **Note that AND/OR logical operations can be used with filters together.**

    - `Transaction hash`: Identify the transactions which have a (set of) specific transaction hash(es), and identify the bundles which contain these transactions.

    - `signatureMessageFragment`: Identify the transactions those contain a (set of) specific signatureMessageFragment(s), and identify the bundles contain these transactions.

    - `address`: Identify the transactions those contain a (set of) specific address(es), and identify the bundles contain these transactions.

    - `value`: Identify the transactions which value is in a specific range, and identify the bundles contain these transactions.

    - `obsolete tag`: Identify the transactions those contain a (set of) specific obsolete tag(s), and identify the bundles contain these transactions.

    - `timestamp`: Identify the transactions which timestamp is in a (set of) specific range(s), and identify the bundles contain these transactions.

    - `bundle hash`: Identify the transactions which have a (set of) specific transaction hash(es), and identify the bundles which contain these transactions.

    - `attachmentTag`: Identify the transactions which have a (set of) specific attachmentTag(es), and identify the bundles which contain these transactions.

    - `attachementTimestamp`: Identify the transactions which have a (set of) specific attachmentTag(es), and identify the bundles which contain these transactions.

    - `nonce`: Identify the transactions which have a (set of) specific attachmentTag(es), and identify the bundles which contain these transactions.

- Given a set of transactions and/or bundles, construct the corresponding transaction flow graph by connecting the input and out addresses.

- Monitor a set of addresses(es) and the identify the corresponding output addresses if new transactions are requested.

## Prerequisites

- Python 3.8+
- [PyOTA] https://github.com/iotaledger/iota.py

## Examples

TODO