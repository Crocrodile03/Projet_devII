import tkinter as tk
from tkinter import ttk, messagebox

from classParking import Parking
from classEvent import Event
from classSubscriber import Subscriber
import datetime

event = Event()
mon_parking = Parking()

# Palette de couleur
COLOR_BG = "#344e41"      # Vert foncé
COLOR_BTN = "#588157"     # Vert moyen pour boutons
COLOR_BTN_HOVER = "#5a9758" # Vert clair sur hover
COLOR_LABEL = "#bbd58e"   # Vert clair pour labels/log
COLOR_ENTRY = "#3a5a40"  # Vert très clair (fond entrée)


# ============================================================
# APPLICATION TKINTER
# ============================================================

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de Parking")
        self.geometry("1920x1080")  # espace pour sidebar et log

        self.config(bg=COLOR_BG)

        # --- État du parking ---
        sidebar = tk.Frame(self, width=400, bg=COLOR_BG, relief="sunken", bd=2)
        sidebar.pack(side="right", fill="both")

        tk.Label(sidebar, text="État du parking", font=("Arial", 14, "bold"), bg=COLOR_BG, fg="white").pack(pady=10)
        self.sidebar_label = tk.Label(sidebar, text="", font=("Arial", 12), bg=COLOR_LABEL, justify="left")
        self.sidebar_label.pack(pady=10, padx=5, fill="both")

        # --- FRAME PRINCIPAL ---
        main_container = tk.Frame(self, bg=COLOR_BG)
        main_container.pack(side="right", fill="both", expand=True)

        # --- ZONE LOG EN BAS ---
        log_frame = tk.Frame(self, height=120, bg=COLOR_BG)
        log_frame.pack(side="bottom", fill="x", expand=False)

        tk.Label(log_frame, text="Journal des actions", font=("Arial", 12, "bold"), bg=COLOR_BG, fg="white").pack(anchor="w")

        self.log_text = tk.Text(log_frame, height=6, state="disabled", bg=COLOR_LABEL)
        self.log_text.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Chargement des pages
        self.frames = {}
        for F in (MenuPrincipal, EntreeVehicule, SortieVehicule, Abonnement):
            frame = F(main_container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MenuPrincipal)

        # Démarrer la mise à jour de la barre d'état
        self.update_sidebar()

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def update_sidebar(self):
        v, h, e, a = mon_parking.current_capacity
        texte = (
            f"Visiteurs : {v}\n"
            f"Handicapés : {h}\n"
            f"Électriques : {e}\n"
            f"Abonnés : {a}"
        )
        self.sidebar_label.config(text=texte)
        self.after(500, self.update_sidebar)

    def log_info(self, msg):
        self.log_text.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")


# ============================================================
# MENU PRINCIPAL
# ============================================================

class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="Gestionnaire de Parking", font=("Arial", 20), bg=COLOR_BG, fg="white").pack(pady=20)

        for text, page in [("Entrée d'un véhicule", EntreeVehicule),
                           ("Sortie d'un véhicule", SortieVehicule),
                           ("Gérer les abonnements", Abonnement)]:
            btn = tk.Button(self, text=text, font=("Arial", 12), bg=COLOR_BTN, fg="white",
                            activebackground=COLOR_BTN_HOVER, activeforeground="white",
                            command=lambda p=page: controller.show_frame(p))
            btn.pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(self, text="Quitter", command=controller.quit).pack(pady=20)


# ============================================================
# ENTRÉE VEHICULE
# ============================================================

class EntreeVehicule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        tk.Label(self, text="Entrée d'un véhicule", font=("Arial", 18), bg=COLOR_BG, fg="white").pack(pady=10)

        tk.Label(self, text="Immatriculation Format: ABC-123", bg=COLOR_BG, fg="white").pack()
        self.immatriculation_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.immatriculation_entry.pack()

        tk.Label(self, text="Type de place", bg=COLOR_BG, fg="white").pack(pady=5)
        self.type_var = tk.StringVar(value="visiteur")  # précoché

        types = [("Visiteur", "visiteur"), ("Handicapé", "handicapé"), ("Électrique", "électrique")]
        for text, value in types:
            tk.Radiobutton(self, text=text, variable=self.type_var, value=value,
                           bg=COLOR_BG, fg="white", selectcolor=COLOR_BTN).pack(anchor="n",width=15, pady=2)

        ttk.Button(self, text="Valider", command=self.valider).pack(pady=10)
        ttk.Button(self, text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack()

    def valider(self):
        immat = self.immatriculation_entry.get().strip()
        type_place = self.type_var.get()
        if not immat:
            self.controller.log_info("Erreur : immatriculation vide.")
            return
        mon_parking.vehicules_entry(immat, type_place)
        self.controller.log_info(f"Véhicule {immat} entré en place {type_place}.")
        self.immatriculation_entry.delete(0, tk.END)
        self.type_var.set("visiteur")


# ============================================================
# SORTIE VEHICULE
# ============================================================

class SortieVehicule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="Sortie d'un véhicule", font=("Arial", 18), bg=COLOR_BG, fg="white").pack(pady=10)

        tk.Label(self, text="Immatriculation (ABC-123)", bg=COLOR_BG, fg="white").pack()
        self.immatriculation_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.immatriculation_entry.pack()

        ttk.Button(self, text="Valider", command=self.valider).pack(pady=10)
        ttk.Button(self, text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack()

    def valider(self):
        immat = self.immatriculation_entry.get().strip()
        if not immat:
            self.controller.log_info("Erreur : immatriculation vide.")
            return
        mon_parking.calculate_tarif(immat)
        mon_parking.vehicules_leave(immat)
        self.controller.log_info(f"Véhicule {immat} sorti du parking.")
        self.immatriculation_entry.delete(0, tk.END)


# ============================================================
# ABONNEMENT
# ============================================================

class Abonnement(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="Abonnement d'un utilisateur", font=("Arial", 18), bg=COLOR_BG, fg="white").pack(pady=10)
        tk.Label(self, text="Prénom", bg=COLOR_BG, fg="white").pack()
        self.first_name_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.first_name_entry.pack()
        tk.Label(self, text="Nom", bg=COLOR_BG, fg="white").pack()
        self.name_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.name_entry.pack()
        tk.Label(self, text="Numéro de téléphone (+32123456789)", bg=COLOR_BG, fg="white").pack()
        self.phone_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.phone_entry.pack()
        tk.Label(self, text="Immatriculation (ABC-123)", bg=COLOR_BG, fg="white").pack()
        self.immatriculation_entry = tk.Entry(self, bg=COLOR_ENTRY)
        self.immatriculation_entry.pack()

        ttk.Button(self, text="Valider", command=self.valider).pack(pady=10)
        ttk.Button(self, text="Retour menu",
                   command=lambda: controller.show_frame(MenuPrincipal)).pack()

    def valider(self):
        immat = self.immatriculation_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not immat or not name or not first_name or not phone:
            self.controller.log_info("Erreur : Tous les champs doivent être complétés.")
            return
        subscriber = Subscriber(immat, first_name, name, phone)
        subscriber.subscribe(mon_parking)
        self.controller.log_info(f"Utilisateur {name} {first_name} abonné avec immatriculation {immat}." )
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
