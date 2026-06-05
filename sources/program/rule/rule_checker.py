#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from sys import stderr
import jarbin_toolkit_console as Console
import jarbin_toolkit_time as Time
from jarbin_toolkit_log import Log

from program.helper import get_color, get_level
from program.rule.rule_manager import RuleManager

print = Console.Console.print
Text = Console.Text.Text
Color = Console.ANSI.Color
Cursor = Console.ANSI.Cursor

Console.init(banner=False)

def check(
        rules: RuleManager,
        paths: list[str],
        log: Log,
        root: str = ".",
        silent: int = 0,
        verbose: int = 0
    ) -> int:

    log_type = log.log_file_type

    error_count = 0
    show_category_boxes = silent < 2
    show_rule_errors = silent == 0

    jccs_timer = Time.StopWatch()
    category_timer = Time.StopWatch()
    rule_timer = Time.StopWatch()

    args = paths
    log.log("INFO", "Rule", "*args set")

    if log_type == "jar-log":
        log.comment(f"*args set to: {paths}")

    jccs_timer.start()

    for cat_key, category in rules.items():

        category_timer.start()
        category_error_count = 0

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f'entering category "{cat_key}" ({category.name})').debug()
            )

        log.log("INFO", "Category", f"entering category {repr(cat_key)}")

        len_title_line = len(f"┏━ {category.name} {'━'*5} [•STARTED•] ━┓")

        if show_category_boxes:
            print(
                "┏━",
                Text(category.name).bold(),
                "━" * 5,
                Text("[•STARTED•]").valid(),
                "━┓"
            )
            print(
                Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃")
            )

        for rule_name, rule in category.rules.items():

            try:
                log.log("INFO", f"Rule {rule_name}", f"entering rule {repr(rule_name)}")

                # Build kwargs
                keywords_args = dict(rule.variables)
                keywords_args["verbose"] = verbose
                keywords_args["root"] = root

                log.log("INFO", f"Rule {rule_name}", "**kwargs set")
                if log_type == "jar-log":
                    log.comment(f"kwargs set to: {keywords_args}")

                rule_timer.start()

                errors = rule.check(args, **keywords_args)

                rule_time = rule_timer.elapsed()
                rule_timer.reset()

                if verbose:
                    print(
                        Text(" ").debug(title=True),
                        Text(f"elapsed time for {cat_key}/{rule_name} : {rule_time}").debug()
                    )

                if log_type == "jar-log":
                    log.comment(f"{rule_name} ({rule.info.strip()})")
                    log.comment(f"elapsed time: {rule_time:.5f}")

                if errors:
                    count = len(errors)
                    category_error_count += count

                    log.log("INFO", f"Rule {rule_name}", f"errors found ({count})")

                    if show_category_boxes:
                        color = get_color("", rule.level)
                        print(
                            color + "┃",
                            get_color(rule_name, rule.level).bold(),
                            get_color(f"({count})", rule.level).italic(),
                            end=""
                        )
                        print(
                            Cursor.move_column(len_title_line - 6) + get_color("[KO]", rule.level),
                            get_color(" ┃", rule.level),
                            get_color(f"◀ {get_level(rule.level)}", rule.level)
                        )

                    for err in errors:
                        log.log("ERROR", f"Rule {rule_name}", err.message.split("\n")[0])

                        if show_rule_errors:
                            print(
                                get_color("┃ ", rule.level)
                                + str(err).replace(
                                    "\n",
                                    str(Color(Color.C_RESET) + "\n" + get_color("┃ ", rule.level))
                                ),
                                end=get_color("┃\n", rule.level) + Color(Color.C_RESET),
                            )

                else:
                    if show_category_boxes:
                        print(
                            Text("┃"),
                            Text(rule_name).bold(),
                            Text("(no error)").italic(),
                            end=""
                        )
                        print(
                            Cursor.move_column(len_title_line - 6) + Text("[OK]").valid(),
                            Text(" ┃")
                        )

                log.log("INFO", f"Rule {rule_name}", f"leaving rule {repr(rule_name)}")

            except BaseException as err:
                log.log("CRIT", f"Rule {rule_name}", str(err))

                if show_category_boxes:
                    print(
                        Text("┃"),
                        Text(f"{rule_name} [FATAL ERROR]").critic(),
                        file=stderr
                    )
                    print(
                        Text("┃"),
                        Text("terminating JCCS").error(),
                        file=stderr
                    )
                    print(
                        "┗━",
                        Text(category.name).bold(),
                        "━" * 5,
                        Text("[••TERM••]").critic(),
                        "━┛\n",
                        file=stderr
                    )
                return -1

        if show_category_boxes:
            print(
                Text("┃") + Cursor.move_column(len_title_line - 1) + Text(" ┃")
            )
            print(
                "┗━",
                Text(category.name).bold(),
                "━" * 5,
                (Text("[••ENDED••]").error() if category_error_count else Text("[••ENDED••]").valid()),
                "━┛\n"
            )

        error_count += category_error_count
        category_time = category_timer.elapsed()
        category_timer.reset()

        if verbose:
            print(
                Text(" ").debug(title=True),
                Text(f"elapsed time for {cat_key} : {category_time}").debug()
            )

        if log_type == "jar-log":
            log.comment(f"{cat_key} elapsed: {category_time}")

    total_time = jccs_timer.elapsed()

    if verbose:
        print(
            Text(" ").debug(title=True),
            Text(f"total elapsed time : {total_time}").debug()
        )

    if log_type == "jar-log":
        log.comment(f"total elapsed time : {total_time}")

    return error_count
