import iota
import logging
from pyfiglet import Figlet, figlet_format
from tangleanalyzer import ZmqSub, AddressFilter, BundleFilter, TagFilter, TimeFilter, TransactionFilter, ValueFilter
import toml
from termcolor import cprint


def main():

    f = Figlet(font='slant')
    cprint(figlet_format('Tangle Analyzer', font="slant"), "red")

    # Get the config toml file
    config = toml.load("config.toml")

    # Set the debug level
    debug_level = config['logger']['level']
    logging.basicConfig(
        level=debug_level,
        format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Get the version
    version = config['version']['version']
    logging.info(f"Version: {version}")

    # Init the filters
    filters = config.get("filters", {})
    addr_set = set(filters.get('address', []))
    bundle_set = set(filters.get('bundle', []))
    tag_set = set(filters.get('tag', []))
    transaction_set = set(filters.get('transaction', []))
    time_list = filters.get('time', {})
    value_list = filters.get('value', {})
    zmq_conf = config.get("zmq", {})

    # Make filters
    filter_list = []
    if addr_set:
        filter_list.append(AddressFilter(addr_set).make_filter())
    if bundle_set:
        filter_list.append(BundleFilter(bundle_set).make_filter())
    if tag_set:
        filter_list.append(TagFilter(tag_set).make_filter())
    if transaction_set:
        filter_list.append(TransactionFilter(transaction_set).make_filter())
    for t in time_list:
        filter_list.append(TimeFilter(
            start_date=t['start'], end_date=t['end']).make_filter(t['rlse']))
    for t in value_list:
        filter_list.append(ValueFilter(
            min=int(t['min']), max=int(t['max'])).make_filter(t['rlse']))

    if zmq_conf:
        sub = ZmqSub(url=zmq_conf['node_ip'],
                     topic=zmq_conf['topic'], filterlist=filter_list)
        sub.run()


if __name__ == "__main__":
    main()
