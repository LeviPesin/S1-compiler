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
		
class Return(AST):
	def __init__(self, expr):
		self.expr = expr

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
		self.current_token = self.lexer.get_next_token()
		
	def next(self):
		self.current_token = self.lexer.get_next_token()
	
	def parse(self):
		node = self.program()
		assert self.current_token.type == 'EOF'
		return node
	
	def program(self):
		node = Program()
		while (self.current_token.type != 'EOF'):
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
			token = self.current_token
			try:
				return self.func()
			except:
				self.lexer.pos = pos
				self.current_token = token
				return self.statement_list()
	
	def ife(self):
		assert self.current_token.type == 'IFE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		expr = self.expr()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		self.next()
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return IfE(expr, stats_list)
	
	def ifne(self):
		assert self.current_token.type == 'IFNE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		expr = self.expr()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		self.next()
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return IfNe(expr, stats_list)
	
	def whilee(self):
		assert self.current_token.type == 'WHIE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		expr = self.expr()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		self.next()
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return WhileE(expr, stats_list)
	
	def whilene(self):
		assert self.current_token.type == 'WHINE'
		self.next()
		assert self.current_token.type == 'LBR'
		self.next()
		expr = self.expr()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		self.next()
		stats_list = self.statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		return WhileNe(expr, stats_list)
		
	def func(self):
		name = self.func_name()
		assert self.current_token.type == 'LBR'
		self.next()
		pars = self.formparams()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		self.next()
		stats_list = self.func_statement_list()
		assert self.current_token.type == 'RCBR'
		self.next()
		node = Func(name, stats_list)
		node.pars = pars
		return node
		
	def formparams(self):
		node = []
		while self.current_token.type == 'ID':
			node.append(self.var())
			if self.current_token.type != 'COMMA':
				pos = self.lexer.pos
				token = self.current_token
				self.next()
				assert self.current_token.type != 'ID'
				self.lexer.pos = pos
				self.current_token = token
			else:
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
			if self.current_token.type in ['ID', 'LCOMM']:
				stats_list.append(self.statement())
			else:
				break
		return stats_list
	
	def func_statement_list(self):
		stats_list = []
		while True:
			if self.current_token.type in ['ID', 'LCOMM', 'IFE', 'IFNE', 'WHIE', 'WHINE']:
				stats_list.append(self.statement())
			else:
				if self.current_token.type == 'RET':
					stats_list.append(self.func_statement())
				else:
					break
		return stats_list
	
	def func_statement(self):
		assert self.current_token.type == 'RET'
		self.next()
		node = Return(self.expr())
		assert self.current_token.type == 'SEMICOL'
		self.next()
		return node
	
	def statement(self):
		if self.current_token.type == 'EMP':
			self.next()
			return NoOp()
		elif self.current_token.type == 'LCOMM':
			self.next()
			return NoOp()
		elif self.current_token.type in ['IFE', 'IFNE', 'WHIE', 'WHINE']:
			return self.block()
		else:
			assert self.current_token.type == 'ID'
			pos = self.lexer.pos
			token = self.current_token
			try:
				node = self.assign()
				assert self.current_token.type == 'SEMICOL'
				self.next()
				return node
			except:
				try:
					self.lexer.pos = pos
					self.current_token = token
					node = self.funcall()
					assert self.current_token.type == 'SEMICOL'
					self.next()
					return node
				except:
					self.lexer.pos = pos
					self.current_token = token
					return self.func()
				
	def params(self):
		node = []
		signal = False
		signal2 = True
		while True:
			pos = self.lexer.pos
			token = self.current_token
			try:
				node.append(self.expr())
				if signal:
					signal2 = False
				if self.current_token.type != 'COMMA':
					signal = True
				else:
					self.next()
			except:
				self.lexer.pos = pos
				self.current_token = token
				assert signal2
				break
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
		assert self.current_token.type in ['ID', 'LBR', 'LSBR']
		left = self.term()
		token = self.current_token
		if self.current_token.type in ['UNION', 'INTER', 'DIFF', 'SYMDIFF']:
			self.next()
			right = self.expr()
			return BinOp(left, token, right)
		return left
	
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
			token = self.current_token
			try:
				node = self.funcall()
				return node
			except:
				self.lexer.pos = pos
				self.current_token = token
				node = self.var()
				return node
	
	def set1(self):
		assert self.current_token.type == 'LSBR'
		self.next()
		pars = self.params()
		node = Set()
		node.pars = pars
		assert self.current_token.type == 'RSBR'
		self.next()
		return node