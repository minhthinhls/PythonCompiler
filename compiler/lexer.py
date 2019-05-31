from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self.__add_tokens()

    def __add_tokens(self):
        # Constant
        self.lexer.add('E', r'-?__E__')
        self.lexer.add('PI', r'-?__PI__')
        self.lexer.add('FLOAT', r'-?\d+\.\d+')
        self.lexer.add('INTEGER', r'-?\d+')
        self.lexer.add('STRING', r'(""".*""")|(".*")|(\'.*\')')
        self.lexer.add('BOOLEAN', r'true(?!\w)|false(?!\w)|True(?!\w)|False(?!\w)|TRUE(?!\w)|FALSE(?!\w)')
        # Mathematical Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        # Binary Operator
        self.lexer.add('AND', r'and(?!\w)')
        self.lexer.add('OR', r'or(?!\w)')
        self.lexer.add('==', r'\=\=')
        self.lexer.add('!=', r'\!\=')
        self.lexer.add('>=', r'\>\=')
        self.lexer.add('<=', r'\<\=')
        self.lexer.add('>', r'\>')
        self.lexer.add('<', r'\<')
        self.lexer.add('=', r'\=')
        # Statement
        self.lexer.add('IF', r'if(?!\w)')
        self.lexer.add('ELSE', r'else(?!\w)')
        self.lexer.add('NOT', r'not(?!\w)')
        # Semi Colon
        self.lexer.add(';', r'\;')
        self.lexer.add(',', r'\,')
        # Parenthesis
        self.lexer.add('(', r'\(')
        self.lexer.add(')', r'\)')
        self.lexer.add('{', r'\{')
        self.lexer.add('}', r'\}')
        # Function
        self.lexer.add('CONSOLE_INPUT', r'input')
        self.lexer.add('FUNCTION', r'function')
        self.lexer.add('PRINT', r'print')
        self.lexer.add('ABSOLUTE', r'abs')
        self.lexer.add('SIN', r'sin')
        self.lexer.add('COS', r'cos')
        self.lexer.add('TAN', r'tan')
        self.lexer.add('POWER', r'pow')
        # Assignment
        self.lexer.add('LET', r'let(?!\w)')
        self.lexer.add('IDENTIFIER', "[a-zA-Z_][a-zA-Z0-9_]*")
        # Ignore spaces
        self.lexer.ignore('\s+')

        # self.lexer.add('OPT_LINE', r'\n*')

    def build(self):
        return self.lexer.build()
