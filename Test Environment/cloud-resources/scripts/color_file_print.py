import argparse
from python_lib.msg_format import mcolors
def main():
    """
    Main entry point
    """
    # Import Args
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', dest='input', help='Folder containing each of the projects.')
    parser.add_argument('--red_line_strings', action='store', type=str, dest='red_line_strings', help='These strings separated by commas, will print the whole line red.')
    parser.add_argument('--yellow_line_strings', action='store', type=str, dest='yellow_line_strings', help='These strings separated by commas, will print the whole line yellow.')
    parser.add_argument('--green_line_strings', action='store', type=str, dest='green_line_strings', help='These strings separated by commas, will print the whole line green.')
    parser.add_argument('--red_strings', action='store', type=str, dest='red_strings', help='These strings separated by commas, will print red.')
    parser.add_argument('--yellow_strings', action='store', type=str, dest='yellow_strings', help='These strings separated by commas, will print yellow.')
    parser.add_argument('--green_strings', action='store', type=str, dest='green_strings', help='These strings separated by commas, will print green.')
    parser.add_argument('--split_char', action='store', type=str, dest='split_char', help='Character that will split the strings, default is commas.')
    """
    Note:
        The list of strings is not case sensitive.

        The order of the lists matters. The first list will have priority over the second and so on.
        Therefore red_line_strings takes priority over yellow_strings, so if a string in red_line_strings is in the given
        input the whole line will be the color red regardless of what else is in the following lists.
    """
    args = parser.parse_args()

    use_default_settings = True
    if args.split_char != None:
        split_char = args.split_char
    else:
        split_char = ','

    if args.red_line_strings != None:
        red_line_strings = args.red_line_strings.split(split_char)
        use_default_settings = False
    else:
        red_line_strings = []
    if args.yellow_line_strings != None:
        yellow_line_strings = args.yellow_line_strings.split(split_char)
        use_default_settings = False
    else:
        yellow_line_strings = []
    if args.green_line_strings != None:
        green_line_strings = args.green_line_strings.split(split_char)
        use_default_settings = False
    else:
        green_line_strings = []

    if args.red_strings != None:
        red_strings = args.red_strings.split(split_char)
        use_default_settings = False
    else:
        red_strings = []
    if args.yellow_strings != None:
        yellow_strings = args.yellow_strings.split(split_char)
        use_default_settings = False
    else:
        yellow_strings = []
    if args.green_strings != None:
        green_strings = args.green_strings.split(split_char)
        use_default_settings = False
    else:
        green_strings = []

    if use_default_settings:
        mcolors.print_file(args.input, #If at least one of these strings are present in a line of input...
        ["Denied", "Validating", "VALIDATING POLICY DETAIL"],               #The whole line will print red.
        ["warning"],                                                        #The whole line will print yellow.
        [",", "Projects Allowed", "OVERALL POLICY DETAILS"],                #The whole line will print green.
        ["Not Allowed", "Allowed: False"],                                  #The string alone will be red.
        [">>> POLICY DETAIL <<<", "Allowed: Not Enforced - False"],         #The string alone will be yellow.
        ["Allowed: True", "Project(s) Allowed", "Project(s)", "Allowed"])   #The string alone will be green.
    else:
        mcolors.print_file(args.input, red_line_strings, yellow_line_strings, green_line_strings, red_strings, yellow_strings, green_strings)

if __name__ == "__main__":
    main()
