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
    out, err, code = Get.Redirect.cmd_full("JCCS", "--root", ".")

    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_root_short():
    out_s, err_s, code_s = Get.Redirect.cmd_full("JCCS", "-r", ".")
    out_l, err_l, code_l = Get.Redirect.cmd_full("JCCS", "--root", ".")

    Assertion.eq((err_s, code_s), (err_l, code_l))
    Assertion.eq(out_s, out_l)
    Assertion.neq(len(out_s), 0)


# =========================================================
# EXCLUDE FLAG (-e / --exclude) (multi)
# =========================================================
def JT_exclude_single():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--exclude", "test_file.py")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_exclude_multi():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--exclude",
        "a.py",
        "--exclude",
        "b.py"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_exclude_consistency():
    out_s, err_s, code_s = Get.Redirect.cmd_full(
        "JCCS", "-e", "a.py", "-e", "b.py"
    )
    out_l, err_l, code_l = Get.Redirect.cmd_full(
        "JCCS", "--exclude", "a.py", "--exclude", "b.py"
    )

    Assertion.eq((out_s, err_s, code_s), (out_l, err_l, code_l))
    Assertion.neq(len(out_s), 0)


# =========================================================
# RULE FLAG (-R / --rule) (multi)
# =========================================================
def JT_rule_single():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--rule", "O1")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_rule_multi():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--rule",
        "O1",
        "--rule",
        "O2"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_rule_consistency():
    out_s, err_s, code_s = Get.Redirect.cmd_full("JCCS", "-R", "O1", "-R", "O2")
    out_l, err_l, code_l = Get.Redirect.cmd_full("JCCS", "--rule", "O1", "--rule", "O2")

    Assertion.eq((err_s, code_s), (err_l, code_l))
    Assertion.eq(out_s, out_l)
    Assertion.neq(len(out_s), 0)


# =========================================================
# SET FLAG (-S / --set) (multi)
# =========================================================
def JT_set_single():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--set", "KEY=VALUE")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_set_multi():
    out, err, code = Get.Redirect.cmd_full(
        "JCCS",
        "--set", "A=1",
        "--set", "B=2"
    )

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_set_consistency():
    out_s, err_s, code_s = Get.Redirect.cmd_full(
        "JCCS", "-S", "A=1", "-S", "B=2"
    )
    out_l, err_l, code_l = Get.Redirect.cmd_full(
        "JCCS", "--set", "A=1", "--set", "B=2"
    )

    Assertion.eq((out_s, err_s, code_s), (out_l, err_l, code_l))
    Assertion.neq(len(out_s), 0)


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Args = JarTest()
JTT_Args.fetch()
