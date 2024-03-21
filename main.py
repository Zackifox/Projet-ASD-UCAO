import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

class Tache:
    def __init__(self, description, priorite, date_limite, categorie):
        self.description = description
        self.priorite = priorite
        self.date_limite = date_limite
        self.categorie = categorie

class Application:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Gestion des tâches")
        self.fenetre.configure(bg="#FFFF55")

        self.label_liste_taches = tk.Label(self.fenetre, text="Liste des tâches", font=("Arial", 20, "bold"), bg="#ffff55")
        self.label_liste_taches.pack(pady=50)

        self.arborescence_frame = tk.Frame(self.fenetre)
        self.arborescence_frame.pack(padx=10, pady=10)

        self.arborescence_tree = ttk.Treeview(self.arborescence_frame, columns=("Description", "Priorité", "Date limite"))
        self.arborescence_tree.heading("#0", text="Catégorie")
        self.arborescence_tree.heading("Description", text="Description")
        self.arborescence_tree.heading("Priorité", text="Priorité")
        self.arborescence_tree.heading("Date limite", text="Date limite")
        self.arborescence_tree.pack()

        self.description_label = tk.Label(self.fenetre, text="Description", font=("Arial", 10, "bold"), bg="#ffff55")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.fenetre)
        self.description_entry.pack(pady=5)

        self.priorite_label = tk.Label(self.fenetre, text="Priorité", font=("Arial", 10, "bold"), bg="#ffff55")
        self.priorite_label.pack()

        self.priorite_combobox = ttk.Combobox(self.fenetre, values=["Faible", "Moyenne", "Élevée"])
        self.priorite_combobox.pack(pady=5)

        self.date_label = tk.Label(self.fenetre, text="Date limite", font=("Arial", 10, "bold"), bg="#ffff55")
        self.date_label.pack()

        self.date_entry = DateEntry(self.fenetre, date_pattern="yyyy-mm-dd")
        self.date_entry.pack(pady=5)

        self.categorie_label = tk.Label(self.fenetre, text="Catégorie", font=("Arial", 10, "bold"), bg="#ffff55")
        self.categorie_label.pack()

        self.categorie_combobox = ttk.Combobox(self.fenetre, values=["Urgent", "Important", "Personnel"])
        self.categorie_combobox.pack(pady=5)

        self.frame_buttons = tk.Frame(self.fenetre, bg="#ffff55")
        self.frame_buttons.pack(pady=10)

        self.ajouter_bouton = tk.Button(self.frame_buttons, text="Ajouter", command=self.ajouter_tache,
                                        font=("arial", 12), bg="#4286f4", fg="white", relief="flat", padx=10)
        self.ajouter_bouton.pack(side=tk.LEFT, padx=5)

        self.modifier_bouton = tk.Button(self.frame_buttons, text="Modifier", command=self.modifier_tache,
                                         font=("arial", 12), bg="#01f308", fg="white", relief="flat", padx=10)
        self.modifier_bouton.pack(side=tk.LEFT, padx=5)

        self.supprimer_bouton = tk.Button(self.frame_buttons, text="Supprimer", command=self.supprimer_tache,
                                          font=("arial", 12), bg="#f44336", fg="white", relief="flat", padx=10)
        self.supprimer_bouton.pack(side=tk.LEFT, padx=5)

        self.liste_taches = []

        self.afficher_arborescence_taches()

    def ajouter_tache(self):
        description = self.description_entry.get()
        priorite = self.priorite_combobox.get()
        date_limite = self.date_entry.get()
        categorie = self.categorie_combobox.get()

        if description and priorite and date_limite and categorie:
            # Vérifier si la tâche existe déjà dans la liste
            if not self.tache_existe(description, priorite, date_limite, categorie):
                tache = Tache(description, priorite, date_limite, categorie)
                self.liste_taches.append(tache)
                self.afficher_arborescence_taches()
                self.description_entry.delete(0, 'end')
                self.priorite_combobox.set('')
                self.date_entry.set_date('')
                self.categorie_combobox.set('')
            else:
                messagebox.showerror("Erreur", "Cette tâche existe déjà.")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    def tache_existe(self, description, priorite, date_limite, categorie):
        for tache in self.liste_taches:
            if tache.description == description and tache.priorite == priorite \
                    and tache.date_limite == date_limite and tache.categorie == categorie:
                return True
        return False

    def modifier_tache(self):
        selected_item = self.arborescence_tree.selection()
        if selected_item:
            values = self.arborescence_tree.item(selected_item)["values"]
            if values:
                index = self.arborescence_tree.index(selected_item)
                description = self.description_entry.get()
                priorite = self.priorite_combobox.get()
                date_limite = self.date_entry.get()
                categorie = self.categorie_combobox.get()


                if description and priorite and date_limite and categorie:
                    ancienne_tache = self.liste_taches[index]
                    nouvelle_tache = Tache(description, priorite, date_limite, categorie)

                    self.liste_taches[index] = nouvelle_tache

                    self.afficher_arborescence_taches()

                else:
                    messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            else:
                messagebox.showerror("Erreur", "Veuillez sélectionner une tâche.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une tâche.")

    def supprimer_tache(self):
        selected_item = self.arborescence_tree.selection()
        if selected_item:
            values = self.arborescence_tree.item(selected_item)["values"]
            if values:
                index = self.arborescence_tree.index(selected_item)
                self.liste_taches.pop(index)
                self.afficher_arborescence_taches()
            else:
                messagebox.showerror("Erreur", "Veuillez sélectionner une tâche.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une tâche.")

    def afficher_arborescence_taches(self):
        self.arborescence_tree.delete(*self.arborescence_tree.get_children())
        self.liste_taches.sort(key=lambda x: (x.categorie, x.date_limite))
        current_categorie = None
        for tache in self.liste_taches:
            if tache.categorie != current_categorie:
                current_categorie = tache.categorie
                categorie_node = self.arborescence_tree.insert("", "end", text=current_categorie, open=True)
            self.arborescence_tree.insert(categorie_node, "end", values=(
                tache.description, tache.priorite, tache.date_limite, tache.categorie))


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = Application(fenetre)
    fenetre.mainloop()
