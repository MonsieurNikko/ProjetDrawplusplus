import subprocess
import sys
import os
import json
import shutil
 
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"La bibliothèque '{package}' n'est pas installée. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"La bibliothèque '{package}' a été installée avec succès.")
    else:
        print(f"La bibliothèque '{package}' est déjà installée.")

# Vérifier et installer la bibliothèque 'ply' si nécessaire
install_and_import('ply')

#-----------------------------------------------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc

#=================================================================================================================
# ANALYSE LEXICALE (LEXER)
#=================================================================================================================

reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'and': 'AND',
    'or': 'OR',
    'then':'THEN',
    'end':'END',
    'animation' : 'ANIMATION',
    'drawline':'DRAWLINE',
    'drawsquare' : "DRAWSQUARE",
    'drawrectangle' : "DRAWRECTANGLE",
    'drawrhombus' : 'DRAWRHOMBUS',
    'drawtriangle' : 'DRAWTRIANGLE',
    'drawrighttriangle' : 'DRAWRIGHTTRIANGLE',
    'drawparallelogram' : 'DRAWPARALLELOGRAM',
    'drawtrapezium' : 'DRAWTRAPEZIUM',
    'drawpolygon' : 'DRAWPOLYGON',
    'drawcircle' : 'DRAWCIRCLE',
    'renderer':'RENDERER'
}

tokens = (
    'ID', 'NUMBFLOAT', 'NUMBINT', 'EQUALS', 'SEMICOLON', 'COLON', 'COMMA',
    'LPAREN', 'RPAREN','LT', 'GT', 'EQ', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NEWLINE'
) + tuple(reserved.values())

t_EQUALS = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LT = r'<'
t_GT = r'>'
t_EQ = r'=='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ANIMATION = r'animation'
t_DRAWLINE = r'drawline'
t_DRAWSQUARE = r'drawsquare'
t_DRAWRECTANGLE = r'drawrectangle'
t_DRAWRHOMBUS = r'drawrhombus'
t_DRAWTRIANGLE = r'drawtriangle'
t_DRAWRIGHTTRIANGLE = r'drawrighttriangle'
t_DRAWPARALLELOGRAM = r'drawparallelogram'
t_DRAWTRAPEZIUM = r'drawtrapezium'
t_DRAWPOLYGON = r'drawpolygon'
t_DRAWCIRCLE = r'drawcircle'
t_RENDERER = r'renderer'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Règle pour les nombres flottants
def t_NUMBFLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Règle pour les nombres entiers
def t_NUMBINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t



def t_error(t):
    print(f"Erreur lexicale : caractère inattendu '{t.value[0]}' à la ligne {t.lexer.lineno}.")
    t.lexer.skip(1)

# Ignorer espaces et commentaires
t_ignore = ' \t'
t_ignore_COMMENT = r'//.*'

lexer = lex.lex()

#=================================================================================================================
# ANALYSE SYNTAXIQUE (PARSER)
#=================================================================================================================


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'LT', 'GT'),
)

scope_stack = [{}]

def enter_scope():
    """Ajoute un nouveau scope au scope_stack."""
    scope_stack.append({})


def exit_scope():
    """Supprime le scope le plus récent du scope_stack."""
    if len(scope_stack) > 1:  # Vérifie qu'on ne supprime pas le dernier scope global
        scope_stack.pop()
    else:
        print(f"[DEBUG] Tentative de sortie du dernier scope global ignorée.")

def declare_variable(name, value):
    scope_stack[-1][name] = value

def find_variable(name):
    for scope in reversed(scope_stack):
        if name in scope:
            return scope[name]
    raise NameError(f"Variable '{name}' non déclarée.")

def p_program(p):
    '''program : block'''
    p[0] = p[1]

def p_block(p):
    '''block : block_element
             | block block_element
             | block NEWLINE block_element'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1] + [p[3]]


def p_block_element(p):
    '''block_element : declaration
                     | statement
                     | animation
                     | drawline
                     | drawsquare
                     | drawrectangle
                     | drawrhombus
                     | drawtriangle
                     | drawrighttriangle
                     | drawparallelogram
                     | drawtrapezium
                     | drawpolygon
                     | drawcircle'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : INT ID EQUALS expression
                   | FLOAT ID EQUALS expression
                   | ID EQUALS expression'''
    if len(p) == 4:  # Assignation
        variable = find_variable(p[1])
        if variable:
            # Assignation à une variable existante
            p[0] = {
                "type": "assignment",
                "name": p[1],
                "expression": p[3]
            }
        else:
            raise NameError(f"Variable '{p[1]}' non déclarée avant l'assignation.")
    elif len(p) == 5:  # Nouvelle déclaration
        if p[2] in scope_stack[-1]:
            raise SyntaxError(f"Variable '{p[2]}' déjà déclarée dans le scope actuel.")
        # Déclaration avec un type explicite
        variable = {
            "type": p[1],  # int ou float
            "name": p[2],
            "expression": p[4]
        }
        declare_variable(p[2], variable)
        p[0] = variable




def p_statement(p):
    '''statement : if
                 | for
                 | while'''
    p[0] = p[1]

def p_condition(p):
    '''condition : expression LT expression
                 | expression GT expression
                 | expression EQ expression
                 | condition AND condition
                 | condition OR condition'''
    p[0] = {
        'left': p[1],
        'operator': p[2],
        'right': p[3]
    }

def p_expression(p):
    '''expression : NUMBFLOAT
                  | NUMBINT
                  | ID
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    if len(p) == 2:  # Valeur simple ou identifiant
        if isinstance(p[1], (int, float)):  # NUMBFLOAT ou NUMBINT
            p[0] = {'type': 'literal', 'value': p[1]}
        elif isinstance(p[1], str):  # Identifiant
            try:
                variable = find_variable(p[1])  # Vérifie si la variable existe
                p[0] = {'type': 'identifier', 'name': p[1]}
            except NameError as e:
                print(f"[ERREUR] {e}")  # Message d'erreur si la variable n'existe pas
                raise
    elif len(p) == 4:  # Opération binaire
        # Créez une représentation de l'opération
        p[0] = {
            'type': 'binary_operation',
            'operator': p[2],
            'left': p[1],
            'right': p[3]
        }


def p_if(p):
    '''if : IF LPAREN condition RPAREN THEN block NEWLINE END
          | IF LPAREN condition RPAREN THEN NEWLINE block NEWLINE END
          | IF LPAREN condition RPAREN THEN block ELSE block NEWLINE END
          | IF LPAREN condition RPAREN THEN NEWLINE block ELSE block NEWLINE END
          | IF LPAREN condition RPAREN THEN NEWLINE block ELSE NEWLINE block NEWLINE END'''
    enter_scope()  # Entrez dans un nouveau scope pour la structure conditionnelle entière
    # Déterminez l'index pour le corps du if
    if_body_index = 7 if p[6] == '\n' else 6
    p[0] = {'type': 'if', 'condition': p[3], 'if_body': p[if_body_index]}

    # Vérifiez la présence de 'else'
    else_index = None
    for i in range(len(p)):
        if p[i] == 'else':
            else_index = i
            break

    if else_index:
        # Déterminez l'index pour le corps du else, prenant en compte un NEWLINE possible
        if p[else_index + 1] != '\n':
            else_body_index = else_index + 1
        else:
            else_body_index = else_index + 2
        p[0]['else_body'] = p[else_body_index]

    if p[-1] == 'end':
        exit_scope()  # Sortez du scope après la fin complète de la structure if-else



def p_for(p):
    '''for : FOR LPAREN declaration SEMICOLON condition SEMICOLON declaration RPAREN COLON block NEWLINE END
           | FOR LPAREN declaration SEMICOLON condition SEMICOLON declaration RPAREN COLON NEWLINE block NEWLINE END'''
    enter_scope()
    p[0] = {'type': 'for', 'init': p[3], 'condition': p[5], 'update': p[7], 'body': p[10] if p[10] != '\n' else p[11]}

    if p[11] == 'end' or p[12] == 'end':
        exit_scope()


def p_while(p):
    '''while : WHILE LPAREN condition RPAREN COLON block NEWLINE END
             | WHILE LPAREN condition RPAREN COLON NEWLINE block NEWLINE END'''
    enter_scope()
    p[0] = {'type': 'while', 'condition': p[3], 'body': p[6] if p[6] != '\n' else p[7]}

    if p[8] == 'end'  or p[9] == 'end':
        exit_scope()






def p_animation(p):
    '''animation : ANIMATION LPAREN RENDERER COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'animation',
        'renderer': p[3],         # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9]]  # Liste des expressions
    }

def p_drawline(p):
    '''drawline : DRAWLINE LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawline',
        'renderer': p[3],         # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15]],  # Liste des expressions
    }

def p_drawsquare(p):
    '''drawsquare : DRAWSQUARE LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawsquare',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13]]   # Liste des expressions
    }

def p_drawrectangle(p):
    '''drawrectangle : DRAWRECTANGLE LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawrectangle',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15]]   # Liste des expressions
    }

def p_drawrhombus(p):
    '''drawrhombus : DRAWRHOMBUS LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawrhombus',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15]]   # Liste des expressions
    }

def p_drawtriangle(p):
    '''drawtriangle : DRAWTRIANGLE LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawtriangle',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13]]   # Liste des expressions
    }

def p_drawrighttriangle(p):
    '''drawrighttriangle : DRAWRIGHTTRIANGLE LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawrighttriangle',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15]]   # Liste des expressions
    }

def p_drawparallelogram(p):
    '''drawparallelogram : DRAWPARALLELOGRAM LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawparallelogram',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15], p[17]]   # Liste des expressions
    }

def p_drawtrapezium(p):
    '''drawtrapezium : DRAWTRAPEZIUM LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawtrapezium',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15], p[17]]   # Liste des expressions
    }

def p_drawpolygon(p):
    '''drawpolygon : DRAWPOLYGON LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawpolygon',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11], p[13], p[15]]   # Liste des expressions
    }

def p_drawcircle(p):
    '''drawcircle : DRAWCIRCLE LPAREN RENDERER COMMA expression COMMA expression COMMA expression COMMA expression RPAREN'''
    p[0] = {
        'type': 'drawcircle',
        'renderer': p[3],       # Renderer est une chaîne de caractères
        'arguments': [p[5], p[7], p[9], p[11]]   # Liste des expressions
    }






def p_error(p):
    if p:
        # Cas d'erreur syntaxique
        print(f"Erreur syntaxique : token inattendu '{p.value}' (type : {p.type}) à la ligne {p.lineno}.")

        # Afficher le contexte autour de l'erreur
        context_lines = get_context_lines(p.lexer.lexdata, p.lineno, 3)
        print("Contexte autour de l'erreur :")
        print(context_lines)

        # Suggérer des vérifications pour corriger l'erreur
        print("Vérifiez votre syntaxe près de cette ligne.")
    else:
        # Cas d'erreur sans token détecté
        print("Erreur syntaxique : fin de fichier inattendue ou élément non attendu.")
        try:
            # Affiche la dernière ligne du fichier pour donner un indice
            with open(input_file, 'r') as f:
                lines = f.readlines()
                if lexer.lineno <= len(lines):
                    print(f"Erreur à la ligne {lexer.lineno} : {lines[lexer.lineno - 1].strip()}")
                else:
                    print("Impossible de localiser la ligne fautive.")
        except Exception as e:
            print(f"Impossible de récupérer le contexte du fichier : {e}")

def find_variable_error(name):
    """
    Vérifie si une variable est déclarée. Si elle n'existe pas, lève une exception.
    """
    try:
        return find_variable(name)
    except NameError as e:
        print(f"Erreur : {e}")


def get_context_lines(input_data, lineno, num_lines=3):
    """
    Retourne quelques lignes autour de l'erreur pour donner un contexte.
    """
    lines = input_data.split('\n')
    start = max(0, lineno - num_lines - 1)
    end = min(len(lines), lineno + num_lines)
    return '\n'.join(f"{i + 1}: {lines[i]}" for i in range(start, end))

parser = yacc.yacc()





def translate_to_c(ast, indent_level=1):
    """
    Traduit un arbre syntaxique complet en code C.
    """
    translated_code = ""
    indent = "\t" * indent_level

    for node in ast:
        if node['type'] == 'int':
            value = translate_expression_to_c(node['expression'])
            translated_code += f"{indent}int {node['name']} = {value};\n"
        elif node['type'] == 'float':
            value = translate_expression_to_c(node['expression'])
            translated_code += f"{indent}float {node['name']} = {value};\n"
        elif node['type'] == 'assignment':
            value = translate_expression_to_c(node['expression'])
            translated_code += f"{indent}{node['name']} = {value};\n"
        elif node['type'] == 'animation':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}animation({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawline':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawLine({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawsquare':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawSquare({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawrectangle':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawRectangle({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawrhombus':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawRhombus({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawtriangle':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawTriangle({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawrighttriangle':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawRightTriangle({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawparallelogram':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawParallelogram({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawtrapezium':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawTrapezium({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawpolygon':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawPolygon({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'drawcircle':
            renderer = node['renderer']
            arguments = [translate_expression_to_c(arg) for arg in node['arguments']]
            translated_code += f"{indent}drawFilledCircle({renderer}, {', '.join(arguments)});\n"
        elif node['type'] == 'if':
            condition = translate_condition_to_c(node['condition'])
            translated_code += f"{indent}if ({condition}) {{\n"
            translated_code += translate_to_c(node['if_body'], indent_level + 1)
            translated_code += f"{indent}}}\n"
            if 'else_body' in node:
                translated_code += f"{indent}else {{\n"
                translated_code += translate_to_c(node['else_body'], indent_level + 1)
                translated_code += f"{indent}}}\n"
        elif node['type'] == 'if':
            condition = translate_condition_to_c(node['condition'])
            translated_code += f"{indent}if ({condition}) {{\n"
            translated_code += translate_to_c(node['if_body'], indent_level + 1)
            translated_code += f"{indent}}}\n"
            if 'else_body' in node:
                translated_code += f"{indent}else {{\n"
                translated_code += translate_to_c(node['else_body'], indent_level + 1)
                translated_code += f"{indent}}}\n"
        elif node['type'] == 'for':
            init = translate_to_c([node['init']], 0).strip()
            condition = translate_condition_to_c(node['condition'])
            update = translate_to_c([node['update']], 0).strip()
            if update.endswith(";"):
                update = update[:-1]  # Enlève le dernier caractère s'il s'agit d'un point-virgule
            translated_code += f"{indent}for ({init} {condition}; {update}) {{\n"
            translated_code += translate_to_c(node['body'], indent_level + 1)
            translated_code += f"{indent}}}\n"
        elif node['type'] == 'while':
            condition = translate_condition_to_c(node['condition'])
            translated_code += f"{indent}while ({condition}) {{\n"
            translated_code += translate_to_c(node['body'], indent_level + 1)
            translated_code += f"{indent}}}\n"
        else:
            raise ValueError(f"Type de nœud inconnu : {node['type']}")

    return translated_code



def translate_expression_to_c(expression):
    """
    Traduit une expression en code C.
    """
    if expression['type'] == 'literal':
        return str(expression['value'])
    elif expression['type'] == 'identifier':
        return expression['name']
    elif expression['type'] == 'binary_operation':
        left = translate_expression_to_c(expression['left'])
        right = translate_expression_to_c(expression['right'])
        operator = expression['operator']
        return f"({left} {operator} {right})"
    else:
        raise ValueError(f"Type d'expression inconnu : {expression['type']}")


def translate_condition_to_c(condition):
    """
    Traduit une condition en code C, même sans champ 'type'.
    """
    # Vérifiez si la condition contient un opérateur logique ou de comparaison
    if condition['operator'] in ['<', '>', '==']:
        # C'est une comparaison
        left = translate_expression_to_c(condition['left'])
        right = translate_expression_to_c(condition['right'])
        return f"({left} {condition['operator']} {right})"
    elif condition['operator'] in ['&&', '||']:
        # C'est une opération logique
        left = translate_condition_to_c(condition['left'])
        right = translate_condition_to_c(condition['right'])
        return f"({left} {condition['operator']} {right})"
    else:
        raise ValueError(f"Opérateur inconnu dans la condition : {condition['operator']}")



def replace_code_in_c_file(c_filename, translated_code):
    try:
        with open(c_filename, 'r') as file:
            c_code = file.read()
        insertion_point = c_code.find("SDL_RenderClear(renderer);")
        if insertion_point == -1:
            raise ValueError("Ligne SDL_RenderClear(renderer); non trouvée dans le fichier C.")

        new_c_code = (c_code[:insertion_point + len("SDL_RenderClear(renderer);\n")]
                     + "\n" + translated_code + "\n" + c_code[insertion_point + len("SDL_RenderClear(renderer);\n"):])

        with open(c_filename, 'w') as file:
            file.write(new_c_code)
    except Exception as e:
        print(f"Erreur lors de la modification du fichier C : {e}")


def delete_file_if_exists(file_path):
    """Supprime le fichier s'il existe."""
    if os.path.exists(file_path):
        os.remove(file_path)

def copy_and_rename_file(src, dest):
    """Copie un fichier et le renomme."""
    shutil.copy(src, dest)


def replace_code_in_c_file(file_path, translated_code):
    """Remplace une section spécifique dans le fichier C."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Trouve l'endroit où insérer le code traduit
    with open(file_path, 'w') as file:
        for line in lines:
            if "SDL_RenderClear(renderer);" in line:  # Exemple de point d'insertion
                file.write(line)
                file.write(translated_code + "\n")  # Insère le code traduit
            else:
                file.write(line)

def compile_and_run_c_file():
    """Compile et exécute un fichier C avec SDL2."""
    compile_command = [
        "gcc", "-o", "sdltest", "newtemp.c",
        "-Isrc/include", "-Lsrc/lib",
        "-lmingw32", "-lSDL2main", "-lSDL2"
    ]

    try:
        # Compilation
        result = subprocess.run(
            compile_command,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Compilation réussie.")
            print(result.stdout)  # Affiche la sortie standard (si nécessaire)

            # Exécution
            run_command = ["./sdltest"] if os.name != "nt" else ["sdltest.exe"]
            subprocess.run(run_command, check=True)
            print("Exécution terminée.")
        else:
            print("Erreur de compilation.")
            print(result.stderr)  # Affiche les erreurs de compilation

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution : {e}")

# -----------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python newtrad.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Erreur : Le fichier {input_file} n'existe pas.")
        sys.exit(1)
    current_directory = os.getcwd()

    template_file = "template.c"
    new_file = "newtemp.c"

    with open(input_file, 'r') as file:
        drawpp_code = file.read().rstrip()
        try:
            # Initialisation du lexer
            lexer.input(drawpp_code)

            while True:
                tok = lexer.token()
                if not tok:
                    break


            # Analyse syntaxique
            lexer.lineno = 1
            parsed_code = parser.parse(drawpp_code)

            # Vérification explicite de la position
            if lexer.lexpos < len(lexer.lexdata):
                print(f"[DEBUG] Données non consommées après analyse : Position actuelle : {lexer.lexpos}/{len(lexer.lexdata)}")
            else:
                print("[DEBUG] Analyse terminée sans données résiduelles.")
                print("Code analysé (formaté) :")
                print(json.dumps(parsed_code, indent=4))

                traduite = translate_to_c(parsed_code)

                delete_file_if_exists(new_file)  # Étape 1 : Supprimer newtemp.c
                copy_and_rename_file(template_file, new_file)  # Étape 2 : Copier et renommer template.c
                replace_code_in_c_file(new_file, traduite)  # Étape 3 : Insérer le code traduit
                compile_and_run_c_file()  # Étape 4 : Compiler et exécuter

        except Exception as e:
            print(f"Erreur inattendue : {e}")