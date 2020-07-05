from iota import TryteString


def tryte_to_int(tryte, begin, end) -> int:
    """Convert tryte to int

        Parameters
        ----------
        tryte : binary str
            The tryte to calculate
        begin : int
            The begin location of the tryte
        begin : int
            The end location of the tryte

        Returns:
        ----------
        value : int
            The int value

    """
    tryte = TryteString(tryte[begin: end]).as_integers()
    v = 0
    for power, t in enumerate(tryte):
        v += t*(27 ** power)
    return v
