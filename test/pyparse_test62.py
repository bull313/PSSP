from pyinputbuffer import InputBuffer
from pytoken import Token

class Lexer:
    SINGLE_LINE_COMMENT_CHAR = '#'
    STRING_CHARS = { '"', '\'' }

    SINGLE_LEXICON_TOKEN_TYPES = {
        '(' : "LPAREN",
        ')' : "RPAREN",
        '#' : "POUND",
        ',' : "COMMA",
        '\n': "NEWLINE",
        ';' : "SEMICOLON",
        '{' : "LBRACE",
        '}' : "RBRACE",
        '[' : "LBRACKET",
        ']' : "RBRACKET",
        "~" : "TILDE"
    }

    KEYWORD_TYPES = {
        "True" : "TRUE",
        "False" : "FALSE",
        "None" : "NONE",
        "import" : "IMPORT",
        "from" : "FROM",
        "as" : "AS",
        "if" : "IF",
        "elif" : "ELIF",
        "else" : "ELSE",
        "class" : "CLASS",
        "def" : "DEF",
        "async" : "ASYNC",
        "del" : "DEL",
        "pass" : "PASS",
        "break" : "BREAK",
        "continue" : "CONTINUE",
        "return" : "RETURN",
        "raise" : "RAISE",
        "global" : "GLOBAL",
        "nonlocal" : "NONLOCAL",
        "assert" : "ASSERT",
        "while" : "WHILE",
        "for" : "FOR",
        "in" : "IN",
        "try" : "TRY",
        "except" : "EXCEPT",
        "finally" : "FINALLY",
        "with" : "WITH",
        "lambda" : "LAMBDA",
        "or" : "OR",
        "and" : "AND",
        "not" : "NOT",
        "is" : "IS",
        "await" : "AWAIT",
        "yield" : "YIELD"
    }

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
            while next_char is not None and next_char in { ' ', '\t' } or next_char == Lexer.SINGLE_LINE_COMMENT_CHAR:
                if next_char == Lexer.SINGLE_LINE_COMMENT_CHAR:
                    while next_char != '\n' and next_char is not None:
                        next_char = self._input_buffer.get_char()
                elif next_char == '\t':
                    token.indent += 1
                    next_char = self._input_buffer.get_char()
                else:
                    while next_char is not None and next_char == ' ':
                        space_count = 0
                        
                        while next_char == ' ' and space_count < 4:
                            space_count += 1
                            next_char = self._input_buffer.get_char()
                        
                        if space_count == 4:
                            token.indent += 1

            if next_char is None:
                token.type = "EOF"
            elif next_char in Lexer.STRING_CHARS:
                quote_type = next_char
                quote_count = 1
                next_char = self._input_buffer.get_char()

                while next_char == quote_type:
                    quote_count += 1
                    next_char = self._input_buffer.get_char()
                
                if quote_count == 1:
                    escaped = False
                    while next_char not in { quote_type, '\n', None } or escaped:
                        if escaped: escaped = False
                        if next_char == '\\': escaped = True
                        
                        token.content += next_char
                        next_char = self._input_buffer.get_char()
                    
                    if next_char == quote_type:
                        token.type = "STRING"

                elif quote_count == 2:
                    self._input_buffer.put_char(next_char)
                    token.type = "STRING"

                else:
                    quote_count = 0

                    while quote_count < 3 and next_char is not None:
                        token.content += next_char

                        if next_char == '\n':
                            self._line_number += 1

                        next_char = self._input_buffer.get_char()

                        if next_char == quote_type:
                            quote_count += 1
                        else:
                            quote_count = 0
                    
                    token.type = "STRING"

            elif next_char in Lexer.SINGLE_LEXICON_TOKEN_TYPES.keys():
                if next_char == '\n':
                    self._line_number += 1

                token.content = next_char
                token.type = Lexer.SINGLE_LEXICON_TOKEN_TYPES[next_char]
            elif next_char.isalpha() or next_char in { '_', '$' }:
                if next_char in { 'r', 'f' }:
                    prev_char = next_char
                    next_char = self._input_buffer.get_char()

                    if next_char in Lexer.STRING_CHARS:
                        quote_type = next_char
                        next_char = self._input_buffer.get_char()
                        escaped = False
                        
                        while next_char not in { quote_type, '\n', None } or escaped:
                            if escaped: escaped = False
                            if next_char == '\\': escaped = True
                            
                            token.content += next_char
                            next_char = self._input_buffer.get_char()
                        
                        if next_char == quote_type:
                            token.type = "STRING"
                    else:
                        self._input_buffer.put_char(next_char)
                        next_char = prev_char
                
                if token.type == "UNKNOWN":
                    while next_char is not None and ( next_char.isalnum() or next_char.isnumeric() or next_char in { '_', '$' } ):
                        token.content += next_char
                        next_char = self._input_buffer.get_char()
                    
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)

                    if token.content in Lexer.KEYWORD_TYPES.keys():
                        token.type = Lexer.KEYWORD_TYPES[token.content]
                    else:
                        token.type = "NAME"

            elif next_char.isnumeric():
                while next_char is not None and next_char.isnumeric():
                    token.content += next_char
                    next_char = self._input_buffer.get_char()
                
                if next_char == '.':
                    token.content += next_char
                    next_char = self._input_buffer.get_char()

                    while next_char.isnumeric():
                        token.content += next_char
                        next_char = self._input_buffer.get_char()

                    self._input_buffer.put_char(next_char)
                elif next_char == 'j':
                    token.content += next_char
                else:
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)
                        
                token.type = "NUMBER"
            elif next_char in { '+', '-', '*', '/', '%', '>', '<', '=', '!', '@', '&', '|', '^', ':' }:
                token.content = next_char
                next_char = self._input_buffer.get_char()

                if next_char == token.content and next_char in { '*', '/', '=', '>', '<' }:
                    token.content += next_char

                    operator = next_char
                    next_char = self._input_buffer.get_char()
                    assignment_operator = next_char == '='

                    if assignment_operator:
                        token.content += next_char

                        if operator == '*': token.type = "POWER_EQUALS"
                        elif operator == '/': token.type = "FLOOR_DIVIDE_EQUALS"
                        elif operator == '>': token.type = "SHIFT_RIGHT_EQUALS"
                        elif operator == '<': token.type = "SHIFT_LEFT_EQUALS"
                    else:
                        self._input_buffer.put_char(next_char)

                        if operator == '*': token.type = "POWER"
                        elif operator == '/': token.type = "FLOOR_DIVISION"
                        elif operator == '=': token.type = "DOUBLE_EQUALS"
                        elif operator == '>': token.type = "SHIFT_RIGHT"
                        elif operator == '<': token.type = "SHIFT_LEFT"

                elif next_char == '=':
                    if token.content == "+": token.type = "PLUS_EQUALS"
                    elif token.content == "-": token.type = "MINUS_EQUALS"
                    elif token.content == "*": token.type = "TIMES_EQUALS"
                    elif token.content == "/": token.type = "DIVIDE_EQUALS"
                    elif token.content == "%": token.type = "MODULUS_EQUALS"
                    elif token.content == "!": token.type = "NOT_EQUALS"
                    elif token.content == ">": token.type = "GEQ"
                    elif token.content == "<": token.type = "LEQ"
                    elif token.content == "@": token.type = "AT_EQUALS"
                    elif token.content == "&": token.type = "AND_EQUALS"
                    elif token.content == "|": token.type = "OR_EQUALS"
                    elif token.content == "^": token.type = "XOR_EQUALS"
                    elif token.content == ":": token.type = "WALRUS"

                    token.content += next_char
                elif next_char == '>':
                    if token.content == "-": token.type = "ARROW"
                else:
                    self._input_buffer.put_char(next_char)

                    if token.content == "+": token.type = "PLUS"
                    elif token.content == "-": token.type = "MINUS"
                    elif token.content == "*": token.type = "ASTERISK"
                    elif token.content == "/": token.type = "SLASH"
                    elif token.content == "%": token.type = "PERCENT"
                    elif token.content == ">": token.type = "GREATER_THAN"
                    elif token.content == "<": token.type = "LESS_THAN"
                    elif token.content == "=": token.type = "EQUAL"
                    elif token.content == "@": token.type = "AT"
                    elif token.content == "&": token.type = "AMPERSAND"
                    elif token.content == "|": token.type = "PIPE"
                    elif token.content == "^": token.type = "CARROT"
                    elif token.content == ":": token.type = "COLON"
            elif next_char == '.':
                token.content = next_char
                next_char = self._input_buffer.get_char()
                next_next_char = self._input_buffer.get_char()

                if next_char == '.' and next_next_char == '.':
                    token.content += next_char
                    token.content += next_next_char
                    token.type = "ELLIPSIS"
                elif next_char.isnumeric():
                    token.content = "." + next_char

                    if next_next_char.isnumeric():
                        token.content += next_next_char
                        next_char = self._input_buffer.get_char()

                        while next_char is not None and next_char.isnumeric():
                            token.type += next_char
                            next_char += self._input_buffer()
                        
                        if next_char is not None:
                            self._input_buffer.put_char(next_char)
                    
                    token.type = "NUMBER"
                        
                else:
                    if next_next_char is not None:
                        self._input_buffer.put_char(next_next_char)
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)

                    token.type = "DOT"
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