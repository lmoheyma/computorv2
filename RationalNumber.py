# numerator, denominator, is_simplified, is_positive
from BaseAssignmentValue import BaseAssignmentValue

class RationalNumber(BaseAssignmentValue):
	def __init__(self) -> None:
		super.__init__()
		self.numerator = self.value
		self.denominator = 1
		self.is_simplified = False
		self.is_positive = self.value > 0