from pylexer import Lexer

class Parser:
    def __init__(self, source):
        self._lexer = Lexer(source)
        self._indent_level = 0
    
    def _syntax_error(self, expected, actual):
        raise Exception("Syntax Error: Expected %s; Received %s" % (expected, actual)) 
    
    def _expect(self, expected):
        self._expect([ expected ])
    
    def _expect(self, expected_list):
        token_string, token_type = self._lexer.get_token()

        if token_type in expected_list:
            return token_string
        
        self._syntax_error(expected_list, token_type)

    def _expect_indent(self, indent_direction=1):
        _, next_type = self._lexer.peek_token()
        tab_count = 0
        expected_tab_count = self._indent_level + indent_direction

        while next_type == "TAB":
            self._expect("TAB")
            tab_count += 1
            _, next_type = self._lexer.peek_token()
        
        if tab_count == expected_tab_count:
            self._indent_level = expected_tab_count
        else:
            self._syntax_error("Tab level %d" % expected_tab_count, "Tab level %d" % tab_count)

    def _expect_dedent(self):
        self._expect_indent(indent_direction=-1)
    
    def parse(self):
        token_str, next_type = self._lexer.peek_token()
        stmt_first_set = []

        while next_type != "EOF":
            if next_type == "NEWLINE":
                self._expect("NEWLINE")
            elif next_type in stmt_first_set:
                self._parse_stmt()
            else:
                self._syntax_error(stmt_first_set + ["NEWLINE"], next_type)
            
            _, next_type = self._lexer.peek_token()

    def _parse_decorator(self):
        self._expect("AT")
        self._parse_dotted_name()

        token_str, next_type = self._lexer.peek_token()

        if next_type == "LPAREN":
            self._expect("LPAREN")
            argslist_first_set = []

            _, next_type = self._lexer.peek_token()

            if next_type in argslist_first_set:
                self._parse_arglist()
            
            self._expect("RPAREN")

        self._expect("NEWLINE")
    
    def _parse_decorators(self):
        self._parse_decorator()

        _, next_type = self._lexer.peek_token()
        decorator_first_set = []

        if next_type in decorator_first_set:
            self._parse_decorators()
    
    def _parse_decorated(self):
        self._parse_decorators()

        _, next_type = self._lexer.get_token()

        if next_type == "CLASS":
            self._parse_classdef()
        elif next_type == "DEF":
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

        _, next_type = self._lexer.peek_token()

        if next_type == "ARROW":
            self._expect("ARROW")
            self._parse_test()
        
        self._expect("COLON")
        self._parse_suite()
    
    def _parse_parameters(self):
        self._expect("LPAREN")
        
        typedargslist_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in typedargslist_first_set:
            self._parse_typedargslist()

        self._expect("RPAREN")
    
    def _parse_typedargslist(self):
        tfpdef_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in tfpdef_first_set:
            self._parse_tfpdef()
            _, next_type = self._lexer.peek_token()

            if next_type == "EQUAL":
                self._expect("EQUAL")
                self._parse_test()
                _, next_type = self._lexer.peek_token()
            
            if next_type == "COMMA":
                self._expect("COMMA")
                _, next_type = self._lexer.peek_token()

                if next_type == "STRING":
                    self._expect("STRING")
                    _, next_type = self._lexer.peek_token()
                
                while next_type in tfpdef_first_set:
                    self._parse_tfpdef()
                    _, next_type = self._lexer.peek_token()

                    if next_type == "EQUAL":
                        self._expect("EQUAL")
                        self._parse_test()
                        _, next_type = self._lexer.peek_token()
                    
                    if next_type == "STRING":
                        self._expect("STRING")
                        return  
                    
                    self._expect("COMMA")
                    _, next_type = self._lexer.peek_token()

                    if next_type == "STRING":
                        self._expect("STRING")
                        _, next_type = self._lexer.peek_token()
                
                if next_type == "SLASH":
                    self._expect("SLASH")
                    _, next_type = self._lexer.peek_token()

                    if next_type == "COMMA":
                        self._expect("COMMA")
                        _, next_type = self._lexer.peek_token()

                        if next_type == "STRING" or next_type in tfpdef_first_set:
                            if next_type == "STRING":
                                self._expect("STRING")
                                _, next_type = self._lexer.peek_token()
                            
                            self._parse_tfpdef()
                            _, next_type = self._lexer.peek_token()

                            if next_type == "EQUAL":
                                self._expect("EQUAL")
                                self._parse_test()
                                _, next_type = self._lexer.peek_token()
                            
                            if next_type == "STRING":
                                self._expect("STRING")
                            elif next_type == "COMMA":
                                self._expect("COMMA")
                                _, next_type = self._lexer.peek_token()

                                if next_type == "STRING":
                                    self._expect("STRING")
                                    _, next_type = self._lexer.peek_token()
                                
                                while next_type in tfpdef_first_set:
                                    self._parse_tfpdef()
                                    _, next_type = self._lexer.peek_token()

                                    if next_type == "EQUAL":
                                        self._expect("EQUAL")
                                        self._parse_test()
                                        _, next_type = self._lexer.peek_token()

                                    if next_type == "STRING":
                                        self._expect("STRING")
                                        parse_end = True
                                        break
                                    
                                    self._expect("COMMA")
                                    _, next_type = self._lexer.peek_token()

                                    if next_type == "STRING":
                                        self._expect("STRING")
                                
                                if next_type == "STRING":
                                    self._expect("STRING")
                                elif next_type == "ASTERISK":
                                    self._expect("ASTERISK")
                                    _, next_type = self._lexer.peek_token()

                                    if next_type in tfpdef_first_set:
                                        self._parse_tfpdef()
                                        _, next_type = self._lexer.peek_token()
                                    
                                    while next_type == "COMMA":
                                        self._expect("COMMA")
                                        _, next_type = self._lexer.peek_token()

                                        if next_type == "STRING":
                                            self._expect("STRING")
                                            _, next_type = self._lexer.peek_token()
                                        
                                        self._parse_tfpdef()
                                        _, next_type = self._lexer.peek_token()

                                        if next_type == "EQUAL":
                                            self._expect("EQUAL")
                                            self._parse_test()
                                            _, next_type = self._lexer.peek_token()
                                    
                                    if next_type == "STRING":
                                        self._expect("STRING")
                                    elif next_type == "COMMA":
                                        self._expect("COMMA")
                                        _, next_type = self._lexer.peek_token()

                                        if next_type == "STRING":
                                            self._expect("STRING")
                                            _, next_type = self._lexer.peek_token()
                                        
                                        if next_type == "POWER":
                                            self._expect("POWER")
                                            self._parse_tfpdef()

                                            _, next_type = self._lexer.peek_token()

                                            if next_type == "COMMA":
                                                self._expect("COMMA")
                                                _, next_type = self._lexer.peek_token()
                                            
                                            if next_type == "STRING":
                                                self._expect("STRING")
                                elif next_type == "POWER":
                                    self._expect("POWER")
                                    self._parse_tfpdef()
                                    _, next_type = self._lexer.peek_token()

                                    if next_type == "COMMA":
                                        self._expect("COMMA")
                                        _, next_type = self._lexer.peek_token()
                                    
                                    if next_type == "STRING":
                                        self._expect("STRING")

                            
                        elif next_type == "ASTERISK":
                            self._expect("ASTERISK")
                            _, next_type = self._lexer.peek_token()

                            if next_type in tfpdef_first_set:
                                self._parse_tfpdef()
                                _, next_type = self._lexer.peek_token()
                            
                            while next_type == "COMMA":
                                self._expect("COMMA")
                                _, next_type = self._lexer.peek_token()

                                if next_type == "STRING":
                                    self._expect("STRING")
                                    _, next_type = self._lexer.peek_token()
                                
                                self._parse_tfpdef()
                                _, next_type = self._lexer.peek_token()

                                if next_type == "EQUAL":
                                    self._expect("EQUAL")
                                    self._parse_test()
                                    _, next_type = self._lexer.peek_token()
                            
                            if next_type == "STRING":
                                self._expect("STRING")
                            elif next_type == "COMMA":
                                self._expect("COMMA")
                                _, next_type = self._lexer.peek_token()

                                if next_type == "STRING":
                                    self._expect("STRING")
                                    _, next_type = self._lexer.peek_token()
                                
                                if next_type == "POWER":
                                    self._expect("POWER")
                                    self._parse_tfpdef()

                                    _, next_type = self._lexer.peek_token()

                                    if next_type == "COMMA":
                                        self._expect("COMMA")
                                        _, next_type = self._lexer.peek_token()
                                    
                                    if next_type == "STRING":
                                        self._expect("STRING")
                        elif next_type == "POWER":
                            self._expect("POWER")
                            self._parse_tfpdef()
                            _, next_type = self._lexer.peek_token()

                            if next_type == "COMMA":
                                self._expect("COMMA")
                                _, next_type = self._lexer.peek_token()
                            
                            if next_type == "STRING":
                                self._expect("STRING")

                elif next_type == "ASTERISK":
                    self._expect("ASTERISK")
                    _, next_type = self._lexer.peek_token()

                    if next_type in tfpdef_first_set:
                        self._parse_tfpdef()
                        _, next_type = self._lexer.peek_token()
                    
                    while next_type == "COMMA":
                        self._expect("COMMA")
                        _, next_type = self._lexer.peek_token()

                        if next_type == "STRING":
                            self._expect("STRING")
                            _, next_type = self._lexer.peek_token()
                        
                        self._parse_tfpdef()
                        _, next_type = self._lexer.peek_token()

                        if next_type == "EQUAL":
                            self._expect("EQUAL")
                            self._parse_test()
                            _, next_type = self._lexer.peek_token()
                    
                    if next_type == "STRING":
                        self._expect("STRING")
                    elif next_type == "COMMA":
                        self._expect("COMMA")
                        _, next_type = self._lexer.peek_token()

                        if next_type == "STRING":
                            self._expect("STRING")
                            _, next_type = self._lexer.peek_token()
                        
                        if next_type == "POWER":
                            self._expect("POWER")
                            self._parse_tfpdef()

                            _, next_type = self._lexer.peek_token()

                            if next_type == "COMMA":
                                self._expect("COMMA")
                                _, next_type = self._lexer.peek_token()
                            
                            if next_type == "STRING":
                                self._expect("STRING")
                elif next_type == "POWER":
                    self._expect("POWER")
                    self._parse_tfpdef()
                    _, next_type = self._lexer.peek_token()

                    if next_type == "COMMA":
                        self._expect("COMMA")
                        _, next_type = self._lexer.peek_token()
                    
                    if next_type == "STRING":
                        self._expect("STRING")
                        
                    elif next_type == "STRING":
                        self._expect("STRING")

        elif next_type == "ASTERISK":
            self._expect("ASTERISK")
            _, next_type = self._lexer.peek_token()

            if next_type in tfpdef_first_set:
                self._parse_tfpdef()
                _, next_type = self._lexer.peek_token()
            
            while next_type == "COMMA":
                self._expect("COMMA")
                _, next_type = self._lexer.peek_token()

                if next_type == "STRING":
                    self._expect("STRING")
                    _, next_type = self._lexer.peek_token()
                
                self._parse_tfpdef()
                _, next_type = self._lexer.peek_token()

                if next_type == "EQUAL":
                    self._expect("EQUAL")
                    self._parse_test()
                    _, next_type = self._lexer.peek_token()
            
            if next_type == "STRING":
                self._expect("STRING")
            elif next_type == "COMMA":
                self._expect("COMMA")
                _, next_type = self._lexer.peek_token()

                if next_type == "STRING":
                    self._expect("STRING")
                    _, next_type = self._lexer.peek_token()
                
                if next_type == "POWER":
                    self._expect("POWER")
                    self._parse_tfpdef()

                    _, next_type = self._lexer.peek_token()

                    if next_type == "COMMA":
                        self._expect("COMMA")
                        _, next_type = self._lexer.peek_token()
                    
                    if next_type == "STRING":
                        self._expect("STRING")

        elif next_type == "POWER":
            self._expect("POWER")
            self._parse_tfpdef()
            _, next_type = self._lexer.peek_token()

            if next_type == "COMMA":
                self._expect("COMMA")
                _, next_type = self._lexer.peek_token()
            
            if next_type == "STRING":
                self._expect("STRING")

        else:
            self._syntax_error(tfpdef_first_set + [ "ASTERISK", "POWER" ], next_type)

    def _parse_tfpdef(self):
        self._expect("NAME")
        _, next_type = self._lexer.peek_token()

        if next_type == "COMMA":
            self._expect("COMMA")
            self._parse_test()
    
    def _parse_varargslist(self):
        _, next_type = self._lexer.peek_token()
        vfpdef_first_set = []

        if next_type == "ASTERISK":
            self._expect("ASTERISK")
            _, next_type = self._lexer.peek_token()

            if next_type in vfpdef_first_set:
                self._parse_vfpdef()
                _, next_type = self._lexer.peek_token()
            
            if next_type == "COMMA":
                self._expect("COMMA")
                
                _, next_type = self._lexer.peek_token()

                if next_type in vfpdef_first_set:
                    self._parse_vfpdef()

                    _, next_type = self._lexer.peek_token()

                    if next_type == "EQUAL":
                        self._expect("EQUAL")
                        self._parse_test()
                        _, next_type = self._lexer.peek_token()
                    
                    while next_type == "COMMA":
                        self._expect("COMMA")
                        self._parse_vfpdef()

                        _, next_type = self._lexer.peek_token()

                        if next_type == "EQUAL":
                            self._expect("EQUAL")
                            self._parse_test()
                            _, next_type = self._lexer.peek_token()
                            
                elif next_type == "POWER":
                    self._expect("POWER")
                    self._parse_vfpdef()
                    _, next_type = self._lexer.peek_token()

                    if next_type == "COMMA":
                        self._expect("COMMA")

                else:
                    self._syntax_error(vfpdef_first_set + [ "POWER" ], next_type)

        elif next_type == "POWER":
            self._expect("POWER")
            self._parse_vfpdef()
            _, next_type = self._lexer.peek_token()

            if next_type == "COMMA":
                self._expect("COMMA")

        else:
            self._parse_vfpdef()
            
            _, next_type = self._lexer.peek_token()

            if next_type == "EQUAL":
                self._expect("EQUAL")
                self._parse_test()
                _, next_type = self._lexer.peek_token()

            if next_type == "COMMA":
                self._expect("COMMA")

                _, next_type = self._lexer.peek_token()

                if next_type in vfpdef_first_set:
                    self._parse_vfpdef()

                    _, next_type = self._lexer.peek_token()

                    if next_type == "EQUAL":
                        self._expect("EQUAL")
                        self._parse_test()
                        _, next_type = self._lexer.peek_token()
                    
                    while next_type == "COMMA":
                        self._expect("COMMA")
                        self._parse_vfpdef()

                        _, next_type = self._lexer.peek_token()

                        if next_type == "EQUAL":
                            self._expect("EQUAL")
                            self._parse_test()
                            _, next_type = self._lexer.peek_token()

                elif next_type == "ASTERISK":
                    self._expect("ASTERISK")
                    _, next_type = self._lexer.peek_token()

                    if next_type in vfpdef_first_set:
                        self._parse_vfpdef()
                        _, next_type = self._lexer.peek_token()
                    
                    if next_type == "COMMA":
                        self._expect("COMMA")
                        
                        _, next_type = self._lexer.peek_token()

                        if next_type in vfpdef_first_set:
                            self._parse_vfpdef()

                            _, next_type = self._lexer.peek_token()

                            if next_type == "EQUAL":
                                self._expect("EQUAL")
                                self._parse_test()
                                _, next_type = self._lexer.peek_token()
                            
                            while next_type == "COMMA":
                                self._expect("COMMA")
                                self._parse_vfpdef()

                                _, next_type = self._lexer.peek_token()

                                if next_type == "EQUAL":
                                    self._expect("EQUAL")
                                    self._parse_test()
                                    _, next_type = self._lexer.peek_token()

                        elif next_type == "POWER":
                            self._expect("POWER")
                            self._parse_vfpdef()
                            _, next_type = self._lexer.peek_token()

                            if next_type == "COMMA":
                                self._expect("COMMA")

                        else:
                            self._syntax_error(vfpdef_first_set + [ "POWER" ], next_type)

                elif next_type == "POWER":
                    self._expect("POWER")
                    self._parse_vfpdef()
                    _, next_type = self._lexer.peek_token()

                    if next_type == "COMMA":
                        self._expect("COMMA")

                else:
                    self._syntax_error(vfpdef_first_set + [ "ASTERISK", "POWER" ], next_type)
    
    def _parse_vfpdef(self):
        self._expect("NAME")
    
    def _parse_stmt(self):
        simple_stmt_first_set = []
        compound_stmt_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in simple_stmt_first_set:
            self._parse_simple_stmt()
        elif next_type in compound_stmt_first_set:
            self._parse_compound_stmt()
        else:
            self._syntax_error(simple_stmt_first_set + compound_stmt_first_set, next_type)
    
    def _parse_simple_stmt(self):
        self._pare_small_stmt()
        _, next_type = self._lexer.peek_token()
        small_stmt_first_set = []

        while next_type == "SEMICOLON":
            self._expect("SEMICOLON")
            _, next_type = self._lexer.peek_token()

            if next_type in small_stmt_first_set:
                self._parse_small_stmt()
                _, next_type = self._lexer.peek_token()
            else:
                break

        self._expect("NEWLINE")

    def _parse_small_stmt(self):
        expr_stmt_first_set = []
        del_stmt_first_set = []
        pass_stmt_first_set = []
        flow_stmt_first_set = []
        import_stmt_first_set = []
        global_stmt_first_set = []
        nonlocal_stmt_first_set = []
        assert_stmt_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in expr_stmt_first_set: self._parse_expr_stmt()
        elif next_type in del_stmt_first_set: self._parse_del_stmt()
        elif next_type in pass_stmt_first_set: self._parse_pass_stmt()
        elif next_type in flow_stmt_first_set: self._parse_flow_stmt()
        elif next_type in import_stmt_first_set: self._parse_import_stmt()
        elif next_type in global_stmt_first_set: self._parse_global_stmt()
        elif next_type in nonlocal_stmt_first_set: self._parse_nonlocal_stmt()
        elif next_type in assert_stmt_first_set: self._parse_assert_stmt()
        else:
            self._syntax_error(
                expr_stmt_first_set
                + del_stmt_first_set
                + pass_stmt_first_set
                + flow_stmt_first_set
                + import_stmt_first_set
                + global_stmt_first_set
                + nonlocal_stmt_first_set
                + assert_stmt_first_set
                , next_type
            )

    def _parse_expr_stmt(self):
        self._parse_testlist_star_expr()
        annassign_first_set = []
        augassign_first_set = []
        yeild_expr_first_set = []
        testlist_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in annassign_first_set:
            self._parse_annasign()
        elif next_type in augassign_first_set:
            self._parse_augassign()
            _, next_type = self._lexer.peek_token()

            if next_type in yeild_expr_first_set:
                self._parse_yield_expr()
            elif next_type in testlist_first_set:
                self._parse_testlist()
            else:
                self._parse_syntax_error(yeild_expr_first_set + testlist_first_set, next_type)
            
        elif next_type == "EQUAL":
            while next_type == "EQUAL":
                self._expect("EQUAL")
                _, next_type = self._lexer.peek_token()

                if next_type in yeild_expr_first_set:
                    self._parse_yield_expr()
                else:
                    self._parse_testlist_star_expr()
                
                _, next_type = self._lexer.peek_token()
            
            if next_type == "STRING":
                self._expect("STRING")
    
    def _parse_annasign(self):
        self._expect("COLON")
        self._parse_test()
        _, next_type = self._lexer.peek_token()
        yeild_expr_first_set = []

        if next_type == "EQUAL":
            self._expect("EQUAL")
            _, next_type = self._lexer.peek_token()

            if next_type in yeild_expr_first_set:
                self._parse_yeild_expr()
            else:
                self._parse_testlist_star_expr()
    
    def _parse_testlist_star_expr(self):
        test_first_set = []
        star_expr_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in testlist_first_set:
            self._parse_test()
        elif next_type in star_expr_first_set:
            self._parse_star_expr()
        else:
            self._syntax_error(test_first_set + star_expr_first_set, next_type)
        
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in testlist_first_set:
                self._parse_test()
            elif next_type in star_expr_first_set:
                self._parse_star_expr()
            else:
                break
            
            _, next_type = self._lexer.peek_token()
    
    def _parse_augassign(self):
        self._expect([
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
        ])
    
    def _parse_del_stmt(self):
        self._expect("DEL")
        self._parse_expr_list()
    
    def _parse_pass_stmt(self):
        self._expect("PASS")
    
    def _parse_flow_stmt(self):
        break_stmt_first_set = []
        continue_stmt_first_set = []
        return_stmt_first_set = []
        raise_stmt_first_set = []
        yeild_stmt_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in break_stmt_first_set:
            self._parse_break_stmt()
        elif next_type in continue_stmt_first_set:
            self._parse_continue_stmt()
        elif next_type in return_stmt_first_set:
            self._parse_return_stmt()
        elif next_type in raise_stmt_first_set:
            self._parse_raise_stmt()
        elif next_type in yeild_stmt_first_set:
            self._parse_yeild_stmt()
        else:
            self._syntax_error(
                break_stmt_first_set
                + continue_stmt_first_set
                + return_stmt_first_set
                + raise_stmt_first_set
                + yeild_stmt_first_set
                , next_type
            )
    
    def _parse_break_stmt(self):
        self._expect("BREAK")
    
    def _parse_continue_stmt(self):
        self._expect("CONTINUE")
    
    def _parse_return_stmt(self):
        self._expect("RETURN")
        testlist_star_expr_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in testlist_star_expr_first_set:
            self._parse_testlist_star_expr()
    
    def _parse_yeild_stmt(self):
        self._parse_yeild_expr()
    
    def _parse_raise_stmt(self):
        self._expect("RAISE")
        test_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in test_first_set:
            self._parse_test()
            _, next_type = self._lexer.peek_token()

            if next_type == "FROM":
                self._expect("FROM")
                self._parse_test()
    
    def _parse_import_stmt(self):
        self._parse_import_name()
        self._parse_import_from()
    
    def _parse_import_name(self):
        self._expect("IMPORT")
        self._parse_dotted_as_names()
    
    def _parse_import_from(self):
        self._expect("FROM")
        _, next_type = self._lexer.peek_token()
        dot_or_ellipsis_found = False
        dotted_name_first_set = []

        while next_type in [ "DOT", "ELLIPSIS" ]:
            dot_or_ellipsis_found = True
            self._expect([ "DOT", "ELLIPSIS" ])
            _, next_type = self._lexer.peek_token()
        
        if dot_or_ellipsis_found:
            _, next_type = self._lexer.peek_token()

            if next_type in dotted_name_first_set:
                self._parse_dotted_name()
        else:
            self._parse_dotted_name()
        
        self._expect("IMPORT")
        import_as_names_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type == "ASTERISK":
            self._expect("ASTERISK")
        elif next_type == "LPAREN":
            self._expect("LPAREN")
            self._pares_import_as_names()
            self._expect("RPAREN")
        elif next_type in import_as_names_first_set:
            self._parse_import_as_names()
        else:
            self._syntax_error([ "ASTERISK", "LPAREN" ] + import_as_names_first_set, next_type)
    
    def _parse_import_as_name(self):
        self._expect("NAME")
        _, next_type = self._lexer.peek_token()

        if next_type == "AS":
            self._expect("AS")
            self._expect("NAME")
    
    def _parse_dotted_as_name(self):
        self._parse_dotted_name()
        _, next_type = self._lexer.peek_token()

        if next_type == "AS":
            self._expect("AS")
            self._expect("NAME")
    
    def _import_as_names(self):
        self._pares_import_as_name()
        _, next_type = self._lexer.peek_token()
        import_as_name_first_set = []

        while next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in import_as_name_first_set:
                self._parse_import_as_name()
                _, next_type = self._lexer.peek_token()
            else:
                break
    
    def _parse_dotted_as_names(self):
        self._parse_dotted_as_name()
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            self._parse_dotted_as_name()
            _, next_type = self._lexer.peek_token()
    
    def _parse_dotted_name(self):
        self._expect("NAME")
        _, next_type = self._lexer.peek_token()

        while next_type == "DOT":
            self._expect("DOT")
            self._expect("NAME")
            _, next_type = self._lexer.peek_token()
    
    def _parse_global_stmt(self):
        self._expect("GLOBAL")
        self._expect("NAME")
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            self._expect("NAME")
            _, next_type = self._lexer.peek_token()
    
    def _parse_nonlocal_stmt(self):
        self._expect("NONLOCAL")
        self._expect("NAME")
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            self._expect("NAME")
            _, next_type = self._lexer.peek_token()
    
    def _parse_assert_stmt(self):
        self._expect("ASSERT")
        self._parse_test()
        _, next_type = self._lexer.peek_token()

        if next_type == "COMMA":
            self._expect("COMMA")
            self._parse_test()
    
    def _parse_compound_stmt(self):
        if_stmt_first_set = []
        while_stmt_first_set = []
        for_stmt_first_set = []
        try_stmt_first_set = []
        with_stmt_first_set = []
        funcdef_first_set = []
        classdef_first_set = []
        decorated_first_set = []
        async_stmt_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in if_stmt_first_set:
            self._parse_if_stmt()
        elif next_type in while_stmt_first_set:
            self._parse_while_stmt()
        elif next_type in for_stmt_first_set:
            self._parse_for_stmt()
        elif next_type in try_stmt_first_set:
            self._parse_try_stmt()
        elif next_type in with_stmt_first_set:
            self._parse_with_stmt()
        elif next_type in funcdef_first_set:
            self._parse_funcdef()
        elif next_type in classdef_first_set:
            self._parse_classdef()
        elif next_type in decorated_first_set:
            self._parse_decorated()
        elif next_type in async_stmt_first_set:
            self._parse_async_stmt()
        else:
            self._syntax_error(
                if_stmt_first_set
                + while_stmt_first_set
                + for_stmt_first_set
                + try_stmt_first_set
                + with_stmt_first_set
                + funcdef_first_set
                + classdef_first_set
                + decorated_first_set
                + async_stmt_first_set
                , next_type
            )

    def _parse_async_stmt(self):
        self._expect("ASYNC")
        for_stmt_first_set = []
        with_stmt_first_set = []
        funcdef_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in for_stmt_first_set:
            self._parse_for_stmt()
        elif next_type in with_stmt_first_set:
            self._parse_with_stmt()
        elif next_type in funcdef_first_set:
            self._parse_funcdef()
        else:
            self._syntax_error(
                for_stmt_first_set
                + with_stmt_first_set
                + funcdef_first_set,
                next_type
            )
    
    def _parse_if_stmt(self):
        self._expect("IF")
        self._parse_namedexpr_test()
        self._expect("COLON")
        self._parse_suite()
        
        _, next_type = self._lexer.peek_token()

        while next_type == "ELIF":
            self._expect("ELIF")
            self._parse_namedexpr_test()
            self._expect("COLON")
            self._parse_suite()
            _, next_type = self._lexer.peek_token()

        _, next_type = self._lexer.peek_token()

        if next_type == "ELSE":
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    def _parse_while_stmt(self):
        self._expect("WHILE")
        self._parse_namedexpr_test()
        self._expect("COLON")
        self._parse_suite()

        _, next_type = self._lexer.peek_token()

        if next_type == "ELSE":
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    def _parse_for_stmt(self):
        self._expect("FOR")
        self._parse_exprlist()
        self._expect("IN")
        self._parse_testlist()
        self._expect("COLON")
        _, next_type = self._lexer.peek_token()

        if next_type == "STRING":
            self._expect("STRING")

        self._parse_suite()

        _, next_type = self._lexer.peek_token()

        if next_type == "ELSE":
            self._expect("ELSE")
            self._expect("COLON")
            self._parse_suite()
    
    def _parse_try_stmt(self):        
        self._expect("TRY")
        self._expect("COLON")
        self._parse_suite()

        _, next_type = self._lexer.peek_token()
        except_clause_first_set = []

        if next_type in except_clause_first_set:
            self._parse_except_clause()
            self._expect("COLON")
            self._parse_suite()

            _, next_type = self._lexer.peek_token()

            while next_type in except_clause_first_set:
                self._parse_except_clause()
                self._expect("COLON")
                self._parse_suite()
                _, next_type = self._lexer.peek_token()
            
            _, next_type = self._lexer.peek_token()

            if next_type == "ELSE":
                self._expect("ELSE")
                self._expect("COLON")
                self._parse_suite()
                _, next_type = self._lexer.peek_token()

            if next_type == "FINALLY":
                self._expect("FINALLY")
                self._expect("COLON")
                self._parse_suite()

        elif next_type == "FINALLY":
            self._expect("FINALLY")
            self._expect("COLON")
            self._parse_suite()

        else:
            self._syntax_error(except_clause_first_set + ["FINALLY"], next_type)
    
    def _parse_with_stmt(self):
        self._expect("WITH")
        self._parse_with_item()
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            self._parse_with_item()
            _, next_type = self._lexer.peek_token()

        self._expect("COLON")
        _, next_type = self._lexer.peek_token()

        if next_type == "STRING":
            self._expect("STRING")

        self._parse_suite()
    
    def _pasre_swith_item(self):
        self._parse_test()
        _, next_type = self._lexer.peek_token()

        if next_type == "AS":
            self._expect("AS")
            self._parse_expr()
    
    def _parse_except_clause(self):
        self._expect("EXCEPT")
        _, next_type = self._lexer.peek_token()
        test_first_set = []

        if next_type in test_first_set:
            self._parse_test()
            _, next_type = self._lexer.peek_token()

            if next_type == "AS":
                self._expect("AS")
                self._expect("NAME")
        
    def _parse_suite(self):
        simple_stmt_first_set = []
        stmt_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in simple_stmt_first_set:
            self._parse_simple_stmt()
        else:
            self._expect("NEWLINE")
            self._expect_indent()
            self._parse_stmt()

            _, next_type = self._lexer.peek_token()

            while next_type in stmt_first_set:
                self._parse_stmt()
                _, next_type = self._lexer.peek_token()
            
            self._expect_dedent()
    
    def _parse_namedexpr_test(self):
        self._parse_test()
        _, next_type = self._lexer.peek_token()

        if next_type == "COLON_EQUALS":
            self._expect("COLON_EQUALS")
            self._parse_test()
    
    def _parse_test(self):
        or_test_first_set = []
        lambdef_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in or_test_first_set:
            self._parse_or_test()

            _, next_type = self._lexer.peek_token()

            if next_type == "IF":
                self._expect("IF")
                self._parse_or_test()
                self._expect("ELSE")
                self._parse_test()

        elif next_type in lambdef_first_set:
            self.parse_lambdef()
        else:
            self._syntax_error(or_test_first_set + lambdef_first_set, next_type)
    
    def _parse_test_nocond(self):
        or_test_first_set = []
        lambdef_nocond_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in or_test_first_set:
            self._parse_or_test()
        elif next_type in lambdef_nocond_first_set:
            self.parse_lambdef_nocond()
        else:
            self._syntax_error(or_test_first_set + lambdef_nocond_first_set, next_type)
    
    def _parse_lambdef(self):
        self._expect("LAMBDA")
        varargslist_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in varargslist_first_set:
            self._parse_varargslist()
            _, next_type = self._lexer.peek_token()
        
        self._expect("COLON")
        self._parse_test()
    
    def _parse_lambdef_nocond(self):
        self._expect("LAMBDA")
        varargslist_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in varargslist_first_set:
            self._parse_varargslist()
            _, next_type = self._lexer.peek_token()
        
        self._expect("COLON")
        self._parse_test_nocond()
    
    def _parse_or_test(self):
        self._parse_and_test()
        _, next_type = self._lexer.peek_token()

        while next_type == "OR":
            self._expect("OR")
            self._parse_and_test()
            _, next_type = self._lexer.peek_token()
    
    def _parse_and_test(self):
        self._parse_not_test()
        _, next_type = self._lexer.peek_token()

        while next_type == "AND":
            self._expect("AND")
            self._parse_not_test()
            _, next_type = self._lexer.peek_token()
    
    def _parse_not_test(self):
        comparison_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type == "NOT":
            self._expect("NOT")
            self._parse_not_test()
        elif next_type in comparison_first_set:
            self._parse_comparison()
    
    def _parse_comparison(self):
        self._parse_expr()
        comp_op_first_set = []

        _, next_type = self._lexer.peek_token()

        while next_type in comp_op_first_set:
            self._parse_comp_op()
            self._parse_expr()
            _, next_type = self._lexer.peek_token()
    
    def _parse_comp_op(self):
        _, next_type = self._lexer.peek_token()

        if next_type == "NOT":
            self._expect("NOT")
            _, next_type = self._lexer.peek_token()

            if next_type == "IN":
                self._expect("IN")
        elif next_type == "IS":
            self._expect("IS")
            _, next_type = self._lexer.peek_token()

            if next_type == "NOT":
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
        _, next_type = self._lexer.peek_token()

        while next_type == "PIPE":
            self._expect("PIPE")
            self._parse_xor_expr()
            _, next_type = self._lexer.peek_token()
    
    def _parse_xor_expr(self):
        self._parse_and_expr()
        _, next_type = self._lexer.peek_token()

        while next_type == "CARROT":
            self._expect("CARROT")
            self._parse_and_expr()
            _, next_type = self._lexer.peek_token()
    
    def _parse_and_expr(self):
        self._parse_shift_expr()
        _, next_type = self._lexer.peek_token()

        while next_type == "AMPERSAND":
            self._expect("AMPERSAND")
            self._parse_shift_expr()
            _, next_type = self._lexer.peek_token()
    
    def _parse_shift_expr(self):
        self._parse_arith_expr()
        _, next_type = self._lexer.peek_token()

        while next_type in [ "SHIFT_LEFT", "SHIFT_RIGHT" ]:
            if next_type == "SHIFT_LEFT":
                self._expect("SHIFT_LEFT")
            elif next_type == "SHIFT_RIGHT":
                self._expect("SHIFT_RIGHT")

            self._parse_arith_expr()
            _, next_type = self._lexer.peek_token()
    
    def _parse_arith_expr(self):
        self._parse_term()
        _, next_type = self._lexer.peek_token()

        while next_type in [ "PLUS", " MINUS" ]:
            if next_type == "PLUS":
                self._expect("PLUS")
            elif next_type == "MINUS":
                self._expect("MINUS")

            self._parse_term()
            _, next_type = self._lexer.peek_token()
    
    def _parse_term(self):
        self._parse_factor()
        _, next_type = self._lexer.peek_token()

        while next_type in [ "ASTERISK", "AT", "SLASH", "PERCENT", "FLOOR_DIVISION" ]:
            if next_type == "ASTERISK":
                self._expect("ASTERISK")
            elif next_type == "AT":
                self._expect("AT")
            elif next_type == "SLASH":
                self._expect("SLASH")
            elif next_type == "PERCENT":
                self._expect("PERCENT")
            elif next_type == "FLOOR_DIVISION":
                self._expect("FLOOR_DIVISION")

            self._parse_factor()
            _, next_type = self._lexer.peek_token()
    
    def _parse_factor(self):
        power_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in [ "PLUS", "MINUS", "TILDE" ]:
            if next_type == "PLUS":
                self._expect("PLUS")
            elif next_type == "MINUS":
                self._expect("MINUS")
            elif next_type == "TILDE":
                self._expect("TILDE")
            
            self._parse_factor()

        elif next_type in power_first_set:
            self._parse_power()
        
        else:
            self._syntax_error([ "PLUS", "MINUS", "TILDE" ] + power_first_set, next_type)
    
    def _parse_power(self):
        self._parse_atom_expr()
        _, next_type = self._lexer.peek_token()

        if next_type == "POWER":
            self._expect("POWER")
            self._parse_factor()
    
    def _parse_atom_expr(self):
        trailer_first_set = []
        _, next_type = self._lexer.peek_token()
        
        if next_type == "AWAIT":
            self._expect("AWAIT")
        
        self._parse_atom()
        _, next_type = self._lexer.peek_token()

        while next_type in trailer_first_set:
            self._parse_trailer()
            _, next_type = self._lexer.peek_token()
    
    def _parse_atom(self):
        testlist_comp_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type == "LPAREN":
            self._expect("LPAREN")
            yeild_expr_first_set = []

            _, next_type = self._lexer.peek_token()

            if next_type in yeild_expr_first_set:
                self._parse_yield_expr()
            elif next_type in testlist_comp_first_set:
                self._parse_testlist_comp()
            
            self._expect("RPAREN")
        elif next_type == "LBRACKET":
            self._expect("LBRACKET")

            _, next_type = self._lexer.peek_token()

            if next_type in testlist_comp_first_set:
                self._parse_testlist_comp()
            
            self._expect("RBRACKET")
        elif next_type == "LBRACE":
            self._expect("LBRACE")

            dictorsetmaker_first_set = []
            _, next_type = self._lexer.peek_token()

            if next_type in dictorsetmaker_first_set:
                self._parse_dictorsetmaker()
            
            self._expect("RBRACE")
        elif next_type == "NAME":
            self._expect("NAME")
        elif next_type == "NUMBER":
            self._expect("NUMBER")
        elif next_type == "STRING":
            while next_type == "STRING":
                self._expect("STRING")
                _, next_type = self._lexer.peek_token()
        elif next_type == "ELLIPSIS":
            self._expect("ELLIPSIS")
        elif next_type == "NONE":
            self._expect("NONE")
        elif next_type == "TRUE":
            self._expect("TRUE")
        elif next_type == "FALSE":
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
                "FALSE  "
            ], next_type)
    
    def _parse_testlist_comp(self):        
        namedexpr_test_first_set = []
        star_expr_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in namedexpr_test_first_set:
            self._parse_namedexpr_test()
        elif next_type in star_expr_first_set:
            self._parse_star_expr()
        else:
            self._syntax_error(namedexpr_test_first_set + star_expr_first_set, next_type)
        
        comp_for_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in comp_for_first_set:
            self._parse_comp_for()
        elif next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in namedexpr_test_first_set:
                self._parse_namedexpr_test()
            elif next_type in star_expr_first_set:
                self._parse_star_expr()

            _, next_type = self._lexer.peek_token()

            while next_type == "COMMA":
                self._expect("COMMA")
                _, next_type = self._lexer.peek_token()

                if next_type in namedexpr_test_first_set:
                    self._parse_namedexpr_test()
                elif next_type in star_expr_first_set:
                    self._parse_star_expr()
                else:
                    break

                _, next_type = self._lexer.peek_token()
    
    def _parse_trailer(self):
        _, next_type = self._lexer.peek_token()

        if next_type == "LPAREN":
            self._expect("LPAREN")
            argslist_first_set = []
            _, next_type = self._lexer.peek_token()

            if next_type in argslist_first_set:
                self._parse_argslist()
                _, next_type = self._lexer.peek_token()

            self._expect("RBRACKET")
        elif next_type == "LBRACKET":
            self._expect("LBRACKET")
            self._parse_subscriptlist()
            self._expect("RBRACKET")
        elif next_type == "DOT":
            self._expect("DOT")
            self._expect("NAME")
        else:
            self._syntax_error([ "LPAREN", "LBRACKET", "DOT" ], next_type)

    def _parse_subscriptlist(self):
        self._parse_subscript()
        _, next_type = self._lexer.peek_token()
        subscript_first_set = []
        
        while next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in subscript_first_set:
                self._parse_subscript()
            else:
                break

            _, next_type = self._lexer.peek_token()
    
    def _parse_subscript(self):
        test_first_set = []
        sliceop_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in test_first_set:
            self._parse_test()
            _, next_type = self._lexer.peek_token()

            if next_type == "COLON":
                self._expect("COLON")
                _, next_type = self._lexer.peek_token()

                if next_type in test_first_set:
                    self._parse_test()
                    _, next_type = self._lexer.peek_token()
                
                if next_type in sliceop_first_set:
                    self._parse_sliceop()

        elif next_type == "COLON":
            self._expect("COLON")
            _, next_type = self._lexer.peek_token()

            if next_type in test_first_set:
                self._parse_test()
                _, next_type = self._lexer.peek_token()
            
            if next_type in sliceop_first_set:
                self._parse_sliceop()
    
    def _parse_sliceop(self):
        self._expect("COLON")
        test_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in test_first_set:
            self._parse_test()
    
    def _parse_exprlist(self):
        expr_first_set = []
        star_expr_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type in expr_first_set:
            self._parse_expr()
        elif next_type in star_expr_first_set:
            self._parse_star_expr()
        else:
            self._syntax_error(expr_first_set + star_expr_first_set, next_type)
        
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in expr_first_set:
                self._parse_expr()
            elif next_type in star_expr_first_set:
                self._parse_star_expr()
            else:
                break
            
            _, next_type = self._lexer.peek_token()
    
    def _parse_testlist(self):
        self._parse_test()
        
        test_first_set = []
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in test_first_set:
                self._parse_test()
            else:
                break
            
            _, next_type = self._lexer.peek_token()
    
    def _parse_dictorsetmaker(self):        
        test_first_set = []
        star_expr_first_set = []
        comp_for_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in test_first_set:
            self._parse_test()
            _, next_type = self._lexer.peek_token()

            if next_type == "COLON":
                self._expect("COLON")
                self._parse_test()

                _, next_type = self._lexer.peek_token()

                if next_type in comp_for_first_set:
                    self._parse_comp_for()
                elif next_type == "COMMA":
                    while next_type == "COMMA":
                        self._expect("COMMA")
                        _, next_type = self._lexer.peek_token()

                        if next_type in test_first_set:
                            self._parse_test()
                        elif next_type in star_expr_first_set:
                            self._parse_star_expr()
                        else:
                            break

                        _, next_type = self._lexer.peek_token()
            elif next_type in comp_for_first_set:
                self._parse_comp_for()
            elif next_type == "COMMA":
                while next_type == "COMMA":
                    self._expect("COMMA")
                    _, next_type = self._lexer.peek_token()

                    if next_type in test_first_set:
                        self._parse_test()
                        self._expect("COLON")
                        self._parse_test()
                    elif next_type == "POWER":
                        self._expect("POWER")
                        self._parse_expr()
                    else:
                        break

                    _, next_type = self._lexer.peek_token()

        elif next_type == "POWER":
            self._expect("POWER")
            self._parse_expr()
            _, next_type = self._lexer.peek_token()

            if next_type in comp_for_first_set:
                self._parse_comp_for()
            elif next_type == "COMMA":
                while next_type == "COMMA":
                    self._expect("COMMA")
                    _, next_type = self._lexer.peek_token()

                    if next_type in test_first_set:
                        self._parse_test()
                    elif next_type in star_expr_first_set:
                        self._parse_star_expr()
                    else:
                        break

                    _, next_type = self._lexer.peek_token()
            
        elif next_type in star_expr_first_set:
            self._parse_star_expr()
            _, next_type = self._lexer.peek_token()

            if next_type in comp_for_first_set:
                self._parse_comp_for()
            elif next_type == "COMMA":
                while next_type == "COMMA":
                    self._expect("COMMA")
                    _, next_type = self._lexer.peek_token()

                    if next_type in test_first_set:
                        self._parse_test()
                        self._expect("COLON")
                        self._parse_test()
                    elif next_type == "POWER":
                        self._expect("POWER")
                        self._parse_expr()
                    else:
                        break

                    _, next_type = self._lexer.peek_token()
        else:
            self._syntax_error(test_first_set + [ "POWER" ] + star_expr_first_set, next_type)

    def _parse_classdef(self):
        self._expect("CLASS")
        self._expect("NAME")
        arglist_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type == "LPAREN":
            self._expect("LPAREN")
            _, next_type = self._lexer.peek_token()

            if next_type in argslist_first_set:
                self._parse_arglist()
            
            self._expect("RPAREN")
        
        self._expect("COLON")
        self._parse_suite()
    
    def _parse_arglist(self):
        self._parse_argument()
        argument_first_set = []
        _, next_type = self._lexer.peek_token()

        while next_type == "COMMA":
            self._expect("COMMA")
            _, next_type = self._lexer.peek_token()

            if next_type in argument_first_set:
                self._parse_argument()
            else:
                break
            
            _, next_type = self._lexer.peek_token()
    
    def _pares_argument(self):
        test_first_set = []
        comp_for_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in test_first_set:
            self._parse_test()
            _, next_type = self._lexer.peek_token()

            if next_type in comp_for_first_set:
                self._pares_comp_for()
            elif next_type == "COLON_EQUALS":
                self._expect("COLON_EQUALS")
            elif next_type == "EQUAL":
                self._expect("EQUAL")

        elif next_type == "POWER":
            self._expect("POWER")
            self._parse_test()
        elif next_type == "ASTERISK":
            self._expect("ASTERISK")
            self._parse_test()
        else:
            self._syntax_error(test_first_set + [ "POWER", "ASTERISK" ], next_type)
    
    def _parse_comp_iter(self):
        comp_for_first_set = []
        comp_if_first_set = []

        _, next_type = self._lexer.peek_token()

        if next_type in comp_for_first_set:
            self._parse_comp_for()
        elif next_type in comp_if_first_set:
            self._parse_comp_if()
        else:
            self._syntax_error(comp_for_first_set + comp_if_first_set, next_type)
    
    def _sync_comp_for(self):
        comp_iter_first_set = []

        self._expect("FOR")
        self._parse_exprlist()
        self._expect("IN")
        self._parse_or_test()

        _, next_type = self._lexer.peek_token()

        if next_type in comp_iter_first_set:
            self._parse_comp_iter()

    def _parse_comp_for(self):
        _, next_type = self._lexer.peek_token()

        if next_type == "ASYNC":
            self._expect("ASYNC")
        
        self._parse_sync_comp_for()

    def _parse_comp_if(self):
        comp_iter_first_set = []

        self._expect("IF")
        self._parse_test_nocond()

        _, next_type = self._lexer.peek_token()

        if next_type in comp_iter_first_set:
            self._parse_comp_iter()

    def _parse_yield_expr(self):
        yield_arg_first_set = []

        self._expect("YIELD")
        _, next_type = self._lexer.peek_token()

        if next_type in yield_arg_first_set:
            self._parse_yield_arg()
    
    def _parse_yield_arg(self):
        testlist_star_expr_first_set = []
        _, next_type = self._lexer.peek_token()

        if next_type == "FROM":
            self._expect("FROM")
            self._parse_test()
        elif next_type in testlist_star_expr_first_set:
            self._parse_testlist_star_expr()
        else:
            self._syntax_error([ "FROM" ] + testlist_star_expr_first_set, next_type)
