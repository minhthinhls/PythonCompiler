from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState
from compiler.JSONparsedTree import Node, write
from rply.lexer import LexerStream
from copy import copy
from pprint import pprint
import traceback

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

lexer = Lexer().build()  # Build the lexer using LexerGenerator
tokens: LexerStream
try:
    tokens = lexer.lex(call_declared_functions)  # Stream the input to analysis the lexical syntax
    tokenType = map(lambda x: x.gettokentype(), copy(tokens))
    tokenName = map(lambda x: x.getstr(), copy(tokens))
    pprint(list(copy(tokens)))
    # pprint(list(copy(tokenType)))
    # pprint(list(copy(tokenName)))
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("Finish lexical analysis !")

SymbolTable = ParserState()
parser = Parser().build()  # Build the LR-parser using ParserGenerator
syntaxRoot: Node
semanticRoot = Node("main")
try:
    treeProgram = parser.parse(tokens, state=SymbolTable)
    treeProgram.eval(semanticRoot)
    syntaxRoot = Node("syntax")
except (BaseException, Exception):
    traceback.print_exc()
finally:
    write(syntaxRoot, "SyntaxAnalyzer")
    write(semanticRoot, "SemanticAnalyzer")
    print("------------------------------Declared Variables & Functions are:------------------------------")
    pprint(SymbolTable.variables)
    pprint(SymbolTable.functions)
