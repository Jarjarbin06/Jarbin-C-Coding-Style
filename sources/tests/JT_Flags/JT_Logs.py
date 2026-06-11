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
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--json-log")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_verbose():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--verbose")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_super_verbose():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--super-verbose")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


# =========================================================
# LOG CONTROL FLAGS
# =========================================================
def JT_no_log():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--no-log")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_show_log():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--show-log")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


# =========================================================
# SILENT MODES
# =========================================================
def JT_silent():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--silent")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_super_silent():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--super-silent")

    Assertion.eq(err, "")
    Assertion.neq(out, "")


def JT_extreme_silent():
    out, err, code = Get.Redirect.cmd_all_std("python", "./sources/JCCS.py", "--extreme-silent")

    Assertion.eq(err, "")
    Assertion.eq(out, "")


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Logs = JarTest()
failed: list = JTT_Logs.fetch()
