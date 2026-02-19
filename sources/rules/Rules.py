#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from typing import Callable, Any

# Rules #
## C-O ##
from rules.C_O import C_O1, C_O2, C_O3, C_O4

RULES: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]] = {
    "C-O1": {
        "info": C_O1.info,
        "check": C_O1.check,
        "arguments": {
            "UNAUTHORIZED_EXTENSIONS": C_O1.UNAUTHORIZED_EXTENSIONS,
            "EXCLUDED_FOLDERS": C_O1.EXCLUDED_FOLDERS
        }
    },
    "C-O2": {
        "info": C_O2.info,
        "check": C_O2.check,
        "arguments": {
            "AUTHORIZED_EXTENSIONS": C_O2.AUTHORIZED_EXTENSIONS,
            "INCLUDED_FOLDERS": C_O2.INCLUDED_FOLDERS
        }
    },
    "C-O3": {
        "info": C_O3.info,
        "check": C_O3.check,
        "arguments": {
        }
    },
    "C-O4": {
        "info": C_O4.info,
        "check": C_O4.check,
        "arguments": {
            "CHECKED_EXTENSIONS": C_O4.CHECKED_EXTENSIONS,
            "VALID_CHARACTERS": C_O4.VALID_CHARACTERS
        }
    }
}
