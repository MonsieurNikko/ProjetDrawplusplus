import subprocess  # Import pour exécuter le traducteur
import os
import sys

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"La bibliothèque '{package}' n'est pas installée. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"La bibliothèque '{package}' a été installée avec succès.")

# Vérifier et installer la bibliothèque 'tkinter' si nécessaire
install_and_import('tkinter')
# Vérifier et installer la bibliothèque 'customtkinter' si nécessaire
install_and_import('customtkinter')

import customtkinter as tk
from tkinter import filedialog, Menu

# Déclare la variable classic_file_path globalement
classic_file_path = ""

# Fonction pour ouvrir un fichier
def open_file():
    global classic_file_path  # Utilisation globale de classic_file_path
    file_path = filedialog.askopenfilename(
        title="Recherche un fichier",
        filetypes=[("Text Files", "*.txt"), ("Draw++ Files", "*.drawpp")]
    )
    if file_path:
        with open(file_path, "r") as file:
            editor.delete(1.0, tk.END)  # Supprime tout le texte dans l'éditeur
            editor.insert(tk.END, file.read())  # Insère le contenu du fichier
        classic_file_path = file_path  # Enregistre le chemin du fichier ouvert
        print(f"Fichier ouvert : {classic_file_path}")  # Affiche pour le débogage
    else:
        print("Aucun fichier n'a été sélectionné.")  # Affiche pour le débogage

# Fonction pour sauvegarder un fichier
def save_file():
    try:
        with open(classic_file_path, "w") as file:
            file.write(editor.get(1.0, tk.END))  # Sauvegarde le texte
    except NameError:
        save_as_file()

# Fonction pour sauvegarder un fichier sous un nouveau nom
def save_as_file():
    file_path = filedialog.asksaveasfilename(
        title="Enregistrer sous",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("Draw++ Files", "*.drawpp")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(editor.get(1.0, tk.END))  # Sauvegarde le texte
        global classic_file_path
        classic_file_path = file_path  # Met à jour le chemin du fichier
        print(f"Fichier enregistré sous : {classic_file_path}")  # Affiche pour le débogage
    else:
        print("Aucun fichier n'a été enregistré.")  # Affiche pour le débogage

# Fonction pour exécuter le code
def execute_code():
    global classic_file_path  # Utilisation globale de classic_file_path
    code = ""

    # Si un fichier est ouvert, utilise son contenu
    if classic_file_path:
        with open(classic_file_path, "r") as file:
            code = file.read()
    else:
        # Sinon, utilise le contenu de l'éditeur de texte
        code = editor.get(1.0, tk.END)

    if not code.strip():
        output_text.insert(tk.END, "Erreur : Aucun code à exécuter.\n")
        output_text.yview(tk.END)  # Faire défiler automatiquement
        return

    # Sauvegarde le code dans un fichier temporaire
    temp_file_path = os.path.join(os.getcwd(), 'temp_input.drawpp')
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(code)

    # Exécution du traducteur
    try:
        result = subprocess.run(
            ['python', 'newtrad.py', temp_file_path], 
            text=True, 
            capture_output=True
        )

        if result.returncode == 0:
            output_text.insert(tk.END, result.stdout + "\n")
        else:
            output_text.insert(tk.END, f"Erreur : {result.stderr}\n")

        output_text.yview(tk.END)  # Faire défiler automatiquement
    except Exception as e:
        output_text.insert(tk.END, f"Erreur lors de l'exécution : {e}\n")
        output_text.yview(tk.END)  # Faire défiler automatiquement

def clear_output():
    output_text.delete(1.0, tk.END)  # Supprime tout le contenu de la zone d'affichage

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

# Création d'un cadre pour l'éditeur de texte et la sortie
frame = tk.CTkFrame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Editeur à gauche
editor_frame = tk.CTkFrame(frame, width=400, height=700)
editor_frame.pack(side="left", fill=tk.BOTH, expand=True)

editor = tk.CTkTextbox(editor_frame, height=25, width=80, wrap="word", fg_color="#F0F0F0", text_color="#333333", font=("Arial", 12))  # Police 12
editor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Séparateur entre l'éditeur et la sortie
separator = tk.CTkCanvas(frame, width=20, bg="#333333", height=700)
separator.pack(side="left", fill="y")

# Output à droite
output_frame = tk.CTkFrame(frame, width=400, height=700)
output_frame.pack(side="right", fill=tk.BOTH, expand=True)

output_text = tk.CTkTextbox(output_frame, height=25, width=80, wrap="word", fg_color="#F0F0F0", text_color="#333333", font=("Arial", 12))
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.CTkScrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.configure(yscrollcommand=scrollbar.set)

# Couleur spécifique pour chaque bouton
button_color = "#313bd1"  # Couleur par défaut pour les autres boutons
execute_button_color = "#4CAF50"  # Couleur verte pour le bouton "Exécuter"

# Boutons d’action directement dans la fenêtre principale
open_button = tk.CTkButton(root, text="Ouvrir un fichier", command=open_file, width=15, fg_color=button_color)
open_button.pack(side="left", padx=20, pady=20)

save_button = tk.CTkButton(root, text="Sauvegarder", command=save_file, width=15, fg_color=button_color)
save_button.pack(side="left", padx=20)

save_as_button = tk.CTkButton(root, text="Sauvegarder sous", command=save_as_file, width=15, fg_color=button_color)
save_as_button.pack(side="left", padx=20)

# Bouton "Exécuter" en vert
execute_button = tk.CTkButton(root, text="Exécuter", command=execute_code, width=15, fg_color=execute_button_color)
execute_button.pack(side="left", padx=20)

leave_button = tk.CTkButton(root, text="Quitter", command=root.quit, width=15, fg_color=button_color)
leave_button.pack(side="left", padx=20)

# Centrer les boutons sous l'éditeur
leave_button.pack(side="left", padx=20)

clear_button = tk.CTkButton(root, text="Clear", command=clear_output, width=15, fg_color="#FF6347")  # Bouton rouge clair
clear_button.pack(side="left", padx=20)

# Lancement de l'interface graphique
root.mainloop()
