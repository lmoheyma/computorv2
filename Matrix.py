# rows, cloumns, elements (tab 2D), is_square, determinant
from BaseAssignmentValue import BaseAssignmentValue

class Matrix(BaseAssignmentValue):
	def __init__(self, name, value) -> None:
		super.__init__(name, value)
		self.rows = len(self.value)
		self.columns = len(self.value[0])
		self.elements = self.value
		self.is_square = self.isSquare()
		self.determinant = 0

	def isSquare(self) -> bool:
		for element in self.elements:
			if len(element) != len(self.elements[0]) \
			or len(element) != len(self.elements):
				return False
		return True

	def determinant(self):
		pass