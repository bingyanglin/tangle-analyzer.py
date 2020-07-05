from typing import Callable
from ..common.const import TAG_B, TAG_E
import logging

__all__ = [
    'TagFilter',
]


class TagFilter():
    """
    Tag filter for transactions


    Attributes
    ----------
    _tag_set : set
        The private tag set for monitoring

    Methods
    -------
    make_filter()
        Return the built tag filter

    """

    def __init__(self, tag_set: set) -> None:
        """
        Parameters
        ----------
        tag_set : set
            The set of tags for monitoring

        """
        self._tag_set = tag_set

    def _tag_filter(self, transaction: dict) -> bool:
        """Tag filter

        Parameters
        ----------
        transaction : dict
            The transaction for filtering

        """
        try:
            return transaction['tag'] in self._tag_set
        except:
            logging.error("Objects for tag filtering do not have tag item!")

    def _tag_filter_str(self, transaction: str) -> bool:
        """Tag filter

        Parameters
        ----------
        transaction : str
            The transaction for filtering

        """
        try:
            return transaction[TAG_B:TAG_E] in self._tag_set
        except:
            logging.error(f"Cannot identify tag in trytes: {transaction}!")

    def make_filter(self) -> Callable:
        """
        Returns
        ----------
        The built tag filter.

        """
        return self._tag_filter_str
