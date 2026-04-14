#############################
###                       ###
###         JCCS          ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################

def strip_c_comments(lines: list[str]) -> list[tuple[int, str]]:
    """
    Returns list of (line_index, line) without block comments.
    """

    result = []
    is_comment = False

    for i, line in enumerate(lines):

        if "/*" in line:
            is_comment = True

        if not is_comment:
            result.append((i, line))

        if "*/" in line:
            is_comment = False

    return result