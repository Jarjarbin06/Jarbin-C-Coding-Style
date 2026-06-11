#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from sys import stderr
from typing import Callable

from jarbin_toolkit_console.Text import Text
from jarbin_toolkit_log import Log

import program.helper as Helper
from program.update import update_jccs
from program.rule.rule_manager import RuleManager
from JCCS import EXIT_SUCCESS, EXIT_FAILURE

class Flag:

    def __init__(
        self,
        names: list[str],
        handler: str | Callable,
        has_value: bool = False,
        multi: bool = False,
        description: str = ""
    ) -> None:
        self.names = names
        self.has_value = has_value
        self.multi = multi
        self.handler: str | Callable = handler
        self.description = description

    def __call__(
            self,
            *args,
            **kwargs
        ) -> None:
        self.handler(*args, **kwargs)

class Context:

    def __init__(
            self,
            log: Log,
            rules: RuleManager
        ) -> None:
        self.root: str = "."
        self.silent: int = 0
        self.verbose: int = 0
        self.exclude: list[str] = []
        self.no_log: bool = False
        self.show_log: bool = False
        self.log: Log = log

        # NEW: RuleManager instead of dict
        self.rules: RuleManager = rules

def error(
        msg,
        ctx: Context
    ) -> None:
    print(Text(msg).error(), file=stderr)
    ctx.log.log("ERROR", "Flag", msg)
    ctx.log.log("ERROR", "JCCS", "exiting JCCS")
    ctx.log.close()
    exit(EXIT_FAILURE)

def log_exit(
        ctx: Context,
        exit_code: int | None = None
    ) -> None:
    ctx.log.log("INFO", "JCCS", "exiting JCCS")
    ctx.log.close()
    exit(exit_code or EXIT_SUCCESS)

def parse_args(
    argv,
    ctx: Context,
    simplename: str,
    fullname: str,
    version: str,
    author: str,
    email: str
) -> Context:

    i = 1

    # =========================
    # HELPERS
    # =========================
    def handle_json(_):
        ctx.log.delete()
        ctx.log = Log(".", "JCCS", True)
        ctx.log.log("VALID", "Flag", "-j activated")

    def handle_verbose(_):
        ctx.verbose = 1
        ctx.log.log("VALID", "Flag", "-V activated")

    def handle_super_verbose(_):
        ctx.verbose = 2
        ctx.log.log("VALID", "Flag", "--super-verbose activated")

    def handle_no_log(_):
        ctx.no_log = True
        ctx.log.log("VALID", "Flag", "--no-log activated")

    def handle_show_log(_):
        ctx.show_log = True
        ctx.log.log("VALID", "Flag", "--show-log activated")

    def handle_silent(_):
        ctx.silent = 1
        ctx.log.log("VALID", "Flag", "-s activated")

    def handle_super_silent(_):
        ctx.silent = 2
        ctx.log.log("VALID", "Flag", "--super-silent activated")

    def handle_extreme_silent(_):
        ctx.silent = 3
        ctx.log.log("VALID", "Flag", "--extreme-silent activated")

    def handle_root(values):
        ctx.root = values[0]
        ctx.log.log("VALID", "Flag", f"-r set to {ctx.root}")

    def handle_exclude(values):
        flat = []
        for v in values:
            flat.extend(v.split(" "))

        ctx.exclude.extend([x for x in flat if x and x not in ctx.exclude])

        ctx.log.log("VALID", "Flag", f"-e set")

    # =========================
    # RULE SELECTION (UPDATED)
    # =========================
    def handle_rule(values):
        if len(values) % 2 != 0:
            error("-R expects <CATEGORY> <RULE> pairs", ctx)

        pairs = []
        for i in range(0, len(values), 2):
            pairs.append((values[i], values[i + 1]))

        try:
            ctx.rules = ctx.rules.select(pairs)
        except Exception as e:
            error(str(e), ctx)

        ctx.log.log("VALID", "Flag", "-R applied")

    # =========================
    # RULE SETTING (UPDATED)
    # =========================
    def handle_set(values):
        if len(values) != 4:
            error("-S requires <CATEGORY> <RULE> <ARG> <VALUE>", ctx)

        cat, rule_name, arg, val = values

        try:
            category = ctx.rules.get_category(cat)
            rule = category[rule_name]
        except Exception as e:
            error(str(e), ctx)

        if f"VAR_{arg}" not in rule.variables:
            error(f"{rule_name} has no argument {arg}", ctx)

        rule.variables[f"VAR_{arg}"] = val
        ctx.log.log("VALID", "Flag", f"-S set {cat}/{rule_name}/{arg}")

    # =========================
    # FLAGS
    # =========================
    FLAGS: list[Flag] = [
        Flag(["-j", "--json-log"], handler=handle_json),
        Flag(["-V", "--verbose"], handler=handle_verbose),
        Flag(["--super-verbose"], handler=handle_super_verbose),

        Flag(["--no-log"], handler=handle_no_log),
        Flag(["--show-log"], handler=handle_show_log),

        Flag(["-s", "--silent"], handler=handle_silent),
        Flag(["--super-silent"], handler=handle_super_silent),
        Flag(["--extreme-silent"], handler=handle_extreme_silent),

        Flag(["-r", "--root"], has_value=True, handler=handle_root),
        Flag(["-e", "--exclude"], has_value=True, multi=True, handler=handle_exclude),

        Flag(["-R", "--rule"], has_value=True, multi=True, handler=handle_rule),
        Flag(["-S", "--set"], has_value=True, multi=True, handler=handle_set),

        Flag(["-h"], handler="usage"),
        Flag(["--help"], handler="help"),
        Flag(["-v", "--version"], handler="version"),
        Flag(["-a", "--show-arguments"], handler="arguments"),
        Flag(["--update"], handler="update"),
        Flag(["--test"], handler="test"),
    ]

    # =========================
    # MAIN LOOP
    # =========================
    while i < len(argv):
        arg = argv[i]

        if not arg.startswith("-"):
            error(f"invalid argument {arg}", ctx)

        flag = next((f for f in FLAGS if arg in f.names), None)

        if not flag:
            error(f"unknown flag {arg}", ctx)

        # built-ins
        if flag.handler == "usage":
            ctx.log.log("VALID", "Flag", "-h called")
            Helper.print_usage(simplename)
            log_exit(ctx)

        if flag.handler == "help":
            ctx.log.log("VALID", "Flag", "--help called")
            Helper.print_help(simplename, fullname, version, author, email)
            log_exit(ctx)

        if flag.handler == "version":
            ctx.log.log("VALID", "Flag", "-v/--version called")
            print(Text(version).bold())
            log_exit(ctx)

        if flag.handler == "arguments":
            ctx.log.log("VALID", "Flag", "-a/--show-arguments called")
            Helper.show_arguments(ctx.rules)
            log_exit(ctx)

        if flag.handler == "update":
            ctx.log.log("VALID", "Flag", "--update called")
            update_jccs()
            log_exit(ctx)

        if flag.handler == "test":
            ctx.log.log("VALID", "Flag", "--test called")
            from tests.JT_main import JTT
            exit_code = JTT.run(n = 2)
            log_exit(ctx, exit_code=exit_code)

        # value parsing
        values = []

        if flag.has_value:
            i += 1
            while i < len(argv) and not argv[i].startswith("-"):
                values.append(argv[i])
                i += 1
                if not flag.multi:
                    break

            if not values:
                error(f"missing value for {arg}", ctx)
        else:
            i += 1

        # execute handler
        if callable(flag.handler):
            flag(values)

    return ctx