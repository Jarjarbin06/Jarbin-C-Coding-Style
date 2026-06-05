#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_jartest import JarTest, Get, Assertion

# =========================================================
# LOG FLAGS
# =========================================================
def JT_json_log():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--json-log")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_verbose():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--verbose")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_super_verbose():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--super-verbose")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


# =========================================================
# LOG CONTROL FLAGS
# =========================================================
def JT_no_log():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--no-log")

    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_show_log():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--show-log")

    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


# =========================================================
# SILENT MODES
# =========================================================
def JT_silent():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--silent")

    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_super_silent():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--super-silent")

    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


def JT_extreme_silent():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--extreme-silent")

    Assertion.eq(len(err), 0)
    Assertion.eq(len(out), 0)


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Logs = JarTest()
JTT_Logs.fetch()
