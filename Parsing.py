from BaseAssignmentValue import BaseAssignmentValue
from RationalNumber import RationalNumber
from ImaginaryNumber import ImaginaryNumber
from Function import Function
from Matrix import Matrix
from Environment import Environment
import re

def identifyType(input: str, environment: Environment) -> str:
	def computeRegex(left_arg, right_arg):
		if (matches :=re.finditer(r"[+-]?(((\d+\.\d*|\d*\.\d+|\d+)[+-])?((\d+\.\d*|\d*\.\d+|\d+)i|i(\d+\.\d*|\d*\.\d+|\d+)|i)|(\d+\.\d*|\d*\.\d+|\d+)?e\^(\([+-]?|[+-]?\()((\d+\.\d*|\d*\.\d+|\d+)i|i(\d+\.\d*|\d*\.\d+|\d+)|i)\))", right_arg, re.MULTILINE)):
			results = [match.group() for match in matches]
			if len(results) > 0: return "Imaginary"
		if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\([^i]*\)$', left_arg):
			return "Function"
		if re.match(r'^\[.*\]$', right_arg):
			return "Matrix"
		try:
			eval(right_arg)
			# print(right_arg)
			return "Rational"
		except Exception:
			if right_arg == "?": 
				return "Calculate"
			return "Unknown"

	def matchRegexResult(left_arg, right_arg, environment, flag):
		if not flag:
			varType = computeRegex(left_arg, right_arg)
		else:
			temp = expander(left_arg, environment.variables)
			varType = computeRegex(temp, temp)
		match varType:
			case "Function":
				return Function(left_arg, right_arg, environment)
			case "Matrix":
				return Matrix(left_arg, right_arg, environment)
			case "Rational":
				return RationalNumber(left_arg, right_arg, environment)
			case "Imaginary":
				return ImaginaryNumber(left_arg, right_arg, environment)
			case "Calculate":
				return matchRegexResult(left_arg, right_arg, environment, flag=1)
			case _:
				print("  Syntax error")

	left_arg = input.split('=')[0].strip()
	right_arg = expander(input.split('=')[1].strip(), environment.variables)
	return matchRegexResult(left_arg, right_arg, environment, flag=0)

def preProcessing(input) -> int:
	if input.find('=') == -1 or \
		input.count('=') > 1:
		return -1
	input = input.strip()
	splitedInput = input.split('=')
	if splitedInput[0] == "" or splitedInput[1] == "":
		return -1
	return input.replace(" ", "")

def ft_strchr(element, variables):
	for var in variables:
		if element == var.name:
			return var.value
	return None

def expander(input, variables) -> str:
	expandedInput = ""
	var = ""
	i = 0
	while i < len(input):
		while i < len(input) and input[i].isalpha():
			var += input[i]
			i+=1
		if i == len(input): i-=1
		if var == 'i':
			if input[i] != 'i':
				i-=1
			var = ""
		if (varValue := ft_strchr(var, variables)) and \
			not(input[i] == 'i'):
			expandedInput += varValue
			var = ""
		else:
			expandedInput += input[i]
		i+=1
	return expandedInput

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