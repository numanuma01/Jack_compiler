from JackTokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self._tokenizer = tokenizer
        self._output_file = open(output_file, 'w')
        self._indentation_level = 0
        self._tokenizer.advance() # Get the first token

    def _write_start_tag(self, tag):
        self._output_file.write('  ' * self._indentation_level + f'<{tag}>\n')
        self._indentation_level += 1

    def _write_end_tag(self, tag):
        self._indentation_level -= 1
        self._output_file.write('  ' * self._indentation_level + f'</{tag}>\n')

    def _write_token(self):
        token_type = self._tokenizer.token_type()
        token_value = self._tokenizer.current_token()
        
        if token_value == '<':
            token_value = '&lt;'
        elif token_value == '>':
            token_value = '&gt;'
        elif token_value == '&':
            token_value = '&amp;'

        self._output_file.write('  ' * self._indentation_level + f'<{token_type}> {token_value} </{token_type}>\n')
        self._tokenizer.advance()

    def compile_class(self):
        self._write_start_tag('class')
        self._write_token() # 'class'
        self._write_token() # className
        self._write_token() # '{'

        while self._tokenizer.current_token() in ('static', 'field'):
            self.compile_class_var_dec()
        
        while self._tokenizer.current_token() in ('constructor', 'function', 'method'):
            self.compile_subroutine()
        
        self._write_token() # '}'
        self._write_end_tag('class')

    def compile_class_var_dec(self):
        self._write_start_tag('classVarDec')
        self._write_token() # 'static' or 'field'
        self._write_token() # type
        self._write_token() # varName
        
        while self._tokenizer.current_token() == ',':
            self._write_token() # ','
            self._write_token() # varName
            
        self._write_token() # ';'
        self._write_end_tag('classVarDec')

    def compile_subroutine(self):
        self._write_start_tag('subroutineDec')
        self._write_token() # 'constructor', 'function', or 'method'
        self._write_token() # 'void' or type
        self._write_token() # subroutineName
        self._write_token() # '('
        
        self.compile_parameter_list()
        
        self._write_token() # ')'
        self.compile_subroutine_body()
        
        self._write_end_tag('subroutineDec')

    def compile_parameter_list(self):
        self._write_start_tag('parameterList')
        if self._tokenizer.current_token() != ')':
            self._write_token() # type
            self._write_token() # varName
            while self._tokenizer.current_token() == ',':
                self._write_token() # ','
                self._write_token() # type
                self._write_token() # varName
        self._write_end_tag('parameterList')

    def compile_subroutine_body(self):
        self._write_start_tag('subroutineBody')
        self._write_token() # '{'
        
        while self._tokenizer.current_token() == 'var':
            self.compile_var_dec()
        
        self.compile_statements()
        
        self._write_token() # '}'
        self._write_end_tag('subroutineBody')

    def compile_var_dec(self):
        self._write_start_tag('varDec')
        self._write_token() # 'var'
        self._write_token() # type
        self._write_token() # varName
        
        while self._tokenizer.current_token() == ',':
            self._write_token() # ','
            self._write_token() # varName
            
        self._write_token() # ';'
        self._write_end_tag('varDec')

    def compile_statements(self):
        self._write_start_tag('statements')
        
        while self._tokenizer.current_token() in ('let', 'if', 'while', 'do', 'return'):
            token = self._tokenizer.current_token()
            if token == 'let':
                self.compile_let()
            elif token == 'if':
                self.compile_if()
            elif token == 'while':
                self.compile_while()
            elif token == 'do':
                self.compile_do()
            elif token == 'return':
                self.compile_return()
        
        self._write_end_tag('statements')

    def compile_do(self):
        self._write_start_tag('doStatement')
        self._write_token() # 'do'
        self.compile_subroutine_call()
        self._write_token() # ';'
        self._write_end_tag('doStatement')

    def compile_let(self):
        self._write_start_tag('letStatement')
        self._write_token() # 'let'
        self._write_token() # varName
        
        if self._tokenizer.current_token() == '[':
            self._write_token() # '['
            self.compile_expression()
            self._write_token() # ']'
            
        self._write_token() # '='
        self.compile_expression()
        self._write_token() # ';'
        self._write_end_tag('letStatement')

    def compile_while(self):
        self._write_start_tag('whileStatement')
        self._write_token() # 'while'
        self._write_token() # '('
        self.compile_expression()
        self._write_token() # ')'
        self._write_token() # '{'
        self.compile_statements()
        self._write_token() # '}'
        self._write_end_tag('whileStatement')

    def compile_return(self):
        self._write_start_tag('returnStatement')
        self._write_token() # 'return'
        if self._tokenizer.current_token() != ';':
            self.compile_expression()
        self._write_token() # ';'
        self._write_end_tag('returnStatement')

    def compile_if(self):
        self._write_start_tag('ifStatement')
        self._write_token() # 'if'
        self._write_token() # '('
        self.compile_expression()
        self._write_token() # ')'
        self._write_token() # '{'
        self.compile_statements()
        self._write_token() # '}'
        
        if self._tokenizer.current_token() == 'else':
            self._write_token() # 'else'
            self._write_token() # '{'
            self.compile_statements()
            self._write_token() # '}'

        self._write_end_tag('ifStatement')

    def compile_expression_list(self):
        self._write_start_tag('expressionList')
        if self._tokenizer.current_token() != ')':
            self.compile_expression()
            while self._tokenizer.current_token() == ',':
                self._write_token() # ','
                self.compile_expression()
        self._write_end_tag('expressionList')
        
    def compile_expression(self):
        self._write_start_tag('expression')
        
        self.compile_term()
        
        operators = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
        while self._tokenizer.current_token() in operators:
            self._write_token() # op
            self.compile_term()
            
        self._write_end_tag('expression')

    def compile_term(self):
        self._write_start_tag('term')
        
        current_token = self._tokenizer.current_token()
        token_type = self._tokenizer.token_type()

        if token_type == self._tokenizer.INT_CONST or \
           token_type == self._tokenizer.STRING_CONST or \
           current_token in ('true', 'false', 'null', 'this'):
            self._write_token()
        elif token_type == self._tokenizer.IDENTIFIER:
            next_token = self._tokenizer._tokens[self._tokenizer._current_token_index + 1]
            if next_token in ('(', '.'):
                self.compile_subroutine_call()
            elif next_token == '[':
                self._write_token() # varName
                self._write_token() # '['
                self.compile_expression()
                self._write_token() # ']'
            else:
                self._write_token() # varName
        elif current_token == '(':
            self._write_token() # '('
            self.compile_expression()
            self._write_token() # ')'
        elif current_token in ('-', '~'):
            self._write_token() # unaryOp
            self.compile_term()

        self._write_end_tag('term')

    def compile_subroutine_call(self):
        self._write_token() # subroutineName or className or varName
        
        current_token = self._tokenizer.current_token()
        if current_token == '.':
            self._write_token() # '.'
            self._write_token() # subroutineName
        
        self._write_token() # '('
        self.compile_expression_list()
        self._write_token() # ')'

    def __del__(self):
        self._output_file.close()