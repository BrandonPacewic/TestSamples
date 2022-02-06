#! /usr/bin/python3

from typing import List, Optional

import argparse
import logging
import os


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

    sys.stdout.write(f'{symbol * length}')

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
        logging.error(f'{color}{msg}{colors.ENDC}')
        exit() if leave else print(f'{colors.WARNINGYELLOW}[WORKING]{colors.ENDC}')


def file_not_found(*args) -> None:
    for arg in args:
        logging.error(f'{colors.WARNINGRED}[FILE NOT FOUND]{colors.ENDC} NO FILE IN DIR NAMED -> {arg}')
    exit()


def do_files_exist(*args) -> bool:
    exist = [True if arg in os.listdir() else False for arg in args]
    if all(exist):
        for arg in args:
            logging.info(f'{colors.WARNINGYELLOW}[WARNING]{colors.ENDC} found existing file -> {arg}')
        check_condition(color=colors.WARNINGYELLOW,
                        msg='[WORKING]', leave=False)
        return True
    return False


def multi_input() -> List[str]:
    inputs = []
    while True:
        currentInput = f'{str(input())}\n'
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


def create_files(file: str) -> None:
    print(f'[CREATEING FILES] With Base -> {file}')
    os.system(f'touch {file}_input.txt')
    os.system(f'touch {file}_expected.txt')


def main(file: str):
    logging.basicConfig(
        level=logging.DEBUG,
        format=f'{colors.WARNINGRED}[ERROR - %(asctime)s]{colors.ENDC} - %(message)s',
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    file = args.file[0]

    file = file if file[-3:] != '.cc' else file[:-3]
    inputFile = f'{file}_input.txt'
    expectedFile = f'{file}_expected.txt'

    if not do_files_exist(f'{file}_input.txt', f'{file}_expected.txt'):
        create_files(file)

    separator(symbol='-', length=13, semi=False, startNew=False)
    inputLines = muti_input()
    write_lines(inputFile, inputLines)

    separator(symbol='-', length=13, semi=False, startNew=False)
    expectedLines = muti_input()
    write_lines(expectedFile, expectedLines)

    separator(symbol='-', length=13, semi=False)
    print(f'{colors.OKGREEN}[ACCEPTED]{colors.ENDC}', end='\n\n')


if __name__ == '__main__':
    main()
