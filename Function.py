# expression (2x + 3), variables (x, y), domaine ?, is_continious etc...
from BaseAssignmentValue import BaseAssignmentValue

class Function(BaseAssignmentValue):
	def __init__(self, name, value, environment) -> None:
		super().__init__(name, value, environment)
		self.expression = self.value
		self.variables = self.getVariables()


	def getVariables(self):
		variables = []
		for letter in self.expression:
			if letter.isalpha():
				variables.append(letter)
		return variables
