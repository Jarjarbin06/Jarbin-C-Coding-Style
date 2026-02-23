#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
name = "G6"
info = """
C-G6 - Line endings
Line endings must be done in UNIX style (with \"\\n\"), and must never end with a backslash (\"\\\").
"""

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Checker #
def get_line_error(
        file : str
    ) -> str:

    with open(file, 'r') as f:
        file_list_str = f.readlines()
    f.close()

    for index in range(len(file_list_str)):
        if not file_list_str[index].endswith("\n"):
            return f"line number {index + 1}:\n---\n{file_list_str[index]}{"" if file_list_str[index].endswith("\n") else "\n"}---\nline not ending with \\n"
    return ""

def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: variables set").debug())

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        if not (file.endswith(".c") or file.endswith(".h")):
            if verbose == 2:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} not checked").debug(), Text("(skip)").info().italic())
            return True

        if get_line_error(file):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} has an invalid line ending").debug(), Text("(invalid)").error().italic())
            return False

        if verbose == 2:
            print(Text(" ").debug(title=True), Text(f"C-{name}: {file} line ending valid").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), f"{file}\nLine endings must be done in UNIX style (with \"\\n\"), and must never end with a backslash (\"\\\")\n\n{get_line_error(file)}"

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
