#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
name = "O4"
info = """
C-O4 - Naming files and folders
The name of the file must define the logical entity it represents, and thus be clear, precise, explicit and
unambiguous.
All file names and folders must be in English, according to the snake_case convention (that is, only composed of lowercase, numbers, and underscores).
"""

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
CHECKED_EXTENSIONS = "c h"
VALID_CHARACTERS = "_"
for ascii_int in range(ord("a"), ord("z") + 1):
    VALID_CHARACTERS += chr(ascii_int)
for ascii_int in range(ord("0"), ord("9") + 1):
    VALID_CHARACTERS += chr(ascii_int)

# Checker #
def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    checked_ext = kwargs.get("CHECKED_EXTENSIONS", CHECKED_EXTENSIONS)
    valid_char = kwargs.get("VALID_CHARACTERS", VALID_CHARACTERS)

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: variables set").debug())

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        file_name : str = file.split("/")[-1]

        if "." in file_name :
            file_ext = file_name.split(".")[-1]
            file_name = file_name.split(".")[0]
        else :
            if verbose == 2:
                print(Text(" ").debug(title=True), Text(f"C-{name} {file} doesn't have an extension").debug(), Text("(skip)").info().italic())
            return True

        if not file_ext in checked_ext.split(" ") :
            if verbose == 2:
                print(Text(" ").debug(title=True), Text(f"C-{name}: {file} extension not checked").debug(), Text("(skip)").info().italic())
            return True

        for char in file_name:
            if char not in valid_char:
                if verbose:
                    print(Text(" ").debug(title=True), Text(f"C-{name}: {file} name doesn't only contain allowed letters").debug(), Text("(invalid)").error().italic())

                return False

        if verbose == 2:
            print(Text(" ").debug(title=True), Text(f"C-{name}: {file} name only contain allowed letters").debug(), Text("(valid)").valid().italic())

        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), f"{file}\nThe name of the file must define the logical entity it represents, and thus be clear, precise, explicit and unambiguous"

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
