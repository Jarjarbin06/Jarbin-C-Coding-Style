#############################
###                       ###
###         JCCS          ###
###                       ###
#############################

# INFO #
# L: language
# C: Category
# R: rule number
# LVL: infraction level = INFO | MINOR | MAJOR | FATAL
language = "L"
category = "C"
name = f"{category}R"
info = f"""
{language}-{name} - Rule title
Short description of the rule behavior.
"""
level = "LVL"

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
MY_VAR = ""
MY_VAR_doc = "Short description of this variable."

# Regex #
RE_MY_PATTERN = re.compile(r"...")

# Checker #
def get_content_error(file: str) -> str:
    """
    File content analysis only (NO path logic here)
    """

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    for i, line in cleaned:

        stripped = line.strip()
        if not stripped:
            continue

        if RE_MY_PATTERN.search(line):

            return Format.error(
                i,
                line.rstrip("\n"),
                "rule violation detected"
            )

    return ""

def check(paths, **kwargs) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables override
    global MY_VAR
    MY_VAR = kwargs.get("MY_VAR", MY_VAR)

    if isinstance(MY_VAR, tuple):
        MY_VAR = MY_VAR[0]

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

    # File filter (PATH / EXTENSION logic ONLY)
    def check_file(file: str) -> bool:

        if not (file.endswith(".c") or file.endswith(".h")):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} file no checked").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        if get_content_error(file):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: violation found").debug(),
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

    # Main loop
    for file in paths:
        try:
            assert check_file(file), (
                f"{file}\n"
                "Rule violation detected\n\n"
                f"{get_content_error(file)}"
            )

        except AssertionError as error:
            errors.append(RuleError(f"{category}-{name}", str(error), level=level))

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: ending check").debug(),
            (
                Text(f"({len(errors)} errors found)").error().italic()
                if errors else
                Text("(no error)").valid().italic()
            )
        )

    return errors if errors else None