from typing import Callable
from . import SetFilter
from ..common.const import TRANSACTION_HASH_LENGTH


__all__ = [
    'TransactionHashFilter',
]


class TransactionHashFilter(SetFilter):
    """
    Transaction hash filter for transactions.


    Pamameters
    ----------
    transaction_hash_set : set
        The transaction hash set for monitoring.
    """

    def __init__(self, transaction_hash_set: set) -> None:
        """
        Parameters
        ----------
        transaction_set : set
            The set of transactions for monitoring.
        """
        super().__init__('hash', transaction_hash_set, -TRANSACTION_HASH_LENGTH, None)
