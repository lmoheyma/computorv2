from BaseAssignmentValue import BaseAssignmentValue

def parsing(input) -> int:
	if input.find('=') == -1 or \
		input.count('=') > 1:
		return -1
	input = input.strip()
	splitedInput = input.split('=')
	if splitedInput[0] == "" or splitedInput[1] == "":
		return -1
	try:
		eval(splitedInput[1])
	except Exception:
		return -1
	return input.replace(" ", "")

def ft_strchr(element, variables):
	for var in variables:
		if element == var.name:
			return var.value
	return None

def expander(input, variables) -> str:
	expandedInput = ""
	splitedInput = input.split('=')
	for element in splitedInput[1]:
		if (varValue := ft_strchr(element, variables)) and element.isalpha():
			expandedInput += varValue
		else:
			if element.isalpha():
				print(f"Variable {element} is not defined")
				return None
			else:
				expandedInput += element
	return splitedInput[0] + '=' + expandedInput

def getIndexOfVariable(var: str, variables: list) -> int:
	for i in range(len(variables)):
		if var == variables[i].name:
			return i
	return -1


def addVariable(var: str, variables: list) -> list:
	splitedVar = var.split('=')
	if ft_strchr(splitedVar[0], variables):
		if (index := getIndexOfVariable(splitedVar[0], variables)) == -1:
			print("Can't add variable")
			pass
		variables[index].value = splitedVar[1]
	else:
		variables.append(BaseAssignmentValue(var))
	return variables

def printVar(variables):
	for var in variables:
		print(f"Variable: {var.name}  |  Value: {var.value}")