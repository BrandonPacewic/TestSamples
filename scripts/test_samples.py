#! /usr/bin/python3

from typing import List, Optional, Any, Tuple
from subprocess import Popen, PIPE
import sys
import os
import time
import logging


SEPARATOR = "-------------\n"
DBG_DEF = "DEBUG_MODE"


class colors:
    OKGREEN = '\033[92m'
    WARNINGRED = '\033[91m'
    WARNINGYELLOW = '\033[93m'
    ENDC = '\033[0m'


class errors:
    EXPECTED_ARGUMENTS = "[EXPECTED ONE ARGUMENTS]"
    INVALID_OPPERATOR = "[INVALID OPPERATOR FOUND]"
    NO_FILE = "[EXPECTED FILE FOUND NONE]"
    LEN_MISSMATCH = "[LINE LENGTH MISSMATCH]"
    NO_TARGET_LINE = f"[COULD NOT FIND TARGET LINE]{colors.ENDC} -> None"

    @staticmethod
    def file_not_found(*args) -> None:
        for arg in args:
            logging.error(f"{colors.WARNINGRED}[FILE NOT FOUND]{colors.ENDC} NO FILE IN DIR NAMED -> {arg}")
        exit()

    @staticmethod
    def gpp_file_not_found(file: str) -> None:
        logging.error(f"g++:{colors.WARNINGRED} error: {colors.ENDC}{file}: No such file found")
        exit()


def check_condition(
    condition: bool = False, 
    expect: bool = True, 
    color: str = colors.WARNINGRED, 
    msg: str = None, 
    leave: bool = True,
) -> None:
    """Template for basic console logging"""
    try:
        assert(condition is expect)
    except AssertionError:
        logging.error(f"{color}{msg}{colors.ENDC}")
        exit() if leave else print(f"{colors.WARNINGYELLOW}[WORKING]{colors.ENDC}")


def compair_output_vs_expected(programOutput: List[str], programExpected: List[str]) -> None:
    check_condition(
        len(programOutput) == len(programOutput), 
        color=colors.WARNINGYELLOW, 
        msg=errors.LEN_MISSMATCH, 
        leave=False,
    )

    def _compair_lines(primaryLines: List[str], secondaryLines: List[str]) -> Any:
        goodCount = 0
        missmatch = []
        for lineNum, (priLine, secLine) in enumerate(zip(primaryLines, secondaryLines)):
            if priLine == secLine: 
                goodCount += 1
            else: 
                missmatch.append((priLine, secLine, lineNum + 1))
        return goodCount, missmatch

    def _print_file_lines(lines: List[str], pend='') -> None:
        for line in lines:
            print(line, end=pend)

    def _print_args(*args, midend='', endmsg=None, finish='\n') -> None:
        for arg in args:
            print(arg, end=midend)
        print(endmsg, end=finish)

    def _assign_color(count: int, target: int) -> str:
        """For determining what msg color is needed"""
        if count == 0: 
            return colors.WARNINGRED
        elif count < target: 
            return colors.WARNINGYELLOW
        else: 
            return colors.OKGREEN

    print(f"{SEPARATOR}Expected:", end="\n\n")
    _print_file_lines(programExpected)

    print(f"\n{SEPARATOR}Output:", end="\n\n")
    _print_file_lines(programOutput)

    goodCount, missmatch = _compair_lines(programOutput, programExpected)

    print(f"\n{SEPARATOR}")
    _print_args(
        _assign_color(goodCount, len(programExpected)),
        goodCount,
        " / ",
        len(programExpected),
        " Tests Passed",
        endmsg=colors.ENDC,
        finish='\n\n',
    )

    for i, mv in enumerate(missmatch):
        print(f"Found: {mv[0][:-1]} ~ Expected: {mv[1][:-1]} ~ MissmatchOnLine: {mv[2]}")
        if i >= len(missmatch) - 1: print('', flush=True)


def get_file_lines(fname: str) -> List[str]:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
    except OSError:
        errors.file_not_found(fname)

    return lines


def start_tics() -> List[float]:
    return [time.perf_counter()]


def add_tic(tics: List[float]) -> None:
    tics.append(time.perf_counter())


def get_tic_elapsed(tics: List[int]) -> str:
    check_condition(len(tics) >= 2, msg="[ELAPSED IS NULL]")
    return str("{:.3f}".format(tics[-1] - tics[-2])) 


def locate_target_line(fname: str, target: str) -> Optional[int]:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line == target: 
                    return i
    except OSError:
        errors.file_not_found(fname)
    
    return None


def replace_line(fname: str, targetLine: int, replacementLine: str) -> None:
    if targetLine is None:
        check_condition(color=colors.WARNINGYELLOW, msg=errors.NO_TARGET_LINE, leave=False)
        return

    def _clear_file() -> None:
        file.truncate(0)
        file.seek(0)

    try:
        with open(fname, 'r+') as file:
            lines = file.readlines()
            lines[targetLine] = replacementLine
            _clear_file()
            file.writelines(lines)
    except OSError:
        errors.file_not_found(fname)


def gpp_assert_file_in_dir(fname: str) -> None:
    try:
        assert(fname in os.listdir())
    except AssertionError:
        errors.gpp_file_not_found(fname)


def cpp_program_interact(lines: List[str]) -> List[str]:
    program = Popen([f"{os.getcwd()}/a.out"], stdout=PIPE, stdin=PIPE)
    for line in lines:
        program.stdin.write(line.encode('utf-8'))
    program.stdin.flush()
    return [line.decode() for line in program.stdout.readlines()]


def whole_input_check(
    file: str = None,
    operator: str = None, 
    inputFile: str = None, 
    exitOperator: str = None, 
    expectedFile: str = None,
) -> None:
    check_condition(file is not None, msg=errors.NO_FILE)

    if operator is None:
        return

    def _check_file_real(*args) -> List[str]:
        """Returns a list of files that are not in the working dir"""
        return [arg for arg in args if not arg in os.listdir()]

    check_condition(
        operator == '/' and exitOperator == '/', 
        color=colors.WARNINGYELLOW, 
        msg=errors.INVALID_OPPERATOR, 
        leave=False,
    )

    check_condition(inputFile is not None and expectedFile is not None, msg=errors.NO_FILE)
    missingFiles = _check_file_real(inputFile, expectedFile)
    if len(missingFiles):
        errors.file_not_found(missingFiles)


def main(**kwargs):
    logging.basicConfig(
        level=logging.DEBUG, 
        format=f"{colors.WARNINGRED}[ERROR - %(asctime)s]{colors.ENDC} - %(message)s",
    )

    whole_input_check(
        kwargs.get("file"),
        kwargs.get("operator"), 
        kwargs.get("inputFile"), 
        kwargs.get("exitOperator"), 
        kwargs.get("expectedFile"),
    )

    does_need_suffix = lambda file: file if file[-3:] == ".cc" else f"{file}.cc"
    file = does_need_suffix(kwargs.get("file"))

    def set_default(file: str) -> Tuple[str, str]:
        return f"{file[:-3]}_input.txt", f"{file[:-3]}_expected.txt"

    if kwargs.get("operator") is None: 
        inputFile, expectedFile = set_default(file)
    else:
        inputFile, expectedFile = kwargs.get("inputFile"), kwargs.get("expectedFile")

    gpp_assert_file_in_dir(file)
    targetLine = locate_target_line(file, target="//dbg\n")

    replace_line(file, targetLine, replacementLine="#define DBG_MODE\n")
    os.system(f"g++ -g -std=c++17 -Wall -D{DBG_DEF} {file}")
    replace_line(file, targetLine, replacementLine="//dbg\n")

    tics = start_tics()
    programOutput = cpp_program_interact(get_file_lines(inputFile))
    add_tic(tics)

    print("Compairing...")
    print(f"Time: {get_tic_elapsed(tics)}s")
    compair_output_vs_expected(programOutput, get_file_lines(expectedFile))


if __name__ == '__main__':
    check_condition(len(sys.argv) > 6, expect=False, msg="MAX OF 6 ARGUMENTS IS TO BE PROVIDED")
    main(
        file=sys.argv[1] if len(sys.argv) >= 2 else None, 
        operator=sys.argv[2] if len(sys.argv) >= 3 else None, 
        inputFile=sys.argv[3] if len(sys.argv) >= 4 else None, 
        exitOperator=sys.argv[4] if len(sys.argv) >= 5 else None, 
        expectedFile=sys.argv[5] if len(sys.argv) == 6 else None,
    )
