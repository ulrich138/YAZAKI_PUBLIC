import customtkinter
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from Consulter_Note import open_toplevel_window
from tkinter import ttk
import tkinter as tk
from PIL import Image
from Database import database_con

user = "ulrich1"
database = "evaluation"


def voir_examen(fenetre_precedente):
    fenetre_precedente.withdraw()
    Ajout = ctk.CTkToplevel(fenetre_precedente)
    Ajout.state("zoomed")
    Ajout.iconbitmap("Image/YazakiLogos.ico")
    Ajout.title(" Logiciel de Formation ")

    frame_ajout_button = ctk.CTkFrame(Ajout, height=150, width=500, fg_color="#FFFFFF", border_color="#0000FF")
    frame_ajout_button.pack(side="top", padx=100, pady=10)

    frame_ajout_tree = ctk.CTkScrollableFrame(Ajout)
    frame_ajout_tree.pack(side="bottom", padx=30, pady=10, fill="both", expand="True")

    my_image = customtkinter.CTkImage(light_image=Image.open("Image\LOGO.png"),
                                      size=(100, 15))
    image_label = customtkinter.CTkLabel(Ajout, image=my_image, text="")
    image_label.place(relx=1, rely=0, anchor='ne')

    image_recherche = ctk.CTkImage(light_image=Image.open("Image\search.png"), size=(30, 20))
    global recherche_entry
    recherche_entry = ctk.CTkEntry(frame_ajout_button, width=270, height=35)
    recherche_entry.insert(0, "Recherche")
    recherche_entry.bind("<FocusIn>", lambda e: recherche_entry.delete('0', 'end'))
    recherche_entry.grid(row=1, column=5, padx=0, pady=15)

    button_recherche = ctk.CTkButton(frame_ajout_button, text="", fg_color="#FFFFFF", width=5, font=("Arial Black", 15),
                                     text_color="white",
                                     command=search)
    button_recherche.grid(row=1, column=6, padx=0, pady=15)
    button_recherche.configure(image=image_recherche, compound="right")

    button = ctk.CTkButton(frame_ajout_button, text="Insérer", font=("Arial Black", 15), text_color="white"
                           , command=Ajout_Examen)
    button.configure(fg_color="#32CD32", hover_color="#007F00", compound="right")
    button.grid(row=1, column=0, padx=15, pady=15, sticky="w")

    button_Consulter = ctk.CTkButton(frame_ajout_button, text="Consulter", font=("Arial Black", 15), text_color="white"
                                     , command=lambda: Consulter(Ajout))
    button_Consulter.configure(fg_color="#0000FF", compound="right")
    button_Consulter.grid(row=1, column=2, padx=15, pady=15, sticky="w")

    delete_button = ctk.CTkButton(frame_ajout_button, text="Supprimer", font=("Arial Black", 15), text_color="white"
                                  , command=lambda: delete_selected( database))
    delete_button.configure(fg_color="#D2122E", hover_color="#7C0A02", compound="right")
    delete_button.grid(row=1, column=3, padx=15, pady=15)

    image_ins = ctk.CTkImage(light_image=Image.open("Image\\retour.png"), size=(30, 30))

    exit_button = ctk.CTkButton(Ajout, text="", image=image_ins, width=10, fg_color="#DCDCDC",
                                command=lambda: revenir_fenetre_precedente(Ajout, fenetre_precedente))
    exit_button.place(relx=0.005, rely=0.018)

    cols = ("liste_Session_Examen")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 20, "bold"), rowheight=25)
    style.configure("Treeview", font=("Helvetica", 14), rowheight=20)
    style.map("Treeview", foreground=[('selected', 'white')], background=[('selected', 'blue')])

    global treeview
    treeview = ttk.Treeview(frame_ajout_tree, show="headings",
                            columns=cols, height=frame_ajout_tree.winfo_screenheight(), )
    treeview.column("liste_Session_Examen", width=1500)

    treeview.grid()
    # treeScroll.config(command=treeview.yview)
    Charger_Session( database)


def revenir_fenetre_precedente(fenetre, fenetre_precedente):
    fenetre.withdraw()  # Fermer la fenêtre actuelle
    fenetre_precedente.state("zoomed")
    fenetre_precedente.deiconify()


def Charger_Session(database):
    con, cursor = database_con(database,  user)

    if con is None or cursor is None:
        print(f"pas de connexion")
        return

    try:
        cursor.execute("SHOW TABLES")
        table_names = [row[0] for row in cursor.fetchall()]
        treeview.heading("liste_Session_Examen", text="Liste des Sessions d'examen")

        # Vider le Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insérer les noms des tables dans le Treeview
        for table in table_names:
            treeview.insert('', tk.END, values=(table,))
            print(table)

        cursor.close()
        con.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Erreur", f"Erreur de connexion : {str(e)}")


def Ajout_Examen():
    global input_value
    dialog = ctk.CTkInputDialog(text="Code", title="Session Examen")

    while True:
        input_value = dialog.get_input()
        if input_value is None:
            messagebox.showwarning("info", "Aucun code saisie.")
            return
        if input_value.startswith(" ") or input_value.endswith(" "):
            messagebox.showerror("Erreur", "Format du code incorrect")
            dialog = ctk.CTkInputDialog(text="Code", title="Session Examen")


        else:
            manage_table("evaluation", input_value)
            break


def table_exists(cursor, table_name):
    cursor.execute("SHOW TABLES LIKE %s", (table_name,))
    return cursor.fetchone() is not None


def create_table_with_columns(cursor, table_name, columns):
    columns_definition = ", ".join([f"{col} VARCHAR(40)" for col in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
    try:
        cursor.execute(create_table_query)
        print(f"Table {table_name} created successfully.")
    except mysql.connector.Error as e:
        print(f"Erreur de création de la table: {e}")


def manage_table(database,  table_name):
    # Connexion à la base de données
    con, cursor = database_con(database, user)

    try:
        # Traitement du nom
        table_name = traitement_sheet_name(table_name)
        # Vérifier si la table existe
        if table_exists(cursor, table_name):
            messagebox.showwarning("Warning", f"La session d'examen '{table_name}' existe déjà.")
        else:
            # Demander confirmation à l'utilisateur avant de créer la table
            confirmation = messagebox.askyesno("Confirmation",
                                               f"Voulez-vous vraiment créer la session d'examen '{table_name}' ?")

            if confirmation:

                # Créer la table avec les colonnes spécifiées
                create_table_with_columns(cursor, table_name,
                                          ["Nom", "Matricule", "Note_temps", "Note_qualité", "Note_QCM",
                                           "column_image_1", "column_image_2", "column_image_3", "column_image_4"])
                con.commit()

                Charger_Session( database)

                messagebox.showinfo("Réussie", f"Session d'examen '{table_name}' créée avec succès.")
            else:
                messagebox.showinfo("Annulation", f"Création de la session '{table_name}' annulée.")
    except mysql.connector.Error as e:
        messagebox.showerror("Erreur", f"Erreur de connexion : {str(e)}")
    finally:
        cursor.close()
        con.close()


def search():
    # Obtenir les critères de recherche
    query_name = recherche_entry.get().strip().lower()

    # Effacer les sélections actuelles dans le Treeview
    treeview.selection_remove(treeview.selection())
    for row in treeview.get_children():
        values = treeview.item(row, "values")
        name = values[0].lower()

        # Sélectionner les lignes correspondant aux critères de recherche
        if (query_name and query_name in name):
            treeview.selection_add(row)
            treeview.see(row)


def delete_selected( database):
    selected_item = treeview.selection()

    if not selected_item:
        return

    con, cursor = database_con(database,  user)

    try:
        # Parcourir et supprimer chaque élément sélectionné
        for item in selected_item:
            # Récupérer les informations de l'élément sélectionné
            item_values = treeview.item(item, 'values')
            table_name = item_values[0]  # Supposons que le nom de la table est dans la première colonne

            confirmation = messagebox.askyesno("Confirmation",
                                               f"Voulez-vous vraiment supprimer la Session d'examen '{table_name}' ?")

            if confirmation:
                treeview.delete(item)
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                con.commit()
                messagebox.showinfo("Réussie", f"Suppression de la Session d'examen '{table_name}' réussie.")
            else:
                messagebox.showwarning("Annulation", f"Suppression de la Session d'examen '{table_name}' annulée.")

    except mysql.connector.Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")
    finally:
        cursor.close()
        con.close()

    Charger_Session(database)


def Consulter(master):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner une Session à consulter.")
        return
    for item in selected_item:  # Récupérer les informations de l'élément sélectionné
        item_values = treeview.item(item, 'values')
        fichier_name = item_values[0]
        open_toplevel_window(master, fichier_name)


def traitement_sheet_name(sheet_name):
    # Remplacer les caractères non valides par des underscores ou les supprimer
    invalid_chars = ['/', '\\', '*', '?', ':', '[', ']', '-', " "]
    for char in invalid_chars:
        sheet_name = sheet_name.replace(char, '_')
    sheet_name = "Session_" + sheet_name
    return sheet_name
