from typing import Callable
import logging

__all__ = [
    'ValueFilter',
]


class ValueFilter():
    """
    Value filter for transactions


    Attributes
    ----------
    min : int
        The private minimum value for filtering
    max : int
        The private maximum value for filtering

    Methods
    -------
    make_filter()
        Return the built value filter
    """

    def __init__(self, min: int, max: int) -> None:
        """
        Parameters
        ----------
        min : int
            The minimum value in transactions for monitoring
        max : int
            The maximum value in transactions for monitoring
        """
        self._min = min
        self._max = max

    def _value_range_filter(self, transaction: dict) -> bool:
        try:
            return transaction['value'] < self._max and transaction['value'] > self._min
        except:
            logging.error(
                "Objects for value filtering (min<v<max) do not have value item!")

    def _value_filter_larger_than_min(self, transaction: dict) -> bool:
        try:
            return transaction['value'] > self._min
        except:
            logging.error(
                "Objects for value filtering (v>min) do not have value item!")

    def _value_filter_smaller_than_max(self, transaction: dict) -> bool:
        try:
            return transaction['value'] < self._max
        except:
            logging.error(
                "Objects for smaller value filtering (v<max) do not have value item!")

    def _value_euqal_filter(self, transaction: dict) -> bool:
        try:
            return transaction['value'] == self._min
        except:
            logging.error(
                "Objects for value filtering (v=min) do not have value item!")

    def _value_range_with_euqal_filter(self, transaction: dict) -> bool:
        try:
            return transaction['value'] <= self._max and transaction['value'] >= self._min
        except:
            logging.error(
                "Objects for value filtering (min<=v<=max) do not have value item!")

    def _value_filter_equal_to_or_larger_than_min(self, transaction: dict) -> bool:
        try:
            return transaction['value'] >= self._min
        except:
            logging.error(
                "Objects for value filtering (v>=min) do not have value item!")

    def _value_filter_equal_to_or_smaller_than_max(self, transaction: dict) -> bool:
        try:
            return transaction['value'] <= self._max
        except:
            logging.error(
                "Objects for smaller value filtering (v<=max) do not have value item!")

    def make_filter(self, range_larger_smaller='R') -> Callable:
        """Value filter generation function.

        Parameters
        ----------
        range_larger_smaller_equal (str) :

            'R' for min < value < max
            'm' for value > min
            'M' for value < max
            'E' for value = min
            'RE' for min <= value <= max
            'mE' for value >= min
            'ME' for value <= max

        Returns
        ----------
        The built value filter.

        """
        if range_larger_smaller == 'R':
            return self._value_range_filter
        elif range_larger_smaller == 'm':
            return self._value_filter_larger_than_min
        elif range_larger_smaller == 'M':
            return self._value_filter_smaller_than_max
        elif range_larger_smaller == 'E':
            return self._value_euqal_filter
        elif range_larger_smaller == 'RE':
            return self._value_range_with_euqal_filter
        elif range_larger_smaller == 'mE':
            return self._value_filter_equal_to_or_larger_than_min
        elif range_larger_smaller == 'ME':
            return self._value_filter_equal_to_or_smaller_than_max
        else:
            raise ValueError(
                "{} is not supported!".format(range_larger_smaller))
