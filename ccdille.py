from src.tools import read_file, fatal_error

import src.parse as parse
import src.lexe as lexe
import src.ast as ast

from pprint import pprint

text = read_file("test.cdy")
if text is None:
    fatal_error("File not found")
    
words = lexe.lex(text)
asts = ast.to_asts(words)
ast.print_asts(asts)
pprint(parse.parse(asts))
