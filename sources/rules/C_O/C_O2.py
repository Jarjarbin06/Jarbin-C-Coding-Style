#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# Imports #
from Error import RuleError
import jarbin_toolkit_console as Console

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
AUTHORIZED_EXTENSIONS = "c h"
INCLUDED_FOLDERS = "SOURCES INCLUDES TESTS"

def check(
        *args,
        **kwargs
    ) -> list[RuleError] | None:

    kwargs = kwargs["kwargs"]
    errors = []
    files_path : list[str] = args[0]
    verbose: bool = kwargs.get("verbose", False)

    # Custom variables #
    auth_ext : str = kwargs.get("AUTHORIZED_EXTENSIONS", AUTHORIZED_EXTENSIONS)
    included_folders : str = kwargs.get("INCLUDED_FOLDERS", INCLUDED_FOLDERS)

    if verbose:
        print(Text(" ").debug(title=True), Text("C-02: variables set").debug())

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        folder_check : bool = False

        for folder in included_folders.split(" ") :
            if f"/{folder.upper()}/" in file.upper() or f"{folder.upper()}/" in file.upper() :
                folder_check = True

        if not folder_check :
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-02: {file} not in INCLUDED_FOLDERS").debug(), Text("(skip)").info().italic())
            return True

        file_ext : str = file.split("/")[-1]

        if "." in file_ext :
            file_ext = file_ext.split(".")[-1]
        else :
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-02: {file} doesn't have an extension").debug(), Text("(skip)").info().italic())
            return True

        if not file_ext in auth_ext.split(" ") :
            if verbose:
                print(Text(" ").debug(title=True), Text(f"C-02: {file} extension not allowed").debug(), Text("(invalid)").error().italic())
            return False

        if verbose:
            print(Text(" ").debug(title=True), Text(f"C-02: {file} extension allowed").debug(), Text("(valid)").valid().italic())
        return True

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-02: starting check").debug())

    # Main loop #
    for file in files_path:
        try :
            assert check_file_ext(file), f"{file}\ninvalid extension\n\n(.{file.split("/")[-1].split(".")[-1]} is not in [.{AUTHORIZED_EXTENSIONS.replace(" ", ", .")}])"

        except AssertionError as error:
            errors.append(RuleError("C-O2", str(error)))

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-02: ending check").debug(), Text(f"({len(errors)} errors found)").error().italic() if errors else Text("(no error)").valid().italic())

    return errors if errors else None
