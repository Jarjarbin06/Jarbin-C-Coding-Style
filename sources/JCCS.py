#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


# Program imports #
from os import listdir
from os.path import isfile as path_isfile, join as path_join
from sys import argv, stderr, exit
from typing import Callable, Any
from Error import RuleError
import jarbin_toolkit_console as Console
from rules.Rules import RULES


# Program #
print = Console.Console.print
Text = Console.Text.Text

EXIT_SUCCESS = 0
EXIT_FAILURE = 84

def get_files(
        root: str = "./",
    ) -> list[str]:
    """
        Get all files in root directory and subdirectories

        Parameters:
            root (str): root directory

        Returns:
            list[str]: all files in root directory and subdirectories
    """

    root = root if root[-1] == "/" else f"{root}/"
    files: list[str] = []

    for entry in listdir(root):
        full_path = path_join(root, entry)

        if not entry.startswith("."):
            if path_isfile(full_path):
                files.append(full_path)

            else:
                files += get_files(full_path)

    return files

def check(
        rules: dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]],
        paths: list[str]
    ) -> int:

    """
        Check all rules for all paths

        Parameters:
            rules (dict[str, dict[str, Callable[[list[str]], None] | dict[str, Any]]]): rules established by JCCS + your rules (see top of file)
            paths (list[str]): paths to check

        Returns:
            int: number of errors found
    """

    errors: list[RuleError] | None
    error_count: int = 0
    args : list = paths
    keywords_args: dict

    for rule in rules:

        try:
            keywords_args = {}

            for arg in rules[rule]["arguments"]:
                keywords_args[arg] = rules[rule]["arguments"][arg]

            errors = rules[rule]["check"](args, keywords_args)

            if errors:
                error_count += len(errors)

                print(Text(f"{rule}").bold(), Text(f"({len(errors)})").italic(), ":", Text("[KO]").error())

                for rule_error in errors:
                    print(rule_error, file=stderr)

            else:
                print(Text(f"{rule}").bold(), Text("(no error)").italic(), Text("[OK]").valid())

        except Exception:
            print(Text(f"{rule} [FATAL ERROR]").critic())
            print(Text(f"terminating JCCS").error())
            return 1

    return error_count


# Main #

if __name__ == '__main__':

    exit_status : int = EXIT_FAILURE
    error_amount : int = 0
    root : str = "."

    Console.init()

    if len(argv) > 1 and "-" in argv[1]:
        exit(exit_status)

    elif len(argv) == 2:
        root = argv[1]

    print(Text("JCCS").bold(), "starting...", end="\n\n")

    error_amount = check(RULES, get_files(root))
    exit_status = (EXIT_FAILURE if error_amount else EXIT_SUCCESS)

    Console.quit(delete_log=True)

    if error_amount:
        print(Text("JCCS").bold(), "finished", Text("[KO]").error(), Text(f"({error_amount} error)").italic(), start="\n")
    else:
        print(Text("JCCS").bold(), "finished", Text("[OK]").valid(), start="\n")

    exit(exit_status)
