from src.tools import fatal_error

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
