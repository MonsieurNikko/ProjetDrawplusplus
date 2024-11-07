import customtkinter as tk
from tkinter import filedialog, Menu
import sys
import io

# Fonction pour ouvrir un fichier
def open_file():
    file_path = filedialog.askopenfilename(
        title="Recherche un fichier",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        with open(file_path, "r") as file:
            editor.delete(1.0, tk.END)  # Supprime tout le texte dans l'éditeur
            editor.insert(tk.END, file.read())  # Insère le contenu du fichier
        global classic_file_path
        classic_file_path = file_path

# Fonction pour sauvegarder un fichier
def save_file():
    try:
        with open(classic_file_path, "w") as file:
            file.write(editor.get(1.0, tk.END))  # Sauvegarde le texte
    except NameError:
        save_as_file()

# Fonction pour "Sauvegarder sous" (création d'un nouveau fichier)
def save_as_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(editor.get(1.0, tk.END))  # Sauvegarde le texte
        global classic_file_path
        classic_file_path = file_path

""" 
        # Fonction pour exécuter le code
def execute_code():
    code = editor.get(1.0, tk.END)  # Récupère le texte de l'éditeur
    old_stdout = sys.stdout  # Redirige la sortie standard
    new_stdout = io.StringIO()
    sys.stdout = new_stdout  # Capture la sortie dans la variable `new_stdout`

    try:
        exec(code)  # Exécute le code contenu dans l'éditeur
    except Exception as e:
        new_stdout.write(f"Erreur : {e}")  # Si une erreur se produit, affiche l'erreur
    finally:
        sys.stdout = old_stdout  # Restaure la sortie standard
        result = new_stdout.getvalue()  # Récupère le résultat de l'exécution
        output_label.config(text=result)  # Affiche le résultat dans le label
"""

# Création de la fenêtre principale
root = tk.CTk()
root.title("IDE DRAW++")
root.geometry("1000x800")  # Taille de la fenêtre
root.config(bg="#2E3A47")  # Fond sombre

# Titre et description de l'IDE
title_label = tk.CTkLabel(root, text="Bienvenue dans l'IDE DRAW++", font=("Helvetica", 20, "bold"), text_color="white", bg_color="#2E3A47")
title_label.pack(pady=10)

description_label = tk.CTkLabel(root, text="Un éditeur simple pour vos scripts DRAW++\n\nUtilisez les options du menu pour ouvrir ou sauvegarder un fichier.", font=("Helvetica", 14), text_color="white", bg_color="#2E3A47")
description_label.pack(pady=10)

# Création du menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
file_menu.add_command(label="Ouvrir", command=open_file)
file_menu.add_command(label="Sauvegarder", command=save_file)
file_menu.add_command(label="Sauvegarder sous", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=root.quit)

# Création de l'éditeur de texte avec police plus grande
editor = tk.CTkTextbox(root, height=25, width=80, wrap="word", fg_color="#F0F0F0", text_color="#333333", font=("Arial", 50))  # Police 50
editor.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

# Boutons d’action personnalisés
open_button = tk.CTkButton(root, text="Ouvrir un fichier", command=open_file, width=15)
open_button.pack(side="left", padx=20, pady=20)

save_button = tk.CTkButton(root, text="Sauvegarder", command=save_file, width=15)
save_button.pack(side="left", padx=20)

save_as_button = tk.CTkButton(root, text="Sauvegarder sous", command=save_as_file, width=15)
save_as_button.pack(side="left", padx=20)

leave_button = tk.CTkButton(root, text="Quitter", command=quit, width=15)
leave_button.pack(side="left", padx=20)

""" 
# Bouton d'exécution
execute_button = tk.CTkButton(root, text="Exécuter", command=execute_code, width=15, fg_color="#4CAF50")
execute_button.pack(side="left", padx=20)

# Label pour afficher les résultats de l'exécution du code
output_label = tk.CTkLabel(root, text="", font=("Helvetica", 12), text_color="white", bg_color="#2E3A47")
output_label.pack(pady=10)
"""

# Boucle principale pour afficher l'interface
root.mainloop()
