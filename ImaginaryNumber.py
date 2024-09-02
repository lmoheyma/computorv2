# real_part, imaginary_part, module, argument
from BaseAssignmentValue import BaseAssignmentValue

class ImaginaryNumber(BaseAssignmentValue):
	def __init__(self, name, value, environment) -> None:
		super().__init__(name, value, environment)
		self.real_part = self.parseRealPart()
		self.imaginary_part = self.parseImaginaryPart()
		self.module = self.calculateModule()
		self.argument = self.calculateArgument()

	def parseRealPart(self):
		pass

	def parseImaginaryPart(self):
		pass

	def calculateModule(self):
		pass

	def calculateArgument(self):
		pass

	def parsing(self):
		try:
			if self.value == "?": # print result
				value = eval(self.name)
				print(value)
			else:
				value = eval(self.value) # computed value and add to variables
				# self.addVariable(self.name, self.value)
		except Exception:
			print("Syntax Error")
			return -1
		self.environment.addVariable(self)
		return 0
		


