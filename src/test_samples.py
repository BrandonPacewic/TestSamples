# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import os
import time

from subprocess import Popen, PIPE

DEBUG_DEFINITION = 'DBG_MODE'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


class Timer:
    def __init__(self):
        self.tics = [time.perf_counter()]

    def add_tic(self):
        self.tics.append(time.perf_counter())

    def get_elapsed(self):
        try:
            return str('{:.3f}'.format(self.tics[-1] - self.tics[-2]))
        except IndexError:
            print('Elapsed is null')
            exit()


def print_file_lines(lines):
    for i, line in enumerate(lines):
        print(line.strip(), end='\n' if i != len(lines) - 1 else '')


def get_file_lines(fname):
    with open(fname, 'r') as file:
        return file.readlines()


def cpp_program_interact(input_lines, file):
    compile_time = Timer()
    os.system(f'g++ -g -std=c++17 -Wall -D{DEBUG_DEFINITION} {file}')
    compile_time.add_tic()

    program = Popen(f'./a.exe', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    run_time = Timer()

    for line in input_lines:
        program.stdin.write(line.encode())

    program.stdin.flush()
    program.stdin.close()
    run_time.add_tic()

    output = [line.decode() for line in program.stdout.readlines()]

    return output, compile_time.get_elapsed(), run_time.get_elapsed()


def main():
    parser = argparse.ArgumentParser(description='C++ Test Runner')
    parser.add_argument('file', type=str, help='C++ file to run against tests')
    args = parser.parse_args()

    file = args.file

    if not file.endswith('.cpp'):
        file += '.cpp'

    if file.startswith('.\\'):
        file = file[2:]

    test_input = f'{file.split(".")[0]}_input.txt'
    test_output = f'{file.split(".")[0]}_output.txt'

    program_input = get_file_lines(test_input)
    program_expected_output = get_file_lines(test_output)
    program_actual_output, compile_time, run_time = cpp_program_interact(program_input, file)

    print('Comparing...')
    print(f'Compile time: {compile_time}s')
    print(f'Run time: {run_time}s', end='')

    good_count = 0
    total_count = len(program_expected_output)
    mismatches = []

    for i, output in enumerate(program_actual_output):
        program_actual_output[i] = output.strip()

    for i, expected in enumerate(program_expected_output):
        program_expected_output[i] = expected.strip()

    for i, (output, expected) in enumerate(zip(program_actual_output, program_expected_output)):
        if output == expected:
            good_count += 1
        else:
            mismatches.append((output, expected, i + 1))

    print('\n--------------')
    print('Expected:')
    print_file_lines(program_expected_output)

    print('\n--------------')
    print('Actual:')
    print_file_lines(program_actual_output)

    print('\n--------------')

    if len(mismatches) > 0:
        print('Mismatches:')

    for mismatch in mismatches:
        print(f'Line {mismatch[2]}: {Colors.RED}{mismatch[0]}{Colors.END} != {Colors.GREEN}{mismatch[1]}{Colors.END}')

    if good_count == len(program_expected_output):
        print(f'{Colors.GREEN}All tests passed!{Colors.END}')
    elif good_count >= 1:
        print(f'{Colors.YELLOW}{good_count} / {total_count} tests passed.{Colors.END}')
    else:
        print(f'{Colors.RED}No tests passed.{Colors.END}')


if __name__ == '__main__':
    main()
