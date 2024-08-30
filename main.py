from Parsing import parsing, expander, printVar, addVariable, ft_strchr
from Computing import compute
def main():
	variables = []
	while 42:
		command = input("> ")
		if command == "var":
			printVar(variables)
			continue
		if (command := parsing(command)) == -1:
			print("  Invalid input")
			continue
		command = expander(command, variables)
		command = compute(command)
		variables = addVariable(command, variables)
		print(f" {ft_strchr(command.split('=')[0], variables)}")
	return 0

if __name__ == "__main__":
	main()