#!/usr/bin/python

import sys, pijnu

def generateParserModule(grammer):
    pijnu.makeParser(grammer)

if __name__ == "__main__":
    generateParserModule(file(sys.argv[1]).read())
