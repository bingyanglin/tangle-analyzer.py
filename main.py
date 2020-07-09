import iota
import logging
from pyfiglet import Figlet, figlet_format
from tangleanalyzer import ZmqSub, AddressFilter, BundleFilter, TagFilter, TimeFilter, TransactionFilter, ValueFilter
import toml
from termcolor import cprint
from tangleanalyzer import DmpDecode


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
    version = config['version']['name']
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
    dmp_conf = config.get("dmp", {})

    # Make filters
    filter_list = []
    time_filter_list = []
    dmp_time_filter_list = []

    if addr_set:
        filter_list.append(AddressFilter(addr_set).make_filter())
    if bundle_set:
        filter_list.append(BundleFilter(bundle_set).make_filter())
    if tag_set:
        filter_list.append(TagFilter(tag_set).make_filter())
    if transaction_set:
        filter_list.append(TransactionFilter(transaction_set).make_filter())
    for t in value_list:
        filter_list.append(ValueFilter(
            min=int(t['min']), max=int(t['max'])).make_filter(t['rlse']))

    if zmq_conf.get("enable", "FALSE") == "TRUE":
        for t in time_list:
            time_filter_list.append(TimeFilter(
                start_date=t['start'], end_date=t['end']).make_filter(t['rlse']))
        sub = ZmqSub(url=zmq_conf['node_ip'],
                     topic=zmq_conf['topic'], filterlist=filter_list+time_filter_list)
        sub.run()
    if dmp_conf.get("enable", "FALSE") == "TRUE":
        for t in time_list:
            dmp_time_filter_list.append(TimeFilter(
                start_date=t['start'], end_date=t['end']).make_dmp_filter(t['rlse']))
        dmpdecode = DmpDecode(dmp_folder=dmp_conf.get(
            "input_folder", "dmp"), decoded_dmp_folder=dmp_conf.get(
            "output_folder", "decoded_data"), filter_list=filter_list, time_filter_list=dmp_time_filter_list)
        dmpdecode.run()


if __name__ == "__main__":
    main()
