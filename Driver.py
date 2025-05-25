import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from Interpreter import Interpreter, InterpreterError


def main():
    if len(sys.argv) != 2:
        print("Использование: python Driver.py <входной_файл>")
        return
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        input_stream = InputStream(input_text)
        lexer = ExprLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ExprParser(stream)
        
        tree = parser.program()
        
        interpreter = Interpreter()
        interpreter.visit(tree)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден")
    except InterpreterError as e:
        print(f"Ошибка выполнения: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()