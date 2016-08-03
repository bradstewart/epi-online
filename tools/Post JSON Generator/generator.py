import argparse
import sys
import json

INSERT_ME_MARKER = "//INSERT_ME\n"


class Token:
    TEXT = 0
    HEADER = 1
    HARNESS = 2
    IGNORE = 3
    END = 4
    INCLUDE = 5
    SKELETON = 6


class BaseFilter:
    def __init__(self, ctx: dict, targets):
        self.ctx = ctx
        self.targets = targets
        for t in self.targets:
            ctx.setdefault(t, "")

    def process(self, line, tok):
        for t in self.targets:
            self.ctx[t] += line

    def get_ignore(self):
        return get_filter(self.ctx, None)


class SkeletonFilter(BaseFilter):
    def __init__(self, ctx):
        BaseFilter.__init__(self, ctx, ["skeleton"])
        self.marker_inserted = False

    def get_ignore(self):
        if not self.marker_inserted:
            self.process(INSERT_ME_MARKER, None)
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


def get_filter(ctx, tok):
    if tok is None:
        return BaseFilter(ctx, [])

    if tok == Token.HARNESS:
        return BaseFilter(ctx, ["harness"])
    if tok == Token.HEADER:
        return BaseFilter(ctx, ["harness", "header"])
    if tok == Token.SKELETON:
        return SkeletonFilter(ctx)
    return BaseFilter(ctx, [])


def get_token(line: str):
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

    return Token.TEXT


def process_include(line: str, prefix="pg_include"):
    pos = line.index(prefix) + len(prefix)
    if pos >= len(line):
        sys.exit("Missing argument in @pg_include")
    return line[pos:-1].strip()


def process(filename: str, base_folder: str):
    ctx = dict()
    filter_stack = [get_filter(ctx, None)]
    stream = LineStream()
    stream.insert_file(filename)

    for line in stream:
        tok = get_token(line)
        if tok == Token.TEXT:
            filter_stack[-1].process(line, tok)
        elif tok == Token.INCLUDE:
            stream.insert_file(base_folder + process_include(line))
        elif tok == Token.END:
            if len(filter_stack) == 1:
                sys.exit('pg_end token found with no open tag')
            filter_stack.pop()
        elif tok == Token.IGNORE:
            filter_stack.append(filter_stack[-1].get_ignore())
        else:
            filter_stack.append(get_filter(ctx, tok))

    return ctx


parser = argparse.ArgumentParser(description="Generate problem post in JSON format for EPI frontend.")
parser.add_argument('-l', dest='lang', choices=['cpp', 'java'], required=True, help='language')
parser.add_argument('-f', dest='file', required=True, help='test file')
parser.add_argument('-t', dest='template', required=True, help='JSON template file')
parser.add_argument('-o', dest='output', required=True, help='JSON output file')
config = parser.parse_args()

folder = config.file.rpartition('/')[0] + '/'

cpp = process(config.file, folder)

template = json.load(open_or_exit(config.template))
template["cpp"] = cpp
json.dump(template, open_or_exit(config.output, mode='w'))
