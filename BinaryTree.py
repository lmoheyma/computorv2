class Node:
	def __init__(self, value) -> None:
		self.value = value
		self.left_child = None
		self.right_child = None
		self.parent = None

	def is_leaf(self, node):
		if node.left_child == None and \
			node.right_child == None:
			return True
		return False

class BinaryTree:
	def __init__(self, root_value) -> None:
		self.root = Node(root_value)
		self.current = self.root
	
	def move_to_left(self):
		if self.current.left_child:
			self.current = self.current.left_child

	def move_to_right(self):
		if self.current.right_child:
			self.current = self.current.right_child

	def move_to_parent(self):
		if self.current.parent:
			self.current = self.current.parent

	def add_left(self, value) -> None:
		if self.current.left_child == None:
			self.current.left_child = Node(value)
			self.current.left_child.parent = self.current
		
	def add_right(self, value) -> None:
		if self.current.right_child == None:
			self.current.right_child = Node(value)
			self.current.right_child.parent = self.current

	def get_value(self):
		return self.current.value

	def get_left_value(self):
		return self.current.left_child
	
	def get_right_value(self):
		return self.current.right_child
	
	def tree_generation(self, expression: list):
		token_list = ["+", "-", "/", "*"]
		for token in expression:
			if token == "(":
				self.add_left(None)
				self.move_to_left()
			elif token in token_list:
				self.current.value = token
				self.add_right(None)
				self.move_to_right()
			elif token == ")":
				if self.current.parent:
					self.current = self.current.parent
			else:
				self.current.value = token
				self.current = self.current.parent

	def tree_computation(self, node=None):
		if node is None:
			node = self.root
		if node.left_child is None and node.right_child is None:
			return node.value
		if node.left_child:
			left_value = self.tree_computation(node.left_child)
			node.left_child.value = eval(left_value + node.value + node.left_child.value)
		if node.right_child:
			right_value = self.tree_computation(node.right_child)
			node.right_child.value = eval(right_value + node.value + node.right_child.value)
		return node.value


	def print_tree(self, node=None, level=0, prefix="Root: "):
		if node is None:
			node = self.root
		print(" " * (level * 4) + prefix + str(node.value))
		if node.left_child:
			self.print_tree(node.left_child, level + 1, "L--- ")
		if node.right_child:
			self.print_tree(node.right_child, level + 1, "R--- ")

expression = ['(', '3', '+', '(', '4', '*', '5' ,')',')']
binary_tree = BinaryTree(None)
binary_tree.tree_generation(expression)
binary_tree.print_tree()
binary_tree.tree_computation(binary_tree.root)
binary_tree.print_tree()