from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState
from pprint import pprint
import traceback


class Environment(object):
    # Dummy class for later on purposes !
    def __init__(self):
        # We want to hold a dict of declared variables & functions.
        self.variables = {}
        self.functions = {}
        pass  # End Environment's constructor !


if_else_statement = """
if (False) {
    print(False == (5 != 5));
    print(5.1111 != 5.1);
    print(5 != 5);
    print(not True);
} else {
    print(abs(3.5 - 4));
    print(sin(3.5 - 4));
    print(cos(__E__ - __PI__));
    print(tan(__PI__ - __E__));
    print(pow(-2, 5));
}
"""
assignment_and_variables = """
    let a = 5 - 2;
    let b = 5;
    print(sin(a));
    print(a); print(b); print(b - a);
    print(not False);
"""
call_declared_functions = """
function userDefined() {
    let pi = __PI__;
    let e = __E__;
    print(2 * (pi + e - 1) / 3);
    print(abs(e - pi));
    print(sin(pi));
    print(cos(pi));
    print(tan(pi));
    print(pow(pi, e));
}

function main() {
    let i = input("Please input the number: ");
    if (i > 0) {
        print("-> Call User Defined Function !");
        userDefined();
    } else {
        print();
        print("Input value equal to or less than 0 !");
    }
}

main();

"""
parsed_tree = """
let a = 2 / 5 + 6 * 20;
"""

lexer = Lexer().build()  # Build the lexer using LexerGenerator
try:
    tokens = lexer.lex(parsed_tree)  # Stream the input to analysis the lexical syntax
    tokenType = map(lambda x: x.gettokentype(), list(tokens))
    tokenName = map(lambda x: x.getstr(), list(tokens))
    # pprint(list(tokens))
    # pprint(list(tokenType))
    # pprint(list(tokenName))
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("Finish lexical analysis !")

SymbolTable = ParserState()
parser = Parser().build()  # Build the LR-parser using ParserGenerator
try:
    parser.parse(lexer.lex(parsed_tree), state=SymbolTable).eval(Environment())
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("------------------------------Declared Variables & Functions are:------------------------------")
    pprint(SymbolTable.variables)
    pprint(SymbolTable.functions)
