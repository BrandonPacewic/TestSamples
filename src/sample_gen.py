#! /usr/bin/python3

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Generate new test samples')
    parser.add_argument('file', help='File to generate samples for')
    args = parser.parse_args()

    file = args.file

    if file.endswith('.cpp'):
        file = file[:-4]

    if file.startswith('.\\'):
        file = file[2:]

    test_input = f'{file}_input.txt'
    test_output = f'{file}_output.txt'

    os.system(f'code {test_output}')
    os.system(f'code {test_input}')

    
if __name__ == '__main__':
    main()
