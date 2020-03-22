"""
Parser:
    Contains a Lexer which holds the input text
    Parses input text using Python syntax specified in ../grammar/python_grammar.txt
"""

"""
Imports
"""
from pylexer import Lexer

class Parser:
    """
    Constants
    """
    ANNASSIGN_FIRST_SET = { "COLON" }

    ARGLIST_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "POWER", "ASTERISK"
    }
    
    ARGUMENT_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "POWER", "ASTERISK"
    }

    ASSERT_STMT_FIRST_SET = { "ASSERT" }

    ASYNC_STMT_FIRST_SET = { "ASYNC" }

    AUGASSIGN_FIRST_SET = {
        "PLUS_EQUALS",
        "MINUS_EQUALS",
        "TIMES_EQUALS",
        "AT_EQUALS",
        "DIVIDE_EQUALS",
        "PERCENT_EQUALS",
        "AND_EQUALS",
        "OR_EQUALS",
        "XOR_EQUALS",
        "SHIFT_LEFT_EQUALS",
        "SHIFT_RIGHT_EQUALS",
        "POWER_EQUALS",
        "FLOOR_DIVIDE_EQUALS"
    }

    BREAK_STMT_FIRST_SET = { "BREAK" }

    CLASSDEF_FIRST_SET = { "CLASS" }

    COMP_FOR_FIRST_SET = { "ASYNC", "FOR" }

    COMP_IF_FIRST_SET = { "IF" }

    COMP_ITER_FIRST_SET = { "ASYNC", "FOR", "IF" }

    COMP_OP_FIRST_SET = {
        "LESS_THAN", "GREATER_THAN", "DOUBLE_EQUALS",
        "GEQ", "LEQ", "NOT_EQUALS", 
        "IN", "NOT", "IS"
    }

    COMPARISON_FIRST_SET = { 
        "PLUS", "MINUS", "TILDE", 
        "AWAIT", "LPAREN", "LBRACKET", 
        "LBRACE", "NAME", "NUMBER", 
        "STRING", "ELLIPSIS", "NONE", 
        "TRUE", "FALSE"
    }

    COMPOUND_STMT_FIRST_SET = { 
        "IF", "WHILE", "FOR", 
        "TRY", "WITH", "DEF", 
        "CLASS", "AT", "ASYNC" 
    }

    CONTINUE_STMT_FIRST_SET = { "CONTINUE" }

    DECORATED_FIRST_SET = { "AT" }

    DECORATOR_FIRST_SET = { "AT" }

    DEL_STMT_FIRST_SET = { "DEL" }
    
    DICTORSETMAKER_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "POWER", "ASTERISK" 
    }

    DOTTED_NAME_FIRST_SET = { "NAME" }

    EXCEPT_CLAUSE_FIRST_SET = { "EXCEPT" } 

    EXPR_FIRST_SET = { 
        "PLUS", "MINUS", "TILDE", 
        "AWAIT", "LPAREN", "LBRACKET", 
        "LBRACE", "NAME", "NUMBER", 
        "STRING", "ELLIPSIS", "NONE", 
        "TRUE", "FALSE"
    }

    EXPR_STMT_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "ASTERISK"
    }

    FLOW_STMT_FIRST_SET = { "BREAK", "CONTINUE", "RETURN", "RAISE", "YIELD" }

    FOR_STMT_FIRST_SET = { "FOR" }

    FUNCDEF_FIRST_SET = { "DEF" }

    GLOBAL_STMT_FIRST_SET = { "GLOBAL" }

    IF_STMT_FIRST_SET = { "IF" }

    IMPORT_AS_NAME_FIRST_SET = { "NAME" }

    IMPORT_AS_NAMES_FIRST_SET = { "NAME" }

    IMPORT_FROM_FIRST_SET = { "FROM" }

    IMPORT_NAME_FIRST_SET = { "IMPORT" }

    IMPORT_STMT_FIRST_SET = { "IMPORT", "FROM" }

    LAMBDEF_FIRST_SET = { "LAMBDA" }

    LAMBDEF_NOCOND_FIRST_SET = { "LAMBDA" }

    NAMEDEXPR_TEST_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA" 
    }

    NONLOCAL_STMT_FIRST_SET = { "NONLOCAL" }

    OR_TEST_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE" 
    }

    PASS_STMT_FIRST_SET = { "PASS" }

    POWER_FIRST_SET = { 
        "AWAIT", "LPAREN", "LBRACKET", 
        "LBRACE", "NAME", "NUMBER", 
        "STRING", "ELLIPSIS", "NONE", 
        "TRUE", "FALSE" 
    }

    RAISE_STMT_FIRST_SET =  { "RAISE" }

    RETURN_STMT_FIRST_SET = { "RETURN" }

    SLICEOP_FIRST_SET = { "COLON" }

    STMT_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", "TILDE", 
        "AWAIT", "LPAREN", "LBRACKET", 
        "LBRACE", "NAME", "NUMBER", 
        "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "ASTERISK", "DEL", 
        "PASS", "BREAK", "CONTINUE", 
        "RETURN", "RAISE", "YIELD", 
        "IMPORT", "FROM", "GLOBAL", 
        "NONLOCAL", "ASSERT", "IF", 
        "WHILE", "FOR", "TRY", "WITH", 
        "DEF", "CLASS", "AT", "ASYNC" 
    }

    SIMPLE_STMT_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "ASTERISK", "DEL", 
        "PASS", "BREAK", "CONTINUE", 
        "RETURN", "RAISE", "YIELD", 
        "IMPORT", "FROM", "GLOBAL", 
        "NONLOCAL", "ASSERT" 
    }

    SMALL_STMT_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "ASTERISK", "DEL", 
        "PASS", "BREAK", "CONTINUE", 
        "RETURN", "RAISE", "YIELD", 
        "IMPORT", "FROM", "GLOBAL", 
        "NONLOCAL", "ASSERT" 
    }

    STAR_EXPR_FIRST_SET = { "ASTERISK" }

    SUBSCRIPT_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "COLON"
    }

    TEST_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA" 
    }

    TESTLIST_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA" 
    }

    TESTLIST_COMP_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", "LAMBDA" 
    }

    TESTLIST_STAR_EXPR_FIRST_SET = { 
        "NOT", "PLUS", "MINUS", 
        "TILDE", "AWAIT", "LPAREN", 
        "LBRACKET", "LBRACE", "NAME", 
        "NUMBER", "STRING", "ELLIPSIS", 
        "NONE", "TRUE", "FALSE", 
        "LAMBDA", "ASTERISK"
    }

    TFPDEF_FIRST_SET = { "NAME" }

    TRAILER_FIRST_SET = { "LPAREN", "LBRACKET", "DOT" }

    TRY_STMT_FIRST_SET = { "TRY" }

    TYPEDARGSLIST_FIRST_SET = { "NAME", "POWER", "ASTERISK" }

    VARARGSLIST_FIRST_SET = { "NAME", "ASTERISK", "POWER" }

    VFPDEF_FIRST_SET = { "NAME" }

    WHILE_STMT_FIRST_SET = { "WHILE" }

    WITH_STMT_FIRST_SET = { "WITH" }

    YIELD_ARG_FIRST_SET = { "YIELD" }

    YIELD_EXPR_FIRST_SET = { "YIELD" }

    YIELD_STMT_FIRST_SET =  { "YIELD" }


    SYNTAX_ERROR_MSG = "Syntax Error at line %d: Expected %s; Received %s"
    INDENT_LEVEL_STR = "Indent level %d"

    """
    Constructor:
        Create a Lexer instance and give it the source code to tokenize it
        Keep track of the indent level for scope
    """
    def __init__(self, source):
        self._lexer = Lexer(source)
        self._indent_level = 0
    
    """
    Send a syntax error message and terminate the parsing process
    """
    def _syntax_error(self, expected, actual):
        raise Exception(Parser.SYNTAX_ERROR_MSG % (self._lexer.get_line_number(), expected, actual)) 
    
    """
    Check if the next tokens are of the types passed in and throw a syntax error if there is a mismatch
    """
    def _expect(self, expected_list):
        
        nxtok = self._lexer.get_token()

        if nxtok.type in expected_list:
            return nxtok.content
        
        self._syntax_error(expected_list, nxtok.type)
    
    """
    Check to see the next token has 1 extra indent from the current indent level
    Increment the the indent level if so
    Throw a syntax error if not
    """
    def _expect_indent(self):

        nxtok = self._lexer.peek_token()
        expected = self._indent_level + 1

        if nxtok.indent == expected:
            self._indent_level = expected

        else:
            self._syntax_error(Parser.INDENT_LEVEL_STR % expected, Parser.INDENT_LEVEL_STR % nxtok.indent)
    
    """
    Main parsing method

    file_input: (NEWLINE | stmt)* ENDMARKER

    ENDMARKER is EOF
    """
    def parse(self):

        nxtok = self._lexer.peek_token()

        while nxtok.type != "EOF":
            
            if nxtok.type == "NEWLINE":
                self._expect("NEWLINE")

            elif nxtok.type in Parser.STMT_FIRST_SET:
                self._parse_stmt()

            else:
                self._syntax_error(Parser.STMT_FIRST_SET | { "NEWLINE" }, nxtok.type)
            
            nxtok = self._lexer.peek_token()

    """
    decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE
    """
    def _parse_decorator(self):

        self._expect("AT")
        self._parse_dotted_name()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":

            self._expect("LPAREN")

            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.ARGLIST_FIRST_SET:
                self._parse_arglist()
            
            self._expect("RPAREN")

        self._expect("NEWLINE")
    
    """
    decorators: decorator+
    """
    def _parse_decorators(self):

        self._parse_decorator()

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.DECORATOR_FIRST_SET:
            self._parse_decorators()
    
    """
    decorated: decorators (classdef | funcdef | async_funcdef)
    """
    def _parse_decorated(self):

        self._parse_decorators()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "CLASS":
            self._parse_classdef()

        elif nxtok.type == "DEF":
            self._parse_funcdef()

        else:
            self._parse_async_funcdef()
    
    """
    async_funcdef: ASYNC funcdef
    """
    def _parse_async_funcdef(self):
        self._expect("ASYNC")
        self._parse_funcdef()
    
    """
    funcdef: 'def' NAME parameters ['->' test] ':' [TYPE_COMMENT] func_body_suite
    """
    def _parse_funcdef(self):

        self._expect("DEF")
        self._expect("NAME")
        self._parse_parameters()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ARROW":
            self._expect("ARROW")
            self._parse_test()
        
        self._expect("COLON")
        
        nxtok = self._lexer.peek_token()

        if nxtok.type == "STRING":
            self._expect("STRING")

        self._parse_func_body_suite()
    
    """
    parameters: '(' [typedargslist] ')'
    """
    def _parse_parameters(self):

        self._expect("LPAREN")
        
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TYPEDARGSLIST_FIRST_SET:
            self._parse_typedargslist()

        self._expect("RPAREN")
    
    """
    typedargslist: (
        (
            tfpdef ['=' test] (',' [TYPE_COMMENT] tfpdef ['=' test])* ',' [TYPE_COMMENT] '/'
            [
                ',' [ [TYPE_COMMENT] tfpdef ['=' test]
                (',' [TYPE_COMMENT] tfpdef ['=' test])*
                (
                    TYPE_COMMENT

                    |

                    [
                        ',' [TYPE_COMMENT]
                        [
                            '*' [tfpdef] (',' [TYPE_COMMENT] tfpdef ['=' test])* ( TYPE_COMMENT | [',' [TYPE_COMMENT] [ '**' tfpdef [','] [TYPE_COMMENT] ]] )

                            |
                            
                            '**' tfpdef [','] [TYPE_COMMENT]
                        ]
                    ]
                )

                | '*' [tfpdef] (',' [TYPE_COMMENT] tfpdef ['=' test])* (TYPE_COMMENT | [',' [TYPE_COMMENT] ['**' tfpdef [','] [TYPE_COMMENT]]])

                | '**' tfpdef [','] [TYPE_COMMENT]]
            ]
        )

        |  
        
        (
            tfpdef ['=' test] (',' [TYPE_COMMENT] tfpdef ['=' test])*
            (
                TYPE_COMMENT

                |

                [
                    ',' [TYPE_COMMENT]
                    [
                        '*' [tfpdef] (',' [TYPE_COMMENT] tfpdef ['=' test])* (TYPE_COMMENT | [',' [TYPE_COMMENT] ['**' tfpdef [','] [TYPE_COMMENT]]])
                        | '**' tfpdef [','] [TYPE_COMMENT]
                    ]
                ]
            )

            | '*' [tfpdef] (',' [TYPE_COMMENT] tfpdef ['=' test])* (TYPE_COMMENT | [',' [TYPE_COMMENT] ['**' tfpdef [','] [TYPE_COMMENT]]])

            | '**' tfpdef [','] [TYPE_COMMENT]
        )
    )
    """
    def _parse_typedargslist(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TFPDEF_FIRST_SET:

            self._parse_tfpdef()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "EQUAL":
                self._expect("EQUAL")
                self._parse_test()
                nxtok = self._lexer.peek_token()
            
            if nxtok.type == "COMMA":

                self._expect("COMMA")
                nxtok = self._lexer.peek_token()

                if nxtok.type == "STRING":
                    self._expect("STRING")
                    nxtok = self._lexer.peek_token()
                
                while nxtok.type in Parser.TFPDEF_FIRST_SET:

                    self._parse_tfpdef()
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "EQUAL":
                        self._expect("EQUAL")
                        self._parse_test()
                        nxtok = self._lexer.peek_token()
                    
                    if nxtok.type == "STRING":
                        self._expect("STRING")
                        return  
                    
                    if nxtok.type != "COMMA":
                        break
                    
                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "STRING":
                        self._expect("STRING")
                        nxtok = self._lexer.peek_token()
                
                if nxtok.type == "SLASH":

                    self._expect("SLASH")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "COMMA":

                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()

                        if nxtok.type == "STRING" or nxtok.type in Parser.TFPDEF_FIRST_SET:

                            if nxtok.type == "STRING":
                                self._expect("STRING")
                                nxtok = self._lexer.peek_token()
                            
                            self._parse_tfpdef()
                            nxtok = self._lexer.peek_token()

                            if nxtok.type == "EQUAL":
                                self._expect("EQUAL")
                                self._parse_test()
                                nxtok = self._lexer.peek_token()
                            
                            if nxtok.type == "STRING":
                                self._expect("STRING")

                            elif nxtok.type == "COMMA":

                                self._expect("COMMA")
                                nxtok = self._lexer.peek_token()

                                if nxtok.type == "STRING":
                                    self._expect("STRING")
                                    nxtok = self._lexer.peek_token()
                                
                                while nxtok.type in Parser.TFPDEF_FIRST_SET:

                                    self._parse_tfpdef()
                                    nxtok = self._lexer.peek_token()

                                    if nxtok.type == "EQUAL":
                                        self._expect("EQUAL")
                                        self._parse_test()
                                        nxtok = self._lexer.peek_token()

                                    if nxtok.type == "STRING":
                                        self._expect("STRING")
                                        break
                                    
                                    self._expect("COMMA")
                                    nxtok = self._lexer.peek_token()

                                    if nxtok.type == "STRING":
                                        self._expect("STRING")
                                
                                if nxtok.type == "STRING":
                                    self._expect("STRING")

                                elif nxtok.type == "ASTERISK":

                                    self._expect("ASTERISK")
                                    nxtok = self._lexer.peek_token()

                                    if nxtok.type in Parser.TFPDEF_FIRST_SET:
                                        self._parse_tfpdef()
                                        nxtok = self._lexer.peek_token()
                                    
                                    while nxtok.type == "COMMA":

                                        self._expect("COMMA")
                                        nxtok = self._lexer.peek_token()

                                        if nxtok.type == "STRING":
                                            self._expect("STRING")
                                            nxtok = self._lexer.peek_token()
                                        
                                        self._parse_tfpdef()
                                        nxtok = self._lexer.peek_token()

                                        if nxtok.type == "EQUAL":
                                            self._expect("EQUAL")
                                            self._parse_test()
                                            nxtok = self._lexer.peek_token()
                                    
                                    if nxtok.type == "STRING":
                                        self._expect("STRING")

                                    elif nxtok.type == "COMMA":

                                        self._expect("COMMA")
                                        nxtok = self._lexer.peek_token()

                                        if nxtok.type == "STRING":
                                            self._expect("STRING")
                                            nxtok = self._lexer.peek_token()
                                        
                                        if nxtok.type == "POWER":

                                            self._expect("POWER")
                                            self._parse_tfpdef()

                                            nxtok = self._lexer.peek_token()

                                            if nxtok.type == "COMMA":
                                                self._expect("COMMA")
                                                nxtok = self._lexer.peek_token()
                                            
                                            if nxtok.type == "STRING":
                                                self._expect("STRING")

                                elif nxtok.type == "POWER":

                                    self._expect("POWER")
                                    self._parse_tfpdef()
                                    nxtok = self._lexer.peek_token()

                                    if nxtok.type == "COMMA":
                                        self._expect("COMMA")
                                        nxtok = self._lexer.peek_token()
                                    
                                    if nxtok.type == "STRING":
                                        self._expect("STRING")
                            
                        elif nxtok.type == "ASTERISK":

                            self._expect("ASTERISK")
                            nxtok = self._lexer.peek_token()

                            if nxtok.type in Parser.TFPDEF_FIRST_SET:
                                self._parse_tfpdef()
                                nxtok = self._lexer.peek_token()
                            
                            while nxtok.type == "COMMA":

                                self._expect("COMMA")
                                nxtok = self._lexer.peek_token()

                                if nxtok.type == "STRING":
                                    self._expect("STRING")
                                    nxtok = self._lexer.peek_token()
                                
                                self._parse_tfpdef()
                                nxtok = self._lexer.peek_token()

                                if nxtok.type == "EQUAL":
                                    self._expect("EQUAL")
                                    self._parse_test()
                                    nxtok = self._lexer.peek_token()
                            
                            if nxtok.type == "STRING":
                                self._expect("STRING")
                                
                            elif nxtok.type == "COMMA":

                                self._expect("COMMA")
                                nxtok = self._lexer.peek_token()

                                if nxtok.type == "STRING":
                                    self._expect("STRING")
                                    nxtok = self._lexer.peek_token()
                                
                                if nxtok.type == "POWER":
                                    self._expect("POWER")
                                    self._parse_tfpdef()

                                    nxtok = self._lexer.peek_token()

                                    if nxtok.type == "COMMA":
                                        self._expect("COMMA")
                                        nxtok = self._lexer.peek_token()
                                    
                                    if nxtok.type == "STRING":
                                        self._expect("STRING")

                        elif nxtok.type == "POWER":

                            self._expect("POWER")
                            self._parse_tfpdef()
                            nxtok = self._lexer.peek_token()

                            if nxtok.type == "COMMA":
                                self._expect("COMMA")
                                nxtok = self._lexer.peek_token()
                            
                            if nxtok.type == "STRING":
                                self._expect("STRING")

                elif nxtok.type == "ASTERISK":

                    self._expect("ASTERISK")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type in Parser.TFPDEF_FIRST_SET:
                        self._parse_tfpdef()
                        nxtok = self._lexer.peek_token()
                    
                    while nxtok.type == "COMMA":

                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()

                        if nxtok.type == "STRING":
                            self._expect("STRING")
                            nxtok = self._lexer.peek_token()
                        
                        self._parse_tfpdef()
                        nxtok = self._lexer.peek_token()

                        if nxtok.type == "EQUAL":
                            self._expect("EQUAL")
                            self._parse_test()
                            nxtok = self._lexer.peek_token()
                    
                    if nxtok.type == "STRING":
                        self._expect("STRING")

                    elif nxtok.type == "COMMA":

                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()

                        if nxtok.type == "STRING":
                            self._expect("STRING")
                            nxtok = self._lexer.peek_token()
                        
                        if nxtok.type == "POWER":

                            self._expect("POWER")
                            self._parse_tfpdef()

                            nxtok = self._lexer.peek_token()

                            if nxtok.type == "COMMA":
                                self._expect("COMMA")
                                nxtok = self._lexer.peek_token()
                            
                            if nxtok.type == "STRING":
                                self._expect("STRING")

                elif nxtok.type == "POWER":

                    self._expect("POWER")
                    self._parse_tfpdef()
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "COMMA":
                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()
                    
                    if nxtok.type == "STRING":
                        self._expect("STRING")
                        
                    elif nxtok.type == "STRING":
                        self._expect("STRING")

        elif nxtok.type == "ASTERISK":

            self._expect("ASTERISK")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.TFPDEF_FIRST_SET:
                self._parse_tfpdef()
                nxtok = self._lexer.peek_token()
            
            while nxtok.type == "COMMA":
                
                self._expect("COMMA")
                nxtok = self._lexer.peek_token()

                if nxtok.type == "STRING":
                    self._expect("STRING")
                    nxtok = self._lexer.peek_token()
                
                self._parse_tfpdef()
                nxtok = self._lexer.peek_token()

                if nxtok.type == "EQUAL":
                    self._expect("EQUAL")
                    self._parse_test()
                    nxtok = self._lexer.peek_token()
            
            if nxtok.type == "STRING":
                self._expect("STRING")

            elif nxtok.type == "COMMA":
                self._expect("COMMA")
                nxtok = self._lexer.peek_token()

                if nxtok.type == "STRING":
                    self._expect("STRING")
                    nxtok = self._lexer.peek_token()
                
                if nxtok.type == "POWER":
                    self._expect("POWER")
                    self._parse_tfpdef()

                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "COMMA":
                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()
                    
                    if nxtok.type == "STRING":
                        self._expect("STRING")

        elif nxtok.type == "POWER":

            self._expect("POWER")
            self._parse_tfpdef()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "COMMA":
                self._expect("COMMA")
                nxtok = self._lexer.peek_token()
            
            if nxtok.type == "STRING":
                self._expect("STRING")

        else:
            self._syntax_error(Parser.TFPDEF_FIRST_SET | { "ASTERISK", "POWER" }, nxtok.type)

    """
    tfpdef: NAME [':' test]
    """
    def _parse_tfpdef(self):

        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        if nxtok.type == "COLON":
            self._expect("COLON")
            self._parse_test()
    
    """
    varargslist: vfpdef ['=' test ] (',' vfpdef ['=' test])* ',' '/'
    [

        ',' [ (vfpdef ['=' test] (',' vfpdef ['=' test])* 
        [
            ','
            [
                '*' [vfpdef] (',' vfpdef ['=' test])* [',' [ '**' vfpdef [','] ] ]
                | '**' vfpdef [',']
            ]
        ]

        | '*' [vfpdef] (',' vfpdef ['=' test])* [ ',' [ '**' vfpdef [','] ] ]

        | '**' vfpdef [',']) ]
    ]
    
    |
    
    (
        vfpdef ['=' test] (',' vfpdef ['=' test])* 

        [
            ','
            [
                '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
                | '**' vfpdef [',']
            ]
        ]

        | '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]

        | '**' vfpdef [',']
    )
    """
    def _parse_varargslist(self):
        nxtok = self._lexer.peek_token()

        if nxtok.type == "ASTERISK":

            self._expect("ASTERISK")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.VFPDEF_FIRST_SET:
                self._parse_vfpdef()
                nxtok = self._lexer.peek_token()
            
            if nxtok.type == "COMMA":

                self._expect("COMMA")
                
                nxtok = self._lexer.peek_token()

                if nxtok.type in Parser.VFPDEF_FIRST_SET:
                    
                    self._parse_vfpdef()

                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "EQUAL":
                        self._expect("EQUAL")
                        self._parse_test()
                        nxtok = self._lexer.peek_token()
                    
                    while nxtok.type == "COMMA":

                        self._expect("COMMA")
                        self._parse_vfpdef()

                        nxtok = self._lexer.peek_token()

                        if nxtok.type == "EQUAL":
                            self._expect("EQUAL")
                            self._parse_test()
                            nxtok = self._lexer.peek_token()
                            
                elif nxtok.type == "POWER":

                    self._expect("POWER")
                    self._parse_vfpdef()
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "COMMA":
                        self._expect("COMMA")

                else:
                    self._syntax_error(Parser.VFPDEF_FIRST_SET | { "POWER" }, nxtok.type)

        elif nxtok.type == "POWER":

            self._expect("POWER")
            self._parse_vfpdef()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "COMMA":
                self._expect("COMMA")

        else:

            self._parse_vfpdef()
            
            nxtok = self._lexer.peek_token()

            if nxtok.type == "EQUAL":
                self._expect("EQUAL")
                self._parse_test()
                nxtok = self._lexer.peek_token()

            if nxtok.type == "COMMA":

                self._expect("COMMA")

                nxtok = self._lexer.peek_token()

                if nxtok.type in Parser.VFPDEF_FIRST_SET:

                    self._parse_vfpdef()

                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "EQUAL":
                        self._expect("EQUAL")
                        self._parse_test()
                        nxtok = self._lexer.peek_token()
                    
                    while nxtok.type == "COMMA":

                        self._expect("COMMA")
                        self._parse_vfpdef()

                        nxtok = self._lexer.peek_token()

                        if nxtok.type == "EQUAL":
                            self._expect("EQUAL")
                            self._parse_test()
                            nxtok = self._lexer.peek_token()

                elif nxtok.type == "ASTERISK":

                    self._expect("ASTERISK")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type in Parser.VFPDEF_FIRST_SET:
                        self._parse_vfpdef()
                        nxtok = self._lexer.peek_token()
                    
                    if nxtok.type == "COMMA":

                        self._expect("COMMA")
                        
                        nxtok = self._lexer.peek_token()

                        if nxtok.type in Parser.VFPDEF_FIRST_SET:

                            self._parse_vfpdef()

                            nxtok = self._lexer.peek_token()

                            if nxtok.type == "EQUAL":
                                self._expect("EQUAL")
                                self._parse_test()
                                nxtok = self._lexer.peek_token()
                            
                            while nxtok.type == "COMMA":

                                self._expect("COMMA")
                                self._parse_vfpdef()

                                nxtok = self._lexer.peek_token()

                                if nxtok.type == "EQUAL":
                                    self._expect("EQUAL")
                                    self._parse_test()
                                    nxtok = self._lexer.peek_token()

                        elif nxtok.type == "POWER":

                            self._expect("POWER")
                            self._parse_vfpdef()
                            nxtok = self._lexer.peek_token()

                            if nxtok.type == "COMMA":
                                self._expect("COMMA")

                        else:
                            self._syntax_error(Parser.VFPDEF_FIRST_SET | { "POWER" }, nxtok.type)

                elif nxtok.type == "POWER":

                    self._expect("POWER")
                    self._parse_vfpdef()
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "COMMA":
                        self._expect("COMMA")

                else:
                    self._syntax_error(Parser.VFPDEF_FIRST_SET | { "ASTERISK", "POWER" }, nxtok.type)
    
    """
    vfpdef: NAME
    """
    def _parse_vfpdef(self):
        self._expect("NAME")
    
    """
    stmt: simple_stmt | compound_stmt
    """
    def _parse_stmt(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.SIMPLE_STMT_FIRST_SET:
            self._parse_simple_stmt()

        elif nxtok.type in Parser.COMPOUND_STMT_FIRST_SET:
            self._parse_compound_stmt()

        else:
            self._syntax_error(Parser.SIMPLE_STMT_FIRST_SET | Parser.COMPOUND_STMT_FIRST_SET, nxtok.type)
    
    """
    simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
    """
    def _parse_simple_stmt(self):

        self._parse_small_stmt()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "SEMICOLON":

            self._expect("SEMICOLON")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.SMALL_STMT_FIRST_SET:
                self._parse_small_stmt()
                nxtok = self._lexer.peek_token()
            else:
                break
    
    """
    small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt |
        import_stmt | global_stmt | nonlocal_stmt | assert_stmt)
    """
    def _parse_small_stmt(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.EXPR_STMT_FIRST_SET: self._parse_expr_stmt()

        elif nxtok.type in Parser.DEL_STMT_FIRST_SET: self._parse_del_stmt()

        elif nxtok.type in Parser.PASS_STMT_FIRST_SET: self._parse_pass_stmt()

        elif nxtok.type in Parser.FLOW_STMT_FIRST_SET: self._parse_flow_stmt()

        elif nxtok.type in Parser.IMPORT_STMT_FIRST_SET: self._parse_import_stmt()

        elif nxtok.type in Parser.GLOBAL_STMT_FIRST_SET: self._parse_global_stmt()

        elif nxtok.type in Parser.NONLOCAL_STMT_FIRST_SET: self._parse_nonlocal_stmt()

        elif nxtok.type in Parser.ASSERT_STMT_FIRST_SET: self._parse_assert_stmt()

        else:
            self._syntax_error(
                Parser.EXPR_STMT_FIRST_SET
                | Parser.DEL_STMT_FIRST_SET
                | Parser.PASS_STMT_FIRST_SET
                | Parser.FLOW_STMT_FIRST_SET
                | Parser.IMPORT_STMT_FIRST_SET
                | Parser.GLOBAL_STMT_FIRST_SET
                | Parser.NONLOCAL_STMT_FIRST_SET
                | Parser.ASSERT_STMT_FIRST_SET
                , nxtok.type
            )
    
    """
    expr_stmt: testlist_star_expr (annassign | augassign (yield_expr|testlist) |
        [('=' (yield_expr|testlist_star_expr))+ [TYPE_COMMENT]] )
    """
    def _parse_expr_stmt(self):

        self._parse_testlist_star_expr()
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.ANNASSIGN_FIRST_SET:
            self._parse_annasign()

        elif nxtok.type in Parser.AUGASSIGN_FIRST_SET:

            self._parse_augassign()
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.YIELD_EXPR_FIRST_SET:
                self._parse_yield_expr()

            elif nxtok.type in Parser.TESTLIST_FIRST_SET:
                self._parse_testlist()

            else:
                self._syntax_error(Parser.YIELD_EXPR_FIRST_SET | Parser.TESTLIST_FIRST_SET, nxtok.type)
            
        elif nxtok.type == "EQUAL":
            
            while nxtok.type == "EQUAL":

                self._expect("EQUAL")
                nxtok = self._lexer.peek_token()

                if nxtok.type in Parser.YIELD_EXPR_FIRST_SET:
                    self._parse_yield_expr()

                else:
                    self._parse_testlist_star_expr()
                
                nxtok = self._lexer.peek_token()
            
            if nxtok.type == "STRING":
                self._expect("STRING")
    
    """
    annassign: ':' test ['=' (yield_expr|testlist_star_expr)]
    """
    def _parse_annasign(self):

        self._expect("COLON")
        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "EQUAL":

            self._expect("EQUAL")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.YIELD_EXPR_FIRST_SET:
                self._parse_yield_expr()

            else:
                self._parse_testlist_star_expr()
    
    """
    testlist_star_expr: (test|star_expr) (',' (test|star_expr))* [',']
    """
    def _parse_testlist_star_expr(self):
        
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:
            self._parse_test()

        elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
            self._parse_star_expr()

        else:
            self._syntax_error(Parser.TEST_FIRST_SET | Parser.STAR_EXPR_FIRST_SET, nxtok.type)
        
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.TEST_FIRST_SET:
                self._parse_test()

            elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
                self._parse_star_expr()

            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    """
    augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' |
        '<<=' | '>>=' | '**=' | '//=')
    """
    def _parse_augassign(self):
        self._expect( Parser.AUGASSIGN_FIRST_SET )
    
    """
    del_stmt: 'del' exprlist
    """
    def _parse_del_stmt(self):
        self._expect("DEL")
        self._parse_exprlist()
    
    """
    pass_stmt: 'pass'
    """
    def _parse_pass_stmt(self):
        self._expect("PASS")
    
    """
    flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt
    """
    def _parse_flow_stmt(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.BREAK_STMT_FIRST_SET:
            self._parse_break_stmt()

        elif nxtok.type in Parser.CONTINUE_STMT_FIRST_SET:
            self._parse_continue_stmt()

        elif nxtok.type in Parser.RETURN_STMT_FIRST_SET:
            self._parse_return_stmt()

        elif nxtok.type in Parser.RAISE_STMT_FIRST_SET:
            self._parse_raise_stmt()

        elif nxtok.type in Parser.YIELD_STMT_FIRST_SET:
            self._parse_yeild_stmt()

        else:
            self._syntax_error(
                Parser.BREAK_STMT_FIRST_SET
                | Parser.CONTINUE_STMT_FIRST_SET
                | Parser.RETURN_STMT_FIRST_SET
                | Parser.RAISE_STMT_FIRST_SET
                | Parser.YIELD_STMT_FIRST_SET
                , nxtok.type
            )
    
    """
    break_stmt: 'break'
    """
    def _parse_break_stmt(self):
        self._expect("BREAK")
    
    """
    continue_stmt: 'continue'
    """
    def _parse_continue_stmt(self):
        self._expect("CONTINUE")
    
    """
    return_stmt: 'return' [testlist_star_expr]
    """
    def _parse_return_stmt(self):

        self._expect("RETURN")

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TESTLIST_STAR_EXPR_FIRST_SET:
            self._parse_testlist_star_expr()
    
    """
    yield_stmt: yield_expr
    """
    def _parse_yeild_stmt(self):
        self._parse_yield_expr()
    
    """
    raise_stmt: 'raise' [test ['from' test]]
    """
    def _parse_raise_stmt(self):

        self._expect("RAISE")

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:

            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "FROM":
                self._expect("FROM")
                self._parse_test()
    
    """
    import_stmt: import_name | import_from
    """
    def _parse_import_stmt(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.IMPORT_NAME_FIRST_SET:
            self._parse_import_name()

        elif nxtok.type in Parser.IMPORT_FROM_FIRST_SET:
            self._parse_import_from()
            
        else:
            self._syntax_error(Parser.IMPORT_AS_NAME_FIRST_SET | Parser.IMPORT_FROM_FIRST_SET, nxtok.type)
    
    """
    import_name: 'import' dotted_as_names
    """
    def _parse_import_name(self):
        self._expect("IMPORT")
        self._parse_dotted_as_names()
    
    """
    import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
        'import' ('*' | '(' import_as_names ')' | import_as_names))
    """
    def _parse_import_from(self):

        self._expect("FROM")
        nxtok = self._lexer.peek_token()
        dot_or_ellipsis_found = False

        while nxtok.type in { "DOT", "ELLIPSIS" }:
            dot_or_ellipsis_found = True
            self._expect({ "DOT", "ELLIPSIS" })
            nxtok = self._lexer.peek_token()
        
        if dot_or_ellipsis_found:

            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.DOTTED_NAME_FIRST_SET:
                self._parse_dotted_name()

        else:
            self._parse_dotted_name()
        
        self._expect("IMPORT")

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ASTERISK":
            self._expect("ASTERISK")

        elif nxtok.type == "LPAREN":
            self._expect("LPAREN")
            self._parse_import_as_names()
            self._expect("RPAREN")

        elif nxtok.type in Parser.IMPORT_AS_NAMES_FIRST_SET:
            self._parse_import_as_names()

        else:
            self._syntax_error({ "ASTERISK", "LPAREN" } | Parser.IMPORT_AS_NAMES_FIRST_SET, nxtok.type)
    
    """
    import_as_name: NAME ['as' NAME]
    """
    def _parse_import_as_name(self):

        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        if nxtok.type == "AS":
            self._expect("AS")
            self._expect("NAME")
    
    """
    dotted_as_name: dotted_name ['as' NAME]
    """
    def _parse_dotted_as_name(self):

        self._parse_dotted_name()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "AS":
            self._expect("AS")
            self._expect("NAME")
    
    """
    import_as_names: import_as_name (',' import_as_name)* [',']
    """
    def _parse_import_as_names(self):

        self._parse_import_as_name()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.IMPORT_AS_NAME_FIRST_SET:
                self._parse_import_as_name()
                nxtok = self._lexer.peek_token()
                
            else:
                break
    
    """
    dotted_as_names: dotted_as_name (',' dotted_as_name)*
    """
    def _parse_dotted_as_names(self):

        self._parse_dotted_as_name()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._parse_dotted_as_name()
            nxtok = self._lexer.peek_token()
    
    """
    dotted_name: NAME ('.' NAME)*
    """
    def _parse_dotted_name(self):

        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        while nxtok.type == "DOT":
            self._expect("DOT")
            self._expect("NAME")
            nxtok = self._lexer.peek_token()
    
    """
    global_stmt: 'global' NAME (',' NAME)*
    """
    def _parse_global_stmt(self):

        self._expect("GLOBAL")
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._expect("NAME")
            nxtok = self._lexer.peek_token()
    
    """
    nonlocal_stmt: 'nonlocal' NAME (',' NAME)*
    """
    def _parse_nonlocal_stmt(self):

        self._expect("NONLOCAL")
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._expect("NAME")
            nxtok = self._lexer.peek_token()
    
    """
    assert_stmt: 'assert' test [',' test]
    """
    def _parse_assert_stmt(self):

        self._expect("ASSERT")
        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "COMMA":
            self._expect("COMMA")
            self._parse_test()
    
    """
    compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt
    """
    def _parse_compound_stmt(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.IF_STMT_FIRST_SET:
            self._parse_if_stmt()

        elif nxtok.type in Parser.WHILE_STMT_FIRST_SET:
            self._parse_while_stmt()

        elif nxtok.type in Parser.FOR_STMT_FIRST_SET:
            self._parse_for_stmt()

        elif nxtok.type in Parser.TRY_STMT_FIRST_SET:
            self._parse_try_stmt()

        elif nxtok.type in Parser.WITH_STMT_FIRST_SET:
            self._parse_with_stmt()

        elif nxtok.type in Parser.FUNCDEF_FIRST_SET:
            self._parse_funcdef()

        elif nxtok.type in Parser.CLASSDEF_FIRST_SET:
            self._parse_classdef()

        elif nxtok.type in Parser.DECORATED_FIRST_SET:
            self._parse_decorated()

        elif nxtok.type in Parser.ASYNC_STMT_FIRST_SET:
            self._parse_async_stmt()

        else:
            self._syntax_error(
                Parser.IF_STMT_FIRST_SET
                | Parser.WHILE_STMT_FIRST_SET
                | Parser.FOR_STMT_FIRST_SET
                | Parser.TRY_STMT_FIRST_SET
                | Parser.WITH_STMT_FIRST_SET
                | Parser.FUNCDEF_FIRST_SET
                | Parser.CLASSDEF_FIRST_SET
                | Parser.DECORATED_FIRST_SET
                | Parser.ASYNC_STMT_FIRST_SET
                , nxtok.type
            )
    
    """
    async_stmt: ASYNC (funcdef | with_stmt | for_stmt)
    """
    def _parse_async_stmt(self):

        self._expect("ASYNC")

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.FOR_STMT_FIRST_SET:
            self._parse_for_stmt()

        elif nxtok.type in Parser.WITH_STMT_FIRST_SET:
            self._parse_with_stmt()

        elif nxtok.type in Parser.FUNCDEF_FIRST_SET:
            self._parse_funcdef()

        else:
            self._syntax_error(
                Parser.FOR_STMT_FIRST_SET
                | Parser.WITH_STMT_FIRST_SET
                | Parser.FUNCDEF_FIRST_SET,
                nxtok.type
            )
    
    """
    if_stmt: 'if' namedexpr_test ':' suite ('elif' namedexpr_test ':' suite)* ['else' ':' suite]
    """
    def _parse_if_stmt(self):

        self._expect("IF")
        self._parse_namedexpr_test()
        self._expect("COLON")
        self._parse_suite()
        
        nxtok = self._lexer.peek_token()

        while nxtok.type == "NEWLINE":
            self._expect("NEWLINE")
            nxtok = self._lexer.peek_token()

        while nxtok.type == "ELIF" and nxtok.indent == self._indent_level:
            self._expect("ELIF")
            self._parse_namedexpr_test()
            self._expect("COLON")
            self._parse_suite()
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

        nxtok = self._lexer.peek_token()

        while nxtok.type == "NEWLINE":
            self._expect("NEWLINE")
            nxtok = self._lexer.peek_token()

        if nxtok.type == "ELSE" and nxtok.indent == self._indent_level:
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    """
    while_stmt: 'while' namedexpr_test ':' suite ['else' ':' suite]
    """
    def _parse_while_stmt(self):

        self._expect("WHILE")
        self._parse_namedexpr_test()
        self._expect("COLON")
        self._parse_suite()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ELSE" and nxtok.indent == self._indent_level:
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    """
    for_stmt: 'for' exprlist 'in' testlist ':' [TYPE_COMMENT] suite ['else' ':' suite]
    """
    def _parse_for_stmt(self):

        self._expect("FOR")
        self._parse_exprlist()
        self._expect("IN")
        self._parse_testlist()
        self._expect("COLON")
        nxtok = self._lexer.peek_token()

        if nxtok.type == "STRING":
            self._expect("STRING")

        self._parse_suite()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ELSE":
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    """
    try_stmt: ('try' ':' suite
        ((except_clause ':' suite)+
        ['else' ':' suite]
        ['finally' ':' suite] |
        'finally' ':' suite))
    """
    def _parse_try_stmt(self):

        self._expect("TRY")
        self._expect("COLON")
        self._parse_suite()

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.EXCEPT_CLAUSE_FIRST_SET:

            self._parse_except_clause()
            self._expect("COLON")
            self._parse_suite()

            nxtok = self._lexer.peek_token()

            while nxtok.type in Parser.EXCEPT_CLAUSE_FIRST_SET:
                self._parse_except_clause()
                self._expect("COLON")
                self._parse_suite()
                nxtok = self._lexer.peek_token()
            
            nxtok = self._lexer.peek_token()

            if nxtok.type == "ELSE":
                self._expect("ELSE")
                self._expect("COLON")
                self._parse_suite()
                nxtok = self._lexer.peek_token()

            if nxtok.type == "FINALLY":
                self._expect("FINALLY")
                self._expect("COLON")
                self._parse_suite()

        elif nxtok.type == "FINALLY":
            self._expect("FINALLY")
            self._expect("COLON")
            self._parse_suite()

        else:
            self._syntax_error(Parser.EXCEPT_CLAUSE_FIRST_SET | { "FINALLY" }, nxtok.type)
    
    """
    with_stmt: 'with' with_item (',' with_item)*  ':' [TYPE_COMMENT] suite
    """
    def _parse_with_stmt(self):

        self._expect("WITH")
        self._parse_with_item()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._parse_with_item()
            nxtok = self._lexer.peek_token()

        self._expect("COLON")
        nxtok = self._lexer.peek_token()

        if nxtok.type == "STRING":
            self._expect("STRING")

        self._parse_suite()
    
    """
    with_item: test ['as' expr]
    """
    def _parse_with_item(self):

        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "AS":
            self._expect("AS")
            self._parse_expr()
    
    """
    except_clause: 'except' [test ['as' NAME]]
    """
    def _parse_except_clause(self):

        self._expect("EXCEPT")
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:

            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "AS":
                self._expect("AS")
                self._expect("NAME")

    """
    suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT
    """  
    def _parse_suite(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.SIMPLE_STMT_FIRST_SET:
            self._parse_simple_stmt()

        elif nxtok.type == "NEWLINE":

            self._expect("NEWLINE")

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            self._expect_indent()

            self._parse_stmt()
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            while nxtok.type in Parser.STMT_FIRST_SET and nxtok.indent == self._indent_level:

                self._parse_stmt()
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()
            
            if nxtok.indent > self._indent_level:
                self._syntax_error(Parser.INDENT_LEVEL_STR % self._indent_level, nxtok.indent)

            else:
                self._indent_level -= 1

        else:
            self._syntax_error(Parser.SIMPLE_STMT_FIRST_SET | { "NEWLINE" }, nxtok.type)
    
    """
    namedexpr_test: test [':=' test]
    """
    def _parse_namedexpr_test(self):

        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "WALRUS":
            self._expect("WALRUS")
            self._parse_test()
    
    """
    test: or_test ['if' or_test 'else' test] | lambdef
    """
    def _parse_test(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.OR_TEST_FIRST_SET:

            current_line_number = self._lexer.get_line_number()

            self._parse_or_test()

            if self._lexer.get_line_number() == current_line_number:

                nxtok = self._lexer.peek_token()

                if nxtok.type == "IF":
                    self._expect("IF")
                    self._parse_or_test()
                    self._expect("ELSE")
                    self._parse_test()

        elif nxtok.type in Parser.LAMBDEF_FIRST_SET:
            self._parse_lambdef()

        else:
            self._syntax_error(Parser.OR_TEST_FIRST_SET | Parser.LAMBDEF_FIRST_SET, nxtok.type)
    
    """
    test_nocond: or_test | lambdef_nocond
    """
    def _parse_test_nocond(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.OR_TEST_FIRST_SET:
            self._parse_or_test()

        elif nxtok.type in Parser.LAMBDEF_NOCOND_FIRST_SET:
            self._parse_lambdef_nocond()

        else:
            self._syntax_error(Parser.OR_TEST_FIRST_SET | Parser.LAMBDEF_NOCOND_FIRST_SET, nxtok.type)
    
    """
    lambdef: 'lambda' [varargslist] ':' test
    """
    def _parse_lambdef(self):

        self._expect("LAMBDA")
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.VARARGSLIST_FIRST_SET:
            self._parse_varargslist()
            nxtok = self._lexer.peek_token()
        
        self._expect("COLON")
        self._parse_test()
    
    """
    lambdef_nocond: 'lambda' [varargslist] ':' test_nocond
    """
    def _parse_lambdef_nocond(self):

        self._expect("LAMBDA")
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.VARARGSLIST_FIRST_SET:
            self._parse_varargslist()
            nxtok = self._lexer.peek_token()
        
        self._expect("COLON")
        self._parse_test_nocond()
    
    """
    or_test: and_test ('or' and_test)*
    """
    def _parse_or_test(self):

        self._parse_and_test()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "OR":
            self._expect("OR")
            self._parse_and_test()
            nxtok = self._lexer.peek_token()
    
    """
    and_test: not_test ('and' not_test)*
    """
    def _parse_and_test(self):

        self._parse_not_test()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "AND":
            self._expect("AND")
            self._parse_not_test()
            nxtok = self._lexer.peek_token()
    
    """
    not_test: 'not' not_test | comparison
    """
    def _parse_not_test(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type == "NOT":
            self._expect("NOT")
            self._parse_not_test()

        elif nxtok.type in Parser.COMPARISON_FIRST_SET:
            self._parse_comparison()
    
    """
    comparison: expr (comp_op expr)*
    """
    def _parse_comparison(self):

        self._parse_expr()

        nxtok = self._lexer.peek_token()

        while nxtok.type in Parser.COMP_OP_FIRST_SET:
            self._parse_comp_op()
            self._parse_expr()
            nxtok = self._lexer.peek_token()
    
    """
    comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    """
    def _parse_comp_op(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type == "NOT":

            self._expect("NOT")
            nxtok = self._lexer.peek_token()

            if nxtok.type == "IN":
                self._expect("IN")

        elif nxtok.type == "IS":

            self._expect("IS")
            nxtok = self._lexer.peek_token()

            if nxtok.type == "NOT":
                self._expect("NOT")

        else:
            self._expect([
                "GREATER_THAN", "LESS_THAN", "DOUBLE_EQUALS",
                "GEQ", "LEQ", "NOT_EQUALS",
                "IN", "IS"
            ])
    
    """
    star_expr: '*' expr
    """
    def _parse_star_expr(self):
        self._expect("ASTERISK")
        self._parse_expr()
    
    """
    expr: xor_expr ('|' xor_expr)*
    """
    def _parse_expr(self):

        self._parse_xor_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "PIPE":
            self._expect("PIPE")
            self._parse_xor_expr()
            nxtok = self._lexer.peek_token()
    
    """
    xor_expr: and_expr ('^' and_expr)*
    """
    def _parse_xor_expr(self):

        self._parse_and_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "CARROT":
            self._expect("CARROT")
            self._parse_and_expr()
            nxtok = self._lexer.peek_token()
    
    """
    and_expr: shift_expr ('&' shift_expr)*
    """
    def _parse_and_expr(self):

        self._parse_shift_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "AMPERSAND":
            self._expect("AMPERSAND")
            self._parse_shift_expr()
            nxtok = self._lexer.peek_token()
    
    """
    shift_expr: arith_expr (('<<'|'>>') arith_expr)*
    """
    def _parse_shift_expr(self):

        self._parse_arith_expr()
        nxtok = self._lexer.peek_token()
        is_shift_token = nxtok.type in { "SHIFT_LEFT", "SHIFT_RIGHT" }

        while is_shift_token:

            if nxtok.type == "SHIFT_LEFT":
                self._expect("SHIFT_LEFT")

            elif nxtok.type == "SHIFT_RIGHT":
                self._expect("SHIFT_RIGHT")

            else:
                is_shift_token = False

            if is_shift_token:
                self._parse_arith_expr()
                nxtok = self._lexer.peek_token()
    
    """
    arith_expr: term (('+'|'-') term)*
    """
    def _parse_arith_expr(self):

        self._parse_term()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "NEWLINE":
            self._expect("NEWLINE")
            nxtok = self._lexer.peek_token()

        is_plus_or_minus = nxtok.type in { "PLUS", "MINUS" }

        while is_plus_or_minus:

            if nxtok.type == "PLUS":
                self._expect("PLUS")

            elif nxtok.type == "MINUS":
                self._expect("MINUS")

            else:
                is_plus_or_minus = False

            if is_plus_or_minus:
                self._parse_term()
                nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()
    
    """
    term: factor (('*'|'@'|'/'|'%'|'//') factor)*
    """
    def _parse_term(self):

        self._parse_factor()
        nxtok = self._lexer.peek_token()
        is_factor_op = nxtok.type in { "ASTERISK", "AT", "SLASH", "PERCENT", "FLOOR_DIVISION" }

        while is_factor_op:

            if nxtok.type == "ASTERISK":
                self._expect("ASTERISK")

            elif nxtok.type == "AT":
                self._expect("AT")

            elif nxtok.type == "SLASH":
                self._expect("SLASH")

            elif nxtok.type == "PERCENT":
                self._expect("PERCENT")
                
            elif nxtok.type == "FLOOR_DIVISION":
                self._expect("FLOOR_DIVISION")

            else:
                is_factor_op = False

            if is_factor_op:
                self._parse_factor()
                nxtok = self._lexer.peek_token()
    
    """
    factor: ('+'|'-'|'~') factor | power
    """
    def _parse_factor(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in { "PLUS", "MINUS", "TILDE" }:

            if nxtok.type == "PLUS":
                self._expect("PLUS")

            elif nxtok.type == "MINUS":
                self._expect("MINUS")
                
            elif nxtok.type == "TILDE":
                self._expect("TILDE")
            
            self._parse_factor()

        elif nxtok.type in Parser.POWER_FIRST_SET:
            self._parse_power()
        
        else:
            self._syntax_error({ "PLUS", "MINUS", "TILDE" } | Parser.POWER_FIRST_SET, nxtok.type)
    
    """
    power: atom_expr ['**' factor]
    """
    def _parse_power(self):

        self._parse_atom_expr()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "POWER":
            self._expect("POWER")
            self._parse_factor()
    
    """
    atom_expr: [AWAIT] atom trailer*
    """
    def _parse_atom_expr(self):

        nxtok = self._lexer.peek_token()
        
        if nxtok.type == "AWAIT":
            self._expect("AWAIT")
        
        self._parse_atom()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "NEWLINE":
            self._expect("NEWLINE")
            nxtok = self._lexer.peek_token()

        while nxtok.type in Parser.TRAILER_FIRST_SET:
            self._parse_trailer()
            nxtok = self._lexer.peek_token()
    
    """
    atom: ('(' [yield_expr|testlist_comp] ')' |
        '[' [testlist_comp] ']' |
        '{' [dictorsetmaker] '}' |
        NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
    """
    def _parse_atom(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":

            self._expect("LPAREN")

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.YIELD_EXPR_FIRST_SET:
                self._parse_yield_expr()
                nxtok = self._lexer.peek_token()

            elif nxtok.type in Parser.TESTLIST_COMP_FIRST_SET:
                self._parse_testlist_comp()
                nxtok = self._lexer.peek_token()
            
            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()
            
            self._expect("RPAREN")

        elif nxtok.type == "LBRACKET":

            self._expect("LBRACKET")

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.TESTLIST_COMP_FIRST_SET:
                self._parse_testlist_comp()
                nxtok = self._lexer.peek_token()
            
            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()
            
            self._expect("RBRACKET")

        elif nxtok.type == "LBRACE":

            self._expect("LBRACE")

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.DICTORSETMAKER_FIRST_SET:
                self._parse_dictorsetmaker()
                nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()
            
            self._expect("RBRACE")

        elif nxtok.type == "NAME":
            self._expect("NAME")

        elif nxtok.type == "NUMBER":
            self._expect("NUMBER")

        elif nxtok.type == "STRING":

            while nxtok.type == "STRING":
                self._expect("STRING")
                nxtok = self._lexer.peek_token()

        elif nxtok.type == "ELLIPSIS":
            self._expect("ELLIPSIS")

        elif nxtok.type == "NONE":
            self._expect("NONE")

        elif nxtok.type == "TRUE":
            self._expect("TRUE")

        elif nxtok.type == "FALSE":
            self._expect("FALSE")

        else:
            self._syntax_error({
                "LPAREN", "LBRACKET", "LBRACE",
                "NAME", "NUMBER", "STRING",
                "ELLIPSIS", "NONE", "TRUE",
                "FALSE"
            }, nxtok.type)
    
    """
    testlist_comp: (namedexpr_test|star_expr) ( comp_for | (',' (namedexpr_test|star_expr))* [','] )
    """
    def _parse_testlist_comp(self):     

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.NAMEDEXPR_TEST_FIRST_SET:
            self._parse_namedexpr_test()

        elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
            self._parse_star_expr()

        else:
            self._syntax_error(Parser.NAMEDEXPR_TEST_FIRST_SET | Parser.STAR_EXPR_FIRST_SET, nxtok.type)
        
        comp_for_first_set = { "ASYNC", "FOR" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in comp_for_first_set:
            self._parse_comp_for()

        elif nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.NAMEDEXPR_TEST_FIRST_SET:
                self._parse_namedexpr_test()

            elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
                self._parse_star_expr()

            nxtok = self._lexer.peek_token()

            while nxtok.type == "COMMA":

                self._expect("COMMA")
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()

                if nxtok.type in Parser.NAMEDEXPR_TEST_FIRST_SET:
                    self._parse_namedexpr_test()

                elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
                    self._parse_star_expr()

                else:
                    break

                nxtok = self._lexer.peek_token()
    
    """
    trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
    """
    def _parse_trailer(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":
            
            self._expect("LPAREN")

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.ARGLIST_FIRST_SET:
                
                self._parse_arglist()
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()

            self._expect("RPAREN")
        elif nxtok.type == "LBRACKET":
            self._expect("LBRACKET")
            self._parse_subscriptlist()
            self._expect("RBRACKET")

        elif nxtok.type == "DOT":
            self._expect("DOT")
            self._expect("NAME")

        else:
            self._syntax_error({ "LPAREN", "LBRACKET", "DOT" }, nxtok.type)

    """
    subscriptlist: subscript (',' subscript)* [',']
    """
    def _parse_subscriptlist(self):

        self._parse_subscript()
        nxtok = self._lexer.peek_token()
        
        while nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.SUBSCRIPT_FIRST_SET:
                self._parse_subscript()

            else:
                break

            nxtok = self._lexer.peek_token()
    
    """
    subscript: test | [test] ':' [test] [sliceop]
    """
    def _parse_subscript(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:

            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "COLON":

                self._expect("COLON")
                nxtok = self._lexer.peek_token()

                if nxtok.type in Parser.TEST_FIRST_SET:
                    self._parse_test()
                    nxtok = self._lexer.peek_token()
                
                if nxtok.type in Parser.SLICEOP_FIRST_SET:
                    self._parse_sliceop()

        elif nxtok.type == "COLON":

            self._expect("COLON")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.TEST_FIRST_SET:
                self._parse_test()
                nxtok = self._lexer.peek_token()
            
            if nxtok.type in Parser.SLICEOP_FIRST_SET:
                self._parse_sliceop()
    
    """
    sliceop: ':' [test]
    """
    def _parse_sliceop(self):

        self._expect("COLON")

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:
            self._parse_test()
    
    """
    exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
    """
    def _parse_exprlist(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.EXPR_FIRST_SET:
            self._parse_expr()

        elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
            self._parse_star_expr()

        else:
            self._syntax_error(Parser.EXPR_FIRST_SET | Parser.STAR_EXPR_FIRST_SET, nxtok.type)
        
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.EXPR_FIRST_SET:
                self._parse_expr()

            elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
                self._parse_star_expr()

            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    """
    testlist: test (',' test)* [',']
    """
    def _parse_testlist(self):

        self._parse_test()

        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.TEST_FIRST_SET:
                self._parse_test()

            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    """
    dictorsetmaker: ( ((test ':' test | '**' expr)
        (comp_for | (',' (test ':' test | '**' expr))* [','])) |
        ((test | star_expr)
        (comp_for | (',' (test | star_expr))* [','])) )
    """
    def _parse_dictorsetmaker(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:

            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "COLON":

                self._expect("COLON")
                self._parse_test()

                nxtok = self._lexer.peek_token()

                if nxtok.type in Parser.COMP_FOR_FIRST_SET:
                    self._parse_comp_for()

                elif nxtok.type == "COMMA":

                    while nxtok.type == "COMMA":

                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()

                        while nxtok.type == "NEWLINE":
                            self._expect("NEWLINE")
                            nxtok = self._lexer.peek_token()

                        if nxtok.type in Parser.TEST_FIRST_SET:
                            self._parse_test()
                            self._expect("COLON")
                            self._parse_test()

                        elif nxtok.type == "POWER":
                            self._expect("POWER")
                            self._parse_expr()

                        else:
                            break

                        nxtok = self._lexer.peek_token()

            elif nxtok.type in Parser.COMP_FOR_FIRST_SET:
                self._parse_comp_for()

            elif nxtok.type == "COMMA":

                while nxtok.type == "COMMA":
                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    while nxtok.type == "NEWLINE":
                        self._expect("NEWLINE")
                        nxtok = self._lexer.peek_token()

                    if nxtok.type in Parser.TEST_FIRST_SET:
                        self._parse_test()

                    elif nxtok.type == Parser.STAR_EXPR_FIRST_SET:
                        self._parse_star_expr()

                    else:
                        break

                    nxtok = self._lexer.peek_token()

        elif nxtok.type == "POWER":

            self._expect("POWER")
            self._parse_expr()
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.COMP_FOR_FIRST_SET:
                self._parse_comp_for()

            elif nxtok.type == "COMMA":

                while nxtok.type == "COMMA":

                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type in Parser.TEST_FIRST_SET:
                        self._parse_test()

                    elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:
                        self._parse_star_expr()

                    else:
                        break

                    nxtok = self._lexer.peek_token()
            
        elif nxtok.type in Parser.STAR_EXPR_FIRST_SET:

            self._parse_star_expr()
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.COMP_FOR_FIRST_SET:
                self._parse_comp_for()

            elif nxtok.type == "COMMA":

                while nxtok.type == "COMMA":
                    
                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type in Parser.TEST_FIRST_SET:
                        self._parse_test()
                        self._expect("COLON")
                        self._parse_test()

                    elif nxtok.type == "POWER":
                        self._expect("POWER")
                        self._parse_expr()

                    else:
                        break

                    nxtok = self._lexer.peek_token()
        else:
            self._syntax_error(Parser.TEST_FIRST_SET | { "POWER" } | Parser.STAR_EXPR_FIRST_SET, nxtok.type)

    """
    classdef: 'class' NAME ['(' [arglist] ')'] ':' suite
    """
    def _parse_classdef(self):

        self._expect("CLASS")
        self._expect("NAME")

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":

            self._expect("LPAREN")
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.ARGLIST_FIRST_SET:
                self._parse_arglist()
            
            self._expect("RPAREN")
        
        self._expect("COLON")
        self._parse_suite()
    
    """
    arglist: argument (',' argument)*  [',']
    """
    def _parse_arglist(self):

        self._parse_argument()

        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":

            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.ARGUMENT_FIRST_SET:
                self._parse_argument()
                nxtok = self._lexer.peek_token()

            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    """
    argument: ( test [comp_for] |
        test ':=' test |
        test '=' test |
        '**' test |
        '*' test )
    """
    def _parse_argument(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.TEST_FIRST_SET:

            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type in Parser.COMP_FOR_FIRST_SET:
                self._parse_comp_for()

            elif nxtok.type == "WALRUS":
                self._expect("WALRUS")
                self._parse_test()

            elif nxtok.type == "EQUAL":
                self._expect("EQUAL")
                self._parse_test()

        elif nxtok.type == "POWER":
            self._expect("POWER")
            self._parse_test()

        elif nxtok.type == "ASTERISK":
            self._expect("ASTERISK")
            self._parse_test()

        else:
            self._syntax_error(Parser.TEST_FIRST_SET | { "POWER", "ASTERISK" }, nxtok.type)
    
    """
    comp_iter: comp_for | comp_if
    """
    def _parse_comp_iter(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.COMP_FOR_FIRST_SET:
            self._parse_comp_for()

        elif nxtok.type in Parser.COMP_IF_FIRST_SET:
            self._parse_comp_if()

        else:
            self._syntax_error(Parser.COMP_FOR_FIRST_SET | Parser.COMP_IF_FIRST_SET, nxtok.type)
    
    """
    sync_comp_for: 'for' exprlist 'in' or_test [comp_iter]
    """
    def _parse_sync_comp_for(self):

        self._expect("FOR")
        self._parse_exprlist()
        self._expect("IN")
        self._parse_or_test()

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.COMP_ITER_FIRST_SET:
            self._parse_comp_iter()
    
    """
    comp_for: [ASYNC] sync_comp_for
    """
    def _parse_comp_for(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ASYNC":
            self._expect("ASYNC")
        
        self._parse_sync_comp_for()

    """
    comp_if: 'if' test_nocond [comp_iter]
    """
    def _parse_comp_if(self):

        self._expect("IF")
        self._parse_test_nocond()

        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.COMP_ITER_FIRST_SET:
            self._parse_comp_iter()

    """
    yield_expr: 'yield' [yield_arg]
    """
    def _parse_yield_expr(self):

        self._expect("YIELD")
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.YIELD_ARG_FIRST_SET:
            self._parse_yield_arg()
    
    """
    yield_arg: 'from' test | testlist_star_expr
    """
    def _parse_yield_arg(self):

        nxtok = self._lexer.peek_token()

        if nxtok.type == "FROM":
            self._expect("FROM")
            self._parse_test()

        elif nxtok.type in Parser.TESTLIST_STAR_EXPR_FIRST_SET:
            self._parse_testlist_star_expr()

        else:
            self._syntax_error({ "FROM" } | Parser.TESTLIST_STAR_EXPR_FIRST_SET, nxtok.type)

    """
    func_body_suite: simple_stmt | NEWLINE [TYPE_COMMENT NEWLINE] INDENT stmt+ DEDENT
    """
    def _parse_func_body_suite(self):
        
        nxtok = self._lexer.peek_token()

        if nxtok.type in Parser.SIMPLE_STMT_FIRST_SET:
            self._parse_simple_stmt()

        elif nxtok.type == "NEWLINE":

            self._expect("NEWLINE")
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type == "STRING":
                self._expect("STRING")
                self._expect("NEWLINE")
            
            self._expect_indent()
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()
            
            while nxtok.type in Parser.STMT_FIRST_SET and nxtok.indent == self._indent_level:

                self._parse_stmt()
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()
            
            if nxtok.indent > self._indent_level:
                self._syntax_error(Parser.INDENT_LEVEL_STR % self._indent_level, nxtok.indent)

            else:
                self._indent_level -= 1

        else:
            self._syntax_error(Parser.SIMPLE_STMT_FIRST_SET | { "NEWLINE" }, nxtok.type)
