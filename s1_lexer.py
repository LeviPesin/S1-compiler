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
			('FID', r'(A-Za-z)+'),
			('FORMVID', r'(A-Za-z)+'),
			('VID', r'(0-9A-Za-z)+'),
			('LBR', r'('),
			('RBR', r')'),
			('LCBR', r'{'),
			('RCBR', r'}'),
			('LCOMM', r'/*'),
			('RCOMM', r'*/'),
			('LSBR', r'('),
			('RSBR', r')'),
			('COMMA', r','),
			('SEMICOL', r';'),
			('ASSIGN', r'='),
			('UNION', r'+'),
			('INTER', r'*'),
			('DIFF', r'-'),
			('SYMDIFF', r'~'),
			('EMP', r''),
			('SPACE', r'\s'),
			('MISMATCH', r'.')
		]
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		self.mos = re.finditer(tok_regex, self.text)
		self.reserved_keywords = ['ife', 'ifne', 'whilee', 'whilene', 'return']
		self.reserved_keywords_tokens = [{'ife', 'IFE'}, {'ifne', 'IFNE'}, {'whilee', 'WHIE'}, {'whilene', 'WHINE'}, {'return', 'RET'}]
		
	def get_next_token(self, tokens):
		for mo in self.mos:
			if mo.start() < self.pos:
				continue
			kind = mo.lastgroup
			value = mo.group()
			if kind == 'MISMATCH':
				raise RuntimeError(f'{value!r} unexpected at {self.pos}')
			elif kind == 'SPACE':
				self.pos += 1
				continue
			elif kind in ('FID', 'FORMVID', 'VID'):
				if value in self.reserved_keywords:
					token = self.reserved_keywords_tokens(value)
					if token in tokens:
						kind = token
					raise RuntimeError(f'{value!r} unexpected at {self.pos}')
			self.pos += len(value)
			return Token(kind, value)
		return Token('EOF', 'EOF')
