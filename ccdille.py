from pprint import pprint

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def lex(text):
    words = []
    word_start = 0
    
    instring = False
    inchar = False
    incomment = False
    inblockcomment = False
    inname = False

    for i, c in enumerate(text):
        if incomment:
            if c == '\n':
                incomment = False
            continue
        if inblockcomment:
            if c == '*' and text[i+1] == '/':
                inblockcomment = False
            continue
        if instring:
            if c == '"':
                words.append(('string', text[word_start:i+1]))
                instring = False
            continue
        if inchar:
            if c == "'":
                words.append(('char', text[word_start:i+1]))
                inchar = False
            continue
        if inname:
            if not c.isalnum() and not c == '_':
                words.append(('name', text[word_start:i]))
                inname = False
            else:
                continue
        if c == '/':
            if text[i+1] == '/':
                incomment = True
                continue
            if text[i+1] == '*':
                inblockcomment = True
                continue
        if c == '"':
            instring = True
            word_start = i
            continue
        if c == "'":
            inchar = True
            word_start = i
            continue
        if c.isalnum() or c == '_':
            inname = True
            word_start = i
            continue
        if c.isspace():
            continue
        words.append(('punct', c))

    for i, (type, value) in enumerate(words):
        if type == 'name':
            try:
                int(value)
                words[i] = ('number', value)
            except ValueError:
                pass

    return words

class AST:
    def __init__(self, type, name, parms, body):
        self.type = type
        self.name = name
        self.parms = parms
        self.body = body
    
    def __repr__(self):
        return f'{self.type} {self.name} {self.parms} {self.body}'



text = read_file('test.cdy')
if text is None:
    print('File not found')
    exit()
    
words = lex(text)
pprint(words)
