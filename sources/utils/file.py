#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

class File:

    @staticmethod
    def read_file(file: str) -> list[str]:
        with open(file, "r") as f:
            return f.readlines()
