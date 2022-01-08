#! /usr/bin/python3

# usage sample_gen <filename (without file suffix)> (create all files for running and testing competitive coding samples)

from typing import List, Optional
import os
import sys
import logging


class colors:
    OKGREEN = '\033[92m'
    WARNINGRED = '\033[91m'
    WARNINGYELLOW = '\033[93m'
    ENDC = '\033[0m'


def check_condition(
    condition: bool = False, 
    expect: bool = True, 
    color: str = colors.WARNINGRED, 
    msg: str = None, 
    leave: bool = True,
) -> Optional[exit]:
    """Template for basic console logging"""
    try:
        assert(condition is expect)
    except AssertionError:
        logging.error(f"{color}{msg}{colors.ENDC}")
        exit() if leave else print(f"{colors.WARNINGYELLOW}[WORKING]{colors.ENDC}")


def file_not_found(*args) -> exit:
    for arg in args:
        logging.error(f"{colors.WARNINGRED}[FILE NOT FOUND]{colors.ENDC} NO FILE IN DIR NAMED -> {arg}")
    exit()


def do_files_exist(*args) -> bool:
    exist = [True if arg in os.listdir() else False for arg in args]
    if all(exist):
        for arg in args:
            logging.info(f"{colors.WARNINGYELLOW}[WARNING]{colors.ENDC} found existing file -> {arg}")
        check_condition(color=colors.WARNINGYELLOW, msg="[WORKING]", leave=False)
        return True
    return False
    

def create_files(file: str) -> None:
    print(f"[CREATEING FILES] With Base -> {file}")
    os.system(f"touch {file}_input.txt")
    os.system(f"touch {file}_expected.txt")


def multi_input() -> List[str]:
    inputs = []
    while True:
        currentInput = f"{str(input())}\n"
        if currentInput == '\n':
            return inputs
        else:
            inputs.append(currentInput)


def write_lines(fname: str, lines: List[str]) -> None:
    try:
        with open(fname, 'w') as file:
            file.writelines(lines)
    except OSError:
        file_not_found(fname)


def main(file: str):
    logging.basicConfig(
        level=logging.DEBUG,
        format=f"{colors.WARNINGRED}[ERROR - %(asctime)s]{colors.ENDC} - %(message)s",
    )

    def _seperator(
        initalNewLine: bool = False, 
        endNewLine: bool = True,
        dashCount: int = 5,
    ) -> None:
        def _print_args(*args, midend='', endmsg=None, finish='\n') -> None:
            for arg in args:
                print(arg, end=midend)
            print(endmsg if endmsg is not None else '', end=finish)
        
        _print_args(
            '\n' if initalNewLine else '', 
            ''.join('-' for _ in range(dashCount)),
            finish='\n\n' if endNewLine else '\n'
            )

    def _set_input_file(file: str) -> None:
        print("[INPUT TEXT] Enter Input:")
        _seperator(endNewLine=False, dashCount=14)
        inputLines = multi_input()
        write_lines(file, inputLines)

    def _set_expected_file(file: str) -> None:
        _seperator(dashCount=14)
        print("[EXPECTED TEXT] Enter Expected")
        _seperator(endNewLine=False, dashCount=14)
        inputLines = multi_input()
        write_lines(file, inputLines)

    correct_file_name = lambda file: file if file[-3:] != ".cc" else file[:-3]
    file = correct_file_name(file)

    if not do_files_exist(f"{file}_input.txt", f"{file}_expected.txt"):
        create_files(file)

    _set_input_file(f"{file}_input.txt")
    _set_expected_file(f"{file}_expected.txt")
    _seperator(dashCount=14)
    print(f"{colors.OKGREEN}[Accepted]\n")


if __name__ == "__main__":
    check_condition(len(sys.argv) == 2, msg="[EXPECTED ONE ARGUMENT]")
    main(sys.argv[1])
