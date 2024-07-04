import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkToplevel
from Database import database_con
from Formateur import acess_Formateur
from PIL import Image
from Operateurs import acess_Operateur

user = "ulrich1"

app = ctk.CTk()
ap = app
app.withdraw()
fenetreprin = CTkToplevel(app)
fenetreprin.cgit onfigure(fg_color="white")
fenetreprin.state('zoomed')
fenetreprin.title(" Logiciel de Formation")

frameprin = ctk.CTkFrame(master=fenetreprin, fg_color="white")
frameprin.pack(pady=0, padx=0, fill="both")


# fenetreprin.iconbitmap("Image/YazakiLogos.ico")


def fermer(app, F):
    F.destroy()
    app.destroy()


# Définir l'icône de la fenêtre
# fenetreprin.iconphoto(False, icon_photo)

largeur_fenetre = frameprin.winfo_screenwidth()
longueur_fenetre = frameprin.winfo_screenheight()
print(largeur_fenetre)
print(longueur_fenetre)


def verif(fenetre, selection, nom, matricule):

    acess_Formateur(fenetre, nom, matricule)

    """
    con, cursor = database_con("operateur_formateur", user)

    if selection == "Operateur":

        query_select = f"SELECT COUNT(*) FROM operateur WHERE  nom = %s"
        cursor.execute(query_select, (nom,))
        result = cursor.fetchone()

        if result[0] == 0:
            messagebox.showerror('Erreur', "Cet Operateur n'existe pas",
                                 parent=fenetre)
        else:
            query_select = f"SELECT COUNT(*) FROM operateur WHERE  matricule = %s"
            cursor.execute(query_select, (matricule,))
            result = cursor.fetchone()

            if result[0] == 0 or matricule is None:
                messagebox.showerror('Erreur', "Mot de passe incorrect",
                                     parent=fenetre)
            else:
                acess_Operateur(fenetre, nom, matricule)
                champ_id.delete(0, "end")
                champ_mp.delete(0, "end")


    elif selection == "Formateur":
        query_select = f"SELECT COUNT(*) FROM  formateur WHERE  identifiant = %s"
        cursor.execute(query_select, (nom,))
        result = cursor.fetchone()

        if result[0] == 0 or nom is None:
            messagebox.showerror('Erreur', "Cet Formateur n'existe pas",
                                 parent=fenetre)
        else:
            query_select = f"SELECT COUNT(*) FROM formateur WHERE   mot_de_passe = %s"
            cursor.execute(query_select, (matricule,))
            result = cursor.fetchone()
            if result[0] == 0 or matricule is None:
                messagebox.showerror('Erreur', "Mot de passe incorrect",
                                     parent=fenetre)
            else:
                acess_Formateur(fenetre, nom, matricule)
                champ_id.delete(0, "end")
                champ_mp.delete(0, "end")

    else:
        messagebox.showinfo('Info', "Veuillez choisi votre poste",
                            parent=fenetre)

    con.close()
    cursor.close()"""


def Choix_personnage(fenetre):
    fenetre.withdraw()
    choix_personnage = ctk.CTkToplevel(fenetre)
    global champ_id, champ_mp

    choix_personnage.state("zoomed")
    choix_personnage.title(" Logiciel de Formation ")
    choix_personnage.configure(fg_color="white")
    # choix_personnage.config(bg="Light")

    choix_personnage.iconbitmap("Image/YazakiLogos.ico")

    frame = ctk.CTkScrollableFrame(choix_personnage)
    frame.pack(padx=400, pady=200, fill="both", expand="True")

    text_choix = "Veuillez vous identifier et signaler si vous êtes un formateur ou un opérateur "
    label_choix = ctk.CTkLabel(choix_personnage, text=text_choix, font=("Arial Rounded MT Bold", 30), justify="center")
    label_choix.place(x=largeur_fenetre // 2, anchor="center", y=100)
    # label_choix.configure(  fg_color= "#75BCF5")

    label_login = ctk.CTkLabel(frame, text="Se connecter", font=("Arial Rounded MT Bold", 20), text_color="black")
    label_login.pack(pady=15, padx=10)

    champ_id = ctk.CTkEntry(frame, placeholder_text="Identifiant", text_color="black", width=180, height=29)
    champ_id.pack(pady=15)
    nom = champ_id.get()

    champ_mp = ctk.CTkEntry(frame, placeholder_text="Mot de passe", text_color="black", show="*", width=180, height=29)
    champ_mp.pack(pady=15)
    matricule = champ_mp.get()

    optionmenu_var = ctk.StringVar(value="choisisez")
    optionmenu = ctk.CTkOptionMenu(frame, values=["Operateur", "Formateur"], variable=optionmenu_var,
                                   text_color="white", font=("Arial Black", 15))
    optionmenu.pack(pady=15)
    selection = optionmenu_var.get()

    bp_conex = ctk.CTkButton(frame, text=" Connexion ", text_color="white", font=("Arial Black", 15),
                             command=lambda: verif(choix_personnage, optionmenu_var.get(),
                                                   champ_id.get(), champ_mp.get()))
    bp_conex.configure(fg_color="blue")
    bp_conex.pack(pady=30)

    Exit_button = ctk.CTkButton(choix_personnage, text="Exit", font=("Arial Black", 15), text_color="white",
                                command=lambda: revenir_fenetre_precedente(choix_personnage, fenetre))
    Exit_button.configure(fg_color="red")
    Exit_button.pack(pady=20)
    Exit_button.place(x=30, rely=0.92)

    def revenir_fenetre_precedente(fenetre, fenetre_precedente):
        fenetre.withdraw()  # Fermer la fenêtre actuelle
        fenetre_precedente.state("zoomed")
        fenetre_precedente.deiconify()  # Rendre la fenêtre précédente visible


my_image = ctk.CTkImage(light_image=Image.open("Image\LO.png"),
                        size=(largeur_fenetre, longueur_fenetre))
image_label = ctk.CTkLabel(frameprin, image=my_image, text="", fg_color="white")  # display image with a CTkLabel
image_label.pack()

texte_bienvenueFr = ("Bienvenue sur le logiciel de simulation. Veuillez appuyer sur 'Next' pour continuer ou sur "
                     "'Exit' pour quitter.")
label_bienvenueFr = ctk.CTkLabel(frameprin, text=texte_bienvenueFr, font=("Helvetica", 20), fg_color="white",
                                 justify="center")
label_bienvenueFr.place(x=largeur_fenetre // 2, rely=0.08, anchor="center", )

texte_bienvenueEn = "Welcome to the simulation software. Please press 'Next' to continue or 'Exit' to quit."
label_bienvenueEn = ctk.CTkLabel(frameprin, text=texte_bienvenueEn, font=("Helvetica", 20), fg_color="white",
                                 justify="center")
label_bienvenueEn.place(x=largeur_fenetre // 2, anchor="center", rely=0.13)

texte_bienvenueAn = "シミュレーションソフトウェアへようこそ。続行するには「Next」を押すか、終了するには「Exit」を押してください。"
label_bienvenueAn = ctk.CTkLabel(frameprin, text=texte_bienvenueAn, font=("Helvetica", 20), fg_color="white",
                                 justify="center")
label_bienvenueAn.place(x=largeur_fenetre // 2, anchor="center", rely=0.18)

texte_bienvenueAr = " للمتابعة ,'Next' للخروج أو 'Exit',مرحبًا بك في برنامج المحاكاة. يرجى الضغط على ."
label_bienvenueAr = ctk.CTkLabel(frameprin, text=texte_bienvenueAr, font=("Helvetica", 20), fg_color="white",
                                 justify="center")
label_bienvenueAr.place(x=largeur_fenetre // 2, anchor="center", rely=0.23)

next_button = ctk.CTkButton(frameprin, text="Next", text_color="white", font=("Arial Black", 15),
                            command=lambda: Choix_personnage(fenetreprin))
next_button.configure(fg_color="blue")
next_button.pack(pady=20)
next_button.place(x=largeur_fenetre - 170, rely=0.92)

Exit_button = ctk.CTkButton(frameprin, text="Exit", text_color="white", font=("Arial Black", 15),
                            command=lambda: fermer(ap, fenetreprin))
Exit_button.configure(fg_color="red")
Exit_button.pack(pady=20)
Exit_button.place(x=30, rely=0.92)

fenetreprin.mainloop()
