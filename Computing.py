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

def token_preprocessing(expression: list):
	# pass
	# tokenizedExpression = ""
	# group = []
	# countOperand = [x for x in expression if x.isnum()]
	# print(countOperand)
	if any(char in ['+', '-', '*', '/'] for char in expression):
		expression.insert(0, '(')
		expression.append(')')
	return expression

def compute(input: str) -> str:
	splitedInput = input.split('=')
	expression = stringToList(splitedInput[1])
	expression = token_preprocessing(expression)
	print(expression)
	# expression = ['(', '5', '+', '4', ')']
	binary_tree = BinaryTree(None)
	binary_tree.tree_generation(expression)
	binary_tree.print_tree()
	res = binary_tree.tree_computation(binary_tree.root)
	print("Result: " + str(res))
	return splitedInput[0] + '=' + str(res)