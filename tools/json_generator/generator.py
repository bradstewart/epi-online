#!/usr/bin/env python3

import argparse
import sys
import os
import json
import re
import copy

INSERT_ME_TAG = "//INSERT_ME\n"

tag_re = re.compile('\s*//\s*@')  # matches //@ lines
min_filter_re = re.compile('^\s*(//|$)')  # matches empty lines and comment lines
number_re = re.compile(':\\d+$')
param_char = ':'


class Token:
    TEXT = 0
    HEADER = 1
    HARNESS = 2
    IGNORE = 3
    END = 4
    INCLUDE = 5
    SKELETON = 6
    IMPL = 7
    REPLACE = 8
    IMPORT = 9
    PACKAGE = 10


def tag_lfilter(line):
    return not tag_re.match(line)


def minimizing_lfilter(line):
    return tag_lfilter(line) and not min_filter_re.match(line)


class BaseFilter:
    def __init__(self, ctx: dict, targets, lines_to_process, line_filter):
        self.ctx = ctx
        self.targets = targets
        self.lines_left = lines_to_process if lines_to_process is not None else -1
        self.lfilter = line_filter
        for t in self.targets:
            ctx.setdefault(t, "")

    def process(self, line, override_filter=False):
        assert self.lines_left != 0
        if self.lines_left > 0:
            self.lines_left -= 1

        if self.lfilter(line) or override_filter:
            for t in self.targets:
                self.ctx[t] += line

    def marked_for_deletion(self):
        return self.lines_left == 0

    def get_ignore(self, lines_to_process):
        return get_filter(self.ctx, None, lines_to_process)


class SkeletonFilter(BaseFilter):
    def __init__(self, ctx, lines_to_process, insert_marker):
        BaseFilter.__init__(self, ctx, ["skeleton"], lines_to_process, tag_lfilter)
        self.marker_inserted = not insert_marker

    def get_ignore(self, lines_to_process):
        if not self.marker_inserted:
            self.process('    // Your solution here...\n', True)
            self.marker_inserted = True
        return BaseFilter.get_ignore(self, lines_to_process)


class LineStream:
    def __init__(self):
        self.lines = []

    def insert_file(self, filename):
        l = open_or_exit(filename).readlines()
        l.reverse()
        self.lines.extend(l)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.lines) == 0:
            raise StopIteration
        return self.lines.pop()


def open_or_exit(filename: str, mode='r'):
    try:
        return open(filename, mode=mode)
    except IOError:
        sys.exit("File " + filename + " was not found")


def get_filter(ctx, tok, param=None, last=None):
    if tok is None:
        return BaseFilter(ctx, [], param, tag_lfilter)

    if tok == Token.HARNESS:
        return BaseFilter(ctx, ["harness"], param, minimizing_lfilter)
    if tok == Token.HEADER:
        return BaseFilter(ctx, ["harness", "header"], param, tag_lfilter)
    if tok == Token.PACKAGE:
        return BaseFilter(ctx, ["package"], 1, tag_lfilter)
    if tok == Token.IMPORT:
        return BaseFilter(ctx, ["imports"], param, minimizing_lfilter)
    if tok == Token.SKELETON:
        get_filter(ctx, Token.HARNESS).process(INSERT_ME_TAG, True)
        return SkeletonFilter(ctx, param, True)
    if tok == Token.IMPL:
        last = copy.copy(last)
        last.lines_left = param
        last.lfilter = minimizing_lfilter
        return last
    return BaseFilter(ctx, [], param, tag_lfilter)


def get_rep_count_from_token(token: str):
    m = re.search(number_re, token)
    return int(m.group()[1:]) if m is not None else -1


def get_param_from_token(line: str, prefix: str):
    prefix += param_char
    pos = line.index(prefix) + len(prefix)
    assert (pos < len(line)), 'Missing required param in ' + prefix[:-1]

    return line[pos:]


def get_token(line: str, config):
    line = line.lstrip(' \t/').rstrip()
    if line.startswith('@pg_header'):
        return Token.HEADER, get_rep_count_from_token(line)
    if line.startswith('@pg_harness'):
        return Token.HARNESS, get_rep_count_from_token(line)
    if line.startswith('@pg_skeleton'):
        return Token.SKELETON, get_rep_count_from_token(line)
    if line.startswith('@pg_impl'):
        return Token.IMPL if config.keep_impl else Token.IGNORE, get_rep_count_from_token(line)
    if line.startswith('@pg_ignore'):
        return Token.IGNORE, get_rep_count_from_token(line)
    if line.startswith('@pg_import'):
        return Token.IMPORT, get_rep_count_from_token(line)
    if line.startswith('@pg_package'):
        return Token.PACKAGE, None

    if line.startswith('@pg_end'):
        return Token.END, None
    if line.startswith('@pg_include'):
        return Token.INCLUDE, get_param_from_token(line, '@pg_include')
    if line.startswith('@pg_replace'):
        return Token.REPLACE, get_param_from_token(line, '@pg_replace') + '\n'

    return Token.TEXT, None


def push_package_filter_on_start(stack, ctx):
    stack.append(get_filter(ctx, Token.PACKAGE))


def process(filename: str, config, custom_stack_init=None):
    base_folder = os.path.dirname(filename)
    ctx = dict()
    ctx['filename'] = os.path.basename(filename)
    filter_stack = [get_filter(ctx, Token.HARNESS)]
    if custom_stack_init is not None:
        custom_stack_init(filter_stack, ctx)
    stream = LineStream()
    stream.insert_file(filename)

    for line in stream:
        tok, param = get_token(line, config)
        if tok == Token.TEXT:
            filter_stack[-1].process(line)
        elif tok == Token.INCLUDE:
            stream.insert_file(os.path.join(base_folder, param))
        elif tok == Token.END:
            assert (len(filter_stack) > 1), '@pg_end token found with no open tag'
            filter_stack.pop()
        elif tok == Token.IGNORE:
            filter_stack.append(filter_stack[-1].get_ignore(param))
        elif tok == Token.REPLACE:
            filter_stack[-1].process(param)
            filter_stack.append(get_filter(ctx, None, 1))
        else:
            filter_stack.append(get_filter(ctx, tok, param, filter_stack[-1]))

        while len(filter_stack) > 0 and filter_stack[-1].marked_for_deletion():
            filter_stack.pop()

    return ctx


parser = argparse.ArgumentParser(description="Generate problem post in JSON format for EPI frontend.")
parser.add_argument('--cpp', help='cpp file to process')
parser.add_argument('--java', help='java file to process')
parser.add_argument('--template', required=True, help='JSON template file')
parser.add_argument('--output', required=True, help='JSON output file')
parser.add_argument('-keep-impl', dest='keep_impl',
                    help='Keep implementation (for testing purposes)', action='store_true')
parser.set_defaults(keep_impl=False)

config = parser.parse_args()
code = dict()
if config.cpp is not None:
    if "cpp" in code:
        print("Warning: rewriting cpp harness")
    config.seen_skeleton = False
    code["cpp"] = process(config.cpp, config)
if config.java is not None:
    if "java" in code:
        print("Warning: rewriting java harness")
    config.seen_skeleton = False
    code["java"] = process(config.java, config, push_package_filter_on_start)

template = json.load(open_or_exit(config.template))
template["code"] = code
json.dump(template, open_or_exit(config.output, mode='w'))
