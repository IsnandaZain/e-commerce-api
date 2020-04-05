import re
# regex validation format YYYY-MM-DD
from typing import List

from myshop.exceptions import BadRequest

yyyy_mm_dd = re.compile(
    r"""^[0-9]{4}   # YYYY
        -           # -
        [0-1][0-9]  # MM
        -           # -
        [0-3][0-9]  # DD""", re.VERBOSE)

# regex email pattern
email = re.compile(
    r"""(^[a-zA-Z0-9_.+-]+ # username
        @                  # @
        [a-zA-Z0-9-]+      # domain
        \.                 # .
        [a-zA-Z0-9-.]+$)   # ext""", re.VERBOSE)

# username pattern
username = re.compile(r"^[a-zA-Z0-9_]{3,35}$")