from rply import ParserGenerator
from compiler.AbstractSyntaxTree import *
from compiler.errors import *


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN',
             'PRINT', '(', ')', ';', '{', '}',
             'AND', 'OR', 'NOT', 'IF', 'ELSE',
             '==', '!=', '>=', '>', '<', '<=',
             'SUM', 'SUB', 'MUL', 'DIV'
             ],
            precedence=(
                ('left', ['IF', 'ELSE', ';']),
                ('left', ['AND', 'OR']),
                ('left', ['NOT']),
                ('left', ['==', '!=', '>=', '>', '<', '<=']),
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN'])
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
            return Block(p[0])

        @self.pg.production('block : statement_full block')
        def block_expr_block(p):
            if type(p[1]) is Block:
                b = p[1]
            else:
                b = Block(p[1])
            b.add_statement(p[0])
            return b

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
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(left, right)
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
            left = p[0]
            right = p[2]
            check = p[1]

            if check.gettokentype() == '==':
                return Equal(left, right)
            elif check.gettokentype() == '!=':
                return NotEqual(left, right)
            elif check.gettokentype() == '>=':
                return GreaterThanEqual(left, right)
            elif check.gettokentype() == '<=':
                return LessThanEqual(left, right)
            elif check.gettokentype() == '>':
                return GreaterThan(left, right)
            elif check.gettokentype() == '<':
                return LessThan(left, right)
            elif check.gettokentype() == 'AND':
                return And(left, right)
            elif check.gettokentype() == 'OR':
                return Or(left, right)
            else:
                raise LogicError("Shouldn't be possible")

        @self.pg.production('expression : const')
        def expression_const(p):
            return p[0]

        @self.pg.production('const : FLOAT')
        def expression_float(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return Float(p[0].getstr())

        @self.pg.production('const : BOOLEAN')
        def expression_boolean(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return Boolean(p[0].getstr())

        @self.pg.production('const : INTEGER')
        def expression_integer(p):
            return Integer(p[0].getstr())

        @self.pg.production('const : STRING')
        def expression_string(p):
            return String(p[0].getstr().strip('"\''))

        """
        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(p[0].value)
        """

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def build(self):
        return self.pg.build()
