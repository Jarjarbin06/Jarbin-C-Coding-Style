#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
name = "G5"
info = """
C-G5 - include
include directives must only include C header (.h) files.
"""

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Checker #
def get_include_error(
        file : str
    ) -> str:

    is_a_comment = False
    is_a_function = False

    with open(file, 'r') as f:
        file_list_str = f.readlines()
    f.close()

    for index in range(len(file_list_str)):
        if "/*" in file_list_str[index]:
            is_a_comment = True

        if "*/" in file_list_str[index]:
            is_a_comment = False

        if (not is_a_function or is_a_comment) and "{" in file_list_str[index]:
            is_a_function = True

        if is_a_function and file_list_str[index].replace(" ", "") == "}\n":
            is_a_function = False

        if (not (is_a_comment or is_a_function)) and (not file_list_str[index].replace(" ", "").startswith("//")) and file_list_str[index] != "\n":
            if file_list_str[index].replace(" ", "").startswith("#include") and not ".h" in file_list_str[index]:
                return f"line number {index + 1}:\n---\n{file_list_str[index]}{"" if file_list_str[index].endswith("\n") else "\n"}---\ninclude directive not including a \".h\" file"

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

        if get_include_error(file):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} has an invalid include").debug(), Text("(invalid)").error().italic())
            return False

        if verbose == 2:
            print(Text(" ").debug(title=True), Text(f"C-{name}: {file} includes valid").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), f"{file}\nInclude directives must only include C header (.h) files\n\n{get_include_error(file)}"

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
