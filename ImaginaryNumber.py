# real_part, imaginary_part, module, argument
from BaseAssignmentValue import BaseAssignmentValue

class ImaginaryNumber(BaseAssignmentValue):
	def __init__(self, name, value) -> None:
		super.__init__(name, value)
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


