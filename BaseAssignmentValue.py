class BaseAssignmentValue:
	def __init__(self, input) -> None:
		self.input = input
		self.name = input.split('=')[0]
		self.value = input.split('=')[1]

	def compute(self):
		pass