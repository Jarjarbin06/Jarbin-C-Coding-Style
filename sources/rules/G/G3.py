#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
name = "G3"
info = """
C-G3 - Indentation of preprocessor directives
The preprocessor directives must be indented according to the level of indirection.
"""

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Checker #
def get_indentation_error(
        file : str
    ) -> str:

    indentation_level = 0
    is_a_comment = False

    with open(file, 'r') as f:
        file_list_str = f.readlines()
    f.close()

    for index in range(len(file_list_str)):
        if "/*" in file_list_str[index]:
            is_a_comment = True
        if "*/" in file_list_str[index]:
            is_a_comment = False
        if (not is_a_comment) and file_list_str[index].replace(" ", "") != "\n":
            if file_list_str[index].replace(" ", "").startswith("#end"):
                indentation_level -= 1
            if file_list_str[index].replace(" ", "")[0] == "#" and not file_list_str[index].startswith("    " * indentation_level):
                return f"line number {index + 1}:\n---\n{file_list_str[index]}---\nindentation level must be {indentation_level}"
            if file_list_str[index].replace(" ", "").startswith("#if"):
                indentation_level += 1
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

        if not file.endswith(".h"):
            if verbose == 2:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} not checked").debug(), Text("(skip)").info().italic())
            return True

        if get_indentation_error(file):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} has bad indentation").debug(), Text("(invalid)").error().italic())
            return False

        if verbose == 2:
            print(Text(" ").debug(title=True), Text(f"C-{name}: {file} indentations valid").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), f"{file}\nThe preprocessor directives must be indented according to the level of indirection\n\n{get_indentation_error(file)}"

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
