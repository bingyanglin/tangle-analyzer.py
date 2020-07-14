from typing import Callable
from datetime import datetime, timezone
from time import mktime
from ..common.const import (
    MILESTONES_USING_TIMESTAMP_ONLY,
    TIMESTAMP_B,
    TIMESTAMP_E,
    ATCH_TIMESTAMP_B,
    ATCH_TIMESTAMP_E
)
from ..common import tryte_to_int
import logging

__all__ = [
    'TimeFilter',
]


class TimeFilter():
    """
    Time filter for transaction


    Attributes
    ----------
    min : int
        The private earliest Unix epoch time for filtering
    max : int
        The private latest Unix epoch time for filtering

    Methods
    -------
    make_filter()
        Return the built time filter

    """

    def __init__(self, start_date: str, end_date: str) -> None:
        """
        Parameters
        ----------
        start_date : str
            The start_date (%Y%m%d) of transaction to monitor (e.g., "20200101")
        end_date : str
            The end_date (%Y%m%d) of transaction to monitor (e.g., "20200201")

        """
        try:
            self._min = mktime(datetime.strptime(
                start_date, "%Y%m%d").timetuple())
            self._max = mktime(datetime.strptime(
                end_date, "%Y%m%d").timetuple())
        except:
            logging.error("Dates {} and {} are not supported!".format(
                start_date, end_date))
            logging.error("Plese use \"%Y%m%d\" instead, e.g., \"20200101\"")

    def _get_transaction_dmp(self, timestamp: int, attachmenttimestame: int, milestone: str) -> int:
        if milestone in MILESTONES_USING_TIMESTAMP_ONLY:
            return timestamp
        if attachmenttimestame != 0:
            return attachmenttimestame/1000
        else:
            return timestamp

    def _get_transaction_time(self, timestamp: int, attachmenttimestame: int) -> int:
        if attachmenttimestame != 0:
            return attachmenttimestame/1000
        else:
            return timestamp

    def _time_range_filter(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t < self._max and t > self._min
        except:
            logging.error(
                "Objects for time filtering (min<time<max) do not have time item!")

    def _time_filter_larger_than_min(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t > self._min
        except:
            logging.error(
                "Objects for time filtering (time>min) do not have time item!")

    def _time_filter_smaller_than_max(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t < self._max
        except:
            logging.error(
                "Objects for smaller time filtering (time<max) do not have time item!")

    def _time_euqal_filter(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t == self._min
        except:
            logging.error(
                "Objects for time filtering (time=min) do not have time item!")

    def _time_range_with_euqal_filter(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t <= self._max and t >= self._min
        except:
            logging.error(
                "Objects for time filtering (min<=time<=max) do not have time item!")

    def _time_filter_equal_to_or_larger_than_min(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t >= self._min
        except:
            logging.error(
                "Objects for time filtering (time>=min) do not have time item!")

    def _time_filter_equal_to_or_smaller_than_max(self, transaction: dict) -> bool:
        try:
            t = self._get_transaction_time(
                transaction['timestamp'], transaction['attachment_timestamp'])
            return t <= self._max
        except:
            logging.error(
                "Objects for smaller time filtering (time<=max) do not have time item!")

    def _dmptime_range_filter_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t < self._max and t > self._min
        except:
            logging.error(
                "Objects for time filtering (min<time<max) do not have time item!")

    def _dmptime_filter_larger_than_min_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t > self._min
        except:
            logging.error(
                "Objects for time filtering (time>min) do not have time item!")

    def _dmptime_filter_smaller_than_max_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t < self._max
        except:
            logging.error(
                "Objects for smaller time filtering (time<max) do not have time item!")

    def _dmptime_euqal_filter_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t == self._min
        except:
            logging.error(
                "Objects for time filtering (time=min) do not have time item!")

    def _dmptime_range_with_euqal_filter_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t <= self._max and t >= self._min
        except:
            logging.error(
                "Objects for time filtering (min<=time<=max) do not have time item!")

    def _dmptime_filter_equal_to_or_larger_than_min_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t >= self._min
        except:
            logging.error(
                "Objects for time filtering (time>=min) do not have time item!")

    def _dmptime_filter_equal_to_or_smaller_than_max_str(self, transaction_milestone: tuple) -> bool:
        try:
            timestamp = tryte_to_int(
                transaction_milestone[0], TIMESTAMP_B, TIMESTAMP_E)
            attachment_timestamp = tryte_to_int(
                transaction_milestone[0], ATCH_TIMESTAMP_B, ATCH_TIMESTAMP_E)
            milestone = transaction_milestone[1]
            t = self._get_transaction_dmp(
                timestamp, attachment_timestamp, milestone)
            return t <= self._max
        except:
            logging.error(
                "Objects for smaller time filtering (time<=max) do not have time item!")

    def _time_range_filter_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t < self._max and t > self._min
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def _time_filter_larger_than_min_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t > self._min
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def _time_filter_smaller_than_max_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t < self._max
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def _time_euqal_filter_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t == self._min
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def _time_range_with_euqal_filter_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t <= self._max and t >= self._min
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def _time_filter_equal_to_or_larger_than_min_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t >= self._min
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def _time_filter_equal_to_or_smaller_than_max_str(self, transaction: str) -> bool:
        try:
            t = tryte_to_int(transaction, TIMESTAMP_B, TIMESTAMP_E)
            return t <= self._max
        except:
            logging.error(f"Cannot identify timestamp: {transaction}!")

    def make_filter(self, range_larger_smaller='R') -> Callable:
        """time filter generation function.

        Parameters
        ----------
        range_larger_smaller_equal (str) :

            'R' for min < time < max
            'm' for time > min
            'M' for time < max
            'E' for time = min
            'RE' for min <= time <= max
            'mE' for time >= min
            'ME' for time <= max

        Returns
        ----------
        The built time filter.

        """
        if range_larger_smaller == 'R':
            return self._time_range_filter_str
        elif range_larger_smaller == 'm':
            return self._time_filter_larger_than_min_str
        elif range_larger_smaller == 'M':
            return self._time_filter_smaller_than_max_str
        elif range_larger_smaller == 'E':
            return self._time_euqal_filter_str
        elif range_larger_smaller == 'RE':
            return self._time_range_with_euqal_filter_str
        elif range_larger_smaller == 'mE':
            return self._time_filter_equal_to_or_larger_than_min_str
        elif range_larger_smaller == 'ME':
            return self._time_filter_equal_to_or_smaller_than_max_str
        else:
            raise ValueError(
                "{} is not supported!".format(range_larger_smaller))

    def make_dmp_filter(self, range_larger_smaller='R') -> Callable:
        """time filter generation function for dmp data.
        When using this filter, the milestone for each transaction should be indicated.

        Parameters
        ----------
        range_larger_smaller_equal (str) :

            'R' for min < time < max
            'm' for time > min
            'M' for time < max
            'E' for time = min
            'RE' for min <= time <= max
            'mE' for time >= min
            'ME' for time <= max

        Returns
        ----------
        The built time filter.

        """
        if range_larger_smaller == 'R':
            return self._dmptime_range_filter_str
        elif range_larger_smaller == 'm':
            return self._dmptime_filter_larger_than_min_str
        elif range_larger_smaller == 'M':
            return self._dmptime_filter_smaller_than_max_str
        elif range_larger_smaller == 'E':
            return self._dmptime_euqal_filter_str
        elif range_larger_smaller == 'RE':
            return self._dmptime_range_with_euqal_filter_str
        elif range_larger_smaller == 'mE':
            return self._dmptime_filter_equal_to_or_larger_than_min_str
        elif range_larger_smaller == 'ME':
            return self._dmptime_filter_equal_to_or_smaller_than_max_str
        else:
            raise ValueError(
                "{} is not supported!".format(range_larger_smaller))
