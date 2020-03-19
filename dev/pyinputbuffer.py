"""
InputBuffer:
    Contains program text
    Returns characters one at a time
    Allows for putting characters back into the buffer

    Behaves like a stack: LIFO
"""

class InputBuffer:
    """
    Constructor:
        Get the program text
    """
    def __init__(self, program_text):
        self._text = program_text
    
    """
    Remove a character from the buffer and return it
    """
    def get_char(self):
        if len(self._text) == 0:
            return None
        
        next_char = self._text[0]
        self._text = self._text[1:]

        return next_char
    
    """
    Add the given character to the end of the buffer
    """
    def put_char(self, char):
        self._text = char + self._text
