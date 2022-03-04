#pylint: disable=C0325, C0301, C0114, C0103, C0115, C0116, E0213, E1133, R0913, E1101, R1732
# Standard library imports
#import pathlib
#import sys

class mcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def printFail(msg):
        print(f"{mcolors.FAIL}{msg}{mcolors.ENDC}", end = "")

    def printWarning(msg):
        print(f"{mcolors.WARNING}{msg}{mcolors.ENDC}", end = "")

    def printOKGREEN(msg):
        print(f"{mcolors.OKGREEN}{msg}{mcolors.ENDC}", end = "")

    def line_print(line):
        # Input: ['Plain text ', (0, 'red text'), ' plain text.']
        for item in line:
            if isinstance(item, str):
                print(item, end = "")
            elif item[0] == 0:
                print(f"{mcolors.FAIL}{item[1]}{mcolors.ENDC}", end = "")
            elif item[0] == 1:
                print(f"{mcolors.WARNING}{item[1]}{mcolors.ENDC}", end = "")
            elif item[0] == 2:
                print(f"{mcolors.OKGREEN}{item[1]}{mcolors.ENDC}", end = "")

    def process_word_list(word_list, line_input, color):
        for word in word_list:
            i = 0
            while(i != len(line_input)):
                if isinstance(line_input[i], str) and word.lower() in line_input[i].lower():
                    string_input = line_input.pop(i)
                    location = string_input.lower().find(word.lower())
                    line_input.insert(i, string_input[:location])
                    line_input.insert(i+1, (color, string_input[location:location + len(word)]))
                    line_input.insert(i+2, string_input[location + len(word):])
                    i += 2
                else:
                    i += 1
        return line_input

    def print_color_line(line, denied_line_words, warning_line_words, allowed_line_words,
                                                denied_words, warning_words, allowed_words):
        stop = False
        for word in denied_line_words:
            if word.lower() in line.lower():
                mcolors.printFail(line)
                stop = True
                break
        if stop:
            return

        for word in warning_line_words:
            if word.lower() in line.lower():
                mcolors.printWarning(line)
                stop = True
                break
        if stop:
            return

        for word in allowed_line_words:
            if word.lower() in line.lower():
                mcolors.printOKGREEN(line)
                stop = True
                break
        if stop:
            return

        line_list = [line]
        line_list = mcolors.process_word_list(denied_words, line_list, 0)
        line_list = mcolors.process_word_list(warning_words, line_list, 1)
        line_list = mcolors.process_word_list(allowed_words, line_list,  2)
        mcolors.line_print(line_list)

    def print_file(file_location, denied_line_words, warning_line_words, allowed_line_words,
                                                denied_words, warning_words, allowed_words):
        file = open(file_location, "r")
        for line in file:
            mcolors.print_color_line(line, denied_line_words, warning_line_words, allowed_line_words,
                                                denied_words, warning_words, allowed_words)
        print()
        file.close()
