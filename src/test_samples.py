#! /usr/bin/python3

from subprocess import Popen, PIPE
from typing import List, Optional

import argparse
import logging
import os
import sys
import time

DEBUG_MACRO = '#ifdef DBG_MODE\n'
DEBUG_DEFINITION = 'DBG_MODE'

def separator(*values: Optional[object], symbol: str = '-', separator: str = '', 
              length: int = 3, semi: bool = True, start_new: bool = True, 
              end_new: bool = True) -> None:
    if start_new:
        sys.stdout.write('\n')

    sys.stdout.write(f'{symbol * length}')

    if semi:
        sys.stdout.write(':')

    if end_new:
        sys.stdout.write('\n')

    for value in values:
        sys.stdout.write(f'{value}{separator}')

    sys.stdout.write('\n')
    sys.stdout.flush()


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


class Timer:
    def __init__(self):
        self.tics = [time.perf_counter()]

    def add_tic(self) -> None:
        self.tics.append(time.perf_counter())

    def get_elapsed(self) -> str:
        try:
            return str('{:.3f}'.format(self.tics[-1] - self.tics[-2]))
        except IndexError:
            print('Elapsed is null')


def check_condition(condition: bool = False, expect: bool = True, color: str = Colors.RED, 
                    msg: str = None, leave: bool = True) -> None:
    """Template for basic console logging"""
    try:
        assert(condition is expect)
    except AssertionError:
        logging.error(f'{color}{msg}{Colors.END}')
        
        if leave:
            exit()
        else:
            logging.info(f'{Colors.YELLOW}[WORKING...]{Colors.END}')


class Errors:
    EXPECTED_ARGUMENTS = '[EXPECTED ONE ARGUMENT]'
    INVALID_OPERATOR = '[INVALID OPERATOR FOUND]'
    NO_FILE = '[EXPECTED FILE FOUND NONE]'
    LENGTH_MISMATCH = '[LINE LENGTH MISMATCH]'
    NO_TARGET_LINE = '[NO TARGET LINE FOUND]'


def print_file_lines(lines: List[str]) -> None:
    for line in lines:
        print(line, end='')


def compare_output_against_expected(program_output: List[str], expected_output: List[str]) -> None:
    """Compares the output of a program against the expected output"""
    check_condition(len(program_output) == len(expected_output), True, 
                    Colors.RED, Errors.LENGTH_MISMATCH, False)

    good_count = 0
    mismatches = []

    for i, (output, expected) in enumerate(zip(program_output, expected_output)):
        if output == expected:
            good_count += 1
        else:
            mismatches.append((output, expected, i))

    separator('Expected', length=14, semi=False, start_new=False)
    print_file_lines(expected_output)

    separator('Output:', length=14, semi=False, start_new=True)
    print_file_lines(program_output)

    separator(length=14, semi=False, start_new=True)

    color = Colors.GREEN if good_count == len(program_output) else Colors.RED

    print(f'{color}{good_count} / {len(program_output)} Tests Passed{Colors.END}\n')

    for i, mismatch in enumerate(mismatches):
        print(f'Found: {mismatch[0][:-1]} ~ Expected: {mismatch[1][:-1]} ~ Test: {mismatch[2] + 1}')

        if i >= len(mismatches) -1:
            print('') # New line


def get_file_lines(fname: str) -> List[str]:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error(f'{Colors.RED}{Errors.NO_FILE}{Colors.END}')
        exit()

    return lines


def locate_target_line(fname: str, target: str) -> int:
    try:
        with open(fname, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error(f'{Colors.RED}{Errors.NO_FILE}{Colors.END}')
        exit()

    for i, line in enumerate(lines):
        if target in line:
            return i

    logging.error(f'{Colors.RED}{Errors.NO_TARGET_LINE}{Colors.END}')
    exit()


def cpp_program_interact(input: List[str], file: str) -> any:
    compile_time = Timer()
    os.system(f'g++ -g -std=c++17 -Wall -D{DEBUG_DEFINITION} {file}')
    compile_time.add_tic()

    program = Popen([f'{os.getcwd()}/a.out'], stdin=PIPE, stdout=PIPE)
    run_time = Timer()

    for line in input:
        program.stdin.write(line.encode())

    program.stdin.flush()
    program.stdin.close()
    run_time.add_tic()

    output = [line.decode() for line in program.stdout.readlines()]

    return output, compile_time, run_time


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='C++ Test Runner')
    parser.add_argument('file', type=str, help='The file to run')
    args = parser.parse_args()

    file = args.file

    if file[-4:] != '.cpp':
        file += '.cpp'

    check_condition(locate_target_line(file, DEBUG_MACRO) is not None, True, 
                                       Colors.YELLOW, Errors.NO_TARGET_LINE, False)
    program_input = get_file_lines(f'{file[:-4]}_input.txt')
    expected_output = get_file_lines(f'{file[:-4]}_expected.txt')
    program_output, compile_time, run_time = cpp_program_interact(program_input, file)

    print('Comparing...')
    print(f'Compile Time: {compile_time.get_elapsed()}')
    print(f'Run Time: {run_time.get_elapsed()}')
    compare_output_against_expected(program_output, expected_output)


if __name__ == '__main__':
    main()