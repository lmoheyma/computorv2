class BaseAssignmentValue:
	def __init__(self, name, value, environment) -> None:
		self.name = name
		self.value = value
		self.environment = environment

	def compute(self):
		pass