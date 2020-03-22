from pylexer import Lexer

class Parser:
    def __init__(self, source):
        self._lexer = Lexer(source)
        self._indent_level = 0
    
    def _syntax_error(self, expected, actual):
        raise Exception("Syntax Error at line %d: Expected %s; Received %s" % (self._lexer.get_line_number(), expected, actual)) 
    
    def _expect(self, expected_list):
        nxtok = self._lexer.get_token()

        if nxtok.type in expected_list:
            return nxtok.content
        
        self._syntax_error(expected_list, nxtok.type)
    
    def _expect_indent(self, indent_direction=1):
        nxtok = self._lexer.peek_token()
        expected = self._indent_level + indent_direction

        if nxtok.indent == expected:
            self._indent_level = expected
        else:
            self._syntax_error("Indent level %d" % expected, "Indent level %d" % nxtok.indent)
    
    def parse(self):
        nxtok = self._lexer.peek_token()
        stmt_first_set = { 
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

        while nxtok.type != "EOF":
            if nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
            elif nxtok.type in stmt_first_set:
                self._parse_stmt()
            else:
                self._syntax_error(list(stmt_first_set) + ["NEWLINE"], nxtok.type)
            
            nxtok = self._lexer.peek_token()

    def _parse_decorator(self):
        self._expect("AT")
        self._parse_dotted_name()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":
            self._expect("LPAREN")

            arglist_first_set = { 
                "NOT", "PLUS", "MINUS", 
                "TILDE", "AWAIT", "LPAREN", 
                "LBRACKET", "LBRACE", "NAME", 
                "NUMBER", "STRING", "ELLIPSIS", 
                "NONE", "TRUE", "FALSE", 
                "LAMBDA", "POWER", "ASTERISK"
            }

            nxtok = self._lexer.peek_token()

            if nxtok.type in arglist_first_set:
                self._parse_arglist()
            
            self._expect("RPAREN")

        self._expect("NEWLINE")
    
    def _parse_decorators(self):
        self._parse_decorator()

        nxtok = self._lexer.peek_token()
        decorator_first_set = { "AT" }

        if nxtok.type in decorator_first_set:
            self._parse_decorators()
    
    def _parse_decorated(self):
        self._parse_decorators()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "CLASS":
            self._parse_classdef()
        elif nxtok.type == "DEF":
            self._parse_funcdef()
        else:
            self._parse_async_funcdef()
    
    def _parse_async_funcdef(self):
        self._expect("ASYNC")
        self._parse_funcdef()
    
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
    
    def _parse_parameters(self):
        self._expect("LPAREN")
        
        typedargslist_first_set = { "NAME", "POWER", "ASTERISK" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in typedargslist_first_set:
            self._parse_typedargslist()

        self._expect("RPAREN")
    
    def _parse_typedargslist(self):
        tfpdef_first_set = { "NAME" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in tfpdef_first_set:
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
                
                while nxtok.type in tfpdef_first_set:
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

                        if nxtok.type == "STRING" or nxtok.type in tfpdef_first_set:
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
                                
                                while nxtok.type in tfpdef_first_set:
                                    self._parse_tfpdef()
                                    nxtok = self._lexer.peek_token()

                                    if nxtok.type == "EQUAL":
                                        self._expect("EQUAL")
                                        self._parse_test()
                                        nxtok = self._lexer.peek_token()

                                    if nxtok.type == "STRING":
                                        self._expect("STRING")
                                        parse_end = True
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

                                    if nxtok.type in tfpdef_first_set:
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

                            if nxtok.type in tfpdef_first_set:
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

                    if nxtok.type in tfpdef_first_set:
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

            if nxtok.type in tfpdef_first_set:
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
            self._syntax_error(list(tfpdef_first_set) + [ "ASTERISK", "POWER" ], nxtok.type)

    def _parse_tfpdef(self):
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        if nxtok.type == "COLON":
            self._expect("COLON")
            self._parse_test()
    
    def _parse_varargslist(self):
        nxtok = self._lexer.peek_token()
        vfpdef_first_set = { "NAME" }

        if nxtok.type == "ASTERISK":
            self._expect("ASTERISK")
            nxtok = self._lexer.peek_token()

            if nxtok.type in vfpdef_first_set:
                self._parse_vfpdef()
                nxtok = self._lexer.peek_token()
            
            if nxtok.type == "COMMA":
                self._expect("COMMA")
                
                nxtok = self._lexer.peek_token()

                if nxtok.type in vfpdef_first_set:
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
                    self._syntax_error(list(vfpdef_first_set) + [ "POWER" ], nxtok.type)

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

                if nxtok.type in vfpdef_first_set:
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

                    if nxtok.type in vfpdef_first_set:
                        self._parse_vfpdef()
                        nxtok = self._lexer.peek_token()
                    
                    if nxtok.type == "COMMA":
                        self._expect("COMMA")
                        
                        nxtok = self._lexer.peek_token()

                        if nxtok.type in vfpdef_first_set:
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
                            self._syntax_error(list(vfpdef_first_set) + [ "POWER" ], nxtok.type)

                elif nxtok.type == "POWER":
                    self._expect("POWER")
                    self._parse_vfpdef()
                    nxtok = self._lexer.peek_token()

                    if nxtok.type == "COMMA":
                        self._expect("COMMA")

                else:
                    self._syntax_error(list(vfpdef_first_set) + [ "ASTERISK", "POWER" ], nxtok.type)
    
    def _parse_vfpdef(self):
        self._expect("NAME")
    
    def _parse_stmt(self):
        simple_stmt_first_set = { 
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

        compound_stmt_first_set = { 
            "IF", "WHILE", "FOR", 
            "TRY", "WITH", "DEF", 
            "CLASS", "AT", "ASYNC" 
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type in simple_stmt_first_set:
            self._parse_simple_stmt()
        elif nxtok.type in compound_stmt_first_set:
            self._parse_compound_stmt()
        else:
            self._syntax_error(list(simple_stmt_first_set) + list(compound_stmt_first_set), nxtok.type)
    
    def _parse_simple_stmt(self):
        self._parse_small_stmt()
        nxtok = self._lexer.peek_token()

        small_stmt_first_set = { 
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

        while nxtok.type == "SEMICOLON":
            self._expect("SEMICOLON")
            nxtok = self._lexer.peek_token()

            if nxtok.type in small_stmt_first_set:
                self._parse_small_stmt()
                nxtok = self._lexer.peek_token()
            else:
                break

    def _parse_small_stmt(self):
        expr_stmt_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA", "ASTERISK"
        }

        del_stmt_first_set = { "DEL" }
        pass_stmt_first_set = { "PASS" }
        flow_stmt_first_set = { "BREAK", "CONTINUE", "RETURN", "RAISE", "YIELD" }
        import_stmt_first_set = { "IMPORT", "FROM" }
        global_stmt_first_set = { "GLOBAL" }
        nonlocal_stmt_first_set = { "NONLOCAL" }
        assert_stmt_first_set = { "ASSERT" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in expr_stmt_first_set: self._parse_expr_stmt()
        elif nxtok.type in del_stmt_first_set: self._parse_del_stmt()
        elif nxtok.type in pass_stmt_first_set: self._parse_pass_stmt()
        elif nxtok.type in flow_stmt_first_set: self._parse_flow_stmt()
        elif nxtok.type in import_stmt_first_set: self._parse_import_stmt()
        elif nxtok.type in global_stmt_first_set: self._parse_global_stmt()
        elif nxtok.type in nonlocal_stmt_first_set: self._parse_nonlocal_stmt()
        elif nxtok.type in assert_stmt_first_set: self._parse_assert_stmt()
        else:
            self._syntax_error(
                list(expr_stmt_first_set)
                + list(del_stmt_first_set)
                + list(pass_stmt_first_set)
                + list(flow_stmt_first_set)
                + list(import_stmt_first_set)
                + list(global_stmt_first_set)
                + list(nonlocal_stmt_first_set)
                + list(assert_stmt_first_set)
                , nxtok.type
            )

    def _parse_expr_stmt(self):
        self._parse_testlist_star_expr()
        annassign_first_set = { "COLON" }
        augassign_first_set = {
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

        yeild_expr_first_set = { "YIELD" }
        testlist_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type in annassign_first_set:
            self._parse_annasign()
        elif nxtok.type in augassign_first_set:
            self._parse_augassign()
            nxtok = self._lexer.peek_token()

            if nxtok.type in yeild_expr_first_set:
                self._parse_yield_expr()
            elif nxtok.type in testlist_first_set:
                self._parse_testlist()
            else:
                self._parse_syntax_error(list(yeild_expr_first_set) + list(testlist_first_set), nxtok.type)
            
        elif nxtok.type == "EQUAL":
            while nxtok.type == "EQUAL":
                self._expect("EQUAL")
                nxtok = self._lexer.peek_token()

                if nxtok.type in yeild_expr_first_set:
                    self._parse_yield_expr()
                else:
                    self._parse_testlist_star_expr()
                
                nxtok = self._lexer.peek_token()
            
            if nxtok.type == "STRING":
                self._expect("STRING")
    
    def _parse_annasign(self):
        self._expect("COLON")
        self._parse_test()
        nxtok = self._lexer.peek_token()
        yeild_expr_first_set = { "YIELD" }

        if nxtok.type == "EQUAL":
            self._expect("EQUAL")
            nxtok = self._lexer.peek_token()

            if nxtok.type in yeild_expr_first_set:
                self._parse_yeild_expr()
            else:
                self._parse_testlist_star_expr()
    
    def _parse_testlist_star_expr(self):
        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        star_expr_first_set = { "ASTERISK" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in test_first_set:
            self._parse_test()
        elif nxtok.type in star_expr_first_set:
            self._parse_star_expr()
        else:
            self._syntax_error(list(test_first_set) + list(star_expr_first_set), nxtok.type)
        
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in test_first_set:
                self._parse_test()
            elif nxtok.type in star_expr_first_set:
                self._parse_star_expr()
            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    def _parse_augassign(self):
        self._expect({
            "PLUS_EQUALS",
            "MINUS_EQUALS",
            "TIMES_EQUALS",
            "AT_EQUALS",
            "DIVIDE_EQUALS",
            "MODULUS_EQUALS",
            "AND_EQUALS",
            "OR_EQUALS",
            "XOR_EQUALS",
            "SHIFT_LEFT_EQUALS",
            "SHIFT_RIGHT_EQUALS",
            "POWER_EQUALS",
            "FLOOR_DIVIDE_EQUALS"
        })
    
    def _parse_del_stmt(self):
        self._expect("DEL")
        self._parse_exprlist()
    
    def _parse_pass_stmt(self):
        self._expect("PASS")
    
    def _parse_flow_stmt(self):
        break_stmt_first_set = { "BREAK" }
        continue_stmt_first_set = { "CONTINUE" }
        return_stmt_first_set = { "RETURN" }
        raise_stmt_first_set = { "RAISE" }
        yeild_stmt_first_set = { "YIELD" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in break_stmt_first_set:
            self._parse_break_stmt()
        elif nxtok.type in continue_stmt_first_set:
            self._parse_continue_stmt()
        elif nxtok.type in return_stmt_first_set:
            self._parse_return_stmt()
        elif nxtok.type in raise_stmt_first_set:
            self._parse_raise_stmt()
        elif nxtok.type in yeild_stmt_first_set:
            self._parse_yeild_stmt()
        else:
            self._syntax_error(
                list(break_stmt_first_set)
                + list(continue_stmt_first_set)
                + list(return_stmt_first_set)
                + list(raise_stmt_first_set)
                + list(yeild_stmt_first_set)
                , nxtok.type
            )
    
    def _parse_break_stmt(self):
        self._expect("BREAK")
    
    def _parse_continue_stmt(self):
        self._expect("CONTINUE")
    
    def _parse_return_stmt(self):
        self._expect("RETURN")

        testlist_star_expr_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA", "ASTERISK"
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type in testlist_star_expr_first_set:
            self._parse_testlist_star_expr()
    
    def _parse_yeild_stmt(self):
        self._parse_yeild_expr()
    
    def _parse_raise_stmt(self):
        self._expect("RAISE")
        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type in test_first_set:
            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "FROM":
                self._expect("FROM")
                self._parse_test()
    
    def _parse_import_stmt(self):
        import_name_first_set = { "IMPORT" }
        import_from_first_set = { "FROM" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in import_name_first_set:
            self._parse_import_name()
        elif nxtok.type in import_from_first_set:
            self._parse_import_from()
        else:
            self._syntax_error(list(import_name_first_set) + list(import_from_first_set), nxtok.type)
    
    def _parse_import_name(self):
        self._expect("IMPORT")
        self._parse_dotted_as_names()
    
    def _parse_import_from(self):
        self._expect("FROM")
        nxtok = self._lexer.peek_token()
        dot_or_ellipsis_found = False
        dotted_name_first_set = { "NAME" }

        while nxtok.type in { "DOT", "ELLIPSIS" }:
            dot_or_ellipsis_found = True
            self._expect({ "DOT", "ELLIPSIS" })
            nxtok = self._lexer.peek_token()
        
        if dot_or_ellipsis_found:
            nxtok = self._lexer.peek_token()

            if nxtok.type in dotted_name_first_set:
                self._parse_dotted_name()
        else:
            self._parse_dotted_name()
        
        self._expect("IMPORT")
        import_as_names_first_set = { "NAME" }

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ASTERISK":
            self._expect("ASTERISK")
        elif nxtok.type == "LPAREN":
            self._expect("LPAREN")
            self._parse_import_as_names()
            self._expect("RPAREN")
        elif nxtok.type in import_as_names_first_set:
            self._parse_import_as_names()
        else:
            self._syntax_error([ "ASTERISK", "LPAREN" ] + list(import_as_names_first_set), nxtok.type)
    
    def _parse_import_as_name(self):
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        if nxtok.type == "AS":
            self._expect("AS")
            self._expect("NAME")
    
    def _parse_dotted_as_name(self):
        self._parse_dotted_name()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "AS":
            self._expect("AS")
            self._expect("NAME")
    
    def _parse_import_as_names(self):
        self._parse_import_as_name()
        nxtok = self._lexer.peek_token()
        import_as_name_first_set = { "NAME" }

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in import_as_name_first_set:
                self._parse_import_as_name()
                nxtok = self._lexer.peek_token()
            else:
                break
    
    def _parse_dotted_as_names(self):
        self._parse_dotted_as_name()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._parse_dotted_as_name()
            nxtok = self._lexer.peek_token()
    
    def _parse_dotted_name(self):
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        while nxtok.type == "DOT":
            self._expect("DOT")
            self._expect("NAME")
            nxtok = self._lexer.peek_token()
    
    def _parse_global_stmt(self):
        self._expect("GLOBAL")
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._expect("NAME")
            nxtok = self._lexer.peek_token()
    
    def _parse_nonlocal_stmt(self):
        self._expect("NONLOCAL")
        self._expect("NAME")
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            self._expect("NAME")
            nxtok = self._lexer.peek_token()
    
    def _parse_assert_stmt(self):
        self._expect("ASSERT")
        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "COMMA":
            self._expect("COMMA")
            self._parse_test()
    
    def _parse_compound_stmt(self):
        if_stmt_first_set = { "IF" }
        while_stmt_first_set = { "WHILE" }
        for_stmt_first_set = { "FOR" }
        try_stmt_first_set = { "TRY" }
        with_stmt_first_set = { "WITH" }
        funcdef_first_set = { "DEF" }
        classdef_first_set = { "CLASS" }
        decorated_first_set = { "AT" }
        async_stmt_first_set = { "ASYNC" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in if_stmt_first_set:
            self._parse_if_stmt()
        elif nxtok.type in while_stmt_first_set:
            self._parse_while_stmt()
        elif nxtok.type in for_stmt_first_set:
            self._parse_for_stmt()
        elif nxtok.type in try_stmt_first_set:
            self._parse_try_stmt()
        elif nxtok.type in with_stmt_first_set:
            self._parse_with_stmt()
        elif nxtok.type in funcdef_first_set:
            self._parse_funcdef()
        elif nxtok.type in classdef_first_set:
            self._parse_classdef()
        elif nxtok.type in decorated_first_set:
            self._parse_decorated()
        elif nxtok.type in async_stmt_first_set:
            self._parse_async_stmt()
        else:
            self._syntax_error(
                list(if_stmt_first_set)
                + list(while_stmt_first_set)
                + list(for_stmt_first_set)
                + list(try_stmt_first_set)
                + list(with_stmt_first_set)
                + list(funcdef_first_set)
                + list(classdef_first_set)
                + list(decorated_first_set)
                + list(async_stmt_first_set)
                , nxtok.type
            )

    def _parse_async_stmt(self):
        self._expect("ASYNC")
        for_stmt_first_set = { "FOR" }
        with_stmt_first_set = { "WITH" }
        funcdef_first_set = { "DEF" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in for_stmt_first_set:
            self._parse_for_stmt()
        elif nxtok.type in with_stmt_first_set:
            self._parse_with_stmt()
        elif nxtok.type in funcdef_first_set:
            self._parse_funcdef()
        else:
            self._syntax_error(
                list(for_stmt_first_set)
                + list(with_stmt_first_set)
                + list(funcdef_first_set),
                nxtok.type
            )
    
    def _parse_if_stmt(self):
        self._expect("IF")
        self._parse_namedexpr_test()
        self._expect("COLON")
        self._parse_suite()
        
        nxtok = self._lexer.peek_token()

        while nxtok.type == "ELIF" and nxtok.indent == self._indent_level:
            self._expect("ELIF")
            self._parse_namedexpr_test()
            self._expect("COLON")
            self._parse_suite()
            nxtok = self._lexer.peek_token()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ELSE" and nxtok.indent == self._indent_level:
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    def _parse_while_stmt(self):
        self._expect("WHILE")
        self._parse_namedexpr_test()
        self._expect("COLON")
        self._parse_suite()

        nxtok = self._lexer.peek_token()

        if nxtok.type == "ELSE":
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
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
    
    def _parse_try_stmt(self):        
        self._expect("TRY")
        self._expect("COLON")
        self._parse_suite()

        nxtok = self._lexer.peek_token()
        except_clause_first_set = { "EXCEPT" } 

        if nxtok.type in except_clause_first_set:
            self._parse_except_clause()
            self._expect("COLON")
            self._parse_suite()

            nxtok = self._lexer.peek_token()

            while nxtok.type in except_clause_first_set:
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
            self._syntax_error(list(except_clause_first_set) + [ "FINALLY" ], nxtok.type)
    
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
    
    def _parse_with_item(self):
        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "AS":
            self._expect("AS")
            self._parse_expr()
    
    def _parse_except_clause(self):
        self._expect("EXCEPT")
        nxtok = self._lexer.peek_token()

        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        if nxtok.type in test_first_set:
            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "AS":
                self._expect("AS")
                self._expect("NAME")
        
    def _parse_suite(self):
        simple_stmt_first_set = { 
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

        stmt_first_set = { 
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

        nxtok = self._lexer.peek_token()

        if nxtok.type in simple_stmt_first_set:
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

            while nxtok.type in stmt_first_set and nxtok.indent == self._indent_level:
                self._parse_stmt()
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()
            
            if nxtok.indent > self._indent_level:
                self._syntax_error("Indent level %d" % self._indent_level, nxtok.indent)
            else:
                self._indent_level -= 1

        else:
            self._syntax_error(list(simple_stmt_first_set) + [ "NEWLINE" ], nxtok.type)
    
    def _parse_namedexpr_test(self):
        self._parse_test()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "WALRUS":
            self._expect("WALRUS")
            self._parse_test()
    
    def _parse_test(self):
        or_test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE" 
        }

        lambdef_first_set = { "LAMBDA" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in or_test_first_set:
            current_line_number = self._lexer.get_line_number()

            self._parse_or_test()

            if self._lexer.get_line_number() == current_line_number:
                nxtok = self._lexer.peek_token()

                if nxtok.type == "IF":
                    self._expect("IF")
                    self._parse_or_test()
                    self._expect("ELSE")
                    self._parse_test()

        elif nxtok.type in lambdef_first_set:
            self._parse_lambdef()
        else:
            self._syntax_error(list(or_test_first_set) + list(lambdef_first_set), nxtok.type)
    
    def _parse_test_nocond(self):
        or_test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE" 
        }

        lambdef_nocond_first_set = { "LAMBDA" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in or_test_first_set:
            self._parse_or_test()
        elif nxtok.type in lambdef_nocond_first_set:
            self.parse_lambdef_nocond()
        else:
            self._syntax_error(list(or_test_first_set) + list(lambdef_nocond_first_set), nxtok.type)
    
    def _parse_lambdef(self):
        self._expect("LAMBDA")
        varargslist_first_set = { "NAME", "ASTERISK", "POWER" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in varargslist_first_set:
            self._parse_varargslist()
            nxtok = self._lexer.peek_token()
        
        self._expect("COLON")
        self._parse_test()
    
    def _parse_lambdef_nocond(self):
        self._expect("LAMBDA")
        varargslist_first_set = { "NAME", "ASTERISK", "POWER" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in varargslist_first_set:
            self._parse_varargslist()
            nxtok = self._lexer.peek_token()
        
        self._expect("COLON")
        self._parse_test_nocond()
    
    def _parse_or_test(self):
        self._parse_and_test()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "OR":
            self._expect("OR")
            self._parse_and_test()
            nxtok = self._lexer.peek_token()
    
    def _parse_and_test(self):
        self._parse_not_test()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "AND":
            self._expect("AND")
            self._parse_not_test()
            nxtok = self._lexer.peek_token()
    
    def _parse_not_test(self):
        comparison_first_set = { 
            "PLUS", "MINUS", "TILDE", 
            "AWAIT", "LPAREN", "LBRACKET", 
            "LBRACE", "NAME", "NUMBER", 
            "STRING", "ELLIPSIS", "NONE", 
            "TRUE", "FALSE"
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type == "NOT":
            self._expect("NOT")
            self._parse_not_test()
        elif nxtok.type in comparison_first_set:
            self._parse_comparison()
    
    def _parse_comparison(self):
        self._parse_expr()
        
        comp_op_first_set = {
            "LESS_THAN", "GREATER_THAN", "DOUBLE_EQUALS",
            "GEQ", "LEQ", "NOT_EQUALS", 
            "IN", "NOT", "IS"
        }

        nxtok = self._lexer.peek_token()

        while nxtok.type in comp_op_first_set:
            self._parse_comp_op()
            self._parse_expr()
            nxtok = self._lexer.peek_token()
    
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
                "GREATER_THAN",
                "LESS_THAN",
                "DOUBLE_EQUALS",
                "GEQ",
                "LEQ",
                "NOT_EQUALS",
                "IN",
                "IS"
            ])
    
    def _parse_star_expr(self):
        self._expect("ASTERISK")
        self._parse_expr()
    
    def _parse_expr(self):
        self._parse_xor_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "PIPE":
            self._expect("PIPE")
            self._parse_xor_expr()
            nxtok = self._lexer.peek_token()
    
    def _parse_xor_expr(self):
        self._parse_and_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "CARROT":
            self._expect("CARROT")
            self._parse_and_expr()
            nxtok = self._lexer.peek_token()
    
    def _parse_and_expr(self):
        self._parse_shift_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "AMPERSAND":
            self._expect("AMPERSAND")
            self._parse_shift_expr()
            nxtok = self._lexer.peek_token()
    
    def _parse_shift_expr(self):
        self._parse_arith_expr()
        nxtok = self._lexer.peek_token()

        while nxtok.type in { "SHIFT_LEFT", "SHIFT_RIGHT" }:
            if nxtok.type == "SHIFT_LEFT":
                self._expect("SHIFT_LEFT")
            elif nxtok.type == "SHIFT_RIGHT":
                self._expect("SHIFT_RIGHT")

            self._parse_arith_expr()
            nxtok = self._lexer.peek_token()
    
    def _parse_arith_expr(self):
        self._parse_term()
        nxtok = self._lexer.peek_token()

        while nxtok.type in { "PLUS", "MINUS" }:
            if nxtok.type == "PLUS":
                self._expect("PLUS")
            elif nxtok.type == "MINUS":
                self._expect("MINUS")

            self._parse_term()
            nxtok = self._lexer.peek_token()
    
    def _parse_term(self):
        self._parse_factor()
        nxtok = self._lexer.peek_token()

        while nxtok.type in { "ASTERISK", "AT", "SLASH", "PERCENT", "FLOOR_DIVISION" }:
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

            self._parse_factor()
            nxtok = self._lexer.peek_token()
    
    def _parse_factor(self):
        power_first_set = { 
            "AWAIT", "LPAREN", "LBRACKET", 
            "LBRACE", "NAME", "NUMBER", 
            "STRING", "ELLIPSIS", "NONE", 
            "TRUE", "FALSE" 
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type in { "PLUS", "MINUS", "TILDE" }:
            if nxtok.type == "PLUS":
                self._expect("PLUS")
            elif nxtok.type == "MINUS":
                self._expect("MINUS")
            elif nxtok.type == "TILDE":
                self._expect("TILDE")
            
            self._parse_factor()

        elif nxtok.type in power_first_set:
            self._parse_power()
        
        else:
            self._syntax_error([ "PLUS", "MINUS", "TILDE" ] + list(power_first_set), nxtok.type)
    
    def _parse_power(self):
        self._parse_atom_expr()
        nxtok = self._lexer.peek_token()

        if nxtok.type == "POWER":
            self._expect("POWER")
            self._parse_factor()
    
    def _parse_atom_expr(self):
        trailer_first_set = { "LPAREN", "LBRACKET", "DOT" }
        nxtok = self._lexer.peek_token()
        
        if nxtok.type == "AWAIT":
            self._expect("AWAIT")
        
        self._parse_atom()
        nxtok = self._lexer.peek_token()

        while nxtok.type == "NEWLINE":
            self._expect("NEWLINE")
            nxtok = self._lexer.peek_token()

        while nxtok.type in trailer_first_set:
            self._parse_trailer()
            nxtok = self._lexer.peek_token()
    
    def _parse_atom(self):
        testlist_comp_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", "LAMBDA" 
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":
            self._expect("LPAREN")
            yeild_expr_first_set = { "YIELD" }

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in yeild_expr_first_set:
                self._parse_yield_expr()
                nxtok = self._lexer.peek_token()
            elif nxtok.type in testlist_comp_first_set:
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

            if nxtok.type in testlist_comp_first_set:
                self._parse_testlist_comp()
                nxtok = self._lexer.peek_token()
            
            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()
            
            self._expect("RBRACKET")
        elif nxtok.type == "LBRACE":
            self._expect("LBRACE")

            dictorsetmaker_first_set = { 
                "NOT", "PLUS", "MINUS", 
                "TILDE", "AWAIT", "LPAREN", 
                "LBRACKET", "LBRACE", "NAME", 
                "NUMBER", "STRING", "ELLIPSIS", 
                "NONE", "TRUE", "FALSE", 
                "LAMBDA", "POWER", "ASTERISK" 
            }

            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in dictorsetmaker_first_set:
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
            self._syntax_error([
                "LPAREN",
                "LBRACKET",
                "LBRACE",
                "NAME",
                "NUMBER",
                "STRING",
                "ELLIPSIS",
                "NONE",
                "TRUE",
                "FALSE"
            ], nxtok.type)
    
    def _parse_testlist_comp(self):        
        namedexpr_test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        star_expr_first_set = { "ASTERISK" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in namedexpr_test_first_set:
            self._parse_namedexpr_test()
        elif nxtok.type in star_expr_first_set:
            self._parse_star_expr()
        else:
            self._syntax_error(list(namedexpr_test_first_set) + list(star_expr_first_set), nxtok.type)
        
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

            if nxtok.type in namedexpr_test_first_set:
                self._parse_namedexpr_test()
            elif nxtok.type in star_expr_first_set:
                self._parse_star_expr()

            nxtok = self._lexer.peek_token()

            while nxtok.type == "COMMA":
                self._expect("COMMA")
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()

                if nxtok.type in namedexpr_test_first_set:
                    self._parse_namedexpr_test()
                elif nxtok.type in star_expr_first_set:
                    self._parse_star_expr()
                else:
                    break

                nxtok = self._lexer.peek_token()
    
    def _parse_trailer(self):
        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":
            self._expect("LPAREN")

            arglist_first_set = {
                "NOT", "PLUS", "MINUS",
                "TILDE", "AWAIT", "LPAREN", 
                "LBRACKET", "LBRACE", "NAME", 
                "NUMBER", "STRING", "ELLIPSIS", 
                "NONE", "TRUE", "FALSE", 
                "LAMBDA", "POWER", "ASTERISK"
            }

            nxtok = self._lexer.peek_token()

            if nxtok.type in arglist_first_set:
                self._parse_arglist()
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
            self._syntax_error([ "LPAREN", "LBRACKET", "DOT" ], nxtok.type)

    def _parse_subscriptlist(self):
        self._parse_subscript()
        nxtok = self._lexer.peek_token()

        subscript_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA", "COLON"
        }
        
        while nxtok.type == "COMMA":
            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in subscript_first_set:
                self._parse_subscript()
            else:
                break

            nxtok = self._lexer.peek_token()
    
    def _parse_subscript(self):
        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        sliceop_first_set = { "COLON" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in test_first_set:
            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "COLON":
                self._expect("COLON")
                nxtok = self._lexer.peek_token()

                if nxtok.type in test_first_set:
                    self._parse_test()
                    nxtok = self._lexer.peek_token()
                
                if nxtok.type in sliceop_first_set:
                    self._parse_sliceop()

        elif nxtok.type == "COLON":
            self._expect("COLON")
            nxtok = self._lexer.peek_token()

            if nxtok.type in test_first_set:
                self._parse_test()
                nxtok = self._lexer.peek_token()
            
            if nxtok.type in sliceop_first_set:
                self._parse_sliceop()
    
    def _parse_sliceop(self):
        self._expect("COLON")

        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type in test_first_set:
            self._parse_test()
    
    def _parse_exprlist(self):
        expr_first_set = { 
            "PLUS", "MINUS", "TILDE", 
            "AWAIT", "LPAREN", "LBRACKET", 
            "LBRACE", "NAME", "NUMBER", 
            "STRING", "ELLIPSIS", "NONE", 
            "TRUE", "FALSE"
        }

        star_expr_first_set = { "ASTERISK" }
        nxtok = self._lexer.peek_token()

        if nxtok.type in expr_first_set:
            self._parse_expr()
        elif nxtok.type in star_expr_first_set:
            self._parse_star_expr()
        else:
            self._syntax_error(list(expr_first_set) + list(star_expr_first_set), nxtok.type)
        
        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in expr_first_set:
                self._parse_expr()
            elif nxtok.type in star_expr_first_set:
                self._parse_star_expr()
            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    def _parse_testlist(self):
        self._parse_test()
        
        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            if nxtok.type in test_first_set:
                self._parse_test()
            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    def _parse_dictorsetmaker(self):
        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        star_expr_first_set = { "ASTERISK" }
        comp_for_first_set = { "ASYNC", "FOR" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in test_first_set:
            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type == "COLON":
                self._expect("COLON")
                self._parse_test()

                nxtok = self._lexer.peek_token()

                if nxtok.type in comp_for_first_set:
                    self._parse_comp_for()
                elif nxtok.type == "COMMA":
                    while nxtok.type == "COMMA":
                        self._expect("COMMA")
                        nxtok = self._lexer.peek_token()

                        while nxtok.type == "NEWLINE":
                            self._expect("NEWLINE")
                            nxtok = self._lexer.peek_token()

                        if nxtok.type in test_first_set:
                            self._parse_test()
                            self._expect("COLON")
                            self._parse_test()
                        elif nxtok.type == "POWER":
                            self._expect("POWER")
                            self._parse_expr()
                        else:
                            break

                        nxtok = self._lexer.peek_token()
            elif nxtok.type in comp_for_first_set:
                self._parse_comp_for()
            elif nxtok.type == "COMMA":
                while nxtok.type == "COMMA":
                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    while nxtok.type == "NEWLINE":
                        self._expect("NEWLINE")
                        nxtok = self._lexer.peek_token()

                    if nxtok.type in test_first_set:
                        self._parse_test()
                    elif nxtok.type == star_expr_first_set:
                        self._parse_star_expr()
                    else:
                        break

                    nxtok = self._lexer.peek_token()

        elif nxtok.type == "POWER":
            self._expect("POWER")
            self._parse_expr()
            nxtok = self._lexer.peek_token()

            if nxtok.type in comp_for_first_set:
                self._parse_comp_for()
            elif nxtok.type == "COMMA":
                while nxtok.type == "COMMA":
                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type in test_first_set:
                        self._parse_test()
                    elif nxtok.type in star_expr_first_set:
                        self._parse_star_expr()
                    else:
                        break

                    nxtok = self._lexer.peek_token()
            
        elif nxtok.type in star_expr_first_set:
            self._parse_star_expr()
            nxtok = self._lexer.peek_token()

            if nxtok.type in comp_for_first_set:
                self._parse_comp_for()
            elif nxtok.type == "COMMA":
                while nxtok.type == "COMMA":
                    self._expect("COMMA")
                    nxtok = self._lexer.peek_token()

                    if nxtok.type in test_first_set:
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
            self._syntax_error(list(test_first_set) + [ "POWER" ] + list(star_expr_first_set), nxtok.type)

    def _parse_classdef(self):
        self._expect("CLASS")
        self._expect("NAME")

        arglist_first_set = { 
                "NOT", "PLUS", "MINUS", 
                "TILDE", "AWAIT", "LPAREN", 
                "LBRACKET", "LBRACE", "NAME", 
                "NUMBER", "STRING", "ELLIPSIS", 
                "NONE", "TRUE", "FALSE", 
                "LAMBDA", "POWER", "ASTERISK"
        }

        nxtok = self._lexer.peek_token()

        if nxtok.type == "LPAREN":
            self._expect("LPAREN")
            nxtok = self._lexer.peek_token()

            if nxtok.type in arglist_first_set:
                self._parse_arglist()
            
            self._expect("RPAREN")
        
        self._expect("COLON")
        self._parse_suite()
    
    def _parse_arglist(self):
        self._parse_argument()

        argument_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA", "POWER", "ASTERISK"
        }

        nxtok = self._lexer.peek_token()

        while nxtok.type == "COMMA":
            self._expect("COMMA")
            nxtok = self._lexer.peek_token()

            while nxtok.type == "NEWLINE":
                self._expect("NEWLINE")
                nxtok = self._lexer.peek_token()

            if nxtok.type in argument_first_set:
                self._parse_argument()
                nxtok = self._lexer.peek_token()
            else:
                break
            
            nxtok = self._lexer.peek_token()
    
    def _parse_argument(self):
        test_first_set = { 
            "NOT", "PLUS", "MINUS", 
            "TILDE", "AWAIT", "LPAREN", 
            "LBRACKET", "LBRACE", "NAME", 
            "NUMBER", "STRING", "ELLIPSIS", 
            "NONE", "TRUE", "FALSE", 
            "LAMBDA" 
        }

        comp_for_first_set = { "ASYNC", "FOR" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in test_first_set:
            self._parse_test()
            nxtok = self._lexer.peek_token()

            if nxtok.type in comp_for_first_set:
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
            self._syntax_error(list(test_first_set) + [ "POWER", "ASTERISK" ], nxtok.type)
    
    def _parse_comp_iter(self):
        comp_for_first_set = { "ASYNC", "FOR" }
        comp_if_first_set = { "IF" }

        nxtok = self._lexer.peek_token()

        if nxtok.type in comp_for_first_set:
            self._parse_comp_for()
        elif nxtok.type in comp_if_first_set:
            self._parse_comp_if()
        else:
            self._syntax_error(list(comp_for_first_set) + list(comp_if_first_set), nxtok.type)
    
    def _parse_sync_comp_for(self):
        comp_iter_first_set = { "ASYNC", "FOR", "IF" }

        self._expect("FOR")
        self._parse_exprlist()
        self._expect("IN")
        self._parse_or_test()

        nxtok = self._lexer.peek_token()

        if nxtok.type in comp_iter_first_set:
            self._parse_comp_iter()

    def _parse_comp_for(self):
        nxtok = self._lexer.peek_token()

        if nxtok.type == "ASYNC":
            self._expect("ASYNC")
        
        self._parse_sync_comp_for()

    def _parse_comp_if(self):
        comp_iter_first_set = { "ASYNC", "FOR", "IF" }

        self._expect("IF")
        self._parse_test_nocond()

        nxtok = self._lexer.peek_token()

        if nxtok.type in comp_iter_first_set:
            self._parse_comp_iter()

    def _parse_yield_expr(self):
        yield_arg_first_set = { "YIELD" }

        self._expect("YIELD")
        nxtok = self._lexer.peek_token()

        if nxtok.type in yield_arg_first_set:
            self._parse_yield_arg()
    
    def _parse_yield_arg(self):
        testlist_star_expr_first_set = []
        nxtok = self._lexer.peek_token()

        if nxtok.type == "FROM":
            self._expect("FROM")
            self._parse_test()
        elif nxtok.type in testlist_star_expr_first_set:
            self._parse_testlist_star_expr()
        else:
            self._syntax_error([ "FROM" ] + list(testlist_star_expr_first_set), nxtok.type)

    def _parse_func_body_suite(self):
        simple_stmt_first_set = { 
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

        stmt_first_set = { 
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

        nxtok = self._lexer.peek_token()

        if nxtok.type in simple_stmt_first_set:
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
            
            while nxtok.type in stmt_first_set and nxtok.indent == self._indent_level:
                self._parse_stmt()
                nxtok = self._lexer.peek_token()

                while nxtok.type == "NEWLINE":
                    self._expect("NEWLINE")
                    nxtok = self._lexer.peek_token()
            
            if nxtok.indent > self._indent_level:
                self._syntax_error("Indent level %d" % self._indent_level, nxtok.indent)
            else:
                self._indent_level -= 1

        else:
            self._syntax_error(list(simple_stmt_first_set) + [ "NEWLINE" ], nxtok.type)
