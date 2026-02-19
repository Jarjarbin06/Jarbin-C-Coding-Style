#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
info = """
C-O3 - File coherence
A source file must match a logical entity, and group all the functions associated with that entity.
Grouping functions that are not related to each other in the same file has to be avoided.
You are allowed to have 10 functions (including at most 5 non-static functions) in total per file.
"""

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Checker #
def check(
        *args,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    files_path : list[str] = args[0]
    verbose = kwargs.get("verbose", False)

    # Custom variables #

    if verbose:
        print(Text(" ").debug(title=True), Text("C-03: variables set").debug())

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:
        if verbose:
            print(Text(" ").debug(title=True), Text(f"C-03: {file} cannot check").debug(), Text("(skip)").info().italic())

        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-03: starting check").debug())

    # Main loop #
    for file in files_path:
        try :
            assert check_file_ext(file), f"{file}\nfile isn't coherent"

        except AssertionError as error:
            errors.append(RuleError("C-O3", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-03: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
