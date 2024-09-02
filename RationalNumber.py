from BaseAssignmentValue import BaseAssignmentValue
from Environment import Environment

class RationalNumber(BaseAssignmentValue):
	def __init__(self, name, value, environment) -> None:
		super().__init__(name, value, environment)
		self.numerator = self.value
		self.denominator = 1
		self.is_simplified = False
	
	def parsing(self):
		try:
			if self.value == "?": # print result
				value = eval(self.name)
				print(f"  {value}")
			else:
				print(self.value)
				self.value = eval(self.value) # computed value and add to variables
				self.environment.addVariable(self)
		except Exception:
			print("Syntax Error tt")
			return -1
		return 0
	
	def stringToList(self, expression: str) -> list:
		res = []
		i = 0
		while i < len(expression):
			temp = ""
			if expression[i].isdigit():
				while i < len(expression) and expression[i].isdigit():
					temp += expression[i]
					i+=1
				res.append(temp)
			else:
				res.append(expression[i])
				i += 1
		return res

	def isOperator(self, c: str) -> bool:
		return c == '*' or c == '/' or c == '+' or c == '-'

	def tokenPreprocessing(self, expression: list):
		def parseExpression(expression: list) -> list:
			stack = []
			current = []
			for element in expression:
				if element == '(':
					stack.append(current)
					current = []
				elif element == ')':
					temp = current
					current = stack.pop()
					current.append(temp)
				else:
					current.append(element)
			# print(current)
			return current
		
		def format_expression(expression):
			if isinstance(expression, list):
				if len(expression) == 1:
					return format_expression(expression[0])
				while len(expression) > 1:
					for i in range(1, len(expression), 2):
						if expression[i] in '*/':
							left_expression = format_expression(expression[i - 1])
							right_expression = format_expression(expression[i + 1])
							sub = f"({left_expression} {expression[i]} {right_expression})"
							expression = expression[:i - 1] + [sub] + expression[i + 2:]
							break
					else:
						break
				while len(expression) > 1:
					op = expression[1]
					left_expression = format_expression(expression[0])
					right_expression = format_expression(expression[2])
					expression = [f"({left_expression} {op} {right_expression})"] + expression[3:]
				return expression[0]
			else:
				return expression

		parsed_expression = parseExpression(expression)
		if not (formated_expression := format_expression(parsed_expression)):
			return None
		if isinstance(formated_expression, str):
			formated_expression = self.stringToList(formated_expression.replace(" ", ""))
		return formated_expression

	def compute(self, input: str) -> str:
		splited_input = input.split('=')
		expression = self.stringToList(splited_input[1])
		if not (expression := self.tokenPreprocessing(expression)):
			print("Invalid syntax")
			return None
		# print(expression)
		binary_tree = BinaryTree(None)
		binary_tree.tree_generation(expression)
		# binary_tree.print_tree()
		res = binary_tree.tree_computation(binary_tree.root)
		# print("Result: " + str(res))
		return splited_input[0] + '=' + str(res)



# add Variables if not "= ?"
