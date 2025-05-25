"""
Интерпретатор для императивного языка программирования
Поддерживает типы: int, float, string
Операторы: объявление переменных, присваивание, if/else, while, print
"""

from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from typing import Any, Dict, Union


class InterpreterError(Exception):
    pass


class UndefinedVariableError(InterpreterError):
    pass


class TypeMismatchError(InterpreterError):
    pass


class Value:
    def __init__(self, value: Any, type_name: str):
        self.value = value
        self.type_name = type_name
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"Value({self.value}, {self.type_name})"
    
    def is_truthy(self) -> bool:
        if self.type_name == 'int':
            return self.value != 0
        elif self.type_name == 'float':
            return self.value != 0.0
        elif self.type_name == 'string':
            return len(self.value) > 0
        return False


class Interpreter(ExprVisitor):
    def __init__(self):
        self.variables: Dict[str, Value] = {}
        self.output = []
    
    def get_output(self) -> str:
        return '\n'.join(self.output)
    
    def clear_output(self):
        self.output.clear()
    
    def visitProgram(self, ctx: ExprParser.ProgramContext):
        for statement in ctx.statement():
            self.visit(statement)
        return None
    
    def visitStatement(self, ctx: ExprParser.StatementContext):
        if ctx.declaration():
            return self.visit(ctx.declaration())
        elif ctx.assignment():
            return self.visit(ctx.assignment())
        elif ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        elif ctx.printStatement():
            return self.visit(ctx.printStatement())
        elif ctx.block():
            return self.visit(ctx.block())
        return None
    
    def visitDeclaration(self, ctx: ExprParser.DeclarationContext):
        var_name = ctx.ID().getText()
        type_name = self.visit(ctx.type_())
        
        if ctx.expression():
            value = self.visit(ctx.expression())
            if not self._is_compatible_type(value.type_name, type_name):
                raise TypeMismatchError(
                    f"Невозможно присвоить значение типа {value.type_name} переменной типа {type_name} '{var_name}'"
                )
            converted_value = self._convert_type(value, type_name)
            self.variables[var_name] = converted_value
        else:
            default_value = self._get_default_value(type_name)
            self.variables[var_name] = default_value
        
        return None
    
    def visitAssignment(self, ctx: ExprParser.AssignmentContext):
        var_name = ctx.ID().getText()
        
        if var_name not in self.variables:
            raise UndefinedVariableError(f"Переменная '{var_name}' не объявлена")
        
        value = self.visit(ctx.expression())
        existing_var = self.variables[var_name]
        
        if not self._is_compatible_type(value.type_name, existing_var.type_name):
            raise TypeMismatchError(
                f"Невозможно присвоить значение типа {value.type_name} переменной типа {existing_var.type_name} '{var_name}'"
            )
        
        converted_value = self._convert_type(value, existing_var.type_name)
        self.variables[var_name] = converted_value
        
        return None
    
    def visitIfStatement(self, ctx: ExprParser.IfStatementContext):
        condition = self.visit(ctx.expression())
        
        if condition.is_truthy():
            self.visit(ctx.statement(0))
        elif len(ctx.statement()) > 1:  # есть else
            self.visit(ctx.statement(1))
        
        return None
    
    def visitWhileStatement(self, ctx: ExprParser.WhileStatementContext):
        while True:
            condition = self.visit(ctx.expression())
            if not condition.is_truthy():
                break
            self.visit(ctx.statement())
        
        return None
    
    def visitPrintStatement(self, ctx: ExprParser.PrintStatementContext):
        value = self.visit(ctx.expression())
        output_str = str(value.value)
        print(output_str)
        self.output.append(output_str)
        return None
    
    def visitBlock(self, ctx: ExprParser.BlockContext):
        for statement in ctx.statement():
            self.visit(statement)
        return None
    
    def visitType(self, ctx: ExprParser.TypeContext):
        return ctx.getText()
    
    def visitExpression(self, ctx: ExprParser.ExpressionContext):
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expression(0))
        
        if len(ctx.expression()) == 2:
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            op = ctx.getChild(1).getText()
            
            if op == '*':
                return self._multiply(left, right)
            elif op == '/':
                return self._divide(left, right)
            elif op == '%':
                return self._modulo(left, right)
            elif op == '+':
                return self._add(left, right)
            elif op == '-':
                return self._subtract(left, right)
            
            elif op == '<':
                return self._compare_lt(left, right)
            elif op == '<=':
                return self._compare_le(left, right)
            elif op == '>':
                return self._compare_gt(left, right)
            elif op == '>=':
                return self._compare_ge(left, right)
            elif op == '==':
                return self._compare_eq(left, right)
            elif op == '!=':
                return self._compare_ne(left, right)
            
            elif op == '&&':
                return self._logical_and(left, right)
            elif op == '||':
                return self._logical_or(left, right)
        
        elif len(ctx.expression()) == 1:
            operand = self.visit(ctx.expression(0))
            op = ctx.getChild(0).getText()
            
            if op == '!':
                return self._logical_not(operand)
            elif op == '-':
                return self._unary_minus(operand)
            elif op == '+':
                return self._unary_plus(operand)
        
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name not in self.variables:
                raise UndefinedVariableError(f"Переменная '{var_name}' не объявлена")
            return self.variables[var_name]
        
        elif ctx.literal():
            return self.visit(ctx.literal())
        
        raise InterpreterError(f"Неизвестный тип выражения: {ctx.getText()}")
    
    def visitLiteral(self, ctx: ExprParser.LiteralContext):
        if ctx.INT_LITERAL():
            return Value(int(ctx.INT_LITERAL().getText()), 'int')
        elif ctx.FLOAT_LITERAL():
            return Value(float(ctx.FLOAT_LITERAL().getText()), 'float')
        elif ctx.STRING_LITERAL():
            # Убираем кавычки и обрабатываем escape-последовательности
            text = ctx.STRING_LITERAL().getText()[1:-1]  # убираем кавычки
            text = text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace("\\'", "'")
            return Value(text, 'string')
        
        raise InterpreterError(f"Неизвестный тип литерала: {ctx.getText()}")
    
    # Вспомогательные методы для операций
    
    def _is_compatible_type(self, from_type: str, to_type: str) -> bool:
        """Проверка совместимости типов"""
        if from_type == to_type:
            return True
        # int можно привести к float
        if from_type == 'int' and to_type == 'float':
            return True
        # Любой тип можно привести к string
        if to_type == 'string':
            return True
        return False
    
    def _convert_type(self, value: Value, target_type: str) -> Value:
        """Приведение типа"""
        if value.type_name == target_type:
            return value
        
        if target_type == 'float' and value.type_name == 'int':
            return Value(float(value.value), 'float')
        elif target_type == 'string':
            return Value(str(value.value), 'string')
        
        raise TypeMismatchError(f"Невозможно преобразовать тип {value.type_name} в {target_type}")
    
    def _get_default_value(self, type_name: str) -> Value:
        """Получение значения по умолчанию для типа"""
        if type_name == 'int':
            return Value(0, 'int')
        elif type_name == 'float':
            return Value(0.0, 'float')
        elif type_name == 'string':
            return Value('', 'string')
        
        raise InterpreterError(f"Неизвестный тип: {type_name}")
    
    # Арифметические операции
    def _add(self, left: Value, right: Value) -> Value:
        """Сложение"""
        if left.type_name == 'string' or right.type_name == 'string':
            # Конкатенация строк
            return Value(str(left.value) + str(right.value), 'string')
        elif left.type_name == 'float' or right.type_name == 'float':
            # Вещественная арифметика
            left_val = float(left.value) if left.type_name in ['int', 'float'] else 0.0
            right_val = float(right.value) if right.type_name in ['int', 'float'] else 0.0
            return Value(left_val + right_val, 'float')
        else:
            # Целочисленная арифметика
            return Value(left.value + right.value, 'int')
    
    def _subtract(self, left: Value, right: Value) -> Value:
        """Вычитание"""
        if left.type_name == 'string' and right.type_name == 'string':
            # Удаление подстроки
            result = left.value.replace(right.value, '', 1)
            return Value(result, 'string')
        elif left.type_name == 'float' or right.type_name == 'float':
            left_val = float(left.value) if left.type_name in ['int', 'float'] else 0.0
            right_val = float(right.value) if right.type_name in ['int', 'float'] else 0.0
            return Value(left_val - right_val, 'float')
        else:
            return Value(left.value - right.value, 'int')
    
    def _multiply(self, left: Value, right: Value) -> Value:
        """Умножение"""
        if left.type_name == 'string' and right.type_name == 'int':
            # Повторение строки
            return Value(left.value * right.value, 'string')
        elif left.type_name == 'int' and right.type_name == 'string':
            return Value(left.value * right.value, 'string')
        elif left.type_name == 'float' or right.type_name == 'float':
            left_val = float(left.value) if left.type_name in ['int', 'float'] else 0.0
            right_val = float(right.value) if right.type_name in ['int', 'float'] else 0.0
            return Value(left_val * right_val, 'float')
        else:
            return Value(left.value * right.value, 'int')
    
    def _divide(self, left: Value, right: Value) -> Value:
        """Деление"""
        if right.value == 0:
            raise InterpreterError("Деление на ноль")
        
        if left.type_name in ['int', 'float'] and right.type_name in ['int', 'float']:
            left_val = float(left.value)
            right_val = float(right.value)
            return Value(left_val / right_val, 'float')
        else:
            raise TypeMismatchError("Деление поддерживается только для числовых типов")
    
    def _modulo(self, left: Value, right: Value) -> Value:
        """Остаток от деления"""
        if right.value == 0:
            raise InterpreterError("Деление на ноль при вычислении остатка")
        
        if left.type_name == 'int' and right.type_name == 'int':
            return Value(left.value % right.value, 'int')
        else:
            raise TypeMismatchError("Операция остатка поддерживается только для целых чисел")
    
    # Операции сравнения
    def _compare_lt(self, left: Value, right: Value) -> Value:
        """Меньше"""
        if left.type_name in ['int', 'float'] and right.type_name in ['int', 'float']:
            return Value(1 if left.value < right.value else 0, 'int')
        elif left.type_name == 'string' and right.type_name == 'string':
            return Value(1 if left.value < right.value else 0, 'int')
        else:
            raise TypeMismatchError("Невозможно сравнить значения разных типов")
    
    def _compare_le(self, left: Value, right: Value) -> Value:
        """Меньше или равно"""
        if left.type_name in ['int', 'float'] and right.type_name in ['int', 'float']:
            return Value(1 if left.value <= right.value else 0, 'int')
        elif left.type_name == 'string' and right.type_name == 'string':
            return Value(1 if left.value <= right.value else 0, 'int')
        else:
            raise TypeMismatchError("Невозможно сравнить значения разных типов")
    
    def _compare_gt(self, left: Value, right: Value) -> Value:
        """Больше"""
        if left.type_name in ['int', 'float'] and right.type_name in ['int', 'float']:
            return Value(1 if left.value > right.value else 0, 'int')
        elif left.type_name == 'string' and right.type_name == 'string':
            return Value(1 if left.value > right.value else 0, 'int')
        else:
            raise TypeMismatchError("Невозможно сравнить значения разных типов")
    
    def _compare_ge(self, left: Value, right: Value) -> Value:
        """Больше или равно"""
        if left.type_name in ['int', 'float'] and right.type_name in ['int', 'float']:
            return Value(1 if left.value >= right.value else 0, 'int')
        elif left.type_name == 'string' and right.type_name == 'string':
            return Value(1 if left.value >= right.value else 0, 'int')
        else:
            raise TypeMismatchError("Невозможно сравнить значения разных типов")
    
    def _compare_eq(self, left: Value, right: Value) -> Value:
        """Равно"""
        return Value(1 if left.value == right.value else 0, 'int')
    
    def _compare_ne(self, left: Value, right: Value) -> Value:
        """Не равно"""
        return Value(1 if left.value != right.value else 0, 'int')
    
    # Логические операции
    def _logical_and(self, left: Value, right: Value) -> Value:
        """Логическое И"""
        return Value(1 if left.is_truthy() and right.is_truthy() else 0, 'int')
    
    def _logical_or(self, left: Value, right: Value) -> Value:
        """Логическое ИЛИ"""
        return Value(1 if left.is_truthy() or right.is_truthy() else 0, 'int')
    
    def _logical_not(self, operand: Value) -> Value:
        """Логическое НЕ"""
        return Value(1 if not operand.is_truthy() else 0, 'int')
    
    # Унарные операции
    def _unary_minus(self, operand: Value) -> Value:
        """Унарный минус"""
        if operand.type_name == 'int':
            return Value(-operand.value, 'int')
        elif operand.type_name == 'float':
            return Value(-operand.value, 'float')
        else:
            raise TypeMismatchError("Унарный минус поддерживается только для числовых типов")
    
    def _unary_plus(self, operand: Value) -> Value:
        """Унарный плюс"""
        if operand.type_name in ['int', 'float']:
            return operand
        else:
            raise TypeMismatchError("Унарный плюс поддерживается только для числовых типов") 