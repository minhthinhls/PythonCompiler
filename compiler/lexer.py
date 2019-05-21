from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self.__add_tokens()

    def __add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')
        # Parenthesis
        self.lexer.add('(', r'\(')
        self.lexer.add(')', r'\)')
        self.lexer.add('{', r'\{')
        self.lexer.add('}', r'\}')
        # Semi Colon
        self.lexer.add(';', r'\;')
        # Statement
        self.lexer.add('IF', r'if(?!\w)')
        self.lexer.add('ELSE', r'else(?!\w)')
        self.lexer.add('NOT', r'not(?!\w)')
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
        # Mathematical Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        # Constant
        self.lexer.add('FLOAT', r'-?\d+.\d+')
        self.lexer.add('INTEGER', r'(\-)?\d+')
        self.lexer.add('STRING', r'(""".?""")|(".?")|(\'.?\')')
        self.lexer.add('BOOLEAN', r'true(?!\w)|false(?!\w)|True(?!\w)|False(?!\w)|TRUE(?!\w)|FALSE(?!\w)')
        # Ignore spaces
        self.lexer.ignore('\s+')

        # self.lexer.add('OPT_LINE', r'\n*')

    def build(self):
        return self.lexer.build()
