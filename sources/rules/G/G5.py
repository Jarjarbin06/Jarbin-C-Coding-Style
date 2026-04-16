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
name = f"{category}5"
info = f"""
{language}-{name} - include
include directives must only include C header (.h) files.
"""
level = "MAJOR"

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
RE_INCLUDE = re.compile(r'^\s*#include\s+["<](.+)[">]')

# Checker #
def get_include_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for index, line in cleaned:

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("//"):
            continue

        match = RE_INCLUDE.match(line)
        if not match:
            continue

        include_name = match.group(1)

        if not include_name.endswith(".h"):

            return Format.error(
                index,
                line.rstrip("\n"),
                "include directive must only include .h files"
            )

    return ""

def check(paths, **kwargs) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
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

        error = get_include_error(file)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} has invalid include").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} includes valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "Include directives must only include C header (.h) files"
                f"\n\n{get_include_error(file)}"
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
