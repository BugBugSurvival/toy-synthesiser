import sys
from antlr4 import *
from SygusLexer import SygusLexer
from SygusParser import SygusParser
from SygusVisitor import SygusVisitor
import glob, os

# not in use
# check testIntParser
def main(argv):
    file = open(argv[1], "r")
    file.readline()
    input = InputStream(file.read())
    file.close()
    lexer = SygusLexer(input)
    stream = CommonTokenStream(lexer)
    parser = SygusParser(stream)
    tree = parser.cmdPlus()

    v = SygusVisitor()
    v.visit(tree)
    print v.exprSpec


if __name__ == '__main__':
    main(sys.argv)
