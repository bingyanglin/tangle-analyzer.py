from typing import Callable
from ..common.const import BUNDLE_HASH_B, BUNDLE_HASH_E
import logging

__all__ = [
    'BundleFilter',
]


class BundleFilter():
    """
    Bundle filter for transactions


    Attributes
    ----------
    _bundle_filter : set
        The address set for monitoring

    Methods
    -------
    make_filter()
        Return the built address filter
    """

    def __init__(self, bundle_set: set) -> None:
        """
        Parameters
        ----------
        bundle_set : set
            The set of bundles for monitoring
        """
        self._bundle_set = bundle_set

    def _bundle_filter(self, transaction: dict) -> bool:
        """Bundle filter

        Parameters
        ----------
        transaction : dict
            The transaction for filtering

        """
        try:
            return transaction['bundle_hash'] in self._bundle_set
        except:
            logging.error(
                "Objects for bundle filtering do not have bundle item!")

    def _bundle_filter_str(self, transaction: str) -> bool:
        """Bundle filter

        Parameters
        ----------
        transaction : str
            The transaction for filtering

        """
        try:
            return transaction[BUNDLE_HASH_B:BUNDLE_HASH_E] in self._bundle_set
        except:
            logging.error(f"Cannot identify bundle in trytes: {transaction}!")

    def make_filter(self) -> Callable:
        """
        Returns
        ----------
        The built bundle filter.

        """
        return self._bundle_filter_str
