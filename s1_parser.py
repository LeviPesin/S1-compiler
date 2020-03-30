class AST:
	pass

class IfE(AST):
	def __init__(self, left, right):
		self.cond = left
		self.stat = right

class IfNe(AST):
	def __init__(self, left, right):
		self.cond = left
		self.stat = right

class WhileE(AST):
	def __init__(self, left, right):
		self.cond = left
		self.stat = right

class WhileNe(AST):
	def __init__(self, left, right):
		self.cond = left
		self.stat = right

class Func(AST):
	def __init__(self, left, right):
		self.name = left
		self.pars = []
		self.code = right
		
class StatsList(AST):
	def __init__(self):
		self.stats = []

class Program(AST):
	def __init__(self):
		self.blocks = []

class Assign(AST):
	def __init__(self, left, right):
		self.var = left
		self.value = right

class FuncCall(AST):
	def __init__(self, left):
		self.name = left
		self.pars = []

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

class NoOp(AST):
	def __init__(self):
		pass

class Var(AST):
	def __init__(self, token):
		self.name = token.value

class Set(AST):
	def __init__(self):
		self.pars = []

class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = self.lexer.get_self.next_token()
		
	def next(self):
		self.current_token = self.lexer.get_self.next_token()
	
	def parse(self):
		node = self.program()
		assert self.current_token.type == 'EOF'
		return node
	
	def program(self):
		node = Program()
		while (self.current_token != 'EOF'):
			node.blocks.append(self.block())
		return node
	
	def block(self):
		if self.current_token.type == 'IFE':
			return self.ife()
		elif self.current_token.type == 'IFNE':
			return self.ifne()
		elif self.current_token.type == 'WHIE':
			return self.whilee()
		elif self.current_token.type == 'WHINE':
			return self.whilene()
		else:
			assert self.current_token.type == 'ID'
			pos = self.lexer.pos
			try:
				return self.func()
			except:
				self.lexer.pos = pos
				return self.statement_list()
	
	def ife(self):
		assert self.current_token.type == 'IFE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		var = self.var()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return IfE(var, stats_list)
	
	def ifne(self):
		assert self.current_token.type == 'IFNE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		var = self.var()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return IfNe(var, stats_list)
	
	def whilee(self):
		assert self.current_token.type == 'WHIE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		var = self.var()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return WhileE(var, stats_list)
	
	def whilene(self):
		assert self.current_token.type == 'WHINE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		var = self.var()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return WhileNe(var, stats_list)
		
	def func(self):
		name = self.func_name()
		assert self.current_token.type == 'LBR'
		self.next()
		pars = self.formparams()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		stats_list = self.func_statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		node = Func(name, stats_list)
		node.pars = pars
		self.next()
		return node
		
	def formparams(self):
		node = []
		while self.current_token.type == 'ID':
			node.append(self.var())
			if self.current_token.type != 'COMMA':
				self.next()
				assert self.current_token.type != 'ID'
		if node == []:
			self.next()
		return node
		
	def var(self):
		assert self.current_token.type == 'ID'
		token = self.current_token
		self.next()
		return Var(token)
	
	def func_name(self):
		assert self.current_token.type == 'ID'
		token = self.current_token
		self.next()
		return token.value
		
	def statement_list(self):
		stats_list = []
		while True:
			pos = self.lexer.pos
			try:
				stats_list.append(self.statement())
			except:
				self.lexer.pos = pos
				break
		return stats_list
	
	def func_statement_list(self):
		stats_list = []
		while True:
			pos = self.lexer.pos
			try:
				stats_list.append(self.statement())
			except:
				self.lexer.pos = pos
				try:
					stats_list.append(self.func_statement())
				except:
					self.lexer.pos = pos
					break
		return stats_list
	
	def statement(self):
		if self.current_token.type == 'EMP':
			self.next()
			return NoOp()
		elif self.current_token.type == 'LCOMM':
			self.next()
			return NoOp()
		else:
			assert self.current_token.type == 'ID'
			pos = self.lexer.pos
			try:
				node = self.assign()
				assert self.current_token.type == 'SEMICOL'
				self.next()
				return node
			except:
				node = self.funcall()
				assert self.current_token.type == 'SEMICOL'
				self.next()
				return node
				
	def params(self):
		node = []
		signal = False
		signal2 = True
		while True:
			try:
				if signal:
					signal2 = False
				node.append(self.expr())
				self.next()
				if self.current_token.type != 'COMMA':
					signal = True
			except:
				assert signal2
		if node == []:
			self.next()
		return node
		
	def assign(self):
		assert self.current_token.type == 'ID'
		var = self.var()
		assert self.current_token.type == 'ASSIGN'
		self.next()
		expr = self.expr()
		return Assign(var, expr)
		
	def funcall(self):
		assert self.current_token.type == 'ID'
		node = FuncCall(self.func_name())
		assert self.current_token.type == 'LBR'
		self.next()
		pars = self.params()
		node.pars = pars
		assert self.current_token.type == 'RBR'
		self.next()
		return node
	
	def expr(self):
		pos = self.lexer.pos
		try:
			node = self.term()
			return node
		except:
			self.lexer.pos = pos
			left = self.expr()
			token = self.current_token
			assert token.type in ['UNION', 'INTER', 'DIFF', 'SYMDIFF']
			right = self.expr()
			return BinOp(left, token, right)
	
	def term(self):
		if self.current_token.type == 'LSBR':
			return self.set1()
		elif self.current_token.type == 'LBR':
			self.next()
			node = self.expr()
			assert self.current_token.type == 'RBR'
			self.next()
			return node
		else:
			assert self.current_token.type == 'ID'
			pos = self.lexer.pos
			try:
				node = self.funcall()
				return node
			except:
				self.lexer.pos = pos
				node = self.var()
				return node
	
	def set1(self):
		assert self.current_token.type == 'LSBR'
		pars = self.params()
		node = Set()
		node.pars = pars
		assert self.current_token.type == 'RSBR'
		return node