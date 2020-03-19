"""
Imports
"""
from pyinputbuffer import InputBuffer
from pytoken import Token

class Lexer:
    """
    Constants
    """

    SINGLE_LINE_COMMENT_CHAR = '#'
    STRING_CHARS = { '"', '\'' }
    MULTI_LINE_STRING_QUOTE_LENGTH = 3
    ESCAPE_CHAR = '\\'
    WHITESPACE_CHARS = { ' ', '\t' }
    NONALNUM_ID_CHARS = { '_', '$' }
    SPECIAL_STRING_CHARS = { 'r', 'f' }
    OPERATOR_CHARS = { '+', '-', '*', '/', '%', '>', '<', '=', '!', '@', '&', '|', '^', ':' }

    SINGLE_LEXICON_TOKEN_TYPES = {
        '('         :   "LPAREN",
        ')'         :   "RPAREN",
        '#'         :   "POUND",
        ','         :   "COMMA",
        '\n'        :   "NEWLINE",
        ';'         :   "SEMICOLON",
        '{'         :   "LBRACE",
        '}'         :   "RBRACE",
        '['         :   "LBRACKET",
        ']'         :   "RBRACKET",
        "~"         :   "TILDE"
    }

    KEYWORD_TYPES = {
        "True"      :   "TRUE",
        "False"     :   "FALSE",
        "None"      :   "NONE",
        "import"    :   "IMPORT",
        "from"      :   "FROM",
        "as"        :   "AS",
        "if"        :   "IF",
        "elif"      :   "ELIF",
        "else"      :   "ELSE",
        "class"     :   "CLASS",
        "def"       :   "DEF",
        "async"     :   "ASYNC",
        "del"       :   "DEL",
        "pass"      :   "PASS",
        "break"     :   "BREAK",
        "continue"  :   "CONTINUE",
        "return"    :   "RETURN",
        "raise"     :   "RAISE",
        "global"    :   "GLOBAL",
        "nonlocal"  :   "NONLOCAL",
        "assert"    :   "ASSERT",
        "while"     :   "WHILE",
        "for"       :   "FOR",
        "in"        :   "IN",
        "try"       :   "TRY",
        "except"    :   "EXCEPT",
        "finally"   :   "FINALLY",
        "with"      :   "WITH",
        "lambda"    :   "LAMBDA",
        "or"        :   "OR",
        "and"       :   "AND",
        "not"       :   "NOT",
        "is"        :   "IS",
        "await"     :   "AWAIT",
        "yield"     :   "YIELD"
    }

    OPERATORS = {
        "**==" :    "POWER_EQUALS",
        "//==" :    "FLOOR_DIVIDE_EQUALS",
        ">>==" :    "SHIFT_RIGHT_EQUALS",
        "<<==" :    "SHIFT_LEFT_EQUALS",

        "**"   :   "POWER",
        "//"   :   "FLOOR_DIVISION",
        "=="   :   "DOUBLE_EQUALS",
        ">>"   :   "SHIFT_RIGHT",
        "<<"   :   "SHIFT_LEFT",

        "**="  :    "POWER_EQUALS",
        "//="  :    "FLOOR_DIVIDE_EQUALS",
        ">>="  :    "SHIFT_RIGHT_EQUALS",
        "<<="  :    "SHIFT_LEFT_EQUALS",

        "+="   :    "PLUS_EQUALS",
        "-="   :    "MINUS_EQUALS",
        "*="   :    "TIMES_EQUALS",
        "/="   :    "DIVIDE_EQUALS",
        "%="   :    "MODULUS_EQUALS",
        "!="   :    "NOT_EQUALS",
        ">="   :    "GEQ",
        "<="   :    "LEQ",
        "@="   :    "AT_EQUALS",
        "&="   :    "AND_EQUALS",
        "|="   :    "OR_EQUALS",
        "^="   :    "XOR_EQUALS",
        ":="   :    "WALRUS",

        "->"   :    "ARROW",

        "+"    :    "PLUS",
        "-"    :    "MINUS",
        "*"    :    "ASTERISK",
        "/"    :    "SLASH",
        "%"    :    "PERCENT",
        ">"    :    "GREATER_THAN",
        "<"    :    "LESS_THAN",
        "="    :    "EQUAL",
        "@"    :    "AT",
        "&"    :    "AMPERSAND",
        "|"    :    "PIPE",
        "^"    :    "CARROT",
        ":"    :    "COLON"
    }

    MAX_OPERATOR_SIZE = 4
    NUM_TABS_IN_SPACE = 4

    """
    Constructor:
        Create an Input Buffer with the given program text
        Create a token buffer for more efficient token access (LIFO)
        Create a line number tracker initialized to line #1
    """
    def __init__(self, program_text):
        self._input_buffer = InputBuffer(program_text)
        self._token_buffer = list()
        self._line_number = 1
    
    """
    Parse a single-line string and return the content
    """
    def _get_single_line_string(self, next_char, quote_type):
        token_content = ""

        while next_char not in { quote_type, '\n', None }:

            if next_char == Lexer.ESCAPE_CHAR:
                """
                Ignore escaped character
                """
                token_content += next_char
                next_char = self._input_buffer.get_char()
                    
            token_content += next_char
            next_char = self._input_buffer.get_char()

        return ( token_content, next_char )
    
    """
    Get the next token in the program text
    """
    def get_token(self):
        """
        Return a token from the buffer if there is one
        """
        buffer_not_empty = len(self._token_buffer) > 0
        token = self._token_buffer.pop() if buffer_not_empty else Token()

        if not buffer_not_empty:
            next_char = self._input_buffer.get_char()

            """
            Remove whitespace and comments, but count the number of tabs to track indent level
            """
            while ( next_char in Lexer.WHITESPACE_CHARS ) or ( next_char == Lexer.SINGLE_LINE_COMMENT_CHAR ):

                if next_char == Lexer.SINGLE_LINE_COMMENT_CHAR:
                    """
                    Ignore single-line comment
                    """
                    while next_char != '\n' and next_char is not None:
                        next_char = self._input_buffer.get_char()
                
                else:
                    """
                    Ignore spaces and tabs, but increment indent level for each tab or sequences of 4 consecutive spaces 
                    """
                    consecutive_space_count = 0
                    while next_char in Lexer.WHITESPACE_CHARS:

                        if next_char == ' ':
                            consecutive_space_count += 1
                        else:
                            token.indent += 1
                            consecutive_space_count = 0
                        
                        if consecutive_space_count == Lexer.NUM_TABS_IN_SPACE:
                            token.indent += 1
                            consecutive_space_count = 0
                        
                        next_char = self._input_buffer.get_char()

            if next_char is None:
                """
                Return EOF if there's nothing left in the input buffer
                """
                token.type = "EOF"
            
            elif next_char in Lexer.STRING_CHARS:
                """
                Parse some type of string (single, multi-line)
                """
                EMPTY_MULTILINE_QUOTE_COUNT = Lexer.MULTI_LINE_STRING_QUOTE_LENGTH * 2
                
                quote_type = next_char
                quote_count = 1
                next_char = self._input_buffer.get_char()

                """
                Count number of quotes to determine single or multi-line
                """
                while next_char == quote_type and quote_count < EMPTY_MULTILINE_QUOTE_COUNT:
                    quote_count += 1
                    next_char = self._input_buffer.get_char()
                
                if quote_count == 1:
                    """
                    Singline-line string: fill in content until closing quote symbol is reached (ignore escaped symbols)
                    """
                    token.content, last_char = self._get_single_line_string(next_char, quote_type)
                    
                    if last_char == quote_type:
                        token.type = "STRING"

                elif quote_count == 2 or quote_count == EMPTY_MULTILINE_QUOTE_COUNT:
                    """
                    Empty string (single or multi): return as is
                    """
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)

                    token.type = "STRING"

                else:
                    """
                    Multi-line string: fill in content until we see the correct number of close quotes
                    """
                    quote_count = 0

                    while quote_count < Lexer.MULTI_LINE_STRING_QUOTE_LENGTH and next_char is not None:
                        token.content += next_char

                        if next_char == '\n':
                            """
                            Keep track of line number increments
                            """
                            self._line_number += 1

                        next_char = self._input_buffer.get_char()

                        """
                        Keep track of consecutive quotes to check for closing
                        """
                        if next_char == quote_type:
                            quote_count += 1
                        else:
                            quote_count = 0
                    
                    if next_char is not None:
                        token.type = "STRING"

            elif next_char in Lexer.SINGLE_LEXICON_TOKEN_TYPES.keys():
                """
                Parse any singular lexicons that cannot be extended to a longer lexicon using the table
                """
                if next_char == '\n':
                    self._line_number += 1

                token.content = next_char
                token.type = Lexer.SINGLE_LEXICON_TOKEN_TYPES[next_char]

            elif next_char.isalpha() or next_char in Lexer.NONALNUM_ID_CHARS:
                """
                Parse any of the following:
                    * Raw string
                    * Format string
                    * Keyword
                    * Identifier
                """

                if next_char in Lexer.SPECIAL_STRING_CHARS:
                    prev_char = next_char
                    next_char = self._input_buffer.get_char()

                    if next_char in Lexer.STRING_CHARS:
                        """
                        Parse either raw string or format string
                        """
                        quote_type = next_char
                        next_char = self._input_buffer.get_char()
                        
                        token.content, last_char = self._get_single_line_string(next_char, quote_type)
                        
                        if last_char == quote_type:
                            token.type = "STRING"
                    else:
                        """
                        r or f is part of identifier, so put back the previous character
                        """
                        self._input_buffer.put_char(next_char)
                        next_char = prev_char
                
                if token.type != "STRING":
                    """
                    Parse current token as an identifier
                    """
                    while next_char is not None and ( next_char.isalnum() or next_char in Lexer.NONALNUM_ID_CHARS ):
                        token.content += next_char
                        next_char = self._input_buffer.get_char()
                    
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)

                    if token.content in Lexer.KEYWORD_TYPES.keys():
                        """
                        Identifier is a keyword that can be found from the table
                        """
                        token.type = Lexer.KEYWORD_TYPES[token.content]
                    else:
                        """
                        Identifier is an arbitrary name
                        """
                        token.type = "NAME"

            elif next_char.isnumeric():
                """
                Parse some type of number (integer, decimal, imaginary)
                """
                while next_char is not None and next_char.isnumeric():
                    token.content += next_char
                    next_char = self._input_buffer.get_char()
                
                if next_char == '.':
                    """
                    Number has a decimal point
                    """
                    token.content += next_char
                    next_char = self._input_buffer.get_char()

                    """
                    Parse numbers after decimal point
                    """
                    while next_char.isnumeric():
                        token.content += next_char
                        next_char = self._input_buffer.get_char()

                    self._input_buffer.put_char(next_char)

                elif next_char == 'j':
                    """
                    Number ends in 'j' and is therefore imaginary
                    """
                    token.content += next_char

                else:
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)
                        
                token.type = "NUMBER"

            elif next_char in Lexer.OPERATOR_CHARS:
                token.content = next_char

                for _ in range(1, Lexer.MAX_OPERATOR_SIZE):
                    next_char = self._input_buffer.get_char()

                    if next_char is None:
                        break

                    token.content += next_char

                while token.content not in Lexer.OPERATORS:
                    self._input_buffer.put_char(token.content[-1])
                    token.content = token.content[:-1]
                
                token.type = Lexer.OPERATORS[token.content]
            
            elif next_char == '.':
                """
                Parse dot, ellipsis, or decimal beginning with decimal point (.)
                """
                token.content = next_char
                next_char = self._input_buffer.get_char()
                next_next_char = self._input_buffer.get_char()

                if next_char == '.' and next_next_char == '.':
                    """
                    Next 2 characters are dots, therefore we have an ellipsis
                    """
                    token.content += next_char
                    token.content += next_next_char
                    token.type = "ELLIPSIS"

                elif next_char.isnumeric():
                    """
                    No ellipsis: check for decimal number
                    """
                    token.content = "." + next_char

                    if next_next_char.isnumeric():
                        """
                        Parse decimal number
                        """
                        token.content += next_next_char
                        next_char = self._input_buffer.get_char()

                        while next_char is not None and next_char.isnumeric():
                            token.type += next_char
                            next_char += self._input_buffer()
                        
                        if next_char is not None:
                            self._input_buffer.put_char(next_char)
                    
                    token.type = "NUMBER"
                        
                else:
                    """
                    Parse normal dot
                    """
                    if next_next_char is not None:
                        self._input_buffer.put_char(next_next_char)
                    if next_char is not None:
                        self._input_buffer.put_char(next_char)

                    token.type = "DOT"
            
            else:
                """
                If we get here, token is not recognizable
                """
                token.type = "UNKNOWN"

        """
        Return constructed token object
        """
        return token

    """
    Return a token to the token buffer
    """
    def put_token(self, token):
        self._token_buffer.append(token)

    """
    Return a reference to the next token without removing it from the buffer
        (This is a combination of get and put)
    """
    def peek_token(self):
        peeked_token = self.get_token()
        self.put_token(peeked_token)
        return peeked_token
    
    """
    Getter for current line number
    """
    def get_line_number(self):
        return self._line_number
