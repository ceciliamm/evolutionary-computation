"""Utilities."""


def int_to_gray(n: int, l: int = 8) -> str:
    """Return Gray Code representation of given integer."""
    n = n ^ (n >> 1)
    return bin(n)[2:].zfill(l)


def gray_to_int(s: str) -> int:
    """Given a zero left-padded gray code representation of an int, return int value."""
    s = s.lstrip('0')
    n = int(s, 2)
    mask = n >> 1
    while mask != 0:
        n = n ^ mask
        mask = mask >> 1
    return n
