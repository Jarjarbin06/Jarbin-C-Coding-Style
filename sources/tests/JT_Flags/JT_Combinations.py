#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_jartest import JarTest, Get, Assertion

# =========================================================
# FLAG COMBINATIONS
# =========================================================
def JT_root_exclude():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--root", ".",
        "--exclude", "test_file.py"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_root_exclude_multi():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "-r", ".",
        "-e", "a.py",
        "-e", "b.py"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_rule_exclude():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--rule", "O", "O2",
        "--exclude", "a.py"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_rule_multi_exclude():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "-R", "O", "O2", "G", "G1",
        "-e", "a.py"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_set_rule():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--set", "O", "O1" ,"UNAUTHORIZED_EXTENSIONS", "c h",
        "--rule", "G", "G1"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_set_multi_rule():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "-S", "O", "O1" ,"UNAUTHORIZED_EXTENSIONS", "c h",
        "-S", "O", "O1" ,"EXCLUDED_FOLDERS", "",
        "-R", "O", "O2"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_verbose_json():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--verbose",
        "--json-log"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_silent_vs_verbose():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--silent",
        "--verbose"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_extreme_silent_override():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--extreme-silent",
        "--verbose"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_help_override():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--rule", "O", "O2",
        "--help",
        "--exclude", "."
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")
    Assertion.contain("usage", out.lower())


def JT_version_override():
    out, err, code = Get.Redirect.cmd_all_std(
        "JCCS",
        "--version",
        "--verbose"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


# =========================================================
# CONSISTENCY MATRIX (VERY POWERFUL)
# =========================================================
def JT_flag_matrix_basic():
    flags = [
        "--verbose",
        "--json-log",
        "--silent",
        "--rule O O2",
        "--exclude ."
    ]

    for f1 in flags:
        for f2 in flags:
            out, err, code = Get.Redirect.cmd_all_std("JCCS", *f1.split(" "), *f2.split(" "))

            Assertion.eq(err, "")
            Assertion.neq(out, "")


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Combinations = JarTest()
failed: list = JTT_Combinations.fetch()
