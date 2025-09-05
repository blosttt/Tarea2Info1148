# test_lexer.py
#!/usr/bin/env python3
"""
Script de pruebas para el analizador léxico.
Ejecutar con: python test_lexer.py
"""

import sys
from lexer import Lexer, Token

def run_tests():
    """Ejecuta pruebas unitarias del analizador léxico"""
    print("=== PRUEBAS DEL ANALIZADOR LÉXICO ===\n")
    
    # Test 1: Palabras clave y identificadores
    print("1. Probando palabras clave e identificadores:")
    code1 = "if else while for return x variable_1 _temp"
    lexer1 = Lexer(code1)
    tokens1 = lexer1.tokenize()
    
    expected1 = ['IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'ID', 'ID', 'ID']
    actual1 = [token.type for token in tokens1]
    
    print(f"Código: {code1}")
    print(f"Tokens esperados: {expected1}")
    print(f"Tokens obtenidos: {actual1}")
    print(f"✓ Test pasado" if expected1 == actual1 else "✗ Test fallado")
    print()
    
    # Test 2: Números
    print("2. Probando números:")
    code2 = "123 0 987654321"
    lexer2 = Lexer(code2)
    tokens2 = lexer2.tokenize()
    
    expected2 = ['NUM', 'NUM', 'NUM']
    actual2 = [token.type for token in tokens2]
    
    print(f"Código: {code2}")
    print(f"Tokens esperados: {expected2}")
    print(f"Tokens obtenidos: {actual2}")
    print(f"✓ Test pasado" if expected2 == actual2 else "✗ Test fallado")
    print()
    
    # Test 3: Operadores
    print("3. Probando operadores:")
    code3 = "+ - * / = == != < > <= >= && ||"
    lexer3 = Lexer(code3)
    tokens3 = lexer3.tokenize()
    
    expected3 = ['OP_SUMA', 'OP_RESTA', 'OP_MULT', 'OP_DIV', 'OP_ASIGN', 
                'OP_REL', 'OP_REL', 'OP_REL', 'OP_REL', 'OP_REL', 'OP_REL', 'OP_LOG', 'OP_LOG']
    actual3 = [token.type for token in tokens3]
    
    print(f"Código: {code3}")
    print(f"Tokens esperados: {expected3}")
    print(f"Tokens obtenidos: {actual3}")
    print(f"✓ Test pasado" if expected3 == actual3 else "✗ Test fallado")
    print()
    
    # Test 4: Signos de puntuación
    print("4. Probando signos de puntuación:")
    code4 = "( ) { } ; ,"
    lexer4 = Lexer(code4)
    tokens4 = lexer4.tokenize()
    
    expected4 = ['PAR_IZQ', 'PAR_DER', 'LLAVE_IZQ', 'LLAVE_DER', 'PUNTO_COMA', 'COMA']
    actual4 = [token.type for token in tokens4]
    
    print(f"Código: {code4}")
    print(f"Tokens esperados: {expected4}")
    print(f"Tokens obtenidos: {actual4}")
    print(f"✓ Test pasado" if expected4 == actual4 else "✗ Test fallado")
    print()
    
    # Test 5: Expresión compleja
    print("5. Probando expresión compleja:")
    code5 = "if (x == 10) { return y + 5; }"
    lexer5 = Lexer(code5)
    tokens5 = lexer5.tokenize()
    
    expected5 = ['IF', 'PAR_IZQ', 'ID', 'OP_REL', 'NUM', 'PAR_DER', 
                'LLAVE_IZQ', 'RETURN', 'ID', 'OP_SUMA', 'NUM', 'PUNTO_COMA', 'LLAVE_DER']
    actual5 = [token.type for token in tokens5]
    
    print(f"Código: {code5}")
    print(f"Tokens esperados: {expected5}")
    print(f"Tokens obtenidos: {actual5}")
    print(f"✓ Test pasado" if expected5 == actual5 else "✗ Test fallado")
    print()
    
    # Test 6: Manejo de errores
    print("6. Probando manejo de errores:")
    code6 = "x = @invalid;"
    try:
        lexer6 = Lexer(code6)
        tokens6 = lexer6.tokenize()
        print("✗ Test fallado: debería haber lanzado una excepción")
    except Exception as e:
        print(f"✓ Test pasado: Excepción capturada correctamente - {e}")
    print()

def interactive_mode():
    """Modo interactivo para probar código personalizado"""
    print("=== MODO INTERACTIVO ===")
    print("Escribe código para tokenizar (escribe 'quit' para salir):")
    
    while True:
        try:
            user_input = input("\nCódigo> ")
            if user_input.lower() == 'quit':
                break
                
            if user_input.strip():
                lexer = Lexer(user_input)
                tokens = lexer.tokenize()
                
                print("\nTokens encontrados:")
                for i, token in enumerate(tokens):
                    print(f"{i+1}: {token}")
                    
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
    else:
        print("Ejecuta 'python test_lexer.py --test' para correr las pruebas unitarias")
        interactive_mode()