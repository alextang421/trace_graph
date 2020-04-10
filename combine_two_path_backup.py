#! /usr/bin/env python

import argparse
import linecache
import sys

# def abstract(file_list,combine_list):

def abstract_file(file1,file2):
    new_file = []
    diff_start = 0
    diff_end =0
    diff_color_start = '\033[94m'
    diff_color_end = '\033[0m'


    for i in range(0,len(file1)):
        if file1[i] != file2[i]:
            diff_start = i
            new_file.append(diff_color_start + '-----------------------------------diff path start-----------------------------------' + diff_color_end + '\n')
            break
        else:
            new_file.append(file1[i])

        if i == len(file1) -1 :
            diff_start = len(file1)
            new_file.append(
                diff_color_start + '-----------------------------------diff path start-----------------------------------' + diff_color_end + '\n')


    times = 0
    for j in range(len(file2)-1, 0, -1):
        if file2[j] != file1[len(file1)-1 - times]:
            diff_end = j
            break
        else:
            times = times + 1

    for i in range(diff_start, diff_end+1):
        new_file.append(diff_color_start + file2[i] + diff_color_end)
    new_file.append(diff_color_start + '-----------------------------------diff path end-----------------------------------' + diff_color_end + '\n')
    for i in range(diff_start,len(file1)):
        new_file.append(file1[i])

    for i in range(0, len(new_file)):
        sys.stdout.write(new_file[i])



def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('input_file', nargs='+', help='input file')
    arg = parse.parse_args()

    file_list = []
    for file in arg.input_file:
        # each file create a 'line list'
        fo = open(file, 'r')
        input_file = fo.readlines()
        length = len(input_file)
        fo.close()

        s = {
            'space': ' ',
            'v_line': '|',
            'item': '|--',
            'item_line': '--',
        }
        line_list = []
        for i in range(1, length+1):
            x = linecache.getline(file, i)
            index = 0
            while x[index] == ' ':
                index = index + 1
            space_num = index
            line = ' '
            for step in range(0, space_num * 4, 2 * 6):
                line = line + s['v_line'] + s['space'] * 2 * 6
            line = line + s['item'] + s['item_line'] * 2
            # this line without function is the last

          #  sys.stdout.write(line)
          #  sys.stdout.write(' ' + x.split()[0] + '\n')
            line = line + ' ' + x.split()[0] + '\n'
            # this line is the complete line
            line_list.append(line)
        file_list.append(line_list)

    file1 = file_list[0]
    file2 = file_list[1]
    abstract_file(file1,file2)


if __name__ == '__main__':
    main()
