#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_jartest import JarTest, Get, Assertion
import JCCS

# =========================================================
# VERSION FLAG (-v / --version)
# =========================================================
def JT_version():
    out_s, err_s, code_s = Get.Redirect.cmd_full("JCCS", "-v")
    out_l, err_l, code_l = Get.Redirect.cmd_full("JCCS", "--version")

    Assertion.eq((out_s, err_s, code_s), (out_l, err_l, code_l))
    Assertion.eq(code_s, 0)
    Assertion.eq(len(err_s), 0)
    Assertion.contain(JCCS.__version__, out_s)


# =========================================================
# HELP FLAG (--help)
# =========================================================
def JT_help():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--help")

    Assertion.eq(code, 0, "help: exit code must be 0")
    Assertion.eq(len(err), 0, "help: stderr must be empty")
    assert "usage" in out.lower() or "jccs" in out.lower()
    Assertion.contain("help", out.lower())


# =========================================================
# SHORT HELP (-h)
# =========================================================
def JT_short_help():
    out, err, code = Get.Redirect.cmd_full("JCCS", "-h")

    Assertion.eq(code, 0)
    Assertion.eq(len(err), 0)
    Assertion.neq(len(out), 0)


# =========================================================
# ARGUMENTS DISPLAY (-a / --show-arguments)
# =========================================================
def JT_arguments():
    out_s, err_s, code_s = Get.Redirect.cmd_full("JCCS", "-a")
    out_l, err_l, code_l = Get.Redirect.cmd_full("JCCS", "--show-arguments")

    Assertion.eq((out_s, err_s, code_s), (out_l, err_l, code_l))
    Assertion.eq(code_s, 0)
    Assertion.eq(len(err_s), 0)
    assert "rule" in out_s.lower() or "category" in out_s.lower()


# =========================================================
# UPDATE FLAG (--update)
# =========================================================
def JT_update():
    out, err, code = Get.Redirect.cmd_full("JCCS", "--update")

    Assertion.eq(code, 0)
    Assertion.ncontain("error", out.lower())


# =========================================================
# CONSISTENCY CHECK (GLOBAL FLAGS BEHAVIOR)
# =========================================================
def JT_builtin_consistency():
    flags = [
        ("-v", "--version"),
        ("-a", "--show-arguments"),
    ]

    for short, long in flags:
        out_s, err_s, code_s = Get.Redirect.cmd_full("JCCS", short)
        out_l, err_l, code_l = Get.Redirect.cmd_full("JCCS", long)

        Assertion.eq((out_s, err_s, code_s), (out_l, err_l, code_l))


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Builtins = JarTest()
JTT_Builtins.fetch()
