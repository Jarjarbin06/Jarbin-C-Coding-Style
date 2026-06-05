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
name = f"{category}2"
info = f"""
{language}-{name} - Separation of functions
Inside a source file, implementations of functions must be separated by one and only one empty line.
"""
level = 1

# Imports #
import jarbin_toolkit_console as Console

from utils.error import RuleError
from utils.file import File
from utils.transform import Transform
from utils.format import Format

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Checker #
def get_line_error(file: str) -> str:

    lines = File.read_file(file)

    for index, line in Transform.C.strip_comments(lines):

        if line.strip() == "}":

            if index + 2 >= len(lines):
                continue

            next_line = lines[index + 1]
            next_next_line = lines[index + 2]

            if next_line.strip().startswith("#"):
                continue

            if not (next_line == "\n" and next_next_line != "\n"):

                return Format.error(
                    (index, index + 2),
                    line.rstrip("\n") + "\n" +
                    next_line.rstrip("\n") + "\n" +
                    next_next_line.rstrip("\n"),
                    "there must be exactly one empty line between functions"
                )

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

        if not file.endswith(".c"):
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
                    Text(f"C-{name}: {file} function separation invalid").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} function separation valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    # Main loop #
    for file in paths:

        try:
            assert check_file_ext(file), (
                f"{file}\n"
                "Inside a source file, implementations of functions must be separated by one and only one empty line\n\n"
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
