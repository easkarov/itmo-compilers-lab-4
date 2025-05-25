# Generated from Expr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#program.
    def visitProgram(self, ctx:ExprParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#statement.
    def visitStatement(self, ctx:ExprParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#declaration.
    def visitDeclaration(self, ctx:ExprParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#assignment.
    def visitAssignment(self, ctx:ExprParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#ifStatement.
    def visitIfStatement(self, ctx:ExprParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#whileStatement.
    def visitWhileStatement(self, ctx:ExprParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#printStatement.
    def visitPrintStatement(self, ctx:ExprParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#block.
    def visitBlock(self, ctx:ExprParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#type.
    def visitType(self, ctx:ExprParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#expression.
    def visitExpression(self, ctx:ExprParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#literal.
    def visitLiteral(self, ctx:ExprParser.LiteralContext):
        return self.visitChildren(ctx)



del ExprParser