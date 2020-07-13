import iota
import logging
from pyfiglet import Figlet, figlet_format
import toml
from termcolor import cprint
from tangleanalyzer import (
    DmpDecode,
    ZmqSub,
    AddressFilter,
    BundleFilter,
    TagFilter,
    TimeFilter,
    TransactionFilter,
    ValueFilter
)


def main():

    f = Figlet(font='slant')
    cprint(figlet_format('Tangle Analyzer', font="slant"), "red")

    # Get the config toml file
    config = toml.load("config.toml")

    # Set the debug level
    try:
        debug_level = config['logger']['level']
    except:
        raise ValueError(
            "Please provide the logger debuger level in the toml file!")

    logging.basicConfig(
        level=debug_level,
        format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    # Get the version
    try:
        version = config['version']['name']
    except:
        raise ValueError(
            "Please provide the version name in the toml file!")
    logging.info(f"Version: {version}")

    # Get the filter configuration
    filters_conf = config.get("filters", {})

    # Make filters
    filter_list = []
    time_list = filters_conf.get('time', [])

    if addr_set := set(filters_conf.get('address', [])):
        filter_list.append(AddressFilter(addr_set).make_filter())
    if bundle_set := set(filters_conf.get('bundle', [])):
        filter_list.append(BundleFilter(bundle_set).make_filter())
    if tag_set := set(filters_conf.get('tag', [])):
        filter_list.append(TagFilter(tag_set).make_filter())
    if transaction_set := set(filters_conf.get('transaction', [])):
        filter_list.append(TransactionFilter(transaction_set).make_filter())
    for v in filters_conf.get('value', []):
        filter_list.append(ValueFilter(
            min=int(v['min']),
            max=int(v['max'])).make_filter(v['rlse']))

    if (zmq_conf := config.get("zmq", {})).get("enable", "FALSE") == "TRUE":
        time_filter_list = []
        for t in time_list:
            time_filter_list.append(TimeFilter(
                start_date=t['start'],
                end_date=t['end']).make_filter(t['rlse']))
        sub = ZmqSub(url=zmq_conf['node_ip'],
                     topic=zmq_conf['topic'],
                     filterlist=filter_list+time_filter_list)
        sub.run()

    if (dmp_conf := config.get("dmp", {})).get("enable", "FALSE") == "TRUE":
        dmp_time_filter_list = []
        for t in time_list:
            dmp_time_filter_list.append(TimeFilter(
                start_date=t['start'],
                end_date=t['end']).make_dmp_filter(t['rlse']))

        dmpdecode = DmpDecode(dmp_folder=dmp_conf.get("input_folder", "dmp"),
                              decoded_dmp_folder=dmp_conf.get(
                                  "output_folder", "decoded_data"),
                              filter_list=filter_list,
                              time_filter_list=dmp_time_filter_list)
        dmpdecode.run()


if __name__ == "__main__":
    main()
