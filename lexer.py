import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', línea={self.line}, columna={self.column})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        
        # Palabras clave CORRECTAS
        self.keywords = {
            'if': 'IF',
            'else': 'ELSE', 
            'while': 'WHILE',
            'for': 'FOR',
            'return': 'RETURN',
            'in': 'IN'
        }
        
        # 🔥 TOKENS REORDENADOS - LOS MÁS ESPECÍFICOS PRIMERO
        self.token_patterns = [
            # Operadores multi-carácter PRIMERO
            ('OP_REL',     r'==|!=|<=|>='),         # ==, !=, <=, >= (PRIMERO)
            ('OP_LOG',     r'&&|\|\|'),             # &&, || 
            
            # Operadores y símbolos de un carácter
            ('OP_SUMA',    r'\+'),                  # +
            ('OP_RESTA',   r'\-'),                  # -
            ('OP_MULT',    r'\*'),                  # *
            ('OP_DIV',     r'\/'),                  # /
            ('OP_ASIGN',   r'='),                   # = (individual)
            ('OP_REL',     r'<|>'),                 # <, > (después de <=, >=)
            
            # Símbolos
            ('PAR_IZQ',    r'\('),                  # (
            ('PAR_DER',    r'\)'),                  # )
            ('LLAVE_IZQ',  r'\{'),                  # {
            ('LLAVE_DER',  r'\}'),                  # }
            ('PUNTO_COMA', r';'),                   # ;
            ('COMA',       r','),                   # ,
            
            # Literales e identificadores
            ('NUM',        r'\d+'),                 # Números
            ('ID',         r'[a-zA-Z_]\w*'),        # Identificadores
            
            # Espacios y control
            ('SKIP',       r'[ \t]+'),              # Espacios
            ('NEWLINE',    r'\n'),                  # Saltos de línea
            ('ERROR',      r'.'),                   # Error
        ]

    def tokenize(self):
        """Tokeniza el código fuente correctamente"""
        pos = 0
        line = 1
        line_start = 0
        self.tokens = []
        
        while pos < len(self.code):
            # Encontrar el próximo match
            match = None
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    value = match.group()
                    break
            
            if not match:
                raise Exception(f"Error léxico en línea {line}, columna {pos - line_start + 1}")
            
            # Calcular posición
            column = pos - line_start + 1
            
            # Manejar tokens
            if token_type == 'SKIP':
                pos = match.end()
                continue
            elif token_type == 'NEWLINE':
                line += 1
                line_start = pos + 1
                pos = match.end()
                continue
            elif token_type == 'ERROR':
                raise Exception(f"Carácter inesperado '{value}' en línea {line}, columna {column}")
            
            # Verificar palabras clave
            if token_type == 'ID' and value in self.keywords:
                token_type = self.keywords[value]
            
            # Crear token
            token = Token(token_type, value, line, column)
            self.tokens.append(token)
            
            # Avanzar posición
            pos = match.end()
        
        return self.tokens

    def print_tokens(self):
        """Imprime todos los tokens"""
        for i, token in enumerate(self.tokens, 1):
            print(f"{i}: {token}")

# Prueba inmediata
if __name__ == "__main__":
    print("=== PRUEBA DEL ANALIZADOR LÉXICO ===")
    
    test_codes = [
        "if (x == 18) { return y + 5; }",
        "if (edad > 18 && activo == true) { return resultado; }",
        "x = 10 + y * 3;"
    ]
    
    for i, code in enumerate(test_codes, 1):
        print(f"\n--- Prueba {i} ---")
        print(f"Código: {code}")
        print("Tokens:")
        
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            for token in tokens:
                print(f"  {token}")
        except Exception as e:
            print(f"  ERROR: {e}")


