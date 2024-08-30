# numerator, denominator, is_simplified, is_positive
from BaseAssignmentValue import BaseAssignmentValue

class RationalNumber(BaseAssignmentValue):
	def __init__(self, name, value) -> None:
		super.__init__(name, value)
		self.numerator = self.value
		self.denominator = 1
		self.is_simplified = False
		self.is_positive = self.value > 0