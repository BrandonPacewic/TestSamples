#! /usr/bin/python3

from subprocess import Popen, PIPE
from typing import List, Optional, Tuple

import argparse
import logging
import os
import sys
import time

DBG_DEF = 'DBG_MODE'


"""Should be added to a new modual"""
def separator(
    *values: Optional[object],
    symbol: str, 
    sep: Optional[str] = '', 
    length: int = 3, 
    semi: bool = True, 
    startNew: bool = True, 
    endNew: bool = True,
    ) -> None:
    if startNew:
        sys.stdout.write('\n')

    for _ in range(length):
        sys.stdout.write(symbol)

    if semi:
        sys.stdout.write(':')

    if endNew:
        sys.stdout.write('\n')

    for value in values:
        sys.stdout.write(f'{value}{sep}')

    sys.stdout.write('\n')
    sys.stdout.flush()

class colors:
    OKGREEN = '\033[92m'
    WARNINGRED = '\033[91m'
    WARNINGYELLOW = '\033[93m'
    ENDC = '\033[0m'


class errors:
    EXPECTED_ARGUMENTS = '[EXPECTED ONE ARGUMENTS]'
    INVALID_OPPERATOR = '[INVALID OPPERATOR FOUND]'
    NO_FILE = '[EXPECTED FILE FOUND NONE]'
    LEN_MISSMATCH = '[LINE LENGTH MISSMATCH]'
    NO_TARGET_LINE = f'[COULD NOT FIND TARGET LINE]{colors.ENDC} -> None'

    @staticmethod
    def file_not_found(*args) -> None:
        for arg in args:
            logging.error(f'{colors.WARNINGRED}[FILE NOT FOUND]{colors.ENDC} NO FILE IN DIR NAMED -> {arg}')
        exit()

    @staticmethod
    def gpp_file_not_found(file: str) -> None:
        logging.error(f'g++:{colors.WARNINGRED} error: {colors.ENDC}{file}: No such file found')
        exit()

    """Template for basic console logging"""
    @staticmethod
    def check_condition(
        condition: bool = False, 
        expect: bool = True, 
        color: str = colors.WARNINGRED, 
        msg: str = None, 
        leave: bool = True,
    ) -> None:
        try:
            assert(condition is expect)
        except AssertionError:
            logging.error(f'{color}{msg}{colors.ENDC}')
            exit() if leave else print(f'{colors.WARNINGYELLOW}[WORKING]{colors.ENDC}')


class timer:
    def __init__(self):
        self.tics = [time.perf_counter()]

    def add_tic(self) -> None:
        self.tics.append(time.perf_counter())

    def get_elapsed(self) -> str:
        try:
            return str('{:.3f}'.format(self.tics[-1] - self.tics[-2]))
        except IndexError:
            print('Elapsed is null')
            exit()


def compair_output_vs_expected(programOutput: List[str], programExpected: List[str]) -> None:
    def _compair_lines(
        primaryLines: List[str], 
        secondaryLines: List[str]
    ) -> Tuple[int, List[Tuple[str, str, int]]]:
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

    errors.check_condition(
        len(programOutput) == len(programExpected), 
        color=colors.WARNINGYELLOW, 
        msg=errors.LEN_MISSMATCH, 
        leave=False,
    )

    separator(
        'Expected:',
        symbol='-',
        length=14,
        semi=False,
        startNew=False,
    )
    _print_file_lines(programExpected)


    separator(
        'Output:',
        symbol='-',
        length=14,
        semi=False,
    )
    _print_file_lines(programOutput)

    goodCount, missmatch = _compair_lines(programOutput, programExpected)

    separator(
        symbol='-',
        length=14,
        semi=False,
        startNew=False,
    )
    _print_args(
        _assign_color(goodCount, len(programExpected)),
        goodCount,
        ' / ',
        len(programExpected),
        ' Tests Passed',
        endmsg=colors.ENDC,
        finish='\n\n',
    )

    for i, mv in enumerate(missmatch):
        print(f'Found: {mv[0][:-1]} ~ Expected: {mv[1][:-1]} ~ Line: {mv[2]}')
        
        if i >= len(missmatch) - 1: 
            print('', flush=True)


def get_file_lines(fname: str) -> List[str]:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
    except OSError:
        errors.file_not_found(fname)

    return lines


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


def cpp_program_interact(lines: List[str], file: str) -> List[str]:
    def _gpp_assert_file_in_dir(fname: str) -> None:
        try:
            assert(fname in os.listdir())
        except AssertionError:
            errors.gpp_file_not_found(fname)

    _gpp_assert_file_in_dir(file)
    os.system(f'g++ -g -std=c++17 -Wall -D{DBG_DEF} {file}')

    program = Popen([f'{os.getcwd()}/a.out'], stdout=PIPE, stdin=PIPE)
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
    def _check_file_real(*args) -> List[str]:
        """Returns a list of files that are not in the working dir"""
        return [arg for arg in args if not arg in os.listdir()]

    errors.check_condition(file is not None, msg=errors.NO_FILE)

    if operator is None:
        return

    errors.check_condition(
        operator == '/' and exitOperator == '/', 
        color=colors.WARNINGYELLOW, 
        msg=errors.INVALID_OPPERATOR, 
        leave=False,
    )

    errors.check_condition(inputFile is not None and expectedFile is not None, msg=errors.NO_FILE)
    missingFiles = _check_file_real(inputFile, expectedFile)
    if len(missingFiles):
        errors.file_not_found(missingFiles)


def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format=f'{colors.WARNINGRED}[ERROR - %(asctime)s]{colors.ENDC} - %(message)s',
    )

    """Argument Parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, metavar='N', nargs='+')
    args = parser.parse_args()

    file = args.input[0]
    inputOperator = args.input[1] if len(args.input) > 1 else None
    inputFile = args.input[2] if len(args.input) > 2 else None
    exitOperator = args.input[3] if len(args.input) > 3 else None
    expectedFile = args.input[4] if len(args.input) > 4 else None

    whole_input_check(
        file,
        inputOperator,
        inputFile,
        exitOperator,
        expectedFile,
    )

    """Add suffix"""
    file = file + '.cc' if file[-3:] != '.cc' else file

    """Set to default"""
    if inputOperator is None: 
        inputFile, expectedFile = f'{file[:-3]}_input.txt', f'{file[:-3]}_expected.txt'

    """Looking for debug template"""
    errors.check_condition(
        locate_target_line(file, target='//dbg\n') is not None, 
        color=colors.WARNINGYELLOW, 
        msg=errors.NO_TARGET_LINE, leave=False,
    )

    """Running"""
    tics = timer()
    programOutput = cpp_program_interact(get_file_lines(inputFile), file)
    tics.add_tic()

    """Program output"""
    print('Compairing...')
    print(f'Time: {tics.get_elapsed()}s')
    compair_output_vs_expected(
        programOutput, 
        get_file_lines(expectedFile)
    )


if __name__ == '__main__':
    main()