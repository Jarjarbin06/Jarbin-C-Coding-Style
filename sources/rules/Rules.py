#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from typing import Callable, Any

# Rules #
from rules.C_O import C_O1, C_O2

RULES: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]] = {
    "C-O1": {
        "check": C_O1.check,
        "arguments": {
            "UNAUTHORIZED_EXTENSIONS": C_O1.UNAUTHORIZED_EXTENSIONS,
            "EXCLUDED_FOLDERS": C_O1.EXCLUDED_FOLDERS
        }
    },
    "C-O2": {
        "check": C_O2.check,
        "arguments": {
            "AUTHORIZED_EXTENSIONS": C_O2.AUTHORIZED_EXTENSIONS,
            "INCLUDED_FOLDERS": C_O2.INCLUDED_FOLDERS
        }
    }
}
