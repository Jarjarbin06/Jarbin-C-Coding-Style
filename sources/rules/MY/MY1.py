#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
name = "MY1"
info = """
C-MY1 - banned functions
Files must not contain any banned functions.
"""

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

def get_function_error(
        file : str,
        banned_func : str
    ) -> str:

    is_a_comment = False

    with open(file, 'r') as f:
        file_list_str = f.readlines()
    f.close()

    for index in range(len(file_list_str)):
        if "/*" in file_list_str[index]:
            is_a_comment = True

        if "*/" in file_list_str[index]:
            is_a_comment = False

        if not is_a_comment:
            for banned in banned_func.split():
                if f"{banned}(" in file_list_str[index]:
                    return f"line number {index + 1}:\n---\n{file_list_str[index]}{"" if file_list_str[index].endswith("\n") else "\n"}---\nbanned function: {banned}"
    return ""

# Custom Variables #
BANNED_FUNCTIONS = ""

# Checker #
def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    banned_func = kwargs.get("BANNED_FUNCTIONS", BANNED_FUNCTIONS)

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

        if get_function_error(file, banned_func):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} has an banned function").debug(), Text("(invalid)").error().italic())
            return False

        if verbose == 2:
            print(Text(" ").debug(title=True), Text(f"C-{name}: {file} functions valid").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), f"{file}\nBanned functions must be avoided at all cost\n\n{get_function_error(file, banned_func)}"

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
