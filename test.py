from s1_lexer import *
text = '''nextNumber(num) {
    return num + [num];
}'''
lexer = Lexer(text)
print(lexer.get_next_token(['FID']))
print(lexer.get_next_token(['LBR']))
print(lexer.get_next_token(['FORMVID']))
print(lexer.get_next_token(['RBR']))
print(lexer.get_next_token(['LCBR']))
print(lexer.get_next_token(['RET']))
print(lexer.get_next_token(['VID']))
print(lexer.get_next_token(['UNION']))
print(lexer.get_next_token(['LSBR']))
print(lexer.get_next_token(['VID']))
print(lexer.get_next_token(['RSBR']))
print(lexer.get_next_token(['SEMICOL']))
print(lexer.get_next_token(['RCBR']))
