from .base_filter import SetFilter
from ..common.const import SIGNATURE_B, SIGNATURE_E

__all__ = [
    'SignatureMessageFragmentFilter',
]


class SignatureMessageFragmentFilter(SetFilter):
    """
    Signature message fragment filter for transactions.


    Pamameters
    ----------
    signature_message_fragment_set : set
        The signature message fragment set for monitoring.
    """

    def __init__(self, signature_message_fragment_set: set) -> None:
        """
        Parameters
        ----------
        signature_message_fragment_set : set
            The set of signature message fragments for monitoring.
        """
        super().__init__('signature_message_fragment',
                         signature_message_fragment_set, SIGNATURE_B, SIGNATURE_E)
