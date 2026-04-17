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
name = f"{category}9"
info = f"""
{language}-{name} - Constant values
Non-trivial constant values should be defined either as a global constant or as a macro.
This greatly helps you when you want to modify an important value in your program, because you do not
need to find all occurences of this value scattered throughout your code, and only need to change it in one
place.
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
VAR_AUTHORIZED_VALUES = "NULL"
VAR_AUTHORIZED_VALUES_doc = "Allowed hard coded values"

# Regex #
RE_ARRAY_SIZE = re.compile(r'\[\s*([0-9]+)\s*\]')
RE_ASSIGN = re.compile(r'^\s*[^#\s][^=]*=\s*(.+?);?\s*$')

# Checker #
def get_line_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for index, line in cleaned:

        stripped = line.strip()

        if not stripped:
            continue

        if "=" in line:

            match = RE_ASSIGN.match(line)
            if match:

                value = match.group(1).strip().replace(" ", "")

                is_literal = (
                    re.fullmatch(r"[0-9]+(\.[0-9]+)?", value)
                    or "+" in value
                    or "-" in value
                )

                if is_literal:
                    valid = False
                    for authed_val in VAR_AUTHORIZED_VALUES.split():
                        if value == authed_val:
                            valid = True
                            break

                    if not valid:
                        return Format.error(
                            index,
                            line.rstrip("\n"),
                            "hard coded constant value detected"
                        )

        match_array = RE_ARRAY_SIZE.search(line)
        if match_array:

            value = match_array.group(1)

            valid = False
            for authed_val in VAR_AUTHORIZED_VALUES.split():
                if value == authed_val:
                    valid = True
                    break

            if not valid:
                return Format.error(
                    index,
                    line.rstrip("\n"),
                    "hard coded array size detected"
                )

    return ""

def check(paths, **kwargs) -> list[RuleError] | None:

    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    global VAR_AUTHORIZED_VALUES
    VAR_AUTHORIZED_VALUES = kwargs.get("VAR_AUTHORIZED_VALUES", VAR_AUTHORIZED_VALUES)

    if isinstance(VAR_AUTHORIZED_VALUES, tuple):
        VAR_AUTHORIZED_VALUES = VAR_AUTHORIZED_VALUES[0]

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
                    Text(f"C-{name}: {file} has hard coded value").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} values valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "Non-trivial constant values should be defined either as a global constant or as a macro.\n\n"
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
