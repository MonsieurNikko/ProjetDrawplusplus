import customtkinter as tk
from tkinter import filedialog, Text, Scrollbar, Menu


def open_file():
    file_path = filedialog.askopenfilename(
        title="recherche un fichier",
        filetypes=[("Text Files", ".txt")]
    )
    if file_path:
        with open(file_path, "r") as file:
            editor.delete(1.0, tk.END)  # Supprime tout le texte dans l'éditeur
            editor.insert(tk.END, file.read())  # Insère le contenu du fichier
        global classic_file_path
        classic_file_path = file_path


def save_file():
    try :
        with open(classic_file_path, "w") as file:
            file.write(editor.get(1.0, tk.END))  # Écrit le contenu de l'éditeur dans le fichier
    except NameError : 
        save_as_file()

def save_as_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", ".txt")],
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(editor.get(1.0, tk.END))  # Écrit le contenu de l'éditeur dans le fichier
        global classic_file_path
        classic_file_path = file_path


root = tk.CTk()
root.title("Simple Python IDE")
#root.resizable(False,False)

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
file_menu.add_command(label="Ouvrir", command=open_file)
file_menu.add_command(label="Sauvegarder", command=save_file)
file_menu.add_command(label="Sauvegarder sous", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=root.quit)


editor = Text(root, height=25, width=80, wrap=tk.NONE)
editor.pack(expand=1,fill=tk.BOTH)





root.mainloop()

