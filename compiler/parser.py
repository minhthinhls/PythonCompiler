from rply import ParserGenerator
from compiler.JSONparsedTree import Node
from compiler.AbstractSyntaxTree import *
from compiler.errors import *


# State instance which gets passed to parser !
class ParserState(object):
    def __init__(self):
        # We want to hold a dict of global-declared variables & functions.
        self.variables = {}
        self.functions = {}
        pass  # End ParserState's constructor !


class Parser:
    def __init__(self, syntax=False):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'PI', 'E',
             'PRINT', 'ABSOLUTE', 'SIN', 'COS', 'TAN', 'POWER',
             'CONSOLE_INPUT', '(', ')', ';', ',', '{', '}',
             'LET', 'AND', 'OR', 'NOT', 'IF', 'ELSE',
             '=', '==', '!=', '>=', '>', '<', '<=',
             'SUM', 'SUB', 'MUL', 'DIV', 'IDENTIFIER', 'FUNCTION'
             ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=(
                ('left', ['FUNCTION']),
                ('left', ['LET']),
                ('left', ['=']),
                ('left', ['IF', 'ELSE', ';']),
                ('left', ['AND', 'OR']),
                ('left', ['NOT']),
                ('left', ['==', '!=', '>=', '>', '<', '<=']),
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'PI', 'E'])
            )
        )
        self.syntax = syntax
        self.parse()
        pass  # End Parser's constructor !

    def parse(self):
        @self.pg.production("main : program")
        def main_program(state, p):
            if self.syntax is True:
                return [Node("program", p[0])]
            return Main(p[0])

        @self.pg.production('program : statement_full')
        def program_statement(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0])]
            return Program(p[0], None, state)

        @self.pg.production('program : statement_full program')
        def program_statement_program(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0]), Node("program", p[1])]
            return Program(p[0], p[1], state)

        @self.pg.production('expression : ( expression )')
        def expression_parenthesis(state, p):
            # In this case we need parenthesis only for precedence
            # so we just need to return the inner expression
            if self.syntax is True:
                return [Node("("), Node("expression", p[1]), Node(")")]
            return ExpressParenthesis(p[1])

        @self.pg.production('statement_full : IF ( expression ) { block }')
        def expression_if(state, p):
            if self.syntax is True:
                return [Node("IF"), Node("("), Node("expression", p[2]), Node(")"), Node("{"), Node("block", p[5]), Node("}")]
            return If(condition=p[2], body=p[5], state=state)

        @self.pg.production('statement_full : IF ( expression ) { block } ELSE { block }')
        def expression_if_else(state, p):
            if self.syntax is True:
                return [Node("IF"), Node("("), Node("expression", p[2]), Node(")"), Node("{"), Node("block", p[5]), Node("}"), Node("ELSE"), Node("{"),
                        Node("block", p[9]), Node("}")]
            return If(condition=p[2], body=p[5], else_body=p[9], state=state)

        @self.pg.production('block : statement_full')
        def block_expr(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0])]
            return Block(p[0], None, state)

        @self.pg.production('block : statement_full block')
        def block_expr_block(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0]), Node("block", p[1])]
            return Block(p[0], p[1], state)

        @self.pg.production('statement_full : statement ;')
        def statement_full(state, p):
            if self.syntax is True:
                return [Node("statement", p[0]), Node(";")]
            return StatementFull(p[0])

        @self.pg.production('statement : expression')
        def statement_expr(state, p):
            if self.syntax is True:
                return [Node("expression", p[0])]
            return Statement(p[0])

        @self.pg.production('statement : LET IDENTIFIER = expression')
        def statement_assignment(state, p):
            if self.syntax is True:
                return [Node("LET"), Node("IDENTIFIER", p[1]), Node("="), Node("expression", p[3])]
            return Assignment(Variable(p[1].getstr(), state), p[3], state)

        @self.pg.production('statement_full : FUNCTION IDENTIFIER ( ) { block }')
        def statement_func_noargs(state, p):
            if self.syntax is True:
                return [Node("FUNCTION"), Node("IDENTIFIER", p[1]), Node("("), Node(")"), Node("{"), Node("block", p[5]), Node("}")]
            return FunctionDeclaration(name=p[1].getstr(), args=None, block=p[5], state=state)

        @self.pg.production('expression : NOT expression')
        def expression_not(state, p):
            if self.syntax is True:
                return [Node("NOT"), Node("expression", p[1])]
            return Not(p[1], state)

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_binary_operator(state, p):
            if p[1].gettokentype() == 'SUM':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("+"), Node("expression", p[2])]
                return Sum(p[0], p[2], state)
            elif p[1].gettokentype() == 'SUB':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("-"), Node("expression", p[2])]
                return Sub(p[0], p[2], state)
            elif p[1].gettokentype() == 'MUL':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("*"), Node("expression", p[2])]
                return Mul(p[0], p[2], state)
            elif p[1].gettokentype() == 'DIV':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("/"), Node("expression", p[2])]
                return Div(p[0], p[2], state)
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
        def expression_equality(state, p):
            if p[1].gettokentype() == '==':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("=="), Node("expression", p[2])]
                return Equal(p[0], p[2], state)
            elif p[1].gettokentype() == '!=':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("!="), Node("expression", p[2])]
                return NotEqual(p[0], p[2], state)
            elif p[1].gettokentype() == '>=':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node(">="), Node("expression", p[2])]
                return GreaterThanEqual(p[0], p[2], state)
            elif p[1].gettokentype() == '<=':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("<="), Node("expression", p[2])]
                return LessThanEqual(p[0], p[2], state)
            elif p[1].gettokentype() == '>':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node(">"), Node("expression", p[2])]
                return GreaterThan(p[0], p[2], state)
            elif p[1].gettokentype() == '<':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("<"), Node("expression", p[2])]
                return LessThan(p[0], p[2], state)
            elif p[1].gettokentype() == 'AND':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("AND"), Node("expression", p[2])]
                return And(p[0], p[2], state)
            elif p[1].gettokentype() == 'OR':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("OR"), Node("expression", p[2])]
                return Or(p[0], p[2], state)
            else:
                raise LogicError("Shouldn't be possible")

        @self.pg.production('expression : CONSOLE_INPUT ( )')
        def program(state, p):
            if self.syntax is True:
                return [Node("CONSOLE_INPUT"), Node("("), Node(")")]
            return Input()

        @self.pg.production('expression : CONSOLE_INPUT ( expression )')
        def program(state, p):
            if self.syntax is True:
                return [Node("CONSOLE_INPUT"), Node("("), Node("expression", p[2]), Node(")")]
            return Input(expression=p[2], state=state)

        @self.pg.production('statement : PRINT ( )')
        def program(state, p):
            if self.syntax is True:
                return [Node("PRINT"), Node("("), Node(")")]
            return Print()

        @self.pg.production('statement : PRINT ( expression )')
        def program(state, p):
            if self.syntax is True:
                return [Node("PRINT"), Node("("), Node("expression", p[2]), Node(")")]
            return Print(expression=p[2], state=state)

        @self.pg.production('expression : ABSOLUTE ( expression )')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node("ABSOLUTE"), Node("("), Node("expression", p[2]), Node(")")]
            return Absolute(p[2], state)

        @self.pg.production('expression : SIN ( expression )')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node("SIN"), Node("("), Node("expression", p[2]), Node(")")]
            return Sin(p[2], state)

        @self.pg.production('expression : COS ( expression )')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node("COS"), Node("("), Node("expression", p[2]), Node(")")]
            return Cos(p[2], state)

        @self.pg.production('expression : TAN ( expression )')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node("TAN"), Node("("), Node("expression", p[2]), Node(")")]
            return Tan(p[2], state)

        @self.pg.production('expression : POWER ( expression , expression )')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node("POWER"), Node("("), Node("expression", p[2]), Node(","), Node("expression", p[4]), Node(")")]
            return Pow(p[2], p[4], state)

        @self.pg.production('expression : IDENTIFIER')
        def expression_variable(state, p):
            # Cannot return the value of a variable if it isn't yet defined
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0])]
            return Variable(p[0].getstr(), state)

        @self.pg.production('expression : IDENTIFIER ( )')
        def expression_call_noargs(state, p):
            # Cannot return the value of a function if it isn't yet defined
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0]), Node("("), Node(")")]
            return CallFunction(name=p[0].getstr(), args=None, state=state)

        @self.pg.production('expression : const')
        def expression_const(state, p):
            if self.syntax is True:
                return [Node("const", p[0])]
            return p[0]

        @self.pg.production('const : FLOAT')
        def constant_float(state, p):
            if self.syntax is True:
                return [Node("FLOAT", p[0])]
            return Float(p[0].getstr(), state)

        @self.pg.production('const : BOOLEAN')
        def constant_boolean(state, p):
            if self.syntax is True:
                return [Node("BOOLEAN", p[0])]
            return Boolean(p[0].getstr(), state)

        @self.pg.production('const : INTEGER')
        def constant_integer(state, p):
            if self.syntax is True:
                return [Node("INTEGER", p[0])]
            return Integer(p[0].getstr(), state)

        @self.pg.production('const : STRING')
        def constant_string(state, p):
            if self.syntax is True:
                return [Node("STRING", p[0])]
            return String(p[0].getstr().strip('"\''), state)

        @self.pg.production('const : PI')
        def constant_pi(state, p):
            if self.syntax is True:
                return [Node("PI", p[0])]
            return ConstantPI(p[0].getstr(), state)

        @self.pg.production('const : E')
        def constant_e(state, p):
            if self.syntax is True:
                return [Node("E", p[0])]
            return ConstantE(p[0].getstr(), state)

        @self.pg.error
        def error_handle(state, token):
            raise ValueError(token)

    def build(self):
        return self.pg.build()
