#! /usr/bin/env python

import argparse
import linecache
import sys


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('input_file', help='input file')
    arg = parse.parse_args()

    fo = open(arg.input_file, 'r')
    input_file = fo.readlines()
    length = len(input_file)
    fo.close()

    s = {
        'space': ' ',
        'v_line':'|',
        'item': '|--',
        'item_line': '--',
    }

    fo = open(arg.input_file + 'path', 'w')

    for i in range(1, length):
        x = linecache.getline(arg.input_file, i)
        index = 0
        while x[index] == ' ':
            index = index + 1
        space_num = index
        line = ' '
        for step in range (0,space_num*4,2*6):
            line = line + s['v_line'] + s['space']*2*6
        line = line + s['item'] + s['item_line']*2

        sys.stdout.write(line)
        sys.stdout.write(' ' + x.split()[0] + '\n')
        line = line + ' ' + x.split()[0] + '\n'
        fo.write(line)

    fo.close()


if __name__ == '__main__':
    main()
