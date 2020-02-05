from spearelexer import Lexer

class Parser:
    def __init__(self, source):
        self._lexer = Lexer(source)
    
    def _syntax_error(self, expected, actual):
        raise Exception("Syntax Error at line %d: Expected %s; Received %s" % (self._lexer.get_line_number(), expected, actual)) 
    
    def _expect(self, expected_list):
        nxtok = self._lexer.get_token()

        if nxtok.type in expected_list:
            return nxtok.content
        
        self._syntax_error(expected_list, nxtok.type)
    
    def parse(self):
        pass
