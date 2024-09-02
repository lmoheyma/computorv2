from Parsing import preProcessing, expander, addVariable, ft_strchr, identifyType
from Computing import compute
from Environment import Environment

def main():
	environment = Environment()
	while 42:
		command = input("> ")
		if command == "var":
			environment.printVar()
			continue
		if preProcessing(command) == -1 or command == "":
			continue
		inputType = identifyType(command, environment)
		# print(type(inputType))
		if inputType:
			inputType.parsing()
		# if (command := parsing(command)) == -1:
		# 	print("  Invalid syntax")
		# 	continue
		# if not (command := expander(command, variables)):
		# 	continue
		# if not (command := compute(command)):
		# 	continue
		# variables = addVariable(command, variables)
		# print(f" {ft_strchr(command.split('=')[0], variables)}")
	return 0

if __name__ == "__main__":
	main()