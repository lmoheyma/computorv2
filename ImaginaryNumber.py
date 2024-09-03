from BaseAssignmentValue import BaseAssignmentValue

class ImaginaryNumber(BaseAssignmentValue):
	def __init__(self, name, value, environment) -> None:
		super().__init__(name, value, environment)
		self.real_part = 0
		self.imaginary_part = 0
		self.module = 0
		self.argument = 0

	def parseImaginaryPart(self):
		value = self.value.replace(" ", "")
		if value[0] == 'i': self.imaginary_part += 1
		i = 0
		while i < len(value):
			if value[i] == "i":
				skipCaracters = 0
				j = i - 1
				while (j >= 0) and not value[j].isdigit():
					j-=1
					skipCaracters+=1
				while (j > 0) and (value[j].isdigit() or value[j] in '.'):
					j-=1
				self.imaginary_part += float(value[j:i-skipCaracters])
				value = value[:j] + value[i+1:]
				i-=(i+1)-j
			i+=1
		return value


	def calculateModule(self):
		pass

	def calculateArgument(self):
		pass
	
	def swap(self):
		temp = self.value
		self.value = self.name
		self.name = temp

	def convertToInt(self):
		temp = self.imaginary_part
		try:
			self.imaginary_part = int(self.imaginary_part)
			if self.imaginary_part / temp != 1:
				self.imaginary_part = temp
		except ValueError:
			print("  Value Error")
			

	def preProcess(self):
		value = self.value.replace(" ", "")
		for i in value:
			if i not in '0123456789i+*/-.()':
				print("  Syntax Error")
				return 1
		return 0

	def reorganizeExpression(self):
		if self.real_part == '' or self.real_part == '+' or self.real_part == '-':
			self.real_part = 0
		if self.real_part != 0:
			self.value = str(self.real_part)
			if self.value[0] == '+': self.value = self.value[1:]
			if self.imaginary_part != 0:
				self.convertToInt()
				if self.imaginary_part > 0:
					self.value += " + " + str(self.imaginary_part) + 'i'
				else:
					self.value += " - " + str(self.imaginary_part)[1:] + 'i'
		else:
			if self.imaginary_part != 0:
				self.convertToInt()
				if self.imaginary_part > 0:
					self.value = str(self.imaginary_part) + 'i'
				else:
					self.value = str(self.imaginary_part) + 'i'

	def parsing(self):
		# if self.preProcess():
		# 	return -1
		try:
			if self.value == "?":
				self.swap()
				self.expander(self.value, 'value')
				self.real_part = self.parseImaginaryPart()
				try:
					self.real_part = eval(self.real_part)
				except Exception:
					print("  Compute Error")
					return
				self.reorganizeExpression()
				print(f"  {self.value}")
			else:
				self.real_part = self.parseImaginaryPart()
				try:
					if self.real_part != '' and self.real_part != '+' \
					and self.real_part != '-' and self.real_part != ' ':	
						self.real_part = eval(self.real_part)
				except Exception:
					print("  Compute Error")
					return
				self.reorganizeExpression()
				print(self.imaginary_part, self.real_part)
				self.environment.addVariable(self)
		except Exception:
			print("  Syntax Error")
			return -1
		return 0
	
	def ft_strchr(self, element):
		for var in self.environment.variables:
			if element == var.name:
				return var.value
		return None

	def expander(self, arg, flag):
		expandedInput = ""
		var = ""
		i = 0
		while i < len(arg):
			while i < len(arg) and arg[i].isalpha():
				var += arg[i]
				i+=1
			if i == len(arg): i-=1
			if var == 'i':
				i-=1
				var = ""
			if (varValue := self.ft_strchr(var)) and \
				not(arg[i] == 'i'):
				expandedInput += varValue
				var = ""
			else:
				expandedInput += arg[i]
			i+=1
		if flag == 'name':
			self.name = expandedInput
		else:
			self.value = expandedInput
