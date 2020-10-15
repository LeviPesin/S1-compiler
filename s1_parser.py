class AST:
	repr_start_start = "\n========== START OF "
	repr_end_start = "\n========== END OF "
	repr_end = " =========="
	def parser_format(self, first, second):
		return f"{AST.repr_start_start}{first}{AST.repr_end}\n{str(second)}{AST.repr_end_start}{first}{AST.repr_end}"

class Conditional(AST):
	def __init__(self, left, right):
		self.cond = left
		self.stat = right
	
	def __repr__(self):
		return f"Condition of this {self.__class__.name}:\n" + self.parser_format("CONDITION", self.cond) + \
		       f"\nStatements of this {self.__class__.name}:\n" + self.parser_format("LIST OF STATEMENTS", self.stat)

class IfE(Conditional):
	name = "IfE"

class IfNe(Conditional):
	name = "IfNe"

class WhileE(Conditional):
	name = "WhileE"

class WhileNe(Conditional):
	name = "WhileNe"
		
class Return(AST):
	def __init__(self, expr):
		self.expr = expr
	
	def __repr__(self):
		return "Expression of this return:\n" + self.parser_format("EXPRESSION", self.expr)

class Func(AST):
	def __init__(self, left, middle, right):
		self.name = left
		self.pars = middle
		self.code = right
	
	def __repr__(self):
		repr = "Name of this function:\n" + self.name + "\nFormal parameters of this function:\n"
		for parameter in self.pars:
			repr += str(parameter) + "\n"
		return repr + "Code of this function:\n" + self.parser_format("LIST OF STATEMENTS", self.code)

class Program(AST):
	def __init__(self):
		self.blocks = []
	
	def __repr__(self):
		repr = "Blocks of this program:"
		for block in self.blocks:
			repr += "\n" + self.parser_format("BLOCK", block)
		return repr

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
		
	def __repr__(self):
		return "Variable " + self.name

class Set(AST):
	def __init__(self):
		self.pars = []

class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.next()
		
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
		if self.current_token.type in ['IFE', 'IFNE', 'WHIE', 'WHINE']:
			token = self.current_token.type
			return self.conditional(token, {"IFE": IfE, "IFNE": IfNe, "WHIE": WhileE, "WHINE": WhileNe}[token])
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
	
	def conditional(self, token, class_name):
		assert self.current_token.type == token
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
		return class_name(expr, stats_list)
		
	def func(self):
		name = self.func_name()
		assert self.current_token.type == 'LBR'
		self.next()
		pars = self.formparams()
		assert self.current_token.type == 'RBR'
		self.next()
		assert self.current_token.type == 'LCBR'
		self.next()
		stats_list = self.statement_list(True)
		assert self.current_token.type == 'RCBR'
		self.next()
		return Func(name, pars, stats_list)
		
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
		
	def statement_list(self, is_func = False):
		stats_list = []
		while True:
			if self.current_token.type in ['ID', 'LCOMM', 'IFE', 'IFNE', 'WHIE', 'WHINE']:
				stats_list.append(self.statement())
			elif is_func and (self.current_token.type == 'RET'):
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