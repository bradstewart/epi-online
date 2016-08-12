import argparse
import sys
import os
import json
import re

INSERT_ME_TAG = "//INSERT_ME\n"

tag_re = re.compile('\/\/\s*@')


class Token:
    TEXT = 0
    HEADER = 1
    HARNESS = 2
    IGNORE = 3
    END = 4
    INCLUDE = 5
    SKELETON = 6
    IMPL = 7


class BaseFilter:
    def __init__(self, ctx: dict, targets):
        self.ctx = ctx
        self.targets = targets
        for t in self.targets:
            ctx.setdefault(t, "")

    def process(self, line):
        if not tag_re.match(line):
            for t in self.targets:
                self.ctx[t] += line

    def get_ignore(self):
        return get_filter(self.ctx, None)


class SkeletonFilter(BaseFilter):
    def __init__(self, ctx, insert_marker):
        BaseFilter.__init__(self, ctx, ["skeleton"])
        self.marker_inserted = not insert_marker

    def get_ignore(self):
        if not self.marker_inserted:
            self.process('    // Your solution here...\n')
            self.marker_inserted = True
        return BaseFilter.get_ignore(self)


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


def get_filter(ctx, tok, last=None):
    if tok is None:
        return BaseFilter(ctx, [])

    if tok == Token.HARNESS:
        return BaseFilter(ctx, ["harness"])
    if tok == Token.HEADER:
        return BaseFilter(ctx, ["harness", "header"])
    if tok == Token.SKELETON:
        get_filter(ctx, Token.HARNESS).process(INSERT_ME_TAG)
        return SkeletonFilter(ctx, True)
    if tok == Token.IMPL:
        return last
    return BaseFilter(ctx, [])


def get_token(line: str, config):
    line = line.lstrip(' \t/').rstrip()
    if line == '@pg_header':
        return Token.HEADER
    if line == '@pg_harness':
        return Token.HARNESS
    if line == '@pg_ignore':
        return Token.IGNORE
    if line == '@pg_end':
        return Token.END
    if line.startswith('@pg_include'):
        return Token.INCLUDE
    if line == '@pg_skeleton':
        return Token.SKELETON
    if line == '@pg_impl':
        return Token.IMPL if config.keep_impl else Token.IGNORE

    return Token.TEXT


def process_include(line: str, prefix='pg_include'):
    pos = line.index(prefix) + len(prefix)
    if pos >= len(line):
        sys.exit("Missing argument in @pg_include")
    return line[pos:-1].strip()


def process(filename: str, config):
    base_folder = os.path.dirname(filename)
    ctx = dict()
    ctx['filename'] = os.path.basename(filename)
    filter_stack = [get_filter(ctx, None)]
    stream = LineStream()
    stream.insert_file(filename)

    for line in stream:
        tok = get_token(line, config)
        if tok == Token.TEXT:
            filter_stack[-1].process(line)
        elif tok == Token.INCLUDE:
            stream.insert_file(os.path.join(base_folder, process_include(line)))
        elif tok == Token.END:
            if len(filter_stack) == 1:
                sys.exit('pg_end token found with no open tag')
            filter_stack.pop()
        elif tok == Token.IGNORE:
            filter_stack.append(filter_stack[-1].get_ignore())
        else:
            filter_stack.append(get_filter(ctx, tok, filter_stack[-1]))

    return ctx


parser = argparse.ArgumentParser(description="Generate problem post in JSON format for EPI frontend.")
parser.add_argument('--cpp', help='cpp file to process')
parser.add_argument('--java', help='java file to process')
parser.add_argument('--template', required=True, help='JSON template file')
parser.add_argument('--output', required=True, help='JSON output file')
parser.add_argument('-keep-impl', dest='keep_impl', help='Keep implementation (for testing purposes)', action='store_true')
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
    code["java"] = process(config.java, config)

template = json.load(open_or_exit(config.template))
template["code"] = code
json.dump(template, open_or_exit(config.output, mode='w'))
