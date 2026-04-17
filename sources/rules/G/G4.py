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
name = f"{category}4"
info = f"""
{language}-{name} - Global variables
Global variables must be avoided as much as possible.
Only global constants should be used.
"""
level = 2

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
RE_VAR = re.compile(r'^\s*(?!static\b)(const\s+)?[a-zA-Z_]\w*\s+\w+\s*(=.*)?;')

# Checker #
def get_global_variable_error(file: str) -> str:

    lines = File.read_file(file)
    cleaned = Transform.C.strip_comments(lines)

    scope = 0

    for index, line in cleaned:

        stripped = line.strip()

        if not stripped:
            continue

        scope += line.count("{")
        scope -= line.count("}")

        if scope != 0:
            continue

        if stripped.startswith("#"):
            continue

        if RE_VAR.match(line):

            if "const" in stripped:
                continue

            return Format.error(
                index,
                line.rstrip("\n"),
                "global variable detected (only const globals allowed)"
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

        if not file.endswith(".c"):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} file valid").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        error = get_global_variable_error(file)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} has forbidden global variable").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} variables valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:
        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "Only global constants should be used"
                f"\n\n{get_global_variable_error(file)}"
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
