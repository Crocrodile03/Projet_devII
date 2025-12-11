"""
Module regroupant les importations nécessaires à la création de l'interface
graphique de l'application, ainsi qu'à la gestion du parking et des abonnés.

Imports :
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

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from parking import Parking
from subscriber import Subscriber

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
        elif taux >= 0.5:
            return COLOR_PM
        else:
            return COLOR_PV

    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de Parking")
        self.state('zoomed')  # Maximise la fenêtre automatiquement
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.config(bg=COLOR_BG)
        
        # Garder trace de la liste précédente pour éviter les rafraîchissements inutiles
        self.previous_vehicules = []

        # --- SIDEBAR DROITE ---
        sidebar = tk.Frame(self,
                           width=400,
                           bg=COLOR_BG,
                           relief="sunken",
                           bd=2)
        sidebar.pack(side="right", fill="y")

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

        # --- ZONE VÉHICULES À GAUCHE ---
        vehicules_frame = tk.Frame(self,
                                   width=180,
                                   bg=COLOR_BG,
                                   relief="sunken",
                                   bd=2)
        vehicules_frame.pack(side="left", fill="y")
        vehicules_frame.pack_propagate(False)  # Empêche le frame de s'agrandir

        tk.Label(vehicules_frame,
                 text="Véhicules dans\nle parking",
                 font=("Arial", 14, "bold"),
                 bg=COLOR_BG,
                 fg="white").pack(pady=10)
        frame_etat = tk.Frame(vehicules_frame, bg=COLOR_BG)
        frame_etat.pack(fill="x", padx=10)

        # Canvas avec scrollbar pour la liste des véhicules
        canvas_vehicules = tk.Canvas(vehicules_frame, bg=COLOR_BG, highlightthickness=0, width=165)
        scrollbar_vehicules = tk.Scrollbar(vehicules_frame, orient="vertical", command=canvas_vehicules.yview)
        self.vehicules_list_frame = tk.Frame(canvas_vehicules, bg=COLOR_BG)

        self.vehicules_list_frame.bind(
            "<Configure>",
            lambda e: canvas_vehicules.configure(scrollregion=canvas_vehicules.bbox("all"))
        )

        canvas_vehicules.create_window((0, 0), window=self.vehicules_list_frame, anchor="nw", width=165)
        canvas_vehicules.configure(yscrollcommand=scrollbar_vehicules.set)

        # Activer le scroll avec la molette de la souris
        def on_mousewheel(event):
            canvas_vehicules.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_vehicules.bind_all("<MouseWheel>", on_mousewheel)

        canvas_vehicules.pack(side="left", fill="both", expand=True)
        scrollbar_vehicules.pack(side="right", fill="y")

        # --- FRAME PRINCIPAL ---
        main_container = tk.Frame(self,
                                  height=120,
                                  bg=COLOR_BG)
        main_container.pack(side="right",
                            fill="both",
                            expand=True)

        # --- ZONE LOG EN BAS ---
        log_frame = tk.Frame(self,
                             height=120,
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

        # Chargement des pages
        self.frames = {}
        for F in (MenuPrincipal, EntreeVehicule, SortieVehicule, Abonnement):
            frame = F(main_container,
                      self)
            self.frames[F] = frame
            frame.grid(row=0,
                       column=0,
                       sticky="nsew")

        self.show_frame(MenuPrincipal)

        # Démarrer la mise à jour de la barre d'état et de la liste des véhicules
        self.update_sidebar()
        self.update_vehicules_list()

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
        puis met à jour l’étiquette correspondante. Elle se rappelle
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

    def update_vehicules_list(self):
        """Met à jour la liste des véhicules affichée à gauche."""
        # Vérifier si la liste a changé
        current_vehicules = [v.immatriculation for v in mon_parking.parking]
        if current_vehicules == self.previous_vehicules:
            # Aucun changement, relancer juste la mise à jour périodique
            self.after(1000, self.update_vehicules_list)
            return
        
        # La liste a changé, mettre à jour l'affichage
        self.previous_vehicules = current_vehicules.copy()
        
        # Nettoyer la liste actuelle
        for widget in self.vehicules_list_frame.winfo_children():
            widget.destroy()

        # Afficher chaque véhicule
        for vehicule in mon_parking.parking:
            v_frame = tk.Frame(self.vehicules_list_frame, bg=COLOR_ENTRY, relief="raised", bd=1)
            v_frame.pack(fill="x", padx=5, pady=3)

            # Déterminer le type d'affichage selon si c'est un abonné ou non
            if hasattr(vehicule, 'first_name'):
                # C'est un Subscriber
                info_text = f"{vehicule.immatriculation}\n{vehicule.first_name} {vehicule.last_name}\nType: {vehicule.type_vehicule}"
            else:
                # C'est un Vehicule normal
                info_text = f"{vehicule.immatriculation}\nType: {vehicule.type_vehicule}"

            label = tk.Label(v_frame,
                           text=info_text,
                           font=("Arial", 10),
                           bg=COLOR_ENTRY,
                           fg="white",
                           cursor="hand2",
                           justify="left")
            label.pack(padx=10, pady=5, fill="x")

            # Fonctions pour le survol
            def on_enter(e, frame=v_frame, lbl=label):
                frame.config(bg=COLOR_BG)
                lbl.config(bg=COLOR_BG)

            def on_leave(e, frame=v_frame, lbl=label):
                frame.config(bg=COLOR_ENTRY)
                lbl.config(bg=COLOR_ENTRY)

            # Bind du survol
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            v_frame.bind("<Enter>", on_enter)
            v_frame.bind("<Leave>", on_leave)
            # Bind du clic sur le véhicule
            label.bind("<Button-1>", lambda e, v=vehicule: self.demander_sortie_vehicule(v))
            v_frame.bind("<Button-1>", lambda e, v=vehicule: self.demander_sortie_vehicule(v))

        # Relancer la mise à jour périodique
        self.after(1000, self.update_vehicules_list)

    def demander_sortie_vehicule(self, vehicule):
        """Demande confirmation pour faire sortir un véhicule du parking."""
        reponse = messagebox.askyesno(
            "Sortie de véhicule",
            f"Voulez-vous faire sortir le véhicule {vehicule.immatriculation} du parking ?"
        )
        if reponse:
            try:
                mon_parking.vehicules_leave(vehicule.immatriculation)
                self.log_info(f"Véhicule {vehicule.immatriculation} sorti du parking.")
                self.update_vehicules_list()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
                self.log_info(f"Erreur lors de la sortie de {vehicule.immatriculation}: {str(e)}")

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
            messagebox.showwarning("Place pleine",
            f"Attention, il n'y a plus de place {type_place}, vehicule rajouté en place visiteur.")
        self.controller.log_info(
            f"Véhicule {immat} entré en place {mon_parking.parking[last_v].type_vehicule}.")
        self.immatriculation_entry.delete(0, tk.END)
        self.type_var.set("visiteur")


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
        a = mon_parking.calculate_tarif(immat)
        mon_parking.generer_paiement(immat,mon_parking.parking, a)
        mon_parking.vehicules_leave(immat)
        self.controller.log_info(f"Véhicule {immat} sorti du parking.")
        self.immatriculation_entry.delete(0, tk.END)


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


# ============================================================
# LANCEMENT APP
# ============================================================

if __name__ == "__main__":
    app = Application()
    app.mainloop()
