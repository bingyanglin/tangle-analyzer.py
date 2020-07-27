from . import SetFilter
from ..common.const import ADDRESS_B, ADDRESS_E

__all__ = [
    'AddressFilter',
]


class AddressFilter(SetFilter):
    """
    Address filter for transactions.


    Pamameters
    ----------
    address_set : set
        The address set for monitoring.
    """

    def __init__(self, address_set: set) -> None:
        """
        Parameters
        ----------
        address_set : set
            The set of addresses for monitoring.
        """
        super().__init__('address', address_set, ADDRESS_B, ADDRESS_E)
