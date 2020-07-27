from .base_filter import SetFilter
from ..common.const import TRUNK_B, TRUNK_E

__all__ = [
    'TrunkTransactionHashFilter',
]


class TrunkTransactionHashFilter(SetFilter):
    """
    Branch transaction hash filter for transactions.


    Pamameters
    ----------
    trunk_transaction_hash_set : set
        The trunk transaction hash set for monitoring.
    """

    def __init__(self, trunk_transaction_hash_set: set) -> None:
        """
        Parameters
        ----------
        trunk_transaction_hash_set : set
            The set of trunk transaction hashes for monitoring.
        """
        super().__init__('trunk_transaction_hash',
                         trunk_transaction_hash_set, TRUNK_B, TRUNK_E)
