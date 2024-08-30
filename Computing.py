from BinaryTree import BinaryTree



# def token_preprocessing(expression: list):
# 	pass
# 	tokenizedExpression = ""
# 	group = []
# 	for element in expression:
		

def compute(input: str) -> str:
	splitedInput = input.split('=')
	expression = [x for x in splitedInput[1]]

	print(expression)
	binary_tree = BinaryTree(None)
	binary_tree.tree_generation(expression)
	binary_tree.print_tree()
	res = binary_tree.tree_computation(binary_tree.root)
	print("Result: " + res)
	return splitedInput[0] + '=' + res