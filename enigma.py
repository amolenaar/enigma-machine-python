# vim:sw=4:et:ai
#
# Design constaint: ignored notches.

realAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ROTORS = [
  "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
  "BDFHJLCPRTXVZNYEIWGAKMUSQO"
]

INITIAL_OFFSETS = ( 12, 2, 10 )


def transform_char(char, rotors, offsets):
    """
    """
    rotor = rotors[-1]
    offset = offsets[-1]

def increment_offset(ofs):
    """
    >>> increment_offset((10, 2, 12))
    (10, 2, 13)
    >>> increment_offset((10, 2, 25))
    (10, 2, 0)
    """
    return ofs[:-1] + ((ofs[-1]+1) % 26,)

def transform(message, rotors, offsets):
    ofs = offsets
    for c in message:
        ofs = increment_offset(ofs)
        transform_char(c, rotors, ofs)
