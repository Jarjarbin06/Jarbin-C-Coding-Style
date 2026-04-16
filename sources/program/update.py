#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

# Program imports #
from os.path import abspath
import jarbin_toolkit_console as Console
from subprocess import Popen, DEVNULL


print = Console.Console.print
Text = Console.Text.Text
Cursor = Console.ANSI.Cursor
Animation = Console.Animation

Console.init(banner=False)


# Program #
def update_jccs() -> None:
    spinner = Animation.Spinner.stick(style=Animation.Style(border_left="[", border_right="]")).warning()
    update_script = f"{abspath(__file__).removesuffix("sources/JCCS.py")}scripts/update-jccs"
    proc = Popen(["bash", str(update_script)], stdout=DEVNULL, stderr=DEVNULL)

    while proc.poll() is None:
        spinner()
        print(Text("JCCS").bold(), ":", Text(f"updating {spinner.render()}").warning() + Cursor.previous(), sleep=0.1)

    print(Text("JCCS").bold(), ":", Text("successfully updated").valid())
