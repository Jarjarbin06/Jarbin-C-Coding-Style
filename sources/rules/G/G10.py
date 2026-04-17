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
name = f"{category}10"
info = f"""
{language}-{name} - Inline assembly
Inline assembly must never be used.
Programming in C must be done... in C.
"""
level = 3

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
RE_ASM = re.compile(r'\b(__asm__|asm)\s*\(')

# Checker #
def get_line_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for index, line in cleaned:

        stripped = line.strip()

        if not stripped:
            continue

        if RE_ASM.search(line) or stripped.startswith("asm"):
            return Format.error(
                index,
                line.rstrip("\n"),
                "inline assembly detected"
            )

    return ""

def check(paths, **kwargs) -> list[RuleError] | None:

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

        error = get_line_error(file)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} has inline assembly").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} file valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "Inline assembly must never be used.\n\n"
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
