from typing import Callable
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

    def make_filter(self) -> Callable:
        """
        Returns
        ----------
        The built tag filter.

        """
        return self._tag_filter
