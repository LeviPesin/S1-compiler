from s1_lexer import *
text = '''nextNumber(num) {
    return num + [num];
}'''
lexer = Lexer(text)
tokens = ['FID', 'SPACE', 'MISMATCH']
print(lexer.get_next_token(tokens))
