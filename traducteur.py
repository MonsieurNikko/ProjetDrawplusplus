import re
import subprocess
import os
import sys

subprocess.run([
    "gcc",
    "-o", "sdltest",
    "d:\\projets\\drawpp\\sdltest.c",
    "-Id:\\projets\\drawpp\\src\\include",  # Chemin absolu vers l'inclusion
    "-Ld:\\projets\\drawpp\\src\\lib",      # Chemin absolu vers la bibliothèque
    "-lmingw32", "-lSDL2main", "-lSDL2"
])


# Dictionnaire de traduction de commandes vers les fonctions C
command_dict = {
    "drawSquare": "drawAnimatedSquare",
    "drawCircle": "drawAnimatedCircle",
    "drawLine": "drawAnimatedLine",
    "pause": "SDL_Delay"
}



# Fonction de traduction
def translate_command(command_line):
    match = re.match(r'(\w+)\(([^)]+)\)', command_line)

    command_name, args = match.groups()
    args = args.split(",")  # Diviser les arguments par des virgules

    # Chercher la commande dans le dictionnaire
    if command_name in command_dict:
        c_function = command_dict[command_name]

        # Si c'est une pause, on n'ajoute pas "renderer"
        if command_name == "pause":
            return f"{c_function}({args[0].strip()});"

        # Convertir la commande en appel de fonction C avec les arguments
        args_str = ", ".join(arg.strip() for arg in args)
        return f"{c_function}(renderer, {args_str});"
    else:
        return "// Commande inconnue"




# Lecture du fichier custom et traduction
def translate_custom_file_to_c(input_filename):
    translated_lines = []
    try:
        with open(input_filename, 'r') as file:
            for line in file:
                translated_line = translate_command(line.strip())
                translated_lines.append(translated_line)
    except Exception as e:
        print(f"Erreur lors de la lecture de {input_filename}: {e}")
    return "\n".join(translated_lines)



# Remplacer le code dans le fichier C
def replace_code_in_c_file(c_filename, translated_code):
    try:
        with open(c_filename, 'r') as file:
            c_code = file.read()

        # Rechercher où ajouter le code après SDL_RenderClear(renderer);
        insertion_point = c_code.find("SDL_RenderClear(renderer);")
        if insertion_point == -1:
            raise ValueError("Ligne SDL_RenderClear(renderer); non trouvée dans le fichier C.")

        # Insérer le code après le SDL_RenderClear(renderer);
        new_c_code = (c_code[:insertion_point + len("SDL_RenderClear(renderer);\n")]
                      + translated_code + "\n\n" + c_code[insertion_point + len("SDL_RenderClear(renderer);\n"):])

        with open(c_filename, 'w') as file:
            file.write(new_c_code)

        print("Code C mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de {c_filename}: {e}")


# Récuperation de l'adresse depuis l'IDE
if len(sys.argv) > 1 :
    adresse=sys.argv[1]
    print(adresse)
else : 
    print("echec")

# Exécution du processus
#input_filename = "d:\\projets\\drawpp\\instruction.txt"  # Utilisez le chemin absolu
input_filename = adresse
c_filename = "h:/Documents/Travail/Python/Projet/sdltest.c"  # Utilisez le chemin absolu

# Traduire les commandes et mettre à jour le fichier C
translated_code = translate_custom_file_to_c(input_filename)
if translated_code:
    replace_code_in_c_file(c_filename, translated_code)

    # Compiler le fichier C
    compilation_result = subprocess.run(
        ["gcc", "-o", "sdltest", "sdltest.c", "-Isrc/include", "-Lsrc/lib", "-lmingw32", "-lSDL2main", "-lSDL2"],
        capture_output=True, text=True
    )

    if compilation_result.returncode == 0:
        print("Compilation réussie.")
        # Exécuter le binaire compilé
        subprocess.run(["./sdltest"])
    else:
        print(f"Erreur de compilation:\n{compilation_result.stderr}")
else:
    print("Aucune commande traduite à insérer.")
