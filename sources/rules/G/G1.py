#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# INFO #
language = "C"
category = "G"
name = f"{category}1"
info = f"""
{language}-{name} - File header
C files (.c, .h, ...) and every Makefiles must always start with the standard header of the school.
"""
level = 1

# Imports #
import jarbin_toolkit_console as Console

from utils.error import RuleError
from utils.file import File
from utils.parser import Parser

print = Console.Console.print
Text = Console.Text.Text

# Custom Variables #

# Checker #
def check(paths, **kwargs) -> list[RuleError] | None:

    errors = []
    verbose = kwargs.get("verbose", 0)

    if verbose:
        print(Text(" ").debug(title=True), Text(f"C-{name}: starting check").debug())

    def check_file(file: str) -> bool:

        if not (file.endswith(".c") or file.endswith(".h") or file.endswith("Makefile")):
            return True

        content = "".join(File.read_file(file))

        if file.endswith(".c") or file.endswith(".h"):

            if not Parser.C.has_c_header(content):

                if verbose:
                    print(
                        Text(" ").debug(title=True),
                        Text(f"C-{name}: missing C header").debug(),
                        Text("(invalid)").error().italic()
                    )

                return False

        elif file.endswith("Makefile"):

            if not Parser.Makefile.has_makefile_header(content):

                if verbose:
                    print(
                        Text(" ").debug(title=True),
                        Text(f"C-{name}: missing Makefile header").debug(),
                        Text("(invalid)").error().italic()
                    )

                return False

        if verbose == 2:
            print(
                Text(" ").debug(title=True),
                Text(f"C-{name}: header valid").debug(),
                Text("(valid)").valid().italic()
            )

        return True

    for file in paths:

        try:
            assert check_file(file), (
                f"{file}\n"
                "C files (.c, .h, ...) and every Makefiles must always start with the standard header of the school"
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
