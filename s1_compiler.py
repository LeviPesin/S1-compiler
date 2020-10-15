class Function:
	def __init__(self, name):
		self.name = name
		self.uncompiledPars = [];
		self.uncompiledCode = []
		self.code = dict()
		self.variables = dict()

class Variable:
	def __init__(self, name, func, reg):
		self.name = name
		self.function = func
		self.register = reg

class Compiler:
	'''Operations of Madhine:
		1) MovOp - copy value from source to target.
		2) ClearOp - assign empty set to target.
		3) AddOp - add element to target set.
		4) BinOp - make operation (+, *, - or ~) with arg1 and arg2 and assign result to res.
		5) JumpOp - if test is empty, jump to one state, else to another.
		6) DeconstructOp - if test is empty, jump to one state. Else select one element, assign it to element,
                           assign rest of test to rest, jump to another state.
		7) AssertOp - raise error if test is empty.
		8) CallOp - call function.
		9) ReturnOp - return to return_state, specified by CallOp.'''
    def __init__(self, parser):
        self.tree = parser.parse()
		self.code = dict()
		main = Function("main")
		self.functions = {"main": main}
		self.next_var_register = 0
		self.next_code_register = 0
		self.next_id = 0
	
	def findFunctions(self):
		main_tree = []
		for block in self.tree.blocks:
			if type(block).__name__ == "Func":
				func = Function(block.name)
				self.functions[block.name] = func
				func.uncompiledPars = block.pars
				func.uncompiledCode = block.code
			else:
				main_tree = main_tree + block
		self.functions["main"].uncompiledCode = main_tree
	
	def compile(self):
		self.findFunctions()
		for name in self.functions:
			func = self.functions[name]
			self.parseFunction(func)
		for name in self.functions:
			func = self.functions[name]
			self.parseCallsInFunction(func)
			self.code = self.code.update(func.code)
		return self.code
	
	def parseFunction(self, func):
		func.code.update(self.parseStatList(func.uncompiledCode, func))
	
	def parseCallsInFunction(self, func):
		#???????!!!!????!!!!?????!!!!?????!???!?!?!?!?!?
	
	def parseStatList(self, list, func):
		code = dict()
		for stat in list.stats:
			if type(stat).__name__ in ['IfE', 'IfNe', 'WhileE', 'WhileNe']:
				var = Variable("temp_" + str(self.next_id), func, self.next_var_register)
				func.variables["temp_" + str(self.next_id)] = var
				self.next_id += 1
				self.next_var_register += 1
				code.update(parseExpr(stat.cond, var))
				register = self.next_code_register
				self.next_code_register += 1
				code.update(parseStatList(stat.stat, func))
				if type(stat).__name__ == 'IfE':
					code[register] = JumpOp(register + 1, self.next_code_register, var.register)
				elif type(stat).__name__ == 'IfNe':
					code[register] = JumpOp(self.next_code_register, register + 1, var.register)
				elif type(stat).__name__ == 'WhileE':
					code[register] = code[self.next_code_register] = JumpOp(register + 1, self.next_code_register + 1, \
					    var.register)
					self.next_code_register += 1
				else:
					code[register] = code[self.next_code_register] = JumpOp(self.next_code_register + 1, register + 1, \
					    var.register)
					self.next_code_register += 1
			elif type(stat).__name__ == 'Return':
				var = Variable("temp_" + str(self.next_id), func, self.next_var_register)
				func.variables["temp_" + str(self.next_id)] = var
				self.next_id += 1
				self.next_var_register += 1
				code.update(parseExpr(stat.cond, var))
				code[self.next_register] = ReturnOp(var.register) #???????!!!!????!!!!?????!!!!?????!???!?!?!?!?!?
				self.next_code_register += 1
			elif type(stat).__name__ == 'Assign':
				var_name = stat.var
				try:
					var = func.variables[var_name]
				except:
					var = Variable(var_name, func, self.next_var_register)
					func.variables[var_name] = var
					self.next_var_register += 1
				code.update(parseExpr(stat.value, var))
			else:
				assert type(stat).__name__ == 'FuncCall'
				#???????!!!!????!!!!?????!!!!?????!???!?!?!?!?!?
		return code
		
	def parseExpr(expr, var):
		code = dict()
		func = var.function
		if type(expr).__name__ == 'Var':
			try:
				var2 = func.variables[expr.name]
			except:
				var2 = self.functions["main"].variables[expr.name]
			code[self.next_code_register] = MovOp(self.next_code_register + 1, var2.register, var.register)
			self.next_code_register += 1
			return code
		elif type(expr).__name__ == 'BinOp':
			var2 = Variable("temp_" + str(self.next_id), func, self.next_var_register)
			func.variables["temp_" + str(self.next_id)] = var2
			self.next_id += 1
			self.next_var_register += 1
			var3 = Variable("temp_" + str(self.next_id), func, self.next_var_register)
			func.variables["temp_" + str(self.next_id)] = var3
			self.next_id += 1
			self.next_var_register += 1
			code.update(parseExpr(left, var2))
			code.update(parseExpr(right, var3))
			op = {"+": BinOpType.UNION, "*": BinOpType.INTERSECTION, 
			      "-": BinOpType.DIFFERENCE, "~": BinOpType.SYM_DIFFERENCE}[expr.op.value]
			code[self.next_code_register] = BinOp(self.next_code_register + 1, op, var2, var3, var)
			self.next_code_register += 1
			return code
		elif type(expr).__name__ == 'Set':
			code[self.next_code_register] = ClearOp(self.next_code_register + 1, var)
			self.next_code_register += 1
			var2 = Variable("temp_" + str(self.next_id), func, self.next_var_register)
			func.variables["temp_" + str(self.next_id)] = var2
			self.next_id += 1
			self.next_var_register += 1
			for par in expr.pars:
				code.update(parseExpr(par, var2))
				code[self.next_code_register] = AddOp(self.next_code_register + 1, var2, var)
				self.next_code_register += 1
			return code
		else:
			assert type(expr).__name__ == 'FuncCall'
			#???????!!!!????!!!!?????!!!!?????!???!?!?!?!?!?