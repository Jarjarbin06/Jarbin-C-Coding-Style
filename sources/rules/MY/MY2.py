#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
language = "C"
category = "MY"
name = f"{category}2"
info = f"""
{language}-{name} - banned includes
Files must not contain any banned includes.
"""
level = "FATAL"

# Imports #
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError
from utils.file import File
from utils.transform import Transform
from utils.parser import Parser
from utils.format import Format

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
BANNED_INCLUDES = ""
BANNED_INCLUDES_doc = "Space-separated list of forbidden C header files (without or with .h extension)."

# Regex #

# Checker #
def get_include_error(file: str, banned_include: str) -> str:

    banned_set = set(banned_include.split())
    file_list = File.read_file(file)

    for index, line in Transform.C.strip_comments(file_list):

        includes = Parser.C.extract_includes(line)

        for include_name in includes:

            include_base = include_name.replace(".h", "")

            if include_name in banned_set or include_base in banned_set:
                clean_line = line.rstrip("\n")
                return Format.error(
                    index,
                    clean_line,
                    f"banned include: {include_name}"
                )

    return ""

def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    global BANNED_INCLUDES
    BANNED_INCLUDES = kwargs.get("BANNED_INCLUDES", BANNED_INCLUDES)

    if isinstance(BANNED_INCLUDES, tuple):
        BANNED_INCLUDES = BANNED_INCLUDES[0]

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

    # Regex re-compiling #

    # Custom check #
    def check_file_ext(file: str) -> bool:

        if not (file.endswith(".c") or file.endswith(".h")):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} file valid").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        error = get_include_error(file, BANNED_INCLUDES)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} has a banned include").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"MY-{name}: {file} file valid").debug(),
                Text("(valid)").valid().italic()
            )
        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "Banned includes must be avoided at all cost\n\n"
                f"{get_include_error(file, BANNED_INCLUDES)}"
            )

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error), level=level))

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: ending check").debug(),
            Text(f"({len(errors)} errors found)").error().italic()
            if errors else Text("(no error)").valid().italic()
        )

    return errors if errors else None
