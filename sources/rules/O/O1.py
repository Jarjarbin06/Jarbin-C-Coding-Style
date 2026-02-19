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
UNAUTHORIZED_EXTENSIONS = "o a so out gcda gcno gch pch swp swo tmp bak"
EXCLUDED_FOLDERS = "bonus"

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
    unauth_ext = kwargs.get("UNAUTHORIZED_EXTENSIONS", UNAUTHORIZED_EXTENSIONS)
    excluded_folders = kwargs.get("EXCLUDED_FOLDERS", EXCLUDED_FOLDERS)

    if verbose:
        print(Text(" ").debug(title=True), Text("C-01: variables set").debug())

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        for folder in excluded_folders.split(" ") :
            if f"/{folder.upper()}/" in file.upper() or f"{folder.upper()}/" in file.upper() :
                if verbose:
                    print(Text(" ").debug(title=True), Text(f"C-01: {file} in EXCLUDED_FOLDERS (\"{folder}\")").debug(), Text("(skip)").info().italic())
                return True

        file_ext : str = file.split("/")[-1]

        if "." in file_ext :
            file_ext = file_ext.split(".")[-1]
        else:
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-01: {file} doesn't have an extension").debug(), Text("(skip)").info().italic())
            return True

        if file_ext in unauth_ext.split(" ") :
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-01: {file} extension not allowed").debug(), Text("(invalid)").error().italic())
            return False
        if verbose:
            print(Text(" ").debug(title=True), Text(f"C-01: {file} extension allowed").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-01: starting check").debug())

    # Main loop #
    for file in files_path:
        try :
            assert check_file_ext(file), f"{file}\ninvalid extension (compiled, temporary or unnecessary file)\n\n(.{file.split("/")[-1].split(".")[-1]} is in [.{unauth_ext.replace(" ", ", .")}])"

        except AssertionError as error:
            errors.append(RuleError("C-O1", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-01: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
