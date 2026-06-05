#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

from jarbin_toolkit_jartest import JarTest

# =========================================================
# IMPORT TESTS
# =========================================================
from tests.JT_Flags import JT_Builtins
from tests.JT_Flags import JT_Arg
from tests.JT_Flags import JT_Logs
from tests.JT_Flags import JT_Combinations


# =========================================================
# REGISTER TEST SUITE
# =========================================================
JTT: JarTest = JarTest()
JTT.fetch_tests()
