grammar Expr;

// Главное правило - программа состоит из последовательности операторов
program : statement* EOF ;

// Операторы
statement 
    : declaration ';'                           // Объявление переменной
    | assignment ';'                            // Присваивание
    | ifStatement                               // Условный оператор
    | whileStatement                            // Цикл while
    | printStatement ';'                        // Вывод
    | block                                     // Блок операторов
    ;

// Объявление переменной с типом
// Если значение не задано, для int, float значение по-умолчанию = 0, для строк - пустая строка
declaration : type ID ('=' expression)? ;

// Присваивание
assignment : ID '=' expression ;

// Условный оператор
ifStatement : 'if' '(' expression ')' statement ('else' statement)? ;

// Цикл while
whileStatement : 'while' '(' expression ')' statement ;

// Вывод
printStatement : 'print' '(' expression ')' ;

// Блок операторов
block : '{' statement* '}' ;

// Типы данных
type : 'int' | 'float' | 'string' ;

// Выражения с приоритетами
expression
    : '(' expression ')'                                                    // Скобки
    | ('!' | '-' | '+') expression                                          // Унарные операции
    | expression ('*' | '/' | '%') expression                               // Умножение, деление, остаток
    | expression ('+' | '-') expression                                     // Сложение, вычитание
    | expression ('<' | '<=' | '>' | '>=' | '==' | '!=') expression         // Сравнение
    | expression '&&' expression                                            // Логическое И
    | expression '||' expression                                            // Логическое ИЛИ
    | ID                                                                    // Переменная
    | literal                                                               // Литерал
    ;

// Литералы
literal 
    : INT_LITERAL                               // Целое число
    | FLOAT_LITERAL                             // Вещественное число
    | STRING_LITERAL                            // Строка
    ;

// Лексические правила
ID : [a-zA-Z_][a-zA-Z0-9_]* ;
INT_LITERAL : [0-9]+ ;
FLOAT_LITERAL : [0-9]+ '.' [0-9]+ ;
STRING_LITERAL : '\'' (~['\r\n] | '\\' .)* '\'' ;

// Пробелы и комментарии
WS : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;