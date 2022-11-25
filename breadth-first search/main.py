import sys
import sexp
import pprint
import translator
from collections import deque
from mysolver import hasIte, getSynFunExpr, Solver

def Extend(Stmts, Productions):
    ret = []
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            TryExtend = Extend(Stmts[i], Productions)
            if len(TryExtend) > 0:
                for extended in TryExtend:
                    ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        elif Stmts[i] in Productions.keys():
            for extended in Productions[Stmts[i]]:
                ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        if len(ret) > 0:
            break
    # pprint.pprint(ret)
    return ret


def stripComments(bmFile):
    noComments = '('
    for line in bmFile:
        line = line.split(';', 1)[0]
        noComments += line
    return noComments + ')'


def BFS(SynFunExpr, StartSym, FuncDefine, checker):
# BfsQueue = [[StartSym]]  # Top-down
    BfsQueue = deque([[StartSym]])
    Productions = {StartSym: []}
    Type = {StartSym: SynFunExpr[3]}  # set starting symbol's return type

    for NonTerm in SynFunExpr[4]:  # SynFunExpr[4] is the production rules
        NTName = NonTerm[0]
        NTType = NonTerm[1]
        if NTType == Type[StartSym]:
            Productions[StartSym].append(NTName)
        # Type[NTName] = NTType
        #Productions[NTName] = NonTerm[2]
        Productions[NTName] = []
        for NT in NonTerm[2]:
            if type(NT) == tuple:
                # deal with ('Int',0). You can also utilize type information, but you will suffer from these tuples.
                Productions[NTName].append(str(NT[1]))
            else:
                Productions[NTName].append(NT)
    Count = 0
    TE_set = set()
    Ans = None
    while len(BfsQueue) != 0:
        Curr = BfsQueue.popleft()
        #print("Extending "+str(Curr))
        # pprint.pprint("Expanding:")
        # pprint.pprint(Curr)
        TryExtend = Extend(Curr, Productions)
        # pprint.pprint("Get:")
        # pprint.pprint(TryExtend)
        if(len(TryExtend) == 0):  # Nothing to extend
            # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE ARGUMENT ForceBracket = True.
            FuncDefineStr = translator.toString(FuncDefine, ForceBracket = True)
            CurrStr = translator.toString(Curr)
            #SynFunResult = FuncDefine+Curr
            #Str = translator.toString(SynFunResult)
            # insert Program just before the last bracket ')'
            Str = FuncDefineStr[:-1] + ' ' + CurrStr + FuncDefineStr[-1]
            Count += 1
            counterexample = checker.check(Str)
            
            print ("\033[32m|—\033[33m counterexample -> \033[0m", counterexample)
            if(counterexample == None):  # No counter-example
                Ans = Str
                print(FuncDefine)
                print(Curr)
                break
        #print(TryExtend)
        for TE in TryExtend:
            TE_str = str(TE)
            if not TE_str in TE_set:
                BfsQueue.append(TE)
                TE_set.add(TE_str)
    return Ans


if __name__ == '__main__':

    print("\033[32m\n|\n+----------------------------\n|")
    benchmarkFile = open("max2.sl")
    bm = stripComments(benchmarkFile)
    # Parse string to python list
    bmExpr = sexp.sexp.parseString(bm, parseAll = True).asList()[0]  
    # pprint.pprint(bmExpr)
    checker = translator.ReadQuery(bmExpr)
    SynFunExpr = []
    StartSym = 'My-Start-Symbol'  # virtual starting symbol
    SynFunExpr = getSynFunExpr(bmExpr)
    ProdRule = SynFunExpr[4]
    isIte = hasIte(ProdRule)
    FuncDefine = ['define-fun'] + SynFunExpr[1:4]  # copy function signature
    # candidates = getCandidates(bmExpr)
    #print(FuncDefine)
    if not isIte:
        Ans = BFS(SynFunExpr, StartSym, FuncDefine, checker)
        print(Ans)
    else:
        Ans = Solver(bmExpr)
        counterexample = checker.check(Ans)
        print ("\033[32m|—\033[33m counterexample: \n \033[36m", counterexample)
        # if counterexample == None:
        #     print(sys.argv[1], True)
        print("\033[32m|—\033[33m Ans: \n \033[35m", Ans)
    
    print("\033[32m|\n+----------------------------\n\n")
