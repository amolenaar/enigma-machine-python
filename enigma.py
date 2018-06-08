# vim:sw=4:et:ai
#
# Design constaint: ignored notches.

#ROTOT_BASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ROTORS = [
  "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
  "BDFHJLCPRTXVZNYEIWGAKMUSQO"
]

REFLECTOR = "ABCDEFGDIJKGMKMIEBFTCVVJAT"

INITIAL_OFFSETS = 'MCK'

NOTCHES = 'VEQ'


def to_index(s):
    """
    >>> to_index("BDFHJLCPRTXVZNYEIWGAKMUSQO")
    [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
    """
    return map(lambda c: ord(c) - ord('A'), s)


def to_chars(s):
    """
    >>> to_chars([1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21])
    ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V']
    """
    return map(lambda c: chr(ord('A') + c), s)


def reflect(offset):
    """
    >>> reflect(0)
    24
    >>> reflect(23)
    9
    """
    return (REFLECTOR * 2).index(REFLECTOR[offset % 26], (offset % 26) + 1) % len(REFLECTOR)


def encode_left(offset, rotor):
    """
    >>> encode_left(14, to_index("BDFHJLCPRTXVZNYEIWGAKMUSQO"))
    24
    >>> encode_left(32, to_index("BDFHJLCPRTXVZNYEIWGAKMUSQO"))
    2
    """
    return rotor[offset % 26]


def encode_right(offset, rotor):
    """
    >>> encode_right(4, to_index("BDFHJLCPRTXVZNYEIWGAKMUSQO")) # 4 == 'E'
    15
    >>> encode_right(16, to_index("BDFHJLCPRTXVZNYEIWGAKMUSQO")) # 16 == 'Q'
    24
    >>> encode_right(25, to_index("BDFHJLCPRTXVZNYEIWGAKMUSQO")) # 16 == 'Q'
    12
    """
    return rotor.index(offset % 26)


def transform_char(index, rotors, offsets, drift=0):
    """
    >>> transform_char(4, map(to_index, ["BDFHJLCPRTXVZNYEIWGAKMUSQO"]), to_index('K'))
    7
    >>> transform_char(22, map(to_index, ["BDFHJLCPRTXVZNYEIWGAKMUSQO"]), to_index('K'))
    23
    """
    pos = offsets and offsets[-1] or 0

    offset = pos - drift

    index = index + offset

    if not rotors:
        index = reflect(index)
    else:
        rotor = rotors[-1]
    
        index = encode_left(index, rotor)
        index = transform_char(index, rotors[:-1], offsets[:-1], pos)
        index = encode_right(index, rotor)

    return (index - offset) % 26


def increment_offset(ofs):
    """
    >>> to_chars( increment_offset(to_index('KCM')) )
    ['K', 'C', 'N']
    >>> to_chars( increment_offset(to_index(('K', 'C', 'Z'))))
    ['K', 'C', 'A']
    >>> to_chars( increment_offset(to_index(('K', 'A', 'Z'))))
    ['K', 'A', 'A']
    """
    # TODO: keep in mind notches
    ofs = ofs[:-1] + [(ofs[-1]+1) % 26]
    return ofs


def transform(message, rotors, offsets):
    """
    >>> transform("ENIGMA REVEALED", ROTORS, INITIAL_OFFSETS)
    QMJIDO MZWZJDMG
    >>> transform("QMJIDO MZWZJDMG", ROTORS, INITIAL_OFFSETS)
    ENIGMA REVEALED
    """
    ofs = to_index(offsets)
    output = []
    for c in to_index(message.upper()):
        if 0 <= c <= 25:
            ofs = increment_offset(ofs)
            output.append(transform_char(c, map(to_index, rotors), ofs))
        else:
            output.append(c)
    print "".join(to_chars(output))

