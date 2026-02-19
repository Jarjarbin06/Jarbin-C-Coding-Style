#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from typing import Callable, Any

# Rules #
RULES: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]] = {}

## C-A - Advanced ##

## C-C - Control Structures ##

## C-F - Functions ##

## C-G - Global Scope ##
from rules.G import G1

RULES["C-G1"] = {
    "info": G1.info,
    "check": G1.check,
    "arguments": {
    }
}
## C-H - Header Files ##

## C-L - Layout Inside A Function Scope ##

## C-O - Files Organization ##
from rules.O import O1, O2, O3, O4

RULES["C-O1"] = {
    "info": O1.info,
    "check": O1.check,
    "arguments": {
        "UNAUTHORIZED_EXTENSIONS": O1.UNAUTHORIZED_EXTENSIONS,
        "EXCLUDED_FOLDERS": O1.EXCLUDED_FOLDERS
    }
}
RULES["C-O2"] = {
    "info": O2.info,
    "check": O2.check,
    "arguments": {
        "AUTHORIZED_EXTENSIONS": O2.AUTHORIZED_EXTENSIONS,
        "INCLUDED_FOLDERS": O2.INCLUDED_FOLDERS
    }
}
RULES["C-O3"] = {
    "info": O3.info,
    "check": O3.check,
    "arguments": {
    }
}
RULES["C-O4"] = {
    "info": O4.info,
    "check": O4.check,
    "arguments": {
        "CHECKED_EXTENSIONS": O4.CHECKED_EXTENSIONS,
        "VALID_CHARACTERS": O4.VALID_CHARACTERS
    }
}

## C-V - Variables And Types ##
