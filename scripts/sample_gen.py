#! /usr/bin/python3

# usage sample_gen <filename (without file suffix)> (create all files for running and testing competitive coding samples)

import os
import sys

class colors:
    OKGREEN = '\033[92m'
    WARNINGRED = '\033[91m'
    WARNINGYELLOW = '\033[93m'


def createFiles(file):
    os.system(f"touch {file}_input.txt")
    os.system(f"touch {file}_expected.txt")


def multiInput():
    inputs = []

    while True:
        currentInput = str(input()) + '\n'
        if currentInput == '\n':
            return inputs
        else:
            inputs.append(currentInput)


def setInputTxt(file):
    print("[INPUT TEXT] Enter Input")
    linesInput = multiInput()

    with open(file + "_input.txt", 'w') as f:
        f.writelines(linesInput)


def setOutputTxt(file):
    print("--------------------------", end="\n\n")
    print("[EXAMPLE TEXT] Enter Expected")
    linesInput = multiInput()

    with open(file + "_expected.txt", 'w') as f:
        f.writelines(linesInput)


def main(file):
    print("[CREATEING SAMPLE TEXT FILES]")

    createFiles(file)
    setInputTxt(file)
    setOutputTxt(file)

    print(f"{colors.OKGREEN}[Accepted]\n")


if __name__ == "__main__":
    try:
        assert(len(sys.argv) == 2)
    except AssertionError:
        print(f"{colors.WARNINGRED}[EXPECTED ONE ARGUMENT]")
        exit()

    main(sys.argv[1])