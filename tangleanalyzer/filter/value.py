from .base_filter import RangeFilter
from ..common.const import VALUE_B, VALUE_E

__all__ = [
    'ValueFilter',
]


class ValueFilter(RangeFilter):
    """
    Value filter for transactions


    Attributes
    ----------
    min : int
        The private minimum value for filtering
    max : int
        The private maximum value for filtering

    Methods
    -------
    make_filter()
        Return the built value filter
    """

    def __init__(self, min: int, max: int) -> None:
        """
        Parameters
        ----------
        min : int
            The minimum value in transactions for monitoring
        max : int
            The maximum value in transactions for monitoring
        """
        super().__init__('value', min, max, VALUE_B, VALUE_E)
