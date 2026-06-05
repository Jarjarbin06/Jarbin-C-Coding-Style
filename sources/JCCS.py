#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from os.path import abspath
from sys import argv as sargv, exit, stderr

import jarbin_toolkit_console as Console
from jarbin_toolkit_log import Log

from program.file import get_files
from program.rule.rule_checker import check
from program.rule.rule_manager import RuleManager

import program.arg_handler as ArgH

print = Console.Console.print
Text = Console.Text.Text

Console.init(banner=False)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_FATAL = 84


# =========================
# PROGRAM INFO
# =========================
__simplename__ = "JCCS"
__fullname__ = "Jarbin-C-Coding-Style"
__version__ = open(
    abspath(__file__).removesuffix("sources/JCCS.py") + "VERSION",
    "r"
).read()
__author__ = "Jarjarbin06"
__email__ = "nathan.amaraggi@epitech.eu"


# =========================
# MAIN
# =========================
def main(
        argv,
    ) -> None:
    exit_status: int = EXIT_SUCCESS
    error_amount: int = 0

    # =========================
    # LOG INIT
    # =========================
    if Log.exist("."):
        Log(".", "JCCS").delete()

    log = Log(".", "JCCS")

    # =========================
    # LOAD RULES
    # =========================
    try:
        from rules import Rules

    except BaseException:
        print(Text("Failed to import rules").critic(), file=stderr)
        log.log("CRIT", "Rules", "import failed")
        exit(EXIT_FATAL)

    RULE_MANAGER: RuleManager = Rules.RULE_MANAGER

    for err in getattr(Rules, "ERRORS", []):
        print(Text(f"Rule loading issue: {err}").error())
        log.log("ERROR", "Rules", str(err))

    # =========================
    # CONTEXT / ARGS
    # =========================
    ctx = ArgH.Context(log, RULE_MANAGER)

    ArgH.parse_args(
        argv,
        ctx,
        __simplename__,
        __fullname__,
        __version__,
        __author__,
        __email__
    )

    # Apply context
    log = ctx.log
    root = ctx.root
    verbose = ctx.verbose
    silent = ctx.silent
    exclude = ctx.exclude
    no_log = ctx.no_log
    show_log = ctx.show_log

    RULE_MANAGER = ctx.rules

    # =========================
    # START OUTPUT
    # =========================
    if verbose:
        print(Text(" ").debug(title=True), Text("starting JCCS").debug())

    if silent != 3:
        print(Text("JCCS").bold(), "starting...\n")

    # =========================
    # FILE COLLECTION
    # =========================
    paths = get_files(root, exclude)

    if not paths:
        print(Text("Root not found or empty").error())
        log.log("WARN", "Program", "root invalid or empty")
        exit(EXIT_FAILURE)

    log.log("INFO", "Program", f"{len(paths)} paths found")

    if verbose:
        print(Text(" ").debug(title=True), Text(f"{len(paths)} paths found").debug())

    # =========================
    # RUN CHECKER
    # =========================
    if paths:

        log.log("INFO", "Program", "starting check")

        if verbose:
            print(Text(" ").debug(title=True), Text("starting check").debug())

        error_amount = check(
            RULE_MANAGER,
            paths,
            log,
            root=root,
            silent=silent,
            verbose=verbose
        )

        if error_amount < 0:
            log.log("CRIT", "Program", "check crashed")
        else:
            log.log("INFO", "Program", f"check finished ({error_amount} errors)")

        if verbose:
            print(Text(" ").debug(title=True), Text("ending check").debug())

    exit_status = EXIT_FAILURE if error_amount > 0 else EXIT_SUCCESS

    # =========================
    # FINAL OUTPUT
    # =========================
    if silent != 3:

        if error_amount > 0:
            print(
                Text("JCCS").bold(),
                "finished",
                Text("[KO]").error(),
                Text(f"({error_amount} errors)").italic()
            )
            log.log("ERROR", "Program", f"failed with {error_amount} errors")

        elif error_amount == 0:
            print(Text("JCCS").bold(), "finished", Text("[OK]").valid())
            log.log("VALID", "Program", "success")

        else:
            print(Text("JCCS").critic(), "terminated (fatal)", file=stderr)
            log.log("CRIT", "Program", "fatal error")
            exit_status = EXIT_FATAL

    if verbose:
        print(Text(" ").debug(title=True), Text("ending JCCS").debug())

    # =========================
    # LOG FINALIZATION
    # =========================
    log.close()

    if show_log:
        print(log, start="\n")

    if no_log:
        log.delete()

    exit(exit_status)

if __name__ == "__main__":
    main(sargv)

Console.quit(delete_log=True)
