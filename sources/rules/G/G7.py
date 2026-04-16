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
name = f"{category}7"
info = f"""
{language}-{name} - Trailing spaces
No trailing spaces must be present at the end of a line.
"""
level = "MINOR"

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
RE_TRAILING_SPACE = re.compile(r'[ \t]+$')

# Checker #
def get_line_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for index, line in cleaned:

        if not line:
            continue

        if RE_TRAILING_SPACE.search(line.rstrip("\n")):
            return Format.error(
                index,
                line.rstrip("\n"),
                "line contains trailing spaces"
            )

    return ""

def check(paths, **kwargs) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #

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

        error = get_line_error(file)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} has trailing spaces").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} no trailing spaces").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "No trailing spaces must be present at the end of a line\n\n"
                f"{get_line_error(file)}"
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
