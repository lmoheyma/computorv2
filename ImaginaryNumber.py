# real_part, imaginary_part, module, argument
from BaseAssignmentValue import BaseAssignmentValue
import re

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
		# print("imaginary part: ", self.imaginary_part)
		# print("real part: ", value)
		return value


	def calculateModule(self):
		pass

	def calculateArgument(self):
		pass
	
	def convertToInt(self):
		pass

	def preProcess(self):
		value = self.value.replace(" ", "")
		for i in value:
			if i not in '0123456789i+*/-.()':
				print("  Syntax Error")
				return 1
		return 0

	def parsing(self):
		if self.preProcess():
			return -1
		try:
			if self.value == "?":
				print(f"  {self.name}")
			else:
				self.real_part = self.parseImaginaryPart()
				if self.real_part == '' or self.real_part == '+' or self.real_part == '-':
					self.real_part = 0
				if self.real_part != 0:
					self.value = str(self.real_part)
					if self.value[0] == '+': self.value = self.value[1:]
					if self.imaginary_part != 0:
						if self.imaginary_part > 0:
							self.value += " + " + str(self.imaginary_part) + 'i'
						else:
							self.value += " - " + str(self.imaginary_part)[1:] + 'i'
				else:
					if self.imaginary_part != 0:
						if self.imaginary_part > 0:
							self.value = str(self.imaginary_part) + 'i'
						else:
							self.value = str(self.imaginary_part) + 'i'
				print(f"  {self.value}")
				# self.checkFormat()
				# self.environment.addVariable(self)
		except Exception:
			print("Syntax Error")
			return -1
		return 0
