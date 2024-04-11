from pprint import pprint

def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

def fatal_error(message):
    print("Fatal error:", message)
    exit()

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
            if c == "\n":
                incomment = False
            continue
        if inblockcomment:
            if c == "*" and text[i+1] == "/":
                inblockcomment = False
            continue
        if instring:
            if c == '"':
                words.append(("string", text[word_start:i+1]))
                instring = False
            continue
        if inchar:
            if c == "'":
                words.append(("char", text[word_start:i+1]))
                inchar = False
            continue
        if inname:
            if not c.isalnum() and not c == "_":
                words.append(("name", text[word_start:i]))
                inname = False
            else:
                continue
        if c == "/":
            if text[i+1] == "/":
                incomment = True
                continue
            if text[i+1] == "*":
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
        if c.isalnum() or c == "_":
            inname = True
            word_start = i
            continue
        if c.isspace():
            continue
        words.append(("punct", c))

    for i, (type, value) in enumerate(words):
        if type == "name":
            try:
                int(value)
                words[i] = ("number", value)
            except ValueError:
                pass

    return words

def to_asts(words, level=0):
    asts = []

    i = 0
    while i < len(words):
        type, value = words[i]
        if type == "punct" and value == "(":
            ast = []
            i += 1
            while i < len(words) and words[i][1] != ")":
                if words[i][1] == "(":
                    tmp, a = to_asts(words[i:], level+1)
                    ast.append(tmp)
                    i += a - 1
                else:
                    ast.append(words[i])
                i += 1
            if i == len(words):
                fatal_error("Unmatched (")
            asts.append(ast)
        elif type == "punct" and value == ")":
            if level > 0:
                return (asts[0], i)
            fatal_error("Unmatched )")
        else:
            asts.append(words[i])
        i += 1
    
    return asts

def print_asts(asts, level=0):
    if len(asts) == 0:
        print("  " * level, "()")
    for ast in asts:
        if isinstance(ast, list):
            print_asts(ast, level+1)
        else:
            print("  " * level, ast)

text = read_file("test.cdy")
if text is None:
    fatal_error("File not found")
    
words = lex(text)
asts = to_asts(words)
print_asts(asts)
