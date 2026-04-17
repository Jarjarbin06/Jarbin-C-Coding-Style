#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
language = "C"
category = "G"
name = f"{category}3"
info = f"""
{language}-{name} - Indentation of preprocessor directives
The preprocessor directives must be indented according to the level of indirection.
"""
level = 1

# Imports #
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError
from utils.file import File
from utils.transform import Transform
from utils.format import Format

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Regex #
RE_DIRECTIVE = re.compile(r'^\s*#')
RE_IF = re.compile(r'^\s*#(if|ifdef|ifndef)\b')
RE_ENDIF = re.compile(r'^\s*#endif\b')

# Checker #
def get_indentation_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    indentation_level = 0

    for index, line in cleaned:

        stripped = line.lstrip(" ")

        if not stripped:
            continue

        if RE_ENDIF.match(stripped):
            indentation_level = max(0, indentation_level - 1)

        if RE_DIRECTIVE.match(stripped):

            expected = "    " * indentation_level
            actual = line[:len(line) - len(stripped)]

            if actual != expected:
                return Format.error(
                    index,
                    line.rstrip("\n"),
                    f"indentation level must be {indentation_level}"
                )

        if RE_IF.match(stripped):
            indentation_level += 1

    return ""

def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    errors = []
    verbose = kwargs.get("verbose", 0)

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

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

        error = get_indentation_error(file)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} bad preprocessor indentation").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} indentation valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:
        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "The preprocessor directives must be indented according to the level of indirection\n\n"
                f"{get_indentation_error(file)}"
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
