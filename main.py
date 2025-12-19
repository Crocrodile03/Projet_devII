"""
Module regroupant les importations nécessaires à la création de l'interface
graphique de l'application, ainsi qu'à la gestion du parking et des abonnés.

Imports :
    - os : fournit des fonctionnalités liées au système d'exploitation,
      notamment la manipulation de chemins et de fichiers.
    - tkinter as tk : bibliothèque standard pour construire l'interface
      graphique (widgets, fenêtres, événements).
    - tkinter.ttk : widgets thématiques améliorés (labels, boutons, cadres, etc.).
      Peut également fournir `messagebox` si utilisé pour afficher des dialogues.
    - datetime : gestion des dates et heures, utile notamment pour horodater
      des actions ou des abonnements.
    - Parking: classe représentant la structure et les
      fonctionnalités du parking.
    - Subscriber: classe représentant un abonné, utilisée
      pour gérer les informations et statuts des utilisateurs abonnés.

Ce module sert de base à la partie interface utilisateur de l'application,
permettant d'interagir avec le système de gestion du parking.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from parking import Parking
from subscriber import Subscriber
from exception import IsASubscriber

mon_parking = Parking()
mon_parking.load_state()

# Palette de couleur
COLOR_BG = "#344e41"      # Vert foncé
COLOR_BTN = "#588157"     # Vert moyen pour boutons
COLOR_PV = "#12b000"      # Vert foncé pour parking à -50% de place libre
COLOR_PM = "#ff8400"      # Orange pour parking à +50% de place libre
COLOR_PP = "#ff0008"      # Rouge pour parking à +75% de place libre
COLOR_BTN_HOVER = "#5a9758" # Vert clair sur hover
COLOR_LABEL = "#bbd58e"   # Vert clair pour labels/log
COLOR_ENTRY = "#3a5a40"  # Vert très clair (fond entrée)


# ============================================================
# APPLICATION TKINTER
# ============================================================

class Application(tk.Tk):
    """
    Interface graphique principale de l'application de gestion de parking.

    Cette classe hérite de `tk.Tk` et initialise l'ensemble de l'interface,
    y compris :
        - la barre latérale affichant l'état du parking,
        - la zone principale où sont chargées les différentes pages,
        - la zone de log affichant l'historique des actions utilisateur.

    Elle gère également la navigation entre les pages et la mise à jour
    périodique de l'affichage de l'état du parking.
    """

    @staticmethod
    def couleur_pourcentage(actuel, total):
        """Change la couleur en fonction du pourcentage de places occupées."""
        if total == 0:
            return COLOR_PV

        taux = actuel / total

        if taux >= 0.75:
            return COLOR_PP
        if taux >= 0.5:
            return COLOR_PM
        else:
            return COLOR_PV

    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de Parking")

        # Géométrie dynamique : 70% de la taille de l'écran, centrée
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 1)
        height = int(screen_height * 1)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.config(bg=COLOR_BG)
        # Calcul des tailles pour que tout s'affiche
        log_height = 120
        main_height = height - log_height

        # --- ZONE LOG EN BAS ---
        log_frame = tk.Frame(self,
                             height=log_height,
                             bg=COLOR_BG)
        log_frame.pack(side="bottom",
                       fill="x",
                       expand=False)

        tk.Label(log_frame,
                 text="Journal des actions",
                 font=("Arial", 12, "bold"),
                 bg=COLOR_BG,
                 fg="white").pack(anchor="w")

        self.log_text = tk.Text(log_frame,
                                height=6,
                                state="disabled",
                                bg=COLOR_LABEL)
        self.log_text.pack(side="left",
                           fill="x",
                           expand=True,
                           padx=5,
                           pady=5)

        scrollbar = tk.Scrollbar(log_frame,
                                 command=self.log_text.yview)
        scrollbar.pack(side="right",
                       fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # --- FRAME GAUCHE POUR LA LISTE DES VÉHICULES ---
        left_frame = tk.Frame(self,
                              bg=COLOR_BG,
                              relief="sunken",
                              bd=2)
        left_frame.pack(side="left", fill="y")

        left_frame.pack_propagate(False)
        left_frame.config(width=500)

        tk.Label(left_frame,
                 text="Véhicules Garés",
                 font=("Arial", 14, "bold"),
                 bg=COLOR_BG,
                 fg="white").pack(pady=10)

        # Filtre par type
        tk.Label(left_frame,
                 text="Filtrer par type",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.filter_var = tk.StringVar(value="Tous")
        types = ["Tous", "visiteur", "handicapé", "électrique", "abonné"]
        self.filter_combo = ttk.Combobox(left_frame,
                                         textvariable=self.filter_var,
                                         values=types,
                                         state="readonly")
        self.filter_combo.pack(pady=5)
        self.filter_combo.bind("<<ComboboxSelected>>", self.update_vehicle_list)

        # Frame pour envelopper le Treeview et assurer un fond uniforme
        tree_frame = tk.Frame(left_frame, bg=COLOR_LABEL)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview pour la liste permanente
        columns = ("Immatriculation", "Type", "Heure d'entrée", "Prénom", "Nom", "Téléphone")
        self.vehicle_tree = ttk.Treeview(tree_frame,
                                         columns=columns,
                                         show="headings",
                                         height=20,
                                         style="Custom.Treeview")
        for col in columns:
            self.vehicle_tree.heading(col, text=col, command=lambda c=col: self.sort_vehicle_list(c))
           # self.vehicle_tree.column(col, width=100)  # Ajuster la largeur des colonnes
            self.vehicle_tree.column("Immatriculation", width=100,anchor="center")
            self.vehicle_tree.column("Type", width=65,anchor="center")
            self.vehicle_tree.column("Heure d'entrée", width=100,anchor="center")
            self.vehicle_tree.column("Prénom", width=60,anchor="center")
            self.vehicle_tree.column("Nom", width=60,anchor="center")
            self.vehicle_tree.column("Téléphone", width=85,anchor="center")

        self.vehicle_tree.pack(fill="both", expand=True)  # Retirer padx/pady ici, car ils sont sur le frame

        # Configurer le style pour le Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", background=COLOR_LABEL, fieldbackground=COLOR_LABEL)

        # Configurer le tag pour la sélection persistante
        self.vehicle_tree.tag_configure("selected", background="lightblue")  # Couleur de surbrillance

        # Scrollbar pour le Treeview (dans le même frame)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.vehicle_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.vehicle_tree.configure(yscrollcommand=scrollbar.set)

        # Variable pour stocker l'immatriculation sélectionnée
        self.selected_immat = None
        self.sort_order = {}  # Pour gérer l'ordre de tri (asc/desc)

        # Binder la sélection
        self.vehicle_tree.bind("<<TreeviewSelect>>", self.on_vehicle_select)

        # Bouton pour sortir le véhicule sélectionné
        ttk.Button(left_frame, text="Sortir Véhicule Sélectionné",
                   command=self.remove_selected_vehicle).pack(pady=10)

        # --- FRAME PRINCIPAL ---
        main_container = tk.Frame(self,
                                  bg=COLOR_BG)
        main_container.pack(side="left",
                            fill="both",
                            expand=True)

        # --- SIDEBAR DROITE POUR L'ÉTAT ---
        sidebar = tk.Frame(self,
                           bg=COLOR_BG,
                           relief="sunken",
                           bd=2)
        sidebar.pack(side="right", fill="y")

        sidebar.pack_propagate(False)
        sidebar.config(width=450)

        tk.Label(sidebar,
                 text="État du parking",
                 font=("Arial", 14, "bold"),
                 bg=COLOR_BG,
                 fg="white").pack(pady=10)

        frame_etat = tk.Frame(sidebar, bg=COLOR_BG)
        frame_etat.pack(fill="x", padx=10)

        # --- État du parking ---
        self.label_visiteurs = tk.Label(frame_etat, font=("Arial", 12),
                                        bg=COLOR_LABEL, anchor="w")
        self.label_handicapes = tk.Label(frame_etat, font=("Arial", 12),
                                         bg=COLOR_LABEL, anchor="w")
        self.label_electriques = tk.Label(frame_etat, font=("Arial", 12),
                                          bg=COLOR_LABEL, anchor="w")
        self.label_abonnes = tk.Label(frame_etat, font=("Arial", 12),
                                      bg=COLOR_LABEL, anchor="w")

        self.label_visiteurs.pack(fill="x", pady=3)
        self.label_handicapes.pack(fill="x", pady=3)
        self.label_electriques.pack(fill="x", pady=3)
        self.label_abonnes.pack(fill="x", pady=3)



        # Chargement des pages
        self.frames = {}
        for F in (MenuPrincipal, EntreeVehicule, SortieVehicule, Abonnement, ListeVehicules):
            frame = F(main_container,
                      self)
            self.frames[F] = frame
            frame.grid(row=0,
                       column=0,
                       sticky="nsew")

        self.show_frame(MenuPrincipal)

        # Démarrer les mises à jour
        self.update_sidebar()
        self.update_vehicle_list()

    def show_frame(self, page):
        """
        Affiche la page spécifiée dans le conteneur principal.

        Paramètres: page: class
            La classe de la page à afficher. La page doit avoir été
            préalablement instanciée et stockée dans `self.frames`.
        """
        frame = self.frames[page]
        frame.tkraise()

    def update_sidebar(self):
        """Met à jour le texte de la barre latérale affichant la capacité actuelle
        du parking.

        Cette méthode récupère les valeurs de capacité depuis `mon_parking`
        puis met à jour l'étiquette correspondante. Elle se rappelle
        automatiquement toutes les 500 ms pour assurer une mise à jour continue.
        """
        # Récupération des capacités actuelles
        v, h, e, a = mon_parking.current_capacity

        # Capacités totales
        tot_v = mon_parking.max_capacity[0]
        tot_h = mon_parking.max_capacity[1]
        tot_e = mon_parking.max_capacity[2]
        tot_a = mon_parking.max_capacity[3]

        # Couleurs dynamiques selon le pourcentage
        color_v = self.couleur_pourcentage(v, tot_v)
        color_h = self.couleur_pourcentage(h, tot_h)
        color_e = self.couleur_pourcentage(e, tot_e)
        color_a = self.couleur_pourcentage(a, tot_a)

        # Mise à jour des labels
        self.label_visiteurs.config(text=f"Visiteurs : {v}/{tot_v}", fg=color_v)
        self.label_handicapes.config(text=f"Handicapés : {h}/{tot_h}", fg=color_h)
        self.label_electriques.config(text=f"Électriques : {e}/{tot_e}", fg=color_e)
        self.label_abonnes.config(text=f"Abonnés : {a}/{tot_a}", fg=color_a)

        self.after(500, self.update_sidebar)

    def log_info(self, msg):
        """
        Ajoute une entrée dans la zone de journalisation avec un horodatage.

        Paramètres: msg: str
            Le message à enregistrer dans le journal des actions.
        """
        self.log_text.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end",
                             f"[{timestamp}] {msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def quit(self):
        """Surcharge de la méthode quit pour assurer la sauvegarde."""
        self.on_closing()

    def on_closing(self):
        """Gère la fermeture de l'application en sauvegardant l'état du parking."""
        mon_parking.save_state()
        self.destroy()

    def update_vehicle_list(self, event=None):
        """Met à jour la liste des véhicules garés dans le panneau gauche."""
        # Vider la liste actuelle
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)

        # Récupérer les véhicules filtrés
        selected_type = self.filter_var.get()
        if selected_type == "Tous":
            vehicles = mon_parking.parking
        else:
            vehicles = mon_parking.find_vehicule_by_type(selected_type)

        # Ajouter les véhicules au Treeview
        for v in vehicles:
            entry_time_str = v.entry_time.strftime("%d/%m/%Y %H:%M")
            if isinstance(v, Subscriber):
                self.vehicle_tree.insert("", "end", values=(v.immatriculation,
                                                            v.type_vehicule,
                                                            entry_time_str,
                                                            v.first_name,
                                                            v.last_name,
                                                            v.phone_number))
            else:
                self.vehicle_tree.insert("", "end", values=(v.immatriculation,
                                                            v.type_vehicule,
                                                            entry_time_str,
                                                            "", "", ""))

        # Réappliquer le tag de sélection si un véhicule est sélectionné et présent dans la liste filtrée
        if self.selected_immat:
            for item in self.vehicle_tree.get_children():
                if self.vehicle_tree.item(item, 'values')[0] == self.selected_immat:
                    self.vehicle_tree.item(item, tags=("selected",))
                    break

    def sort_vehicle_list(self, col):
        """Trie la liste des véhicules par la colonne spécifiée."""
        selected_type = self.filter_var.get()
        if selected_type == "Tous":
            vehicles = mon_parking.parking[:]
        else:
            vehicles = mon_parking.find_vehicule_by_type(selected_type)[:]

        # Inverser l'ordre si déjà trié
        reverse = self.sort_order.get(col, False)
        if col == "Immatriculation":
            vehicles.sort(key=lambda v: v.immatriculation, reverse=reverse)
        elif col == "Type":
            vehicles.sort(key=lambda v: v.type_vehicule, reverse=reverse)
        elif col == "Heure d'entrée":
            vehicles.sort(key=lambda v: v.entry_time, reverse=reverse)
        else:
            return

        self.sort_order[col] = not reverse

        # Vider et recharger la liste triée
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)

        for v in vehicles:
            entry_time_str = v.entry_time.strftime("%d/%m/%Y %H:%M")
            if isinstance(v, Subscriber):
                self.vehicle_tree.insert("", "end", values=(v.immatriculation,
                                                            v.type_vehicule,
                                                            entry_time_str,
                                                            v.first_name,
                                                            v.last_name,
                                                            v.phone_number))
            else:
                self.vehicle_tree.insert("", "end", values=(v.immatriculation,
                                                            v.type_vehicule,
                                                            entry_time_str,
                                                            "", "", ""))

        # Réappliquer la sélection
        if self.selected_immat:
            for item in self.vehicle_tree.get_children():
                if self.vehicle_tree.item(item, 'values')[0] == self.selected_immat:
                    self.vehicle_tree.item(item, tags=("selected",))
                    break

    def on_vehicle_select(self, event):
        """Gère la sélection d'un véhicule dans le Treeview."""
        # Supprimer le tag de l'ancien sélectionné
        if self.selected_immat:
            for item in self.vehicle_tree.get_children():
                if self.vehicle_tree.item(item, 'values')[0] == self.selected_immat:
                    self.vehicle_tree.item(item, tags=())
                    break

        selected = self.vehicle_tree.selection()
        if selected:
            item = selected[0]
            # Vérifier si c'est le même véhicule (pour désélectionner)
            new_immat = self.vehicle_tree.item(item, 'values')[0]
            if new_immat == self.selected_immat:
                self.selected_immat = None
            else:
                self.vehicle_tree.item(item, tags=("selected",))
                self.selected_immat = new_immat

    def ouvrir_pdf(self, file_path):
        """Ouvre un fichier PDF avec le lecteur par défaut."""

        if os.name == "nt":  # Windows
            os.startfile(file_path)
        elif os.name == "posix":  # Linux / macOS
            os.system(f'xdg-open "{file_path}"')

    def remove_selected_vehicle(self):
        """Sort le véhicule sélectionné du parking."""
        if not self.selected_immat:
            messagebox.showinfo("Sélection", "Veuillez sélectionner un véhicule dans la liste.")
            return

        vehicule = next(
            (v for v in mon_parking.parking if v.immatriculation == self.selected_immat),
            None
        )

        if not vehicule:
            messagebox.showerror("Erreur", "Véhicule introuvable.")
            self.log_info(f"Erreur : tentative de sortie d'un véhicule inexistant ({self.selected_immat}).")
            return

        if mon_parking.find_vehicule(self.selected_immat).type_vehicule == 'abonné':
            self.log_info("Erreur lors de la sortie: On ne peut pas supprimer un abonné")
            messagebox.showinfo("Retirer", "Vous ne pouvez pas retirer un abonné")
            return

        try:
            tarif = mon_parking.calculate_tarif(self.selected_immat)
            pdf_path = mon_parking.generer_paiement(self.selected_immat, tarif)
            self.ouvrir_pdf(pdf_path)
            mon_parking.vehicules_leave(self.selected_immat)
            self.log_info(f"Véhicule {self.selected_immat} sorti du parking.")
            self.selected_immat = None
        except IsASubscriber as e:
            messagebox.showinfo("Retirer", "Vous ne pouvez pas retirer un abonné")
            self.log_info(f"Erreur lors de la sortie: {str(e)}")

        self.update_vehicle_list()
        self.frames[ListeVehicules].update_list()

# ============================================================
# MENU PRINCIPAL
# ============================================================

class MenuPrincipal(tk.Frame):
    """
    Page d'accueil de l'application de gestion de parking.

    Cette interface propose les actions principales :
        - Enregistrer l'entrée d'un véhicule
        - Enregistrer la sortie d'un véhicule
        - Gérer les abonnements
        - Quitter l'application

    Elle sert de hub central pour naviguer entre les différentes pages
    via les boutons affichés.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self,
                 text="Gestionnaire de Parking",
                 font=("Arial", 20),
                 bg=COLOR_BG,
                 fg="white").pack(pady=20)

        for text, page in [("Entrée d'un véhicule", EntreeVehicule),
                           ("Sortie d'un véhicule", SortieVehicule),
                           ("Gérer les abonnements", Abonnement)]:
            btn = tk.Button(self,
                            text=text,
                            font=("Arial", 12),
                            bg=COLOR_BTN,
                            fg="white",
                            activebackground=COLOR_BTN_HOVER,
                            activeforeground="white",
                            command=lambda p=page: controller.show_frame(p))
            btn.pack(pady=10,
                     ipadx=10,
                     ipady=5)

        ttk.Button(self,
                   text="Quitter",
                   command=controller.quit).pack(pady=20)
# ============================================================
# ENTRÉE VEHICULE
# ============================================================

class EntreeVehicule(tk.Frame):
    """
    Page permettant d'enregistrer l'entrée d'un véhicule dans le parking.

    L'utilisateur doit :
        - saisir l'immatriculation du véhicule,
        - choisir le type de place (visiteur, handicapé, électrique),
        - valider l'enregistrement ou revenir au menu principal.

    L'action est ensuite transmise à l'objet `mon_parking` et ajoutée
    au journal via le contrôleur.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        tk.Label(self,
                 text="Entrée d'un véhicule",
                 font=("Arial", 18),
                 bg=COLOR_BG,
                 fg="white").pack(pady=10)

        tk.Label(self,
                 text="Immatriculation Format: ABC-123",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.immatriculation_entry = tk.Entry(self,
                                              bg=COLOR_ENTRY)
        self.immatriculation_entry.pack()

        tk.Label(self,
                 text="Type de place",
                 bg=COLOR_BG,
                 fg="white").pack(pady=5)
        self.type_var = tk.StringVar(value="visiteur")  # précoché

        types = [("Visiteur", "visiteur"),
                 ("Handicapé", "handicapé"),
                 ("Électrique", "électrique")]
        for text, value in types:
            tk.Radiobutton(self,
                           text=text,
                           variable=self.type_var,
                           value=value,
                           bg=COLOR_BG, fg="white",
                           selectcolor=COLOR_BTN).pack(anchor="n", pady=2)

        ttk.Button(self, text="Valider",
                   command=self.valider).pack(pady=10)
        ttk.Button(self, text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack()

    def valider(self):
        """
        Valide l'entrée du véhicule dans le parking.

        Cette méthode :
            - récupère l'immatriculation et le type de place,
            - vérifie que l'immatriculation n'est pas vide,
            - enregistre l'entrée via `mon_parking.vehicules_entry()`,
            - journalise l'action via `controller.log_info()`,
            - réinitialise les champs pour la prochaine saisie.

        Si l'immatriculation est vide, l'action est interrompue
        et un message d'erreur est envoyé au journal.
        """
        immat = self.immatriculation_entry.get().strip()
        type_place = self.type_var.get()
        if not immat:
            self.controller.log_info("Erreur : immatriculation vide.")
            return
        mon_parking.vehicules_entry(immat, type_place)
        last_v = len(mon_parking.parking) - 1
        if mon_parking.parking[last_v].type_vehicule != type_place:
            choix = messagebox.askyesno(
                "Place pleine",
                f"Attention, il n'y a plus de place {type_place},\n"
                "voulez-vous rajouter le véhicule en place visiteur ?"
            )

            if not choix:
                mon_parking.vehicules_leave(mon_parking.parking[last_v].immatriculation)
                self.controller.log_info(
                    f"Entrée annulée pour {mon_parking.parking[last_v].immatriculation}."
                )
            # à changer    
                return

        self.controller.log_info(
            f"Véhicule {immat} entré en place {mon_parking.parking[last_v].type_vehicule}.")
        self.immatriculation_entry.delete(0, tk.END)
        self.type_var.set("visiteur")
        self.controller.update_vehicle_list()  # Mise à jour de la liste principale
        self.controller.frames[ListeVehicules].update_list()  # Mise à jour de la page ListeVehicules

# ============================================================
# SORTIE VEHICULE
# ============================================================

class SortieVehicule(tk.Frame):
    """
    Page d'enregistrement de l'entrée d'un véhicule dans le parking.

    Cette interface permet de :
        - saisir l'immatriculation du véhicule,
        - choisir le type de place (visiteur, handicapé ou électrique),
        - valider l'entrée du véhicule,
        - revenir au menu principal.

    L'interaction avec le parking est gérée via l'objet `mon_parking`
    et les actions sont journalisées grâce au contrôleur.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self,
                 text="Sortie d'un véhicule",
                 font=("Arial", 18),
                 bg=COLOR_BG,
                 fg="white").pack(pady=10)

        tk.Label(self,
                 text="Immatriculation (ABC-123)",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.immatriculation_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.immatriculation_entry.pack()

        ttk.Button(self,
                   text="Valider",
                   command=self.valider).pack(pady=10)
        ttk.Button(self,
                   text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack()

    def ouvrir_pdf(self, file_path):
        """Ouvre un fichier PDF avec le lecteur par défaut."""

        if os.name == "nt":  # Windows
            os.startfile(file_path)
        elif os.name == "posix":  # Linux / macOS
            os.system(f'xdg-open "{file_path}"')

    def valider(self):
        """
        Valide l'entrée du véhicule dans le parking.

        Cette méthode :
            - récupère l'immatriculation et le type de place sélectionné,
            - vérifie que l'immatriculation n'est pas vide,
            - appelle `mon_parking.vehicules_entry()` pour enregistrer l'entrée,
            - ajoute l'action au journal via `controller.log_info()`,
            - réinitialise les champs du formulaire.
        """
        immat = self.immatriculation_entry.get().strip()
        if not immat:
            self.controller.log_info("Erreur : immatriculation vide.")
            return
        if mon_parking.find_vehicule(immat).type_vehicule == 'abonné':
            self.controller.log_info("Erreur lors de la sortie: On ne peut pas supprimer un abonné")
            messagebox.showinfo("Retirer", "Vous ne pouvez pas retirer un abonné")
            return

        a = mon_parking.calculate_tarif(immat)
        pdf_path = mon_parking.generer_paiement(immat, a)
        self.ouvrir_pdf(pdf_path)
        mon_parking.vehicules_leave(immat)
        self.controller.log_info(f"Véhicule {immat} sorti du parking.")
        self.immatriculation_entry.delete(0, tk.END)
        self.controller.update_vehicle_list()  # Mise à jour de la liste principale
        self.controller.frames[ListeVehicules].update_list()  # Mise à jour de la page ListeVehicules

# ============================================================
# ABONNEMENT
# ============================================================

class Abonnement(tk.Frame):
    """
    Page de gestion des abonnements utilisateurs.

    Cette interface permet de créer un nouvel abonné en renseignant :
        - le prénom,
        - le nom,
        - le numéro de téléphone,
        - l'immatriculation du véhicule.

    Une fois les informations saisies, l'utilisateur peut valider l'abonnement
    ou revenir au menu principal. L'action est ensuite consignée dans le journal.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self,
                 text="Abonnement d'un utilisateur",
                 font=("Arial", 18),
                 bg=COLOR_BG,
                 fg="white").pack(pady=10)
        tk.Label(self,
                 text="Prénom",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.first_name_entry = tk.Entry(self,
                                         bg=COLOR_ENTRY)
        self.first_name_entry.pack()
        tk.Label(self,
                 text="Nom",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.name_entry = tk.Entry(self,
                                   bg=COLOR_ENTRY)
        self.name_entry.pack()
        tk.Label(self, text="Numéro de téléphone (+32123456789)",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.phone_entry = tk.Entry(self,
                                    bg=COLOR_ENTRY)
        self.phone_entry.pack()
        tk.Label(self, text="Immatriculation (ABC-123)",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.immatriculation_entry = tk.Entry(self,
                                              bg=COLOR_ENTRY)
        self.immatriculation_entry.pack()

        ttk.Button(self,
                   text="Valider",
                   command=self.valider).pack(pady=10)
        ttk.Button(self,
                   text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack()

    def valider(self):
        """
        Valide la création d'un nouvel abonné.

        Cette méthode :
            - récupère les informations saisies dans le formulaire,
            - vérifie que tous les champs sont remplis,
            - crée un objet `Subscriber` correspondant,
            - appelle sa méthode `subscribe()` pour l'inscrire dans le parking,
            - journalise l'action,
            - réinitialise le formulaire en cas de succès.
        En cas de champ vide, la validation est interrompue et un message
          d'erreur est envoyé au journal via `controller.log_info()`.
        """
        immat = self.immatriculation_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not immat or not name or not first_name or not phone:
            self.controller.log_info("Erreur : Tous les champs doivent être complétés.")
            return
        subscriber = Subscriber(immat, first_name, name, phone)
        subscriber.subscribe(mon_parking)
        self.controller.log_info(
            f"Utilisateur {name} {first_name} abonné avec immatriculation {immat}.")
        self.immatriculation_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.controller.update_vehicle_list()  # Mise à jour de la liste principale
        self.controller.frames[ListeVehicules].update_list()  # Mise à jour de la page ListeVehicules

# ============================================================
# LISTE VEHICULES
# ============================================================

class ListeVehicules(tk.Frame):
    """
    Page affichant la liste des véhicules garés dans le parking.
    
    Permet de filtrer par type de véhicule via un combobox.
    Utilise un Treeview pour afficher les détails des véhicules.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.sort_order = {}  # Pour gérer l'ordre de tri (asc/desc)

        tk.Label(self,
                 text="Liste des Véhicules Garés",
                 font=("Arial", 18),
                 bg=COLOR_BG,
                 fg=COLOR_LABEL).pack(pady=10)

        # Filtre par type
        tk.Label(self,
                 text="Filtrer par type",
                 bg=COLOR_BG,
                 fg="white").pack()
        self.type_var = tk.StringVar(value="Tous")
        types = ["Tous", "visiteur", "handicapé", "électrique", "abonné"]
        self.type_combo = ttk.Combobox(self,
                                       textvariable=self.type_var,
                                       values=types,
                                       state="readonly")
        self.type_combo.pack(pady=5)
        self.type_combo.bind("<<ComboboxSelected>>", self.update_list)

        # Bouton Refresh
        ttk.Button(self, text="Actualiser", command=self.update_list).pack(pady=5)

        # Treeview pour la liste
        columns = ("Immatriculation", "Type", "Heure d'entrée", "Prénom", "Nom", "Téléphone")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_list(c))
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar pour le Treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack(pady=10)

        # Charger la liste initiale
        self.update_list()

    def update_list(self, event=None):
        """Met à jour la liste des véhicules en fonction du filtre sélectionné."""
        # Vider la liste actuelle
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Récupérer les véhicules filtrés
        selected_type = self.type_var.get()
        if selected_type == "Tous":
            vehicles = mon_parking.parking
        else:
            vehicles = mon_parking.find_vehicule_by_type(selected_type)

        # Ajouter les véhicules au Treeview
        for v in vehicles:
            entry_time_str = v.entry_time.strftime("%d/%m/%Y %H:%M")
            # Vérifier si c'est un Subscriber pour afficher les infos supplémentaires
            if isinstance(v, Subscriber):
                self.tree.insert("", "end", values=(v.immatriculation,
                                                    v.type_vehicule,
                                                    entry_time_str,
                                                    v.first_name,
                                                    v.last_name,
                                                    v.phone_number))
            else:
                self.tree.insert("",
                                 "end",
                                 values=(v.immatriculation,
                                         v.type_vehicule,
                                         entry_time_str,
                                         "",
                                         "",
                                         ""))

    def sort_list(self, col):
        """Trie la liste des véhicules par la colonne spécifiée."""
        selected_type = self.type_var.get()
        if selected_type == "Tous":
            vehicles = mon_parking.parking[:]
        else:
            vehicles = mon_parking.find_vehicule_by_type(selected_type)[:]

        # Inverser l'ordre si déjà trié
        reverse = self.sort_order.get(col, False)
        if col == "Immatriculation":
            vehicles.sort(key=lambda v: v.immatriculation, reverse=reverse)
        elif col == "Type":
            vehicles.sort(key=lambda v: v.type_vehicule, reverse=reverse)
        elif col == "Heure d'entrée":
            vehicles.sort(key=lambda v: v.entry_time, reverse=reverse)
        else:
            return

        self.sort_order[col] = not reverse

        # Vider et recharger la liste triée
        for item in self.tree.get_children():
            self.tree.delete(item)

        for v in vehicles:
            entry_time_str = v.entry_time.strftime("%d/%m/%Y %H:%M")
            if isinstance(v, Subscriber):
                self.tree.insert("", "end", values=(v.immatriculation,
                                                    v.type_vehicule,
                                                    entry_time_str,
                                                    v.first_name,
                                                    v.last_name,
                                                    v.phone_number))
            else:
                self.tree.insert("",
                                 "end",
                                 values=(v.immatriculation,
                                         v.type_vehicule,
                                         entry_time_str,
                                         "",
                                         "",
                                         ""))


# ============================================================
# LANCEMENT APP
# ============================================================

if __name__ == "__main__":
    app = Application()
    app.mainloop()
