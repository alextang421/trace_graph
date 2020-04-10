#! /usr/bin/env python
# 2020.2.25, Alex Tang

import argparse
import linecache
import sys
import hashlib


def combine(diff_start_dict, md5_list, file_main):
    """
    this function insert the md5 to the file_main
    """
    sorted_dict = sorted(diff_start_dict.items(), key=lambda x: x[1], reverse=True)

    for i in range(0, len(sorted_dict)):
        md5 = md5_list[sorted_dict[i][0]]
        md5 = '-----------------------' + md5 + '-----------------------' + '\n'
        start = sorted_dict[i][1]
        pos = 0
        for j in range(start, start + len(md5)):
            file_main.insert(j, md5[pos])
            pos += 1


def save_as_md5(md5,diff_part,dir):
    path = dir + md5
    fo = open(path,'w')
    for i in diff_part:
        fo.write(i);
    fo.close()


def write_to_output(file_main, fo):
    for line in file_main:
        fo.write(line)


def combine_file(file_main, file_remain,dir):

    diff_part_list = []
    # used to store the diff part of the file
    md5_list = []
    # transfer the diff part into md5 and store
    diff_start = 0
    diff_end = 0
    diff_color_start = '\033[94m'
    diff_color_end = '\033[0m'
    diff_name = 1

    diff_start_dict = {}
    dict = 0
    for file_diff in file_remain:
        # collect the diff part into the diff_part_list
        diff_part = []
        for i in range(0, len(file_main)):
            if file_main[i] != file_diff[i]:
                diff_start = i
                break

            if i == len(file_main) - 1:
                diff_start = len(file_main)
        diff_start_dict[dict] = diff_start
        dict += 1

        times = 0
        for j in range(len(file_diff) - 1, 0, -1):
            if file_diff[j] != file_main[len(file_main) - 1 - times]:
                diff_end = j
                break
            else:
                times = times + 1

        for i in range(diff_start, diff_end + 1):
            diff_part.append(diff_color_start + file_diff[i] + diff_color_end)

        str_diff_part = "".join(diff_part)
        md5 = hashlib.md5(str_diff_part.encode('utf-8')).hexdigest()
        md5_list.append(md5)
        save_as_md5(md5,diff_part,dir)
        diff_part_list.append(diff_part)

        diff_name += 1

    combine(diff_start_dict, md5_list, file_main)


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('input_file', nargs='+', help='input file')
    parse.add_argument('-d', '--dir', dest='output_dir', help='output directory')
    arg = parse.parse_args()

    file_list = []
    # file_list contains all the file we input in args
    file_name_list = []
    # to show the path name in order

    """
    here create the treelib-like structure for each file
    """
    for file in arg.input_file:
        # each file create a 'line list'
        fo = open(file, 'r')
        input_file = fo.readlines()
        length = len(input_file)
        fo.close()
        file_name_list.append(file)
        s = {
            'space': ' ',
            'v_line': '|',
            'item': '|--',
            'item_line': '--',
        }
        line_list = []
        for i in range(1, length + 1):
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
            line = line + ' ' + x.split()[0] + '\n'
            # this line is the complete line, actually is the treelib-like structure file
            line_list.append(line)
        file_list.append(line_list)

    file_main = file_list[0]
    # file_main is the main path
    file_remain = []
    # file_remain is the others path list without main file
    for i in range(1, len(file_list)):
        file_remain.append(file_list[i])

    combine_file(file_main, file_remain,arg.output_dir)
    # add all the branch to the 'file_main'

    for line in file_main:
        sys.stdout.write(line)

    """
    here create the output file
    """
    output_file_path = (arg.output_dir + 'combine_result')
    print("Writing to:" + output_file_path)
    if arg.output_dir:
        fo = open(output_file_path, 'w')
        write_to_output(file_main, fo)
        fo.close()


if __name__ == '__main__':
    main()
