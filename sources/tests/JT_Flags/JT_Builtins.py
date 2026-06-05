#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_jartest import JarTest, Get, Assertion

# =========================================================
# VERSION FLAG (-v / --version)
# =========================================================
def JT_version():
    from JCCS import __version__ as version

    out_s, err_s, code_s = Get.Redirect.cmd_all_std("JCCS", "-v")
    out_l, err_l, code_l = Get.Redirect.cmd_all_std("JCCS", "--version")

    Assertion.eq(out_s, out_l)
    Assertion.eq(err_s, err_l)
    Assertion.eq(code_s, code_l)
    Assertion.eq(err_s, "")
    Assertion.neq(out_s, "")
    Assertion.contain(version, out_s)


# =========================================================
# HELP FLAG (--help)
# =========================================================
def JT_help():
    out, err, code = Get.Redirect.cmd_all_std("JCCS", "--help")

    Assertion.eq(code, 0)
    Assertion.eq(err, "")
    Assertion.neq(out, "")
    Assertion.contain("usage", out.lower())
    Assertion.contain("jccs", out.lower())
    Assertion.contain("help", out.lower())


# =========================================================
# SHORT HELP (-h)
# =========================================================
def JT_short_help():
    out, err, code = Get.Redirect.cmd_all_std("JCCS", "-h")

    Assertion.eq(code, 0)
    Assertion.eq(err, "")
    Assertion.neq(out, "")


# =========================================================
# ARGUMENTS DISPLAY (-a / --show-arguments)
# =========================================================
def JT_arguments():
    out_s, err_s, code_s = Get.Redirect.cmd_all_std("JCCS", "-a")
    out_l, err_l, code_l = Get.Redirect.cmd_all_std("JCCS", "--show-arguments")

    Assertion.eq(out_s, out_l)
    Assertion.eq(err_s, err_l)
    Assertion.eq(code_s, code_l)
    Assertion.eq(err_s, "")
    Assertion.neq(out_s, "")
    Assertion.contain("JCCS - RULES", out_s)


# =========================================================
# UPDATE FLAG (--update)
# =========================================================
def JT_update():
    out, err, code = Get.Redirect.cmd_all_std("JCCS", "--update")

    Assertion.eq(code, 0)
    Assertion.eq(err, "")
    Assertion.neq(out, "")
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
        out_s, err_s, code_s = Get.Redirect.cmd_all_std("JCCS", short)
        out_l, err_l, code_l = Get.Redirect.cmd_all_std("JCCS", long)

        Assertion.eq(out_s, out_l)
        Assertion.eq(err_s, err_l)
        Assertion.eq(code_s, code_l)
        Assertion.eq(err_s, "")
        Assertion.neq(out_s, "")


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT_Builtins = JarTest()
failed: list = JTT_Builtins.fetch()
