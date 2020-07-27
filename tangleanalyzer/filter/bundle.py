from .base_filter import SetFilter
from ..common.const import BUNDLE_HASH_B, BUNDLE_HASH_E

__all__ = [
    'BundleFilter',
]


class BundleFilter(SetFilter):
    """
    Bundle filter for transactions.


    Pamameters
    ----------
    bundle_set : set
        The bundle set for monitoring.
    """

    def __init__(self, bundle_set: set) -> None:
        """
        Parameters
        ----------
        bundle_set : set
            The set of bundles for monitoring.
        """
        super().__init__('bundle_hash', bundle_set, BUNDLE_HASH_B, BUNDLE_HASH_E)
