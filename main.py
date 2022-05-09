import os
import sys
import ply.yacc as yacc
import ply.lex as lex


# List of token names
tokens = (
	'NUMBER',
	'NAME',
)


# literals
literals = [
	'+',
	'-',
	'*',
	'/',
	'(',
	')',
	'=',
]


t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


t_ignore = " \t"


# Define a rule for errors
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
	
# Define a rule for newlines
def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	
	
# Define a rule for numbers
def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t


# Parsing rules
precedence = (
	('left', '+', '-'),
	('left', '*', '/'),
	('right', 'UMINUS'),
)


# dictionary of names
names = {}


def p_statement_assign(p):
	'statement : NAME "=" expression'
	names[p[1]] = p[3]
	
	
def p_statement_expr(p):
	'statement : expression'
	print(p[1])
	
	
def p_expression_binop(p):
	'''expression : expression '+' expression
                  | expression '-' expression
				  | expression '*' expression
				  | expression '/' expression'''
    
	if p[2] == '+':
		p[0] = p[1] + p[3]
	elif p[2] == '-':
		p[0] = p[1] - p[3]
		
	elif p[2] == '*':
		p[0] = p[1] * p[3]
		
	elif p[2] == '/':
		p[0] = p[1] / p[3]
		
		
def p_expression_uminus(p):
	"expression : '-' expression %prec UMINUS"
	p[0] = -p[2]
	
	
def p_expression_group(p):
	"expression : '(' expression ')'"
	p[0] = p[2]
	
	
def p_expression_number(p):
	"expression : NUMBER"
	p[0] = p[1]
	
	
def p_expression_name(p):
	"expression : NAME"
	try:
		p[0] = names[p[1]]
	except LookupError:
		print("Undefined name '%s'" % p[1])
		p[0] = 0
		
		
def p_error(p):
	if p:
		print("Syntax error at '%s'" % p.value)
	else:
		print("Syntax error at EOF")
		
		
# Build the parser
parser = yacc.yacc()


# create function to run the program with a file as input
def run_file(file):
	# check the file extension if it isn't .calc it will print an error
	if os.path.splitext(file)[1] != '.calc':
		print('File must be a .calc file')
		return
	
	# open the file and read it
	with open(file, 'r') as f:
		lines = f.readlines()
	for line in lines:
		parser.parse(line)
		
		
# create function to run the program with a string as input
def run_string(string):
	parser.parse(string)
	
	
def main():
	lex.lex()
	# check if there is a file as input
	if len(sys.argv) > 1:
		run_file(sys.argv[1])
	else:
		while True:
			try:
				s = input('calc > ')
			except EOFError:
				break
				
			if not s:
				continue
				
			run_string(s)
			
			
if __name__ == '__main__':
	main()
