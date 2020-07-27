from typing import Callable
import logging

__all__ = [
    'SetFilter',
]


class SetFilter():
    """
    SetFilter for transactions.


    Attributes
    ----------
    inclusive_set : set
        The inclusive set contains a transaction field to reserve.

    Methods
    -------
    make_filter() :
        Return the built set filter.
    """

    def __init__(self, name: str, inclusive_set: set, begin: int, end: int) -> None:
        """
        Parameters
        ----------
        name : str
            The filter name.

        inclusive_set : set
            The set of a transaction field for monitoring.

        begin : int
            The begin location of the field in the transaction string.

        end : int
            The end location of the field in the transaction string.
        """
        self._name = name
        self._inclusive_set = inclusive_set
        self._begin = begin
        self._end = end

    def __str__(self):
        return f'{self._name}: {self._inclusive_set}\nBegin, End: {self._begin}, {self._end}'

    def _filter_for_dict(self, transaction: dict) -> bool:
        """Inclusive filter for transaction dict.

        Parameters
        ----------
        transaction : dict
            The transaction for filtering.

        Return
        ----------
        exist : bool
            Exist or not.

        """
        try:
            return transaction[self._name] in self._inclusive_set
        except:
            raise ValueError(
                f"Objects for {self._name} filtering do not have the field!")

    def _filter_for_str(self, transaction: str) -> bool:
        """Inclusive filter on tryte string directly.

        Parameters
        ----------
        transaction : str
            The transaction for filtering.
        """
        try:
            return transaction[self._begin:self._end] in self._inclusive_set
        except:
            raise ValueError(
                f"Cannot identify {self._name} in trytes {transaction}!")

    def make_filter(self, filter_type="str") -> Callable:
        """
        Parameters
        ----------
        filter_type : str
            Set "str" or "dict" for the filter type.


        Returns
        ----------
        The built set filter.

        """
        if filter_type == "str":
            return self._filter_for_str
        elif filter_type == "dict":
            return self._filter_for_dict
        else:
            ValueError(
                f"Cannot identify {filter_type}, please use \"str\" or \"dict\"!")
