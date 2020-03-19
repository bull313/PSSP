"""
Token:
    Represents an lexicon consisting of its 
        exact content, 
        type, 
        and indent (number of tabs (4 spaces) behind it)
"""
class Token:
    def __init__(self):
        self.content = ""
        self.type = "UNKNOWN"
        self.indent = 0
