from rply import ParserGenerator
from compiler.AbstractSyntaxTree import *
from compiler.errors import *


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'PI', 'E',
             'PRINT', 'ABSOLUTE', 'SIN', 'COS', 'TAN', 'POWER',
             '(', ')', ';', ',', '{', '}',
             'AND', 'OR', 'NOT', 'IF', 'ELSE',
             '==', '!=', '>=', '>', '<', '<=',
             'SUM', 'SUB', 'MUL', 'DIV'
             ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=(
                ('left', ['IF', 'ELSE', ';']),
                ('left', ['AND', 'OR']),
                ('left', ['NOT']),
                ('left', ['==', '!=', '>=', '>', '<', '<=']),
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'PI', 'E'])
            )
        )
        self.parse()
        pass  # End Parser's constructor !

    def parse(self):
        @self.pg.production('expression : PRINT ( expression )')
        def program(p):
            return Print(p[2])

        @self.pg.production('expression : ( expression )')
        def expression_parenthesis(p):
            # In this case we need parenthesis only for precedence
            # so we just need to return the inner expression
            return p[1]

        @self.pg.production('expression : IF ( expression ) { block }')
        def expression_if(p):
            return If(condition=p[2], body=p[5])

        @self.pg.production('expression : IF ( expression ) { block } ELSE { block }')
        def expression_if_else(p):
            return If(condition=p[2], body=p[5], else_body=p[9])

        @self.pg.production('block : statement_full')
        def block_expr(p):
            return Block(p[0], None)

        @self.pg.production('block : statement_full block')
        def block_expr_block(p):
            return Block(p[0], p[1])

        @self.pg.production('statement_full : statement ;')
        def statement_full(p):
            return p[0]

        @self.pg.production('statement : expression')
        def statement_expr(p):
            return p[0]

        @self.pg.production('expression : NOT expression')
        def expression_not(p):
            return Not(p[1])

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_binary_operator(p):
            if p[1].gettokentype() == 'SUM':
                return Sum(p[0], p[2])
            elif p[1].gettokentype() == 'SUB':
                return Sub(p[0], p[2])
            elif p[1].gettokentype() == 'MUL':
                return Mul(p[0], p[2])
            elif p[1].gettokentype() == 'DIV':
                return Div(p[0], p[2])
            else:
                raise LogicError('Oops, this should not be possible!')

        @self.pg.production('expression : expression != expression')
        @self.pg.production('expression : expression == expression')
        @self.pg.production('expression : expression >= expression')
        @self.pg.production('expression : expression <= expression')
        @self.pg.production('expression : expression > expression')
        @self.pg.production('expression : expression < expression')
        @self.pg.production('expression : expression AND expression')
        @self.pg.production('expression : expression OR expression')
        def expression_equality(p):
            if p[1].gettokentype() == '==':
                return Equal(p[0], p[2])
            elif p[1].gettokentype() == '!=':
                return NotEqual(p[0], p[2])
            elif p[1].gettokentype() == '>=':
                return GreaterThanEqual(p[0], p[2])
            elif p[1].gettokentype() == '<=':
                return LessThanEqual(p[0], p[2])
            elif p[1].gettokentype() == '>':
                return GreaterThan(p[0], p[2])
            elif p[1].gettokentype() == '<':
                return LessThan(p[0], p[2])
            elif p[1].gettokentype() == 'AND':
                return And(p[0], p[2])
            elif p[1].gettokentype() == 'OR':
                return Or(p[0], p[2])
            else:
                raise LogicError("Shouldn't be possible")

        @self.pg.production('expression : ABSOLUTE ( expression )')
        def expression_absolute(p):
            return Absolute(p[2])

        @self.pg.production('expression : SIN ( expression )')
        def expression_absolute(p):
            return Sin(p[2])

        @self.pg.production('expression : COS ( expression )')
        def expression_absolute(p):
            return Cos(p[2])

        @self.pg.production('expression : TAN ( expression )')
        def expression_absolute(p):
            return Tan(p[2])

        @self.pg.production('expression : POWER ( expression , expression )')
        def expression_absolute(p):
            return Pow(p[2], p[4])

        @self.pg.production('expression : const')
        def expression_const(p):
            return p[0]

        @self.pg.production('const : FLOAT')
        def constant_float(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return Float(p[0].getstr())

        @self.pg.production('const : BOOLEAN')
        def constant_boolean(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return Boolean(p[0].getstr())

        @self.pg.production('const : INTEGER')
        def constant_integer(p):
            return Integer(p[0].getstr())

        @self.pg.production('const : STRING')
        def constant_string(p):
            return String(p[0].getstr().strip('"\''))

        @self.pg.production('const : PI')
        def constant_pi(p):
            return ConstantPI(p[0].getstr())

        @self.pg.production('const : E')
        def constant_e(p):
            return ConstantE(p[0].getstr())

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def build(self):
        return self.pg.build()
