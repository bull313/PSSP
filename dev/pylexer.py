from pyinputbuffer import InputBuffer

class Lexer:
    SINGLE_LINE_COMMENT_CHAR = '#'
    STRING_CHARS = { '"', '\'' }

    SINGLE_LEXICON_TOKEN_TYPES = {
        '(' : "LPAREN",
        ')' : "RPAREN",
        '#' : "POUND",
        ',' : "COMMA",
        '\n': "NEWLINE",
        '\t': "TAB",
        ';' : "SEMICOLON",
        '{' : "LBRACE",
        '}' : "RBRACE",
        '[' : "LBRACKET",
        ']' : "RBRACKET"
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
    
    def get_token(self):
        if len(self._token_buffer) > 0:
            next_token = self._token_buffer.pop()
            return next_token
        
        next_char = self._input_buffer.get_char()
        token_str = ""
        token_type = "UNKNOWN"

        if next_char is None:
            token_type = "EOF"
        else:
            while next_char is not None and next_char == ' ' or next_char == Lexer.SINGLE_LINE_COMMENT_CHAR or next_char in Lexer.STRING_CHARS:
                if next_char == Lexer.SINGLE_LINE_COMMENT_CHAR:
                    while next_char != '\n' and next_char is not None:
                        next_char = self._input_buffer.get_char()
                    self._input_buffer.put_char(next_char)

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
                            
                            token_str += next_char
                            next_char = self._input_buffer.get_char()
                        
                        if next_char == quote_type:
                            token_type = "STRING"
                            return ( token_str, token_type )

                    elif quote_count == 2:
                        self._input_buffer.put_char(next_char)
                        token_str = ""
                        token_type = "STRING"
                        return ( token_str, token_type )
                    else:
                        quote_count = 0

                        while quote_count < 3 and next_char is not None:
                            token_str += next_char
                            next_char = self._input_buffer.get_char()

                            if next_char == quote_type:
                                quote_count += 1
                            else:
                                quote_count = 0
                        
                        token_type = "STRING"
                        return ( token_str, token_type )
                else:
                    while next_char is not None and next_char == ' ':
                        next_char = self._input_buffer.get_char()

            if next_char is None:
                token_str = ""
                token_type = "EOF"
                return ( token_str, token_type )
            elif next_char in Lexer.SINGLE_LEXICON_TOKEN_TYPES.keys():
                token_str = next_char
                token_type = Lexer.SINGLE_LEXICON_TOKEN_TYPES[next_char]
            elif next_char.isalpha() or next_char in { '_', '$' }:
                while next_char is not None and ( next_char.isalnum() or next_char.isnumeric() or next_char in { '_', '$' } ):
                    token_str += next_char
                    next_char = self._input_buffer.get_char()
                
                self._input_buffer.put_char(next_char)

                if token_str in Lexer.KEYWORD_TYPES.keys():
                    token_type = Lexer.KEYWORD_TYPES[token_str]
                else:
                    token_type = "NAME"
            elif next_char.isnumeric():
                while next_char is not None and next_char.isnumeric():
                    token_str += next_char
                    next_char = self._input_buffer.get_char()
                
                if next_char == '.':
                    token_str += next_char
                    next_char = self._input_buffer.get_char()

                    while next_char.isnumeric():
                        token_str += next_char
                        next_char = self._input_buffer.get_char()

                    self._input_buffer.put_char(next_char)

                    token_type = "DECIMAL"
                elif next_char == 'j':
                    token_type = "IMAGINARY"
                else:
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)
                        
                    token_type = "NUMBER"
            elif next_char in [ '+', '-', '*', '/', '%', '>', '<', '=', '!', '@', '&', '|', '^', ':' ]:
                token_str = next_char
                next_char = self._input_buffer.get_char()

                if next_char == token_str:
                    token_str += next_char

                    operator = next_char
                    next_char = self._input_buffer.get_char()
                    assignment_operator = next_char == '='

                    if assignment_operator:
                        token_str += next_char

                        if operator == '*': token_type = "POWER_EQUALS"
                        elif operator == '/': token_type = "FLOOR_DIVIDE_EQUALS"
                        elif operator == '>': token_type = "SHIFT_RIGHT_EQUALS"
                        elif operator == '<': token_type = "SHIFT_LEFT_EQUALS"
                    else:
                        self._input_buffer.put_char(next_char)

                        if operator == '*': token_type = "POWER"
                        elif operator == '/': token_type = "FLOOR_DIVISION"
                        elif operator == '=': token_type = "DOUBLE_EQUALS"
                        elif operator == '>': token_type = "SHIFT_RIGHT"
                        elif operator == '<': token_type = "SHIFT_LEFT"

                elif next_char == '=':
                    if token_str == "+": token_type = "PLUS_EQUALS"
                    elif token_str == "-": token_type = "MINUS_EQUALS"
                    elif token_str == "*": token_type = "TIMES_EQUALS"
                    elif token_str == "/": token_type = "DIVIDE_EQUALS"
                    elif token_str == "%": token_type = "MODULUS_EQUALS"
                    elif token_str == "!": token_type = "NOT_EQUALS"
                    elif token_str == ">": token_type = "GEQ"
                    elif token_str == "<": token_type = "LEQ"
                    elif token_str == "@": token_type = "AT_EQUALS"
                    elif token_str == "&": token_type = "AND_EQUALS"
                    elif token_str == "|": token_type = "OR_EQUALS"
                    elif token_str == "^": token_type = "XOR_EQUALS"
                    elif token_str == ":": token_type = "COLON_EQUALS"

                    token_str += next_char
                elif next_char == '>':
                    if token_str == "-": token_type = "ARROW"
                else:
                    self._input_buffer.put_char(next_char)

                    if token_str == "+": token_type = "PLUS"
                    elif token_str == "-": token_type = "MINUS"
                    elif token_str == "*": token_type = "ASTERISK"
                    elif token_str == "/": token_type = "SLASH"
                    elif token_str == "%": token_type = "PERCENT"
                    elif token_str == ">": token_type = "GREATER_THAN"
                    elif token_str == "<": token_type = "LESS_THAN"
                    elif token_str == "=": token_type = "EQUAL"
                    elif token_str == "@": token_type = "AT"
                    elif token_str == "&": token_type = "AMPERSAND"
                    elif token_str == "|": token_type = "PIPE"
                    elif token_str == "^": token_type = "CARROT"
                    elif token_str == ":": token_type = "COLON"
            elif next_char == '.':
                token_str = next_char
                next_char = self._input_buffer.get_char()
                next_next_char = self._input_buffer.get_char()

                if next_char == '.' and next_next_char == '.':
                    token_str += next_char
                    token_str += next_next_char
                    token_type = "ELLIPSIS"
                else:
                    if next_next_char is not None:
                        self._input_buffer.put_char(next_next_char)
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)

                    token_type = "DOT"
            else:
                token_str = next_char
                token_type = "UNKNOWN"
            
        return ( token_str, token_type )

    def put_token(self, token):
        self._token_buffer.append(token)

    def peek_token(self):
        peeked_token = self.get_token()
        self.put_token(peeked_token)
        return peeked_token