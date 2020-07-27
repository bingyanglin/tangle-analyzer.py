from .base_filter import SetFilter
from ..common.const import OBSOLETE_TAG_B, OBSOLETE_TAG_E

__all__ = [
    'ObsoleteTagFilter',
]


class ObsoleteTagFilter(SetFilter):
    """
    Obsolete filter for transactions


    Pamameters
    ----------
    obsolete_tag_set : set
        The obsolete tag set for monitoring.
    """

    def __init__(self, obsolete_tag_set: set) -> None:
        """
        Parameters
        ----------
        obsolete_tag_set : set
            The set of obsolete tags for monitoring.
        """
        super().__init__('legacy_tag', obsolete_tag_set, OBSOLETE_TAG_B, OBSOLETE_TAG_E)
