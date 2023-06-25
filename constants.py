import string
from dataclasses import dataclass
from random import choice

ARROWS = {
    2063660802: 'LEFT',
    8124162: 'LEFT',
    97: 'LEFT',  # a
    2080438019: 'RIGHT',
    8189699: 'RIGHT',
    33554532: 'RIGHT',  # d
    8320768: 'UP',
    8255233: 'DOWN',
    7730984: 'DELETE',
    3342463: 'DELETE',
    16777331: 'DELETE',
    855638143: 'DELETE',  # s
    2031727: 'OPEN',
    1031862526: 'OPEN',
    520093807: 'OPEN',
    541065301: 'UNDO',
    536871029: 'UNDO',  # u
    218103927: 'UNDO',  # w
    822083616: 'FIGURE',  # SPACEBAR
    922810622: 'CMD',  # CMD
    201326705: 'QUIT',
}


@dataclass(frozen=True)
class CONSTANTS:
    teaching: str = "teaching"
    finding: str = "finding"
    unknown: str = "unknown"
    uncertain: str = "uncertain"


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(choice(letters) for _ in range(length))
    return result_str
