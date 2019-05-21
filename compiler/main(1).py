from compiler.lexer import Lexer

text_input = """
print(4 + 4 - 2);
"""

lexer = Lexer().build()  # Build the lexer using LexerGenerator
tokens = lexer.lex(text_input)  # Stream the input to analysis the lexical syntax

for token in tokens:
    print(token)
