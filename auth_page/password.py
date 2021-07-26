import random

""" Generate Random Password """
def generate_password(max_len=12, allow_symbols=True):
	DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
	
	L_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
	                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
	                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
	                     'z']
	  
	U_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
	                     'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
	                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
	                     'Z']
	  
	SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', 
	           '*', '(', ')', '<']

	ALL_CHARS = DIGITS + L_CHARACTERS + U_CHARACTERS
	ALL_CHARS = (ALL_CHARS + SYMBOLS) if allow_symbols else ALL_CHARS

	password = random.choice(DIGITS) + random.choice(L_CHARACTERS) + random.choice(U_CHARACTERS) 
	password = (password + random.choice(SYMBOLS)) if allow_symbols else password

	for i in range(max_len):
		password = password + random.choice(ALL_CHARS)

	password_arr = list(password[:max_len])
	random.shuffle(password_arr)
	password = ''.join(password_arr) 

	return password