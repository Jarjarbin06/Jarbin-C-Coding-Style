#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from typing import Callable, Any

# Rules #
RULES: dict = {}

## C-A - Advanced ##

## C-C - Control Structures ##

## C-F - Functions ##

## C-G - Global Scope ##
from rules.G import G1, G2

RULES["G"] = {
    "name": "C-G — Global Scope",
    "info": """
C-G — Global Scope
Multiline statements are allowed but must never use backslashes for line breaks.  
Language extensions and non-standard features are forbidden.  
Files must start with the official Epitech header and functions must be separated by exactly one blank line.  
Preprocessor directives use 4-space indentation (no tabs) and only include .h files.  
Avoid global variables (except const), enforce UNIX line endings, no trailing spaces, controlled empty lines,
defined constants, and no inline assembly.
"""
}

RULES["G"]["C-G1"] = {
    "info": G1.info,
    "check": G1.check,
    "arguments": {
    }
}

RULES["G"]["C-G2"] = {
    "info": G2.info,
    "check": G2.check,
    "arguments": {
    }
}

## C-H - Header Files ##

## C-L - Layout Inside A Function Scope ##

## C-O - Files Organization ##
from rules.O import O1, O2, O3, O4

RULES["O"] = {
    "name": "C-O — Files Organization",
    "info": """
C-O — Files Organization
Keep your repository clean and organized.
Avoid compiled files (.o, .a, .so, ...), temporary files (*~, #*#), and unnecessary clutter.
Only use .c and .h extensions for source files.
Each source file should represent a single logical entity, grouping related functions.
Limit files to 10 functions (max 5 non-static) before splitting into sub-entities.
File and folder names must be clear, descriptive, in English, and follow snake_case conventions.
"""
}

RULES["O"]["C-O1"] = {
    "info": O1.info,
    "check": O1.check,
    "arguments": {
        "UNAUTHORIZED_EXTENSIONS": O1.UNAUTHORIZED_EXTENSIONS,
        "EXCLUDED_FOLDERS": O1.EXCLUDED_FOLDERS
    }
}
RULES["O"]["C-O2"] = {
    "info": O2.info,
    "check": O2.check,
    "arguments": {
        "AUTHORIZED_EXTENSIONS": O2.AUTHORIZED_EXTENSIONS,
        "INCLUDED_FOLDERS": O2.INCLUDED_FOLDERS
    }
}
RULES["O"]["C-O3"] = {
    "info": O3.info,
    "check": O3.check,
    "arguments": {
    }
}
RULES["O"]["C-O4"] = {
    "info": O4.info,
    "check": O4.check,
    "arguments": {
        "CHECKED_EXTENSIONS": O4.CHECKED_EXTENSIONS,
        "VALID_CHARACTERS": O4.VALID_CHARACTERS
    }
}

## C-V - Variables And Types ##
