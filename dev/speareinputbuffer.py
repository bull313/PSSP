class InputBuffer:
    def __init__(self, program_text):
        self._text = program_text
    
    def get_char(self):
        if len(self._text) == 0:
            return None
        
        next_char = self._text[0]
        self._text = self._text[1:]

        return next_char
    
    def put_char(self, char):
        self._text = char + self._text
