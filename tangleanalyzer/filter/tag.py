from .base_filter import SetFilter
from ..common.const import TAG_B, TAG_E


__all__ = [
    'TagFilter',
]


class TagFilter(SetFilter):
    """
    Tag filter for transactions


    Pamameters
    ----------
    tag_set : set
        The tag set for monitoring.
    """

    def __init__(self, tag_set: set) -> None:
        """
        Parameters
        ----------
        tag_set : set
            The set of tags for monitoring.
        """
        super().__init__('tag', tag_set, TAG_B, TAG_E)
