from src.tools import read_file, fatal_error

import src.parse as parse
import src.lexe as lexe
import src.toast as toast

from pprint import pprint

text = read_file("test.cdy")
if text is None:
    fatal_error("File not found")
    
words = lexe.lex(text)
asts = toast.to_asts(words)
toast.print_asts(asts)

print("------------------")
pprint(parse.parse(asts))
