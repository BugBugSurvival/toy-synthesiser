# Generated from Sygus.g4 by ANTLR 4.5.1
from antlr4 import *
from z3 import *
import math
# This class defines a complete generic visitor for a parse tree produced by SygusParser.


class SygusVisitor(ParseTreeVisitor):
    nameSynFunc = ""
    listInvocationInSpec = []
    listExpression = []
    numOfArgs = 0
    exprSpec = None

    # Visit a parse tree produced by SygusParser#start.
    def visitStart(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#prog.
    def visitProg(self, ctx):
        self.visitChildren(ctx)
        return And(*self.listConstraintEpxression)


    # Visit a parse tree produced by SygusParser#setLogicCmd.
    def visitSetLogicCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#weightPlus.
    def visitWeightPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#weight.
    def visitWeight(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#setWeightCmd.
    def visitSetWeightCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#cmdPlus.
    def visitCmdPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#cmd.
    def visitCmd(self, ctx):
        if ctx.constraintCmd() == None:
            self.visitChildren(ctx)
            return None
        #self.listConstraintEpxression.append(self.visitChildren(ctx))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#weightOptimizationCmd.
    def visitWeightOptimizationCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#weightPair.
    def visitWeightPair(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#weightConstraintCmd.
    def visitWeightConstraintCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#varDeclCmd.
    def visitVarDeclCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#sortDefCmd.
    def visitSortDefCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#sortExpr.
    def visitSortExpr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#boolConst.
    def visitBoolConst(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#enumConst.
    def visitEnumConst(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#ecList.
    def visitEcList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#symbolPlus.
    def visitSymbolPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#setOptsCmd.
    def visitSetOptsCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#optList.
    def visitOptList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#symbolPairPlus.
    def visitSymbolPairPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#symbolPair.
    def visitSymbolPair(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#funDefCmd.
    def visitFunDefCmd(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SygusParser#funDeclCmd.
    def visitFunDeclCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#sortStar.
    def visitSortStar(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#argList.
    def visitArgList(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SygusParser#symbolSortPairStar.
    def visitSymbolSortPairStar(self, ctx):
        currentCtx = ctx
        while currentCtx.symbolSortPair()!= None:
            self.numOfArgs += 1
            currentCtx = currentCtx.symbolSortPairStar()
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#symbolSortPair.
    def visitSymbolSortPair(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#application.
    def visitApplication(self, ctx):
        self.visitChildren(ctx)
        op = ctx.SYMBOL().getText()
        if op == self.nameSynFunc:

            listSortOfSynFunc = []
            for i in range(0,self.numOfArgs):
                listSortOfSynFunc.append(IntSort())
            synFunc = Function(op, *listSortOfSynFunc)
            result = synFunc(*self.listExpression)
            for invocation in self.listInvocationInSpec:
                if invocation == result:
                    return result
            self.listInvocationInSpec.append(result)
            return result
        if op == ">=":
            result = self.listExpression[0] >= self.listExpression[1]
            return result
        if op == "<=":
            result = self.listExpression[0] <= self.listExpression[1]
            return result
        if op == "<":
            result = self.listExpression[0] < self.listExpression[1]
            return result
        if op == ">":
            result = self.listExpression[0] > self.listExpression[1]
            return result
        if op == "=" or op == "==":
            result = self.listExpression[0] == self.listExpression[1]
            return result
        if op == "or" or op == "Or":
            result = Or(*self.listExpression)
            return result
        if op == "and" or op == "And":
            result = And(*self.listExpression)
            return result
        if op == "+":
            result = 0
            for expr in self.listExpression:
                result = result + expr
            return result
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SygusParser#liter.
    def visitLiter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#symbol.
    def visitSymbol(self, ctx):
        return Int(ctx.getText())


    # Visit a parse tree produced by SygusParser#let.
    def visitLet(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SygusParser#letTerm.
    def visitLetTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#letBindingTermPlus.
    def visitLetBindingTermPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#letBindingTerm.
    def visitLetBindingTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#termStar.
    def visitTermStar(self, ctx):
        currentCtx = ctx
        listExpression = []
        while currentCtx.term() != None:
            currentTerm = currentCtx.term()
            currentCtx = currentCtx.termStar()
            listExpression.insert( 0, self.visit(currentTerm))
        self.listExpression = listExpression
        return None


    # Visit a parse tree produced by SygusParser#literal.
    def visitLiteral(self, ctx):
        return int(ctx.getText())


    # Visit a parse tree produced by SygusParser#ntDefPlus.
    def visitNtDefPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#ntDef.
    def visitNtDef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#gTermPlus.
    def visitGTermPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#checkSynthCmd.
    def visitCheckSynthCmd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#constraintCmd.
    def visitConstraintCmd(self, ctx):

        self.exprSpec = self.visit(ctx.term())
        return None


    # Visit a parse tree produced by SygusParser#synthFunCmd.
    def visitSynthFunCmd(self, ctx):
        self.nameSynFunc = ctx.SYMBOL().getText()
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#gTermWeighted.
    def visitGTermWeighted(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#literalPlus.
    def visitLiteralPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#gTerm.
    def visitGTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#letGTerm.
    def visitLetGTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#letBindingGTermPlus.
    def visitLetBindingGTermPlus(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#letBindingGTerm.
    def visitLetBindingGTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SygusParser#gTermStar.
    def visitGTermStar(self, ctx):
        return self.visitChildren(ctx)
