#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

class Format:

    @staticmethod
    def error(index: int | tuple[int, int], line: str, reason: str) -> str:

        def get_lines():

            string = ""

            for l in line.split("\n"):
                string += f"\"{l}\"\n"

            return string[:-1]

        return (
            f"{(
                f"from line number {index[0] + 1} to {index[1] + 1}:\n"
                if isinstance(index, tuple) else
                f"line number {index + 1}:\n"
            )}"
            f"---\n"
            f"{get_lines()}\n"
            f"---\n"
            f"{reason}"
    )
