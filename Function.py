from BaseAssignmentValue import BaseAssignmentValue

class Function(BaseAssignmentValue):
	def __init__(self, name, value, environment) -> None:
		super().__init__(name, value, environment)
		self.subname = ""
		self.functionVariable = ""

	def setSubname(self):
		for i in self.name:
			if i == '(':
				break
			self.subname += i

	def setFunctionVar(self):
		for i in range(len(self.name)):
			if self.name[i] == '(':
				while self.name[i] != ')':
					self.functionVariable += self.name[i]
					i+=1
				break

	def getFunctionVar(self):
		fVar = ""
		for i in range(len(self.name)):
			if self.name[i] == '(':
				while self.name[i] != ')':
					fVar += self.name[i]
					i+=1
				break
		return fVar

	def getVarAlias(self, varName):
		alias = ""
		for i in varName:
			if i == '(':
				break
			alias += i
		return alias
	
	def swap(self):
		temp = self.value
		self.value = self.name
		self.name = temp

	def ft_strchr(self, element):
		for var in self.environment.variables:
			alias = self.getVarAlias(var.name)
			print("alias: ", alias)
			if element == alias:
				return var.value
		return None

	def expandFunction(self, arg):
		expandedInput = ""
		for element in arg:
			if (varValue := self.ft_strchr(element)) and element.isalpha() and \
				not(element == 'i'):
				expandedInput += varValue
			else:
				expandedInput += element
			self.value = expandedInput

	def parsing(self):
		self.setSubname()
		self.setFunctionVar()
		try:
			if self.value == '?':
				self.swap()
				self.expandFunction(self.value)
				print(self.value)
				print("compute")
			else:
				self.environment.addVariable(self)
				print("addVariable")
		except Exception:
			print("  Syntax Error")
		self.compute()
	
	def compute(self):
		pass
