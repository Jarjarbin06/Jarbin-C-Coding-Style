#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
language = "C"
category = "O"
name = f"{category}2"
info = f"""
{language}-{name} - File extension
Sources in a C program must only have .c or .h extensions
"""
level = 2

# Imports #
import re
import jarbin_toolkit_console as Console

from utils.error import RuleError

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #
VAR_AUTHORIZED_EXTENSIONS = "c h"
VAR_AUTHORIZED_EXTENSIONS_doc = "List of allowed file extensions for source files."
VAR_INCLUDED_FOLDERS = "sources includes tests"
VAR_INCLUDED_FOLDERS_doc = "List of folders where files are checked by this rule."

# Regex #
RE_INCLUDED_PATTERN = None
RE_EXTENSION_PATTERN = re.compile(r'\.([^.\/]+)$')
RE_AUTHORIZED_PATTERN = None

# Checker #
def check(
        paths,
        **kwargs
    ) -> list[RuleError] | None:

    errors = []
    verbose = kwargs.get("verbose", 0)

    # Custom variables #
    global VAR_AUTHORIZED_EXTENSIONS,VAR_INCLUDED_FOLDERS
    VAR_AUTHORIZED_EXTENSIONS = kwargs.get("VAR_AUTHORIZED_EXTENSIONS", VAR_AUTHORIZED_EXTENSIONS)
    VAR_INCLUDED_FOLDERS = kwargs.get("VAR_INCLUDED_FOLDERS", VAR_INCLUDED_FOLDERS)

    if isinstance(VAR_AUTHORIZED_EXTENSIONS, tuple):
        VAR_AUTHORIZED_EXTENSIONS = VAR_AUTHORIZED_EXTENSIONS[0]
    if isinstance(VAR_INCLUDED_FOLDERS, tuple):
        VAR_INCLUDED_FOLDERS = VAR_INCLUDED_FOLDERS[0]

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: variables set").debug()
        )

    # Regex re-compiling #
    global RE_INCLUDED_PATTERN, RE_AUTHORIZED_PATTERN
    RE_INCLUDED_PATTERN = re.compile(
        rf"(?:^|/)(?:{'|'.join(map(re.escape, VAR_INCLUDED_FOLDERS.split()))})(?:/)",
        re.IGNORECASE
    )
    RE_AUTHORIZED_PATTERN = re.compile(
        rf"^({'|'.join(map(re.escape, VAR_AUTHORIZED_EXTENSIONS.split()))})$",
        re.IGNORECASE
    )

    # Custom check #
    def check_file_ext(
            file : str
        ) -> bool:

        if not RE_INCLUDED_PATTERN.search(file):
            if verbose == 2:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} not in VAR_INCLUDED_FOLDERS").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        match = RE_EXTENSION_PATTERN.search(file)
        if not match:
            if verbose == 2:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} doesn't have an extension").debug(),
                    Text("(skip)").info().italic()
                )
            return True

        file_ext = match.group(1)

        if not RE_AUTHORIZED_PATTERN.match(file_ext):
            if verbose:
                print(
                    Text(" ").debug(title=True),
                    Text(f"C-{name}: {file} extension not allowed").debug(),
                    Text("(invalid)").error().italic()
                )
            return False

        if verbose == 2:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: {file} extension allowed").debug(),
                Text("(valid)").valid().italic()
            )
        return True

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: starting check").debug()
        )

    # Main loop #
    for file in paths:
        try :
            assert check_file_ext(file), (
                f"{file}\n"
                f"Sources in a C program must only have .c or .h extensions"
            )

        except AssertionError as error:
            errors.append(RuleError(f"C-{name}", str(error), level=level))

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"C-{name}: ending check").debug(),
            Text(f"({len(errors)} errors found)").error().italic()
            if errors else Text("(no error)").valid().italic()
        )

    return errors if errors else None
