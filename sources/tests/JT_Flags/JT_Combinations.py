#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################
import os

from jarbin_toolkit_jartest import JarTest, Get, Assertion

# =========================================================
# FLAG COMBINATIONS
# =========================================================
def JT_root_exclude():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--root", ".",
        "--exclude", "test_file.py"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_root_exclude_multi():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "-r", ".",
        "-e", "a.py",
        "-e", "b.py"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_rule_exclude():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--rule", "O1",
        "--exclude", "a.py"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_rule_multi_exclude():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "-R", "O1",
        "-R", "O2",
        "-e", "a.py"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)


def JT_set_rule():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--set", "A=1",
        "--rule", "O1"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)


def JT_set_multi_rule():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "-S", "A=1",
        "-S", "B=2",
        "-R", "O1"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)


def JT_verbose_json():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--verbose",
        "--json-log"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_silent_vs_verbose():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--silent",
        "--verbose"
    )

    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_extreme_silent_override():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--extreme-silent",
        "--verbose"
    )

    Assertion.eq(len(err), 0)
    Assertion.eq(len(out), 0)


def JT_help_override():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--rule", "O", "O1",
        "--help",
        "--exclude", "."
    )

    Assertion.eq(code, 0)
    Assertion.neq(len(err), 0)
    Assertion.contain("usage", out.lower())


def JT_version_override():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--version",
        "--verbose"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)


# =========================================================
# CONSISTENCY MATRIX (VERY POWERFUL)
# =========================================================
def JT_flag_matrix_basic():
    flags = [
        "--verbose",
        "--json-log",
        "--silent",
        "--rule O O1",
        "--exclude ."
    ]

    for f1 in flags:
        for f2 in flags:
            out, err, code = Get.Redirect.cmd_full("JCCS", *f1.split(" "), *f2.split(" "))

            Assertion.eq(len(err), 0)
            Assertion.neq(len(out), 0)


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Combinations = JarTest()
JTT_Combinations.fetch()
