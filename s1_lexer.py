import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token(' + self.type + ', ' + repr(self.value) + ')'

    def __repr__(self):
        return self.__str__()

class Lexer:
	def __init__(self, text):
		self.text = text;
		self.pos = 0;
		token_specification = [
			('IFE', r'ife'),
			('IFNE', r'ifne'),
			('WHIE', r'whilee'),
			('WHINE', r'whilene'),
			('RET', r'return'),
			('ID', r'[0-9A-Za-z]+'),
			('LBR', r'\('),
			('RBR', r'\)'),
			('LCBR', r'{'),
			('RCBR', r'}'),
			('LCOMM', r'/\*'),
			('RCOMM', r'\*/'),
			('LSBR', r'\['),
			('RSBR', r'\]'),
			('COMMA', r','),
			('SEMICOL', r';'),
			('ASSIGN', r'='),
			('UNION', r'\+'),
			('INTER', r'\*'),
			('DIFF', r'-'),
			('SYMDIFF', r'~'),
			('SPACE', r'\s'),
			('EMP', r''),
			('MISMATCH', r'.')
		]
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		self.mos = list(re.finditer(tok_regex, self.text))
		
	def get_next_token(self):
		if (self.pos == (len(self.text) - 1)) or (self.pos == len(self.text)):
			return Token('EOF', 'EOF')
		for mo in self.mos:
			if mo.start() < self.pos:
				continue
			kind = mo.lastgroup
			value = mo.group()
			if kind == 'MISMATCH':
				raise RuntimeError(f'{value!r} unexpected at {self.pos}')
			elif kind == 'SPACE':
				continue
			self.pos = mo.end()
			return Token(kind, value)
