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
name = f"{category}8"
info = f"""
{language}-{name} - Leading/trailing lines
No leading empty lines must be present.
No more than 1 trailing empty line must be present.
Make sure you also follow the C-A3 rule.
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
RE_LEADING_EMPTY = re.compile(r'^\s*\n')
RE_TRAILING_EMPTY = re.compile(r'\n\s*\n\s*$')

# Checker #
def get_line_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for index, line in cleaned:
        if line.strip() != "":
            break
        return Format.error(
            index,
            line.rstrip("\n"),
            "leading empty line detected"
        )

    empty_count = 0

    for index in range(len(cleaned) - 1, -1, -1):
        if cleaned[index][1].strip() == "":
            empty_count += 1
        else:
            break

    if empty_count > 1:
        index = len(cleaned) - 1
        return Format.error(
            index,
            cleaned[index][1].rstrip("\n"),
            "too many trailing empty lines"
        )

    return ""

def check(paths, **kwargs) -> list[RuleError] | None:

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
                    Text(f"C-{name}: {file} invalid leading/trailing lines").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} lines valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "No leading empty lines must be present.\n"
                "No more than 1 trailing empty line must be present.\n\n"
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
