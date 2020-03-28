import re

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token(' + self.type + ', ' + repr(self.value) + ')'

    def __repr__(self):
        return self.__str__()

class Lexer():
	def __init__(self, text):
		self.text = text;
		self.pos = 0;
		self.token_specification = [
			['IFE', r'ife'],
			['IFNE', r'ifne'],
			['WHIE', r'whilee'],
			['WHINE', r'whilene'],
			['FID', r'[A-Za-z]+'],
			['FORMVID', r'[A-Za-z]+'],
			['ACTVID', r'[0-9A-Za-z]+'],
			['LBR', r'('],
			['RBR', r')'],
			['LCBR', r'{'],
			['RCBR', r'}'],
			['LCOMM', r'/*'],
			['RCOMM', r'*/'],
			['LSBR', r'['],
			['RSBR', r']'],
			['COMMA', r','],
			['SEMICOL', r';'],
			['ASSIGN', r'='],
			['UNION', r'+'],
			['INTER', r'*'],
			['DIFF', r'-'],
			['SYMDIFF', r'~'],
			['EMP', r''],
			['SPACE', r'\s'],
			['MISMATCH', r'.']
		]
		
	def get_next_token(tokens):
		//tokens should contain MISMATCH and SPACE
		token_specification = [[token, specification] for [token, specification] in self.token_specification if token in tokens]
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		mos = re.finditer(tok_regex, self.text[pos:])
		for mo in mos:
			kind = mo.lastgroup
			value = mo.group()
			if kind == 'MISMATCH':
				raise RuntimeError(f'{value!r} unexpected at {self.pos}')
			elif kind == 'SPACE':
				continue
			self.pos += len(value) + 1
			return Token(kind, value)
		return Token('EOF', 'EOF')