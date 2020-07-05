from typing import Callable
from ..common.const import TRANSACTION_HASH_LENGTH
import logging

__all__ = [
    'TransactionFilter',
]


class TransactionFilter():
    """
    Transaction filter for transactions


    Attributes
    ----------
    _transaction_set : set
        The private transaction set for monitoring

    Methods
    -------
    make_filter()
        Return the built transaction filter

    """

    def __init__(self, transaction_set: set) -> None:
        """
        Parameters
        ----------
        transaction_set : set
            The set of transactions for monitoring

        """
        self._transaction_set = transaction_set

    def _transaction_filter(self, transaction: dict) -> bool:
        """Transaction filter

        Parameters
        ----------
        transaction : dict
            The transaction for filtering

        """
        try:
            return transaction['hash'] in self._transaction_set
        except:
            logging.error(
                "Objects for transaction filtering do not have transaction item!")

    def _transaction_filter_str(self, transaction: str) -> bool:
        """Transaction filter

        Parameters
        ----------
        transaction : str
            The transaction for filtering

        """
        try:
            return transaction[-TRANSACTION_HASH_LENGTH:] in self._transaction_set
        except:
            logging.error(f"Cannot identify transaction hash: {transaction}!")

    def make_filter(self) -> Callable:
        """Transaction filter generation function.

        Returns
        ----------
        The built transaction filter.

        """
        return self._transaction_filter_str
