import re

a = re.compile(r'if')
b = re.compile(r'else if')
c = re.compile(r'else')
relop = re.compile(r'<|<=|>|>=|!=|==')
assignment = re.compile(r'=')
lparen = re.compile(r'[(]')
rparen = re.compile(r'[)]')
lcurly = re.compile(r'[{]')
rcurly = re.compile(r'[}]')
lsq = re.compile(r'[[]')
rsq = re.compile(r'[]]')
identifier = re.compile(r'\b[a-zA-Z]+[0-9]*[a-zA-Z]*')
digit = re.compile(r'[0-9]+')
num = re.compile(r'([0-9]+)([.][0-9]+)?')
end = re.compile(r'[;]')
doublequote = re.compile(r'["]')
singlequote = re.compile(r'[\']')
ws = re.compile(r'\s')
keywords =['if','else if','else','main','class','public','static','void','int','double','short','float','String','args','System.out.println','System.out.print']
string = re.compile(r'["]\w["]')
comment = re.compile(r'/')

def lex(filecontents):
	SComment = False
	MComment = False
	INString = False

	tok=""
	linenumber=1
	filecontents=list(filecontents)
	index=0
	for char in filecontents:
		if char =='\n' :
			linenumber+=1
			if SComment: SComment = False

		elif INString:
			if re.match(doublequote,char):
				INString = False
				token(tok,linenumber)
				tok = ""
			else: tok+=char

		elif MComment:
			if(char == '*' and filecontents[index+1] == '/'): MComment = False
			else: pass

		elif SComment:pass

		elif re.match(comment,char):
			if(filecontents[index+1] == '/'):SComment = True 

			elif(filecontents[index+1] == '*'):
				MComment = True

		elif re.match(doublequote,char):
			INString = True
			tok+='"'
			
		elif re.match(lparen,char):
			addToSymTable(char,'LPAREN',linenumber)
			tok=''
			
		elif re.match(rparen,char):
			addToSymTable(char,'RPAREN',linenumber)
			tok=''
			
		elif re.match(rcurly,char):
			addToSymTable(char,'RCURLY',linenumber)
			tok=''
			
		elif re.match(lcurly,char):
			addToSymTable(char,'LCURLY',linenumber)
			tok=''
			
		elif re.match(rsq,char):
			addToSymTable(char,'RSQ',linenumber)
			tok=''
			
		elif re.match(lsq,char):
			addToSymTable(char,'LSQ',linenumber)
			tok=''
			
		elif re.match(ws,char):
			token(tok,linenumber)
			tok=''
			
		elif re.match(assignment,char):
			if filecontents[index+1]=='=':
				addToSymTable('==','relop',linenumber)
				if(tok!="=="):
					token(tok.split("==")[0],linenumber)
				tok=''
				
				
			elif filecontents[index-1]=='<' or filecontents[index-1]=='>' or filecontents[index-1]=='=':
				pass 
			else:
				addToSymTable(char,'assignment',linenumber)
				if(tok!="="):
					token(tok.split("=")[0],linenumber)
				tok=''
				
		elif char == '<':
			if filecontents[index+1]=='=':
				addToSymTable('<=','relop',linenumber)
				if(tok!="<="):
					token(tok.split("<=")[0],linenumber)
				tok=''
				
			else:
				addToSymTable('<','relop',linenumber)
				if(tok!="<"):
					token(tok.split("<")[0],linenumber)
		elif char == '>':
			if filecontents[index+1]=='=':
				addToSymTable('>=','relop',linenumber)
				if(tok!=">="):
					token(tok.split(">=")[0],linenumber)
				tok=''
				
			else:
				addToSymTable('>','relop',linenumber)
				if(tok!=">"):
					token(tok.split(">")[0],linenumber)
		elif char == '!':
			if filecontents[index+1]=='=':
				addToSymTable('!=','relop',linenumber)
				if(tok!="!="):
					token(tok.split("!=")[0],linenumber)
				tok=''
						
		elif re.match(end,char):
			addToSymTable(char,'EndOfStatement',linenumber)
			if(tok!=";"):
					token(tok.split(";")[0],linenumber)
			tok=''
			
		else:
			tok += char
		index+=1		


def printf(*args):
	print(args)


def addToSymTable(tok,attr,lno):
	if(tok not in keys):
		keys.add(tok)	
		symbol_table[tok] = (attr,lno)



def token(tok,linenumber):
	if tok in keywords:
		addToSymTable(tok,"KEYWORD",linenumber)
		
	elif re.match('"',tok):
		addToSymTable(tok,"STRING",linenumber)
	elif tok=='':
		pass
	else:
		if(re.match(num,tok)):
			x = re.match(num,tok)
			if(len(x.group()) == len(tok)):
				addToSymTable(tok,"NUM",linenumber)
			else:
				addToSymTable(tok,"INVALID",linenumber)
		elif(re.match(identifier,tok)):
			addToSymTable(tok,"ID",linenumber)
		else:
			addToSymTable(tok,"INVALID",linenumber)

S = "\t\t-----TOKENS-----\n"

def run(filename = None, Code = None):
	global symbol_table 
	global keys
	global S

	symbol_table = dict()
	keys = set()

	if filename:
		data = open(filename).read()
	else: 
		data = Code
	lex(data)

	print("keys",keys)
	print("symbol_table",symbol_table)

	for entry in symbol_table:
		# print("Entry 0",symbol_table[entry][0],"Entry 1",symbol_table[entry][0])
		S+=entry+ "\t--> "+"("+str(symbol_table[entry][0]) + ", " + str(symbol_table[entry][1])+")\n"

		