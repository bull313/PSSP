from speareinputbuffer import InputBuffer
from spearetoken import Token

class Lexer:
    def __init__(self, program_text):
        self._input_buffer = InputBuffer(program_text)
        self._token_buffer = list()
        self._line_number = 1
    
    def get_token(self):
        if len(self._token_buffer) > 0:
            next_token = self._token_buffer.pop()
            return next_token
        
        next_char = self._input_buffer.get_char()
        token = Token()

        if next_char is None:
            token.type = "EOF"
        else:
            while next_char is not None and next_char in { ' ', '\t', '\n' }:
                if next_char == '\n':
                    self._line_number += 1
                
                next_char = self._input_buffer.get_char()

            if next_char is None:
                token.type = "EOF"
            else:
                token.content = next_char
                token.type = "UNKNOWN"
            
        return token

    def put_token(self, token):
        self._token_buffer.append(token)

    def peek_token(self):
        peeked_token = self.get_token()
        self.put_token(peeked_token)
        return peeked_token
    
    def get_line_number(self):
        return self._line_number