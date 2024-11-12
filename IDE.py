import customtkinter as tk
from customtkinter import filedialog
import subprocess
#import sys
#import io

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
    except PermissionError:
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

def traduction():
    save_file()
    subprocess.run(["python3","traducteur.py",classic_file_path])

# Création de l'adresse par défaut 
global classic_file_path
classic_file_path = "H:/Documents/"

# Création de la fenêtre principale
root = tk.CTk()
root.title("IDE DRAW++")
root.geometry("800x600")  # Taille de la fenêtre
root.config(bg="#2E3A47")  # Fond sombre #2E3A47

# Titre et description de l'IDE
title_label = tk.CTkLabel(root, text="Bienvenue dans l'IDE DRAW++", font=("Helvetica", 20, "bold"), text_color="white", bg_color="#2E3A47")
title_label.pack(pady=10)

description_label = tk.CTkLabel(root, text="Un éditeur simple pour vos scripts DRAW++\n\nUtilisez les options du menu pour ouvrir ou sauvegarder un fichier.", font=("Helvetica", 14), text_color="white", bg_color="#2E3A47")
description_label.pack(pady=10)

# Création de l'éditeur de texte avec police plus grande
editor = tk.CTkTextbox(root, height=25, width=80, wrap="word", fg_color="#F0F0F0", text_color="#333333", font=("Arial", 15))  # Police 50
editor.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

# Frame pour y mettre les boutons
frame = tk.CTkFrame(root, fg_color="#2E3A47",corner_radius=0) 
frame.pack(fill="both")

# Boutons d’action personnalisés
open_button = tk.CTkButton(frame, text="Ouvrir un fichier", command=open_file, width=15)
open_button.pack(side="left", padx=20, pady=20)

save_button = tk.CTkButton(frame, text="Sauvegarder", command=save_file, width=15)
save_button.pack(side="left", padx=20)

save_as_button = tk.CTkButton(frame, text="Sauvegarder sous", command=save_as_file, width=15)
save_as_button.pack(side="left", padx=20)

leave_button = tk.CTkButton(frame, text="Quitter", command=quit, width=15)
leave_button.pack(side="left", padx=20)

execute_button = tk.CTkButton(frame, text="Exécuter", width=15, fg_color="#4CAF50", command=traduction)
execute_button.pack(side="left", padx=20)

# Boucle principale pour afficher l'interface
root.mainloop()
