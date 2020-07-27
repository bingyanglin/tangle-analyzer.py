from .base_filter import SetFilter
from ..common.const import NONCE_B, NONCE_E

__all__ = [
    'NonceFilter',
]


class NonceFilter(SetFilter):
    """
    Nonce filter for transactions.


    Pamameters
    ----------
    nonce_set : set
        The nonce set for monitoring.
    """

    def __init__(self, nonce_set: set) -> None:
        """
        Parameters
        ----------
        nonce_set : set
            The set of nonces for monitoring.
        """
        super().__init__('nonce', nonce_set, NONCE_B, NONCE_E)
