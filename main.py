import argparse
from re import match
import fnmatch
import pysubs2
import cchardet as chardet
import os
from pathlib import Path
from os import path

def parse_arg_f(arg_f: str) -> list[str]:
    result = []
    if path.isdir(arg_f):
        result = [file for file in 
                  [path.join(arg_f, file) for file in os.listdir(arg_f) if match('^.*\.(ass|srt)$', file)]
                  if path.isfile(file)]
    elif path.isfile(arg_f):
        result = [arg_f]
    else:
        # try regex
        result = [file for file in os.listdir() if fnmatch.fnmatch(file, arg_f)]
    return result

def shift_file(filename: str, shift_time: float):
    with Path(filename) as fp:
        encoding = chardet.detect(fp.read_bytes())['encoding']
    subs = pysubs2.load(filename, encoding=encoding)
    if shift_time != 0:
        subs.shift(ms=shift_time)
    subs.save(filename, header_notice='')

if __name__ == '__main__':
    class BlankLinesHelpFormatter (argparse.HelpFormatter):
        def _split_lines(self, text, width):
            txt = super()._split_lines(text, width)[0].split('\\n')
            return txt
    parser = argparse.ArgumentParser('python3 main.py', description='subtitles(ass/srt) timeline shifter.', formatter_class=BlankLinesHelpFormatter)
    
    parser.add_argument('-f', help='file or folder to shift.\\ne.g. ./subtitles\\ne.g. episode*.ass', required=True)
    parser.add_argument('-m', type=float, help='shift time, in million second.', default=0)
    parser.add_argument('-d', help='delete lines, "{number}" or "{number}-{number}", only works at .ass file.\\ne.g. 12\\ne.g. -5--16\\ne.g. 4-20')
    # parser.add_argument('-ts', help='change transition(words after \\N) line"s style to.')
    
    args = parser.parse_args()
    files = parse_arg_f(args.f)
    million = args.m
    deletion = args.d
    
    length = len(files)
    answer = input(str(length)+' file'+ ('s' if length>1 else '') + ' to shift, confirm(Y/n): ')
    
    if answer == '' or answer.lower() == 'y':
        for file in files:
            shift_file(file, million)
        print('succeeded')
    else:
        exit('quit')
