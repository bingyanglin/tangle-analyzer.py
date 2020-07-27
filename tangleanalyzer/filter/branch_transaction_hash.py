from .base_filter import SetFilter
from ..common.const import BRANCH_B, BRANCH_E

__all__ = [
    'BranchTransactionHashFilter',
]


class BranchTransactionHashFilter(SetFilter):
    """
    Branch transaction hash filter for transactions.


    Pamameters
    ----------
    branch_transaction_hash_set : set
        The branch transaction hash set for monitoring.
    """

    def __init__(self, branch_transaction_hash_set: set) -> None:
        """
        Parameters
        ----------
        branch_transaction_hash_set : set
            The set of branch transaction hashes for monitoring.
        """
        super().__init__('branch_transaction_hash',
                         branch_transaction_hash_set, BRANCH_B, BRANCH_E)
