from Parsing import parsing, expander, printVar, addVariable, ft_strchr, identify
from Computing import compute

def main():
	variables = []
	while 42:
		command = input("> ")
		if command == "var":
			printVar(variables)
			continue
		if (command := parsing(command)) == -1:
			print("  Invalid syntax")
			continue
		if not (command := expander(command, variables)):
			continue
		if not (command := compute(command)):
			continue
		variables = addVariable(command, variables)
		print(f" {ft_strchr(command.split('=')[0], variables)}")
	return 0

if __name__ == "__main__":
	main()