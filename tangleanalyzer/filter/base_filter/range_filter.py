from typing import Callable
from ...common import tryte_to_int
import logging

__all__ = [
    'RangeFilter',
]


class RangeFilter():
    """
    Range filter for transactions


    Parameters
    ----------
    min : int
        The minimum value for filtering
    max : int
        The maximum value for filtering

    Methods
    -------
    make_filter()
        Return the built range filter
    """

    def __init__(self, name: str, min: int, max: int, begin: int, end: int) -> None:
        """
        Parameters
        ----------
        name : str
            The filter name.

        min : int
            The minimum value in transactions for monitoring.

        max : int
            The maximum value in transactions for monitoring.

        begin : int
            The begin location of the field in the transaction string.

        end : int
            The end location of the field in the transaction string.
        """
        self._name = name
        self._min = min
        self._max = max
        self._begin = begin
        self._end = end

    def __str__(self):
        return (f'Name: {self._name}\n' +
                f'Min: {self._min}\n' +
                f'Max: {self._max}\n' +
                f'Begin: {self._begin}\n' +
                f'End: {self._end}')

    def _range_for_dict(self, transaction: dict) -> bool:
        try:
            return (transaction[self._name] < self._max and
                    transaction[self._name] > self._min)
        except:
            raise ValueError(
                f'Cannot perform {self._name} (min<v<max) filtering!')

    def _larger_than_min_for_dict(self, transaction: dict) -> bool:
        try:
            return transaction[self._name] > self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v>min) filtering!')

    def _smaller_than_max_for_dict(self, transaction: dict) -> bool:
        try:
            return transaction[self._name] < self._max
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v<max) filtering!')

    def _equal_for_dict(self, transaction: dict) -> bool:
        try:
            return transaction[self._name] == self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v=min) filtering!')

    def _range_with_euqal_for_dict(self, transaction: dict) -> bool:
        try:
            return (transaction[self._name] <= self._max and
                    transaction[self._name] >= self._min)
        except:
            raise ValueError(
                f'Cannot perform {self._name} (min<=v<=max) filtering!')

    def _equal_to_or_larger_than_min_for_dict(self, transaction: dict) -> bool:
        try:
            return transaction[self._name] >= self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v>=min) filtering!')

    def _equal_to_or_smaller_than_max_for_dict(self, transaction: dict) -> bool:
        try:
            return transaction[self._name] <= self._max
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v<=max) filtering!')

    def _range_for_str(self, transaction: str) -> bool:
        try:
            value = tryte_to_int(transaction, self._begin, self._end)
            return value < self._max and value > self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (min<v<max) filtering!')

    def _larger_than_min_for_str(self, transaction: str) -> bool:
        try:
            return tryte_to_int(transaction, self._begin, self._end) > self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v>min) filtering!')

    def _smaller_than_max_for_str(self, transaction: str) -> bool:
        try:
            return tryte_to_int(transaction, self._begin, self._end) < self._max
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v<max) filtering!')

    def _equal_for_str(self, transaction: str) -> bool:
        try:
            return tryte_to_int(transaction, self._begin, self._end) == self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v=min) filtering!')

    def _range_with_euqal_for_str(self, transaction: str) -> bool:
        try:
            value = tryte_to_int(transaction, self._begin, self._end)
            return value <= self._max and value >= self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (min<=v<=max) filtering!')

    def _equal_to_or_larger_than_min_for_str(self, transaction: str) -> bool:
        try:
            return tryte_to_int(transaction, self._begin, self._end) >= self._min
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v>=min) filtering!')

    def _equal_to_or_smaller_than_max_for_str(self, transaction: str) -> bool:
        try:
            return tryte_to_int(transaction, self._begin, self._end) <= self._max
        except:
            raise ValueError(
                f'Cannot perform {self._name} (v<=max) filtering!')

    def make_filter(self, range_larger_smaller='R', filter_type='str') -> Callable:
        """Make a range filter.

        Parameters
        ----------
        range_larger_smaller_equal : str

            'R' for min < value < max
            'm' for value > min
            'M' for value < max
            'E' for value = min
            'RE' for min <= value <= max
            'mE' for value >= min
            'ME' for value <= max

        filter_type : str
            Set "str" or "dict" for the filter type.

        Returns
        ----------
        The built range filter.

        """
        if filter_type == 'str':
            if range_larger_smaller == 'R':
                return self._range_for_str
            elif range_larger_smaller == 'm':
                return self._larger_than_min_for_str
            elif range_larger_smaller == 'M':
                return self._smaller_than_max_for_str
            elif range_larger_smaller == 'E':
                return self._equal_for_str
            elif range_larger_smaller == 'RE':
                return self._range_with_euqal_for_str
            elif range_larger_smaller == 'mE':
                return self._equal_to_or_larger_than_min_for_str
            elif range_larger_smaller == 'ME':
                return self._equal_to_or_smaller_than_max_for_str
            else:
                raise ValueError(
                    f"Cannot identify {range_larger_smaller} in range filter for str!")
        elif filter_type == "dict":
            if range_larger_smaller == 'R':
                return self._range_for_dict
            elif range_larger_smaller == 'm':
                return self._larger_than_min_for_dict
            elif range_larger_smaller == 'M':
                return self._smaller_than_max_for_dict
            elif range_larger_smaller == 'E':
                return self._equal_for_dict
            elif range_larger_smaller == 'RE':
                return self._range_with_euqal_for_dict
            elif range_larger_smaller == 'mE':
                return self._equal_to_or_larger_than_min_for_dict
            elif range_larger_smaller == 'ME':
                return self._equal_to_or_smaller_than_max_for_dict
            else:
                raise ValueError(
                    f"Cannot identify {range_larger_smaller} in range filter for dict!")
        else:
            raise ValueError(
                f"Cannot identify {filter_type}, please use \"str\" or \"dict\"!")
