from typing import Callable
import logging

__all__ = [
    'AddressFilter',
]


class AddressFilter():
    """
    Address filter for transactions


    Attributes
    ----------
    _address_set : set
        The private address set for monitoring

    Methods
    -------
    make_filter() :
        Return the built address filter
    """

    def __init__(self, address_set: set) -> None:
        """
        Parameters
        ----------
        address_set : set
            The set of addresses for monitoring
        """
        self._address_set = address_set

    def _address_filter(self, transaction: dict) -> bool:
        """Address filter

        Parameters
        ----------
        transaction : dict
            The transaction for filtering
        """
        try:
            return transaction['address'] in self._address_set
        except:
            logging.error(
                "Objects for address filtering do not have address item!")

    def make_filter(self) -> Callable:
        """
        Returns
        ----------
        The built address filter.

        """
        return self._address_filter
