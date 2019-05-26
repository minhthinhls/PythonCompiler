from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState
from pprint import pprint

text_input = """
print(not(5 != 5 or 6 == 6));
"""
if_else_statement = """
if (False) {
    print(False == (5 != 5));
    print(5.1111 != 5.1);
    print(5 != 5);
    print(not True);
    
    print(abs(3.5 - 4));
    print(abs(__E__ - __PI__));
    print(__PI__);
    print(__E__);
} else {
    let a = 5;
    print(sin(3.5 - 4));
    print(cos(__E__ - __PI__));
    print(tan(__PI__ - __E__));
    print(pow(-2, 5));
}
"""
variable = """
if (True) {
    let a = 5 - 2;
    
    print(True);
}
"""

lexer = Lexer().build()  # Build the lexer using LexerGenerator
tokens = lexer.lex(variable)  # Stream the input to analysis the lexical syntax

pprint(list(tokens))

parser = Parser().build()  # Build the LR-parser using ParserGenerator
parser.parse(lexer.lex(variable), state=ParserState()).eval()
