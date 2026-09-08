import re

class JackTokenizer:
    # Token Type Constants
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    IDENTIFIER = 'identifier'
    INT_CONST = 'integerConstant'
    STRING_CONST = 'stringConstant'

    def __init__(self, input_file):
        """
        Initializes the tokenizer with the input file.
        Reads the entire file, cleans the code, and finds all tokens.
        """
        with open(input_file, 'r') as f:
            code = f.read()

        cleaned_code = self._remove_comments(code)
        
        # Regex to match all specified tokens
        token_regex = re.compile(r'(\b[a-zA-Z_]\w*|\d+|"[^"]*"|[{}()\[\].,;+\-*/&|<>=~])')
        self._tokens = token_regex.findall(cleaned_code)
        
        self._current_token_index = 0

    def _remove_comments(self, code):
        """
        Removes multi-line (/*...*/) and single-line (//...) comments.
        """
        # Remove multi-line comments
        cleaned_code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Remove single-line comments
        cleaned_code = re.sub(r'//.*', '', cleaned_code)
        return cleaned_code

    def has_more_tokens(self):
        """Returns True if there are more tokens in the input."""
        return self._current_token_index < len(self._tokens)

    def advance(self):
        """Gets the next token from the input and makes it the current token."""
        if self.has_more_tokens():
            self._current_token_index += 1

    def token_type(self):
        """Returns the type of the current token."""
        if not self.has_more_tokens():
            return None

        current_token = self.current_token()
        
        keywords = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}
        symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

        if current_token in keywords:
            return self.KEYWORD
        elif current_token in symbols:
            return self.SYMBOL
        elif current_token.startswith('"') and current_token.endswith('"'):
            return self.STRING_CONST
        elif current_token.isdigit():
            return self.INT_CONST
        else:
            return self.IDENTIFIER

    def current_token(self):
        """Returns the current token value."""
        if not self.has_more_tokens():
            return None
        return self._tokens[self._current_token_index]

    def keyword(self):
        """Returns the keyword of the current token."""
        return self.current_token()

    def symbol(self):
        """Returns the symbol of the current token."""
        return self.current_token()

    def identifier(self):
        """Returns the identifier of the current token."""
        return self.current_token()

    def int_val(self):
        """Returns the integer value of the current token."""
        return int(self.current_token())

    def string_val(self):
        """Returns the string value of the current token without the quotes."""
        return self.current_token()[1:-1]