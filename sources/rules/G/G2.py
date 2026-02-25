#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
name = "G2"
info = """
C-G2 - Separation of functions
Inside a source file, implementations of functions must be separated by one and only one empty line.
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

    is_a_comment = False

    with open(file, 'r') as f:
        file_list_str = f.readlines()
    f.close()

    for index in range(len(file_list_str)):
        if "/*" in file_list_str[index]:
            is_a_comment = True

        if "*/" in file_list_str[index]:
            is_a_comment = False

        if (not is_a_comment) and (not file_list_str[index].replace(" ", "").startswith("//")) and file_list_str[index] == "}\n":
            if (index + 3) < len(file_list_str):
                if not file_list_str[index + 1].replace(" ", "").startswith("#") and not (file_list_str[index + 1] == "\n" and file_list_str[index + 2] != "\n"):
                    return f"line number {index + 1}-{index + 3}:\n---\n{file_list_str[index]}{file_list_str[index + 1]}{file_list_str[index + 2]}{"" if file_list_str[index].endswith("\n") else "\n"}---\nthere must be an empty line between functions"

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

        if not file.endswith(".c"):
            if verbose == 2:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} not checked").debug(), Text("(skip)").info().italic())
            return True

        if get_line_error(file):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} functions not separated by empty line").debug(), Text("(invalid)").error().italic())
            return False

        if verbose == 2:
            print(Text(" ").debug(title=True), Text(f"C-{name}: {file} functions separation valid").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), f"{file}\nInside a source file, implementations of functions must be separated by one and only one empty line\n\n{get_line_error(file)}"

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
