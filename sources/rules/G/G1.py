#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
info = """
C-O1 - Contents of the repository
The repository must not contain compiled (.o, .a, .so, ...), temporary or unnecessary files (*~, #*#, etc.).
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
        print(Text(" ").debug(title=True), Text("C-01: variables set").debug())

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        if not (file.endswith(".c") or file.endswith("Makefile")):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-G1: {file} not checked").debug(), Text("(skip)").info().italic())
            return True

        with open(file, 'r') as f:
            file_str = f.read()
        f.close()

        if file.endswith(".c") and not (
            "/*\n** EPITECH PROJECT, " in file_str and
            "\n** File description:" in file_str and
            "\n*/\n" in file_str
        ) or file.endswith("Makefile") and not (
            "##\n## EPITECH PROJECT, " in file_str and
            "\n## File description:" in file_str and
            "\n##\n" in file_str
        ):
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-G1: {file} is missing the epitech file header").debug(), Text("(invalid)").error().italic())
            return False

        if verbose:
            print(Text(" ").debug(title=True), Text(f"C-G1: {file} epitech file header valid").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-01: starting check").debug())

    # Main loop #
    for file in files_path:
        try :
            assert check_file_ext(file), f"{file}\n doesn't contain the epitech file header\n\n(required for *.c and Makefile)"

        except AssertionError as error:
            errors.append(RuleError("C-O1", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-01: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
