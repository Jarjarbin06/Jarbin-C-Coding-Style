#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# Program imports #
from os.path import abspath
from sys import argv, exit
from typing import Callable, Any

import jarbin_toolkit_console as Console
from jarbin_toolkit_log import Log

from program.file import get_files
from program.rule_checker import check
import program.arg_handler as ArgH

print = Console.Console.print
Text = Console.Text.Text
Color = Console.ANSI.Color
Cursor = Console.ANSI.Cursor
Animation = Console.Animation

Console.init(banner=False)

EXIT_SUCCESS = 0
EXIT_FAILURE = 84
EXIT_FATAL = 84
RULES: dict[str, str | dict[str, str | dict[str, str | Callable | dict[str, tuple[Any, str | None]]]]]


# Program info #
__simplename__ = "JCCS"
__fullname__ = "Jarbin-C-Coding-Style"
__version__ : str = open(abspath(__file__).removesuffix("sources/JCCS.py") + "VERSION", 'r').read()
__author__ : str = "Jarjarbin06"
__email__ : str = "nathan.amaraggi@epitech.eu"


# Main #
if __name__ == '__main__':

    exit_status : int
    error_amount : int = 0

    log: Log
    if Log.exist("."):
        log = Log(".", "JCCS")
        log.delete()
    log = Log(".", "JCCS")

    try:
        from rules import Rules

    except BaseException:
        print(Text("Failed to import the rules").critic())

        log.log("CRIT", "Rules", "failed to fetch the rules")
        exit(EXIT_FATAL)

    else:
        for err in Rules.ERRORS:
            err_str = f"Failed to fetch {err} rules"
            print(Text(err_str).error())
            log.log("ERROR", "Rules", err_str)

        RULES = Rules.RULES

    ctx = ArgH.Context(log)
    ctx.rules = RULES

    ArgH.parse_args(argv, ctx, __simplename__, __fullname__, __version__, __author__, __email__)

    log = ctx.log
    root = ctx.root
    arg_verbose = ctx.verbose
    arg_silent = ctx.silent
    arg_exclude = ctx.exclude
    arg_no_log = ctx.no_log
    arg_show_log = ctx.show_log
    RULES = ctx.rules

    if arg_verbose:
        print(Text(" ").debug(title=True), Text(f"starting JCCS").debug())

    if arg_silent != 3:
        print(Text("JCCS").bold(), "starting...", start="\n", end="\n\n")

    paths = get_files(root, arg_exclude)

    if paths is None:
        print(Text("Root not found").error())
        log.log("WARN", "Program", "Root not found")
        exit_status = EXIT_FAILURE

    else:
        if arg_verbose:
            print(Text(" ").debug(title=True), Text(f"{len(paths)} paths found").debug())

        log.log("INFO", "Program", f"{len(paths)} paths found")

        if len(paths) > 0:
            if arg_verbose:
                print(Text(" ").debug(title=True), Text(f"starting check").debug())

            log.log("INFO", "Program", f"start check")
            error_amount = check(RULES, paths, log, root, silent=arg_silent, verbose=arg_verbose)
            if error_amount >= 0:
                log.log("INFO", "Program", f"check finished ({error_amount} error)")
            else:
                log.log("CRIT", "Program", f"check terminated (fatal error)")

            if arg_verbose:
                print(Text(" ").debug(title=True), Text(f"ending check").debug())

        exit_status = (EXIT_FAILURE if error_amount > 0 else EXIT_SUCCESS)

    if arg_silent != 3:
        if error_amount > 0:
            print(Text("JCCS").bold(), "finished", Text("[KO]").error(), Text(f"({error_amount} error)").italic())
            log.log("ERROR", "Program", f"JCCS terminated with {error_amount} error")
        elif error_amount == 0:
            print(Text("JCCS").bold(), "finished", Text("[OK]").valid())
            log.log("VALID", "Program", f"JCCS terminated with success")
        else:
            print(Text("JCCS").bold().critic() + Text(" terminated").critic())
            log.log("CRIT", "Program", f"JCCS terminated due to an internal error")
            exit_status = EXIT_FATAL

    if arg_verbose:
        print(Text(" ").debug(title=True), Text(f"ending JCCS").debug())

    log.close()
    if arg_show_log:
        print(log, start="\n")

    if arg_no_log:
        log.delete()

    exit(exit_status)

Console.quit(delete_log=True)
