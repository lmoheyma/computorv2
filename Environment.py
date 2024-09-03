class Environment:
	def __init__(self) -> None:
		self.variables = []
	
	def ft_strchr(self, element):
		for var in self.variables:
			if element == var.name:
				return var.value
		return None

	def expander(self, input) -> str:
		expandedInput = ""
		splitedInput = input.split('=')
		for element in splitedInput[1]:
			if (varValue := self.ft_strchr(element, self.variables)) and element.isalpha() and \
				not(element == 'i'):
				expandedInput += varValue
			else:
				expandedInput += element
		return splitedInput[0] + '=' + expandedInput

	def getIndexOfVariable(self, var: str) -> int:
		for i in range(len(self.variables)):
			if var == self.variables[i].name:
				return i
		return -1

	def addVariable(self, variable: any) -> list:
		if self.ft_strchr(variable.name):
			if (index := self.getIndexOfVariable(variable.name)) == -1:
				print("Can't add variable")
				return
			if type(variable) != type(self.variables[index]):
				self.variables[index] = variable
			else:
				self.variables[index].value = variable.value
		else:
			# print(variable)
			self.variables.append(variable)
		print(f"  {variable.value}")

	def printVar(self):
		for var in self.variables:
			print(f"Variable: {var.name}  |  Value: {var.value}")
