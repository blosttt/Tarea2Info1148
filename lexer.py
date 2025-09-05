# lexer.py
import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.type}, {self.value}, línea={self.line}, columna={self.column})"
    
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Palabras clave
        self.keywords = {
            'if': 'IF',
            'else': 'ELSE', 
            'while': 'WHILE',
            'for': 'FOR',
            'return': 'RETURN'
        }
        
        # Tabla de transiciones del AFD (simplificada para implementación)
        self.transition_table = {
            'START': {
                'whitespace': ('START', None),
                'letter': ('IDENTIFIER', None),
                'digit': ('NUMBER', None),
                '+': ('PLUS', 'OP_SUMA'),
                '-': ('MINUS', 'OP_RESTA'),
                '*': ('STAR', 'OP_MULT'),
                '/': ('SLASH', 'OP_DIV'),
                '<': ('LESS', 'OP_REL'),
                '>': ('GREATER', 'OP_REL'),
                '=': ('EQUAL', 'OP_ASIGN'),
                '!': ('NOT', None),
                '&': ('AMPERSAND', None),
                '|': ('PIPE', None),
                '(': ('LPAREN', 'PAR_IZQ'),
                ')': ('RPAREN', 'PAR_DER'),
                '{': ('LBRACE', 'LLAVE_IZQ'),
                '}': ('RBRACE', 'LLAVE_DER'),
                ';': ('SEMICOLON', 'PUNTO_COMA'),
                ',': ('COMMA', 'COMA')
            },
            'IDENTIFIER': {
                'letter': ('IDENTIFIER', None),
                'digit': ('IDENTIFIER', None),
                '_': ('IDENTIFIER', None),
                'other': ('END', 'ID')
            },
            'NUMBER': {
                'digit': ('NUMBER', None),
                'other': ('END', 'NUM')
            },
            'PLUS': {
                'other': ('END', 'OP_SUMA')
            },
            'MINUS': {
                'other': ('END', 'OP_RESTA')
            },
            'STAR': {
                'other': ('END', 'OP_MULT')
            },
            'SLASH': {
                'other': ('END', 'OP_DIV')
            },
            'LESS': {
                '=': ('LESS_EQUAL', 'OP_REL'),
                'other': ('END', 'OP_REL')
            },
            'GREATER': {
                '=': ('GREATER_EQUAL', 'OP_REL'),
                'other': ('END', 'OP_REL')
            },
            'EQUAL': {
                '=': ('EQUAL_EQUAL', 'OP_REL'),
                'other': ('END', 'OP_ASIGN')
            },
            'NOT': {
                '=': ('NOT_EQUAL', 'OP_REL'),
                'other': ('ERROR', None)
            },
            'AMPERSAND': {
                '&': ('AND', 'OP_LOG'),
                'other': ('ERROR', None)
            },
            'PIPE': {
                '|': ('OR', 'OP_LOG'),
                'other': ('ERROR', None)
            },
            'LESS_EQUAL': {
                'other': ('END', 'OP_REL')
            },
            'GREATER_EQUAL': {
                'other': ('END', 'OP_REL')
            },
            'EQUAL_EQUAL': {
                'other': ('END', 'OP_REL')
            },
            'NOT_EQUAL': {
                'other': ('END', 'OP_REL')
            },
            'AND': {
                'other': ('END', 'OP_LOG')
            },
            'OR': {
                'other': ('END', 'OP_LOG')
            }
        }

    def get_char_type(self, char):
        """Determina el tipo de carácter para la tabla de transiciones"""
        if char is None:
            return 'EOF'
        if char.isspace():
            return 'whitespace'
        if char.isalpha():
            return 'letter'
        if char.isdigit():
            return 'digit'
        if char in ['+', '-', '*', '/', '<', '>', '=', '!', '&', '|', '(', ')', '{', '}', ';', ',']:
            return char
        return 'other'

    def tokenize(self):
        """Método principal que tokeniza el código fuente"""
        while self.position < len(self.code):
            token = self.get_next_token()
            if token:
                self.tokens.append(token)
        return self.tokens

    def get_next_token(self):
        """Obtiene el siguiente token del código"""
        current_state = 'START'
        lexeme = ''
        start_line = self.line
        start_column = self.column
        
        while self.position < len(self.code):
            current_char = self.code[self.position]
            char_type = self.get_char_type(current_char)
            
            # Manejo de saltos de línea para tracking de posición
            if current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            
            # Consultar tabla de transiciones
            if current_state in self.transition_table and char_type in self.transition_table[current_state]:
                next_state, token_type = self.transition_table[current_state][char_type]
            else:
                # Transición por defecto para otros caracteres
                if current_state in self.transition_table and 'other' in self.transition_table[current_state]:
                    next_state, token_type = self.transition_table[current_state]['other']
                else:
                    # Error: no hay transición definida
                    raise Exception(f"Error léxico: carácter inesperado '{current_char}' en línea {self.line}, columna {self.column}")
            
            if next_state == 'ERROR':
                raise Exception(f"Error léxico: carácter inesperado '{current_char}' en línea {self.line}, columna {self.column}")
            
            # Si estamos en estado START y es whitespace, ignorar
            if current_state == 'START' and char_type == 'whitespace':
                self.position += 1
                continue
                
            # Construir el lexema
            if next_state != 'START':
                lexeme += current_char
                self.position += 1
            
            # Si llegamos a un estado final, generar token
            if next_state == 'END':
                # Verificar si es palabra clave
                if token_type == 'ID' and lexeme in self.keywords:
                    token_type = self.keywords[lexeme]
                
                return Token(token_type, lexeme, start_line, start_column)
            
            current_state = next_state
        
        # Manejar el final del archivo
        if lexeme:
            # Verificar si es palabra clave
            if current_state == 'IDENTIFIER':
                if lexeme in self.keywords:
                    return Token(self.keywords[lexeme], lexeme, start_line, start_column)
                else:
                    return Token('ID', lexeme, start_line, start_column)
            elif current_state == 'NUMBER':
                return Token('NUM', lexeme, start_line, start_column)
        
        return None

    def print_tokens(self):
        """Imprime todos los tokens encontrados"""
        for token in self.tokens:
            print(token)

# Función principal para pruebas
def main():
    # Código de ejemplo para probar el analizador léxico
    test_code = """
    if (x == 10) {
        while y > 5 {
            z = x + y * 2;
            return z;
        }
    }
    """
    
    print("Código fuente:")
    print(test_code)
    print("\nTokens encontrados:")
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()