#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_jartest import JarTest, Get, Assertion

# =========================================================
# ROOT FLAG (-r / --root)
# =========================================================
def JT_root():
    out, err, code = Get.Redirect.cmd_all_std(" ./bin/JCCS", "--root", ".")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_root_short():
    out_s, err_s, code_s = Get.Redirect.cmd_all_std(" ./bin/JCCS", "-r", ".")
    out_l, err_l, code_l = Get.Redirect.cmd_all_std(" ./bin/JCCS", "--root", ".")

    Assertion.eq(out_s, out_l)
    Assertion.eq(err_s, err_l)
    Assertion.eq(code_s, code_l)
    Assertion.eq(err_s, "")
    Assertion.neq(out_s, "")


# =========================================================
# EXCLUDE FLAG (-e / --exclude) (multi)
# =========================================================
def JT_exclude_single():
    out, err, code = Get.Redirect.cmd_all_std(" ./bin/JCCS", "--exclude", "test_file.py")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_exclude_multi():
    out, err, code = Get.Redirect.cmd_all_std(
        " ./bin/JCCS",
        "--exclude",
        "a.py",
        "b.py"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_exclude_consistency():
    out_s, err_s, code_s = Get.Redirect.cmd_all_std(
        " ./bin/JCCS", "-e", "a.py", "-e", "b.py"
    )
    out_l, err_l, code_l = Get.Redirect.cmd_all_std(
        " ./bin/JCCS", "--exclude", "a.py", "b.py"
    )

    Assertion.eq(out_s, out_l)
    Assertion.eq(err_s, err_l)
    Assertion.eq(code_s, code_l)
    Assertion.eq(err_s, "")
    Assertion.neq(out_s, "")


# =========================================================
# RULE FLAG (-R / --rule) (multi)
# =========================================================
# =========================================================
def JT_rule_single():
    out, err, code = Get.Redirect.cmd_all_std(" ./bin/JCCS", "--rule", "O", "O2")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_rule_multi():
    out, err, code = Get.Redirect.cmd_all_std(
        " ./bin/JCCS",
        "--rule",
        "O",
        "O2",
        "G",
        "G1"
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_rule_consistency():
    out_s, err_s, code_s = Get.Redirect.cmd_all_std(" ./bin/JCCS", "-R", "O", "O2", "G", "G1")
    out_l, err_l, code_l = Get.Redirect.cmd_all_std(" ./bin/JCCS", "--rule", "O", "O2", "G", "G1")

    Assertion.eq(out_s, out_l)
    Assertion.eq(err_s, err_l)
    Assertion.eq(code_s, code_l)
    Assertion.eq(err_s, "")
    Assertion.neq(out_s, "")


# =========================================================
# SET FLAG (-S / --set) (multi)
# =========================================================
def JT_set_single():
    out, err, code = Get.Redirect.cmd_all_std(" ./bin/JCCS", "--set", "O", "O1" ,"UNAUTHORIZED_EXTENSIONS", "c h")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_set_multi():
    out, err, code = Get.Redirect.cmd_all_std(
        " ./bin/JCCS",
        "--set", "O", "O1" ,"UNAUTHORIZED_EXTENSIONS", "c h",
        "--set", "O", "O1" ,"EXCLUDED_FOLDERS", ""
    )

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_set_consistency():
    out_s, err_s, code_s = Get.Redirect.cmd_all_std(
        " ./bin/JCCS", "-S", "O", "O1" ,"UNAUTHORIZED_EXTENSIONS", "c h"
    )
    out_l, err_l, code_l = Get.Redirect.cmd_all_std(
        " ./bin/JCCS", "--set", "O", "O1" ,"UNAUTHORIZED_EXTENSIONS", "c h"
    )

    Assertion.eq(out_s, out_l)
    Assertion.eq(err_s, err_l)
    Assertion.eq(code_s, code_l)
    Assertion.eq(err_s, "")
    Assertion.neq(out_s, "")


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Args = JarTest()
failed: list = JTT_Args.fetch()
