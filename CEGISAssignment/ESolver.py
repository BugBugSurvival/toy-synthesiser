import sys
from antlr4 import *
from parser.SygusLexer import SygusLexer
from parser.SygusParser import SygusParser
from parser.SygusVisitor import SygusVisitor
import glob, os
from z3 import *
import time

# the expression of the invocation in the specification
exprInvocation = None
# the list of variables appeared in the specification
listVariable = []
# the expression of the specification
exprSpecification = None

# enumerate terms in L(S) with size 'size'
# S -> 0 | S + 1 | S + x 
def _enumerate_S(size):
    result = []
    # the only 1-sized expression is 0
    if size == 1:
        result.append(IntVal(0))
        return result

    # additive productions
    exprs_S = _enumerate_S(size-1)
    exprs_S2 = _enumerate_S(size-1)
    exprs_B = _enumerate_B(size)
    for expr_S in exprs_S:
        # S + 1
        result.append(expr_S + 1)
        # S + var
        for var in listVariable:
            result.append(expr_S + var)
            
    # TODO: implement the production S -> If B S S
    # you can use method If(expr_B,expr_S1,expr_S2) to construct an if-then-else expression
        for expr_B in exprs_B:
            for expr_S2 in exprs_S2:
                result.append( If( expr_B, expr_S, expr_S2 ) )
    return result

# TODO: implement a method that enumerates expressions in L(B) with size 'size'
# where B -> S > S
# you can use operator > directly, e.g., (expr_S1 > expr_S2) is a comparison expressions
def _enumerate_B(size):
    result = []
    exprs_S1 = _enumerate_S(size-1)
    exprs_S2 = _enumerate_S(size-1)
    for expr_S1 in exprs_S1:
        for expr_S2 in exprs_S2:
            result.append( expr_S1 > expr_S2 )
    return result


# keep enumerating expressions from the language of the following grammar and verify them
# S -> 0 | S + 1 | S + x 
def enumerate():
    # size of terms we are searching
    size_search = 1
    while True:
        # enumerate candidates with size size_search
        candidates = _enumerate_S(size_search)
        for candidate in candidates:
            print("candidate: ", candidate, end="")
            queryResult = verify(candidate)
            print(" failed verification")
            # if a counterexample is not found, the candidate is a solution
            if queryResult == None:
                return candidate

        # increase size_search by 1
        size_search += 1




# verify if a candidate expression satisfies the specification as expression
def verify(candidate):
    # first, substitute invocation of the synthesized function with the candidate expression
    query = substitute(exprSpecification,(exprInvocation,candidate))
    # second, negate the query for the seek of finding conterexample
    query = Not(query)

    # check the query by a solver
    s = Solver()
    s.add(query)

    # avoid free variable
    for var in listVariable:
        s.add(var > -65535)

    if s.check() == unsat:
        # there is no counterexample, that is, the candidate is a solution to the sepcification
        return None
    # get a model (satisfying assignment---counterexample) of the query
    m = s.model()
    return m


def main(argv):
    global exprInvocation
    global exprSpecification
    global listVariable

    # read input file
    file = open(argv[1], "r")
    input = InputStream(file.read())
    file.close()

    # parse the input with the visitor
    lexer = SygusLexer(input)
    stream = CommonTokenStream(lexer)
    parser = SygusParser(stream)
    tree = parser.cmdPlus()
    v = SygusVisitor()
    v.visit(tree)

    # read the specification as an expression
    exprSpecification = v.exprSpec

    # read the list of invocations in the specification
    # the list should contains only one expression for our simplified SyGuS problems
    listInvocation = v.listInvocationInSpec
    exprInvocation = listInvocation[0]

    # read the list of variables in the invocations
    for i in range(exprInvocation.num_args()):
        listVariable.append(exprInvocation.arg(i))


    start_time = time.time()
    solution = enumerate()
    print("--- %s seconds ---" % (time.time() - start_time))
    print ("solution: ", simplify(solution))


if __name__ == '__main__':
    main(sys.argv)
