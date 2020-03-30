from s1_lexer import *
from s1_parser import *
text = '''nextNumber(num) {
    return num + [num];
}'''
lexer = Lexer(text)
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
parser = Parser(lexer)
parsed = parser.parse()
