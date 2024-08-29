from BaseAssignmentValue import BaseAssignmentValue
from Parsing import parsing
from Computing import compute

def main():
	variables = []
	while 42:
		command = input("> ")
		if parsing(command):
			print("  Invalid input")
			continue
		compute(command, variables)
		variables.append(BaseAssignmentValue(command))
		print(f" {variables[-1].value}")
	return 0

if __name__ == "__main__":
	main()