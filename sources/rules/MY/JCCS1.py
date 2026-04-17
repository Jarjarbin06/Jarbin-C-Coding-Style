#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
language = "C"
category = "JCCS"
name = f"{category}1"
info = f"""
{language}-{name} - banned functions
Files must not contain any banned functions.
"""
level = 3

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
VAR_BANNED_FUNCTIONS = ""
VAR_BANNED_FUNCTIONS_doc = "Space-separated list of forbidden function names that must not appear in source files."

# Regex #

# Checker #
def get_function_error(file: str, banned_func: str) -> str:

    banned_set = set(banned_func.split())
    file_list_str = File.read_file(file)

    for index, line in Transform.C.strip_comments(file_list_str):

        matches = Parser.C.extract_function_calls(line)

        for func_name in matches:

            if func_name in banned_set:
                clean_line = line.rstrip("\n")
                return Format.error(index, clean_line, f"banned function: {func_name}")

    return ""

def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    global VAR_BANNED_FUNCTIONS
    VAR_BANNED_FUNCTIONS = kwargs.get("VAR_BANNED_FUNCTIONS", VAR_BANNED_FUNCTIONS)

    if isinstance(VAR_BANNED_FUNCTIONS, tuple):
        VAR_BANNED_FUNCTIONS = VAR_BANNED_FUNCTIONS[0]

    # Regex re-compiling #

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

        error = get_function_error(file, VAR_BANNED_FUNCTIONS)

        if error:
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} has a banned function").debug(),
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
                "Banned functions must be avoided at all cost\n\n"
                f"{get_function_error(file, VAR_BANNED_FUNCTIONS)}"
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
