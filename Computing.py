from BinaryTree import BinaryTree

def stringToList(expression: str) -> list:
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

def isOperator(c: str) -> bool:
	return c == '*' or c == '/' or c == '+' or c == '-'

def tokenPreprocessing(expression: list):
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
	formated_expression = format_expression(parsed_expression)
	formated_expression = stringToList(formated_expression.replace(" ", ""))
	return formated_expression

def compute(input: str) -> str:
	splited_input = input.split('=')
	expression = stringToList(splited_input[1])
	expression = tokenPreprocessing(expression)
	binary_tree = BinaryTree(None)
	binary_tree.tree_generation(expression)
	# binary_tree.print_tree()
	res = binary_tree.tree_computation(binary_tree.root)
	# print("Result: " + str(res))
	return splited_input[0] + '=' + str(res)
