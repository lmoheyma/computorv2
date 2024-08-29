def parsing(input) -> int:
	if input.find('=') == -1 or \
		input.count('=') > 1:
		return 1
	input = input.strip()
	splitedInput = input.split('=')
	if splitedInput[0] == "" or splitedInput[1] == "":
		return 1
	return 0