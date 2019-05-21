from compiler.lexer import Lexer
from compiler.parser import Parser
from pprint import pprint

text_input = """
print(not(5 != 5 or 6 == 6));
"""
if_else_statement = """
if (False) {
    print(False == (5 != 5));
    print(5 != 5);
} else {
    print(5.1111 != 5.1);
    print(5 == 6);
}
"""

lexer = Lexer().build()  # Build the lexer using LexerGenerator
tokens = lexer.lex(if_else_statement)  # Stream the input to analysis the lexical syntax

pprint(list(tokens))

parser = Parser().build()  # Build the LR-parser using ParserGenerator
parser.parse(lexer.lex(if_else_statement)).eval()
