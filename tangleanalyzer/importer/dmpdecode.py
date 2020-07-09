from iota import TryteString
import datetime
from ..common.const import *
from ..common import tryte_to_int
import os
from os import listdir
from os.path import isfile, join
import multiprocessing as mp
import logging


class DmpDecode():
    def __init__(self, dmp_folder="dmp", decoded_dmp_folder="decoded_data", filter_list=[], time_filter_list=None) -> None:
        self.dmp_folder = dmp_folder
        self.decoded_dmp_folder = decoded_dmp_folder
        self.filter_list = filter_list
        self.time_filter_list = time_filter_list

    def output_decoded_results(self, filename) -> tuple:
        target = []
        tx_time_dict = {}
        filepath = join(self.dmp_folder, filename)
        milestone = filename.split(".")[0]
        with open(filepath) as f:
            logging.info(f"Processing {filepath}...")
            lines = f.readlines()
            for l in lines:
                tx_hash = l.split(",")[0]
                tx_hash_str = TryteString(tx_hash)
                tx_str = l.split(",")[1].strip()

                logging.debug(f"tx_hash = {tx_hash}")

                # Apply filters
                trytes_hash = (tx_str + " " + tx_hash,)
                for f in self.filter_list:
                    trytes_hash = tuple(filter(f, trytes_hash))
                if not trytes_hash:
                    continue

                transaction_milestone = ((tx_str, milestone),)
                for f in self.time_filter_list:
                    transaction_milestone = tuple(
                        filter(f, transaction_milestone))
                if not transaction_milestone:
                    continue

                # tx_trytes = TryteString.as_integers(tx_str)
                logging.info(f"trytes_hash = {trytes_hash[0][:10]}...")
                value = tryte_to_int(tx_str, VALUE_B, VALUE_E)
                address = tx_str[ADDRESS_B: ADDRESS_E]
                bundle = tx_str[BUNDLE_HASH_B: BUNDLE_HASH_E]
                timestamp = tryte_to_int(tx_str, TIMESTAMP_B, TIMESTAMP_E)
                attachtimestamp = tryte_to_int(
                    tx_str, ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
                if timestamp > 10e9:
                    timestamp = int(timestamp*10e-4)
                if attachtimestamp > 10e9:
                    attachtimestamp = int(attachtimestamp*10e-4)
                current_index = tryte_to_int(
                    tx_str, CURRENT_IDX_B, CURRENT_IDX_E)
                last_index = tryte_to_int(tx_str, LAST_IDX_B, LAST_IDX_E)
                trunk = tx_str[TRUNK_B: TRUNK_E]
                branch = tx_str[BRANCH_B: BRANCH_E]
                tag = tx_str[TAG_B: TAG_E]

                # Note that for the same to_store string the timestamp will be overrided!
                to_store = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    tx_hash_str, address, value, timestamp, current_index, last_index, bundle, trunk, branch, tag, attachtimestamp)

                # logging.info(f"to_sore = {to_store}")
                if filename.split(".")[0] in MILESTONES_USING_TIMESTAMP_ONLY:
                    attachtimestamp = timestamp
                tx_time_dict[to_store] = timestamp  # attachtimestamp

        # Reorder by the timestamp
        with open("{}/{}.txt".format(self.decoded_dmp_folder, filename.split(".")[0]), 'w') as f:
            f.write("time\ttx_hash_str\taddress\tvalue\ttimestamp\tcurrent_index\tlast_index\tbundle\ttrunk\tbranch\ttag\tattachtimestamp\n")
            for k, v in tx_time_dict.items():
                f.write("{}\t{}\n".format(datetime.datetime.fromtimestamp(
                    v, tz=datetime.timezone.utc).strftime("%Y%m%d"), k))
        logging.info(f"{filename} is done!")
        return (filename, target)

    def run(self) -> None:
        N = mp.cpu_count()
        dmpfiles = [f for f in listdir(
            self.dmp_folder) if isfile(join(self.dmp_folder, f))]

        if not os.path.exists(self.decoded_dmp_folder):
            os.makedirs(self.decoded_dmp_folder)
        with mp.Pool(processes=N) as p:
            results = p.map(self.output_decoded_results, dmpfiles)
