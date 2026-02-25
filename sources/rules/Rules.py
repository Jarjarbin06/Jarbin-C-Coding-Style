#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from typing import Callable, Any
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Rules #
RULES: dict[str, str | dict[str, str | dict[str, str | Callable | dict[str, Any]]]] = {}

## C-A - Advanced ##

## C-C - Control Structures ##

## C-F - Functions ##

## C-G - Global Scope ##
try:
    from rules.G import G1, G2, G3, G4, G5, G6

except Exception:
    print(Text("Failed to import G rules").error())

else:
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

    RULES["G"][G1.name] = {
        "info": G1.info,
        "check": G1.check,
        "arguments": {
        }
    }
    RULES["G"][G2.name] = {
        "info": G2.info,
        "check": G2.check,
        "arguments": {
        }
    }
    RULES["G"][G3.name] = {
        "info": G3.info,
        "check": G3.check,
        "arguments": {
        }
    }
    RULES["G"][G4.name] = {
        "info": G4.info,
        "check": G4.check,
        "arguments": {
        }
    }
    RULES["G"][G5.name] = {
        "info": G5.info,
        "check": G5.check,
        "arguments": {
        }
    }
    RULES["G"][G6.name] = {
        "info": G6.info,
        "check": G6.check,
        "arguments": {
        }
    }

## C-H - Header Files ##

## C-L - Layout Inside A Function Scope ##

## C-O - Files Organization ##
try:
    from rules.O import O1, O2, O3, O4

except Exception:
    print(Text("Failed to import O rules").error())

else:
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

    RULES["O"][O1.name] = {
        "info": O1.info,
        "check": O1.check,
        "arguments": {
            "UNAUTHORIZED_EXTENSIONS": O1.UNAUTHORIZED_EXTENSIONS,
            "EXCLUDED_FOLDERS": O1.EXCLUDED_FOLDERS
        }
    }
    RULES["O"][O2.name] = {
        "info": O2.info,
        "check": O2.check,
        "arguments": {
            "AUTHORIZED_EXTENSIONS": O2.AUTHORIZED_EXTENSIONS,
            "INCLUDED_FOLDERS": O2.INCLUDED_FOLDERS
        }
    }
    RULES["O"][O3.name] = {
        "info": O3.info,
        "check": O3.check,
        "arguments": {
        }
    }
    RULES["O"][O4.name] = {
        "info": O4.info,
        "check": O4.check,
        "arguments": {
            "CHECKED_EXTENSIONS": O4.CHECKED_EXTENSIONS,
            "VALID_CHARACTERS": O4.VALID_CHARACTERS
        }
    }

## C-V - Variables And Types ##

## MY - My Rules ##
try:
    from rules.MY import MY1, MY2

except Exception:
    print(Text("Failed to import MY rules").error())

else:
    RULES["MY"] = {
        "name": "MY — My Rules",
        "info": """
MY — My Rules
Every rules made by Jarjarbin06 that can be helpful
"""
    }

    RULES["MY"][MY1.name] = {
        "info": MY1.info,
        "check": MY1.check,
        "arguments": {
            "BANNED_FUNCTIONS": MY1.BANNED_FUNCTIONS
        }
    }
    RULES["MY"][MY2.name] = {
        "info": MY2.info,
        "check": MY2.check,
        "arguments": {
            "BANNED_INCLUDES": MY2.BANNED_INCLUDES
        }
    }

Console.quit(delete_log=True)