import tkinter as tk
from tkinter import messagebox
import threading
import random

# Définition des rotors et du réflecteur
rotors = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
    "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # Rotor IV
    "VZBRGITYUPSDNHLXAWMJQOFECK",  # Rotor V
]
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"  # Réflecteur B (fictif)

class BombeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bombe de Turing - Simulation Avancée")
        self.root.geometry("950x650")

        # Panneau pour les rotors
        self.rotor_frame = tk.LabelFrame(root, text="Position des Rotors", font=("Arial", 12, "bold"), padx=10, pady=5)
        self.rotor_frame.pack(pady=10, fill="both", expand=True)

        self.create_visual_rotor_panel()

        # Panneau d'entrées
        self.input_frame = tk.LabelFrame(root, text="Entrée Informations", font=("Arial", 12, "bold"), padx=10, pady=5)
        self.input_frame.pack(pady=10, fill="both", expand=True)

        # Entrée utilisateur
        self.message_label = tk.Label(self.input_frame, text="Message chiffré:")
        self.message_label.pack()
        self.message_entry = tk.Entry(self.input_frame, width=80)  # Augmenté à 80 caractères
        self.message_entry.pack()

        self.crib_label = tk.Label(self.input_frame, text="Crib (texte connu partiellement):")
        self.crib_label.pack()
        self.crib_entry = tk.Entry(self.input_frame, width=50)
        self.crib_entry.pack()

        # Panneau pour le plugboard
        self.create_plugboard_panel()

        # Bouton Exemple
        self.example_button = tk.Button(self.input_frame, text="Exemple Pédagogique", command=self.load_example)
        self.example_button.pack(pady=5)

        # Boutons de contrôle
        self.start_button = tk.Button(self.input_frame, text="Démarrer", command=self.start_decryption)
        self.start_button.pack(pady=5)
        self.clear_button = tk.Button(self.input_frame, text="Effacer les champs Résultats et Contradictions", command=self.clear_text)
        self.clear_button.pack(pady=5)

        # Cadre pour les résultats
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10)

        self.result_label = tk.Label(self.result_frame, text="Résultat du déchiffrement:")
        self.result_label.grid(row=0, column=0)
        self.result_text = tk.Text(self.result_frame, height=10, width=50)
        self.result_text.grid(row=1, column=0, padx=(0, 20))  # Espace ajouté entre les champs

        self.contradictions_label = tk.Label(self.result_frame, text="Contradictions détectées:")
        self.contradictions_label.grid(row=0, column=1)
        self.contradictions_text = tk.Text(self.result_frame, height=10, width=50)
        self.contradictions_text.grid(row=1, column=1)

    def create_visual_rotor_panel(self):
        # Panneau visuel des rotors
        self.rotor_labels = []
        for i in range(5):  # 5 rotors comme dans la vraie Bombe
            rotor_label = tk.Label(self.rotor_frame, text=f"Pos 0", font=("Courier", 12))
            rotor_label.grid(row=0, column=i, padx=5)
            rotor_label.config(fg="green")  # Changer la couleur du texte en vert
            
            # Label pour le numéro du rotor
            rotor_number_label = tk.Label(self.rotor_frame, text=f"Rotor {i + 1}", font=("Courier", 12, "bold"), fg="black")
            rotor_number_label.grid(row=1, column=i, padx=5)

            # Centrer les éléments dans le LabelFrame
            rotor_label.grid_configure(sticky='nsew')
            rotor_number_label.grid_configure(sticky='nsew')
            self.rotor_labels.append(rotor_label)

        # Configurer le grid pour centrer les colonnes
        for i in range(5):
            self.rotor_frame.grid_columnconfigure(i, weight=1)

    def create_plugboard_panel(self):
        # Panneau pour le plugboard
        self.plugboard_frame = tk.Frame(self.input_frame)
        self.plugboard_frame.pack(pady=10)
        self.plugboard_label = tk.Label(self.plugboard_frame, text="Plugboard (table de connexion)", font=("Courier", 12))
        self.plugboard_label.grid(row=0, column=0, padx=5)
        self.plugboard_mapping = {}

        # Ajouter des widgets de câblage interactifs pour visualiser les connexions
        plugboard_instructions = tk.Label(
            self.plugboard_frame, text="Ex: A-B pour relier A avec B", font=("Courier", 10)
        )
        plugboard_instructions.grid(row=1, column=0, padx=5)
        self.plugboard_entry = tk.Entry(self.plugboard_frame, width=30)
        self.plugboard_entry.grid(row=2, column=0, pady=5)
        tk.Button(self.plugboard_frame, text="Configurer", command=self.update_plugboard).grid(row=3, column=0, pady=5)

    def update_plugboard(self):
        # Configuration du Plugboard
        plug_config = self.plugboard_entry.get().upper().split()
        self.plugboard_mapping.clear()
        for pair in plug_config:
            if "-" in pair:
                a, b = pair.split("-")
                if len(a) == 1 and len(b) == 1:
                    self.plugboard_mapping[a] = b
                    self.plugboard_mapping[b] = a
        messagebox.showinfo("Plugboard Configuré", f"Plugboard: {self.plugboard_mapping}")

    def load_example(self):
        # Charger les valeurs d'exemple de manière aléatoire
        examples = [
            ("A-B", "HYUBEOKSPXYAUODHWFPCFCDJECVK123", "BONJOUR"),
            ("A-B", "VFLHLPWORYVFUOOIAK99", "TURING"),
            ("B-A", "AWBVOHWFGLSWLLLFKKHAIAFFO", "KE")  # Nouvel exemple
        ]
        plugboard, message, crib = random.choice(examples)
        
        self.plugboard_entry.delete(0, tk.END)
        self.plugboard_entry.insert(0, plugboard)
        self.message_entry.delete(0, tk.END)
        self.message_entry.insert(0, message)
        self.crib_entry.delete(0, tk.END)
        self.crib_entry.insert(0, crib)

    def start_decryption(self):
        message = self.message_entry.get().upper().replace(" ", "")
        crib = self.crib_entry.get().upper().replace(" ", "")
        if not message or not crib:
            messagebox.showerror("Erreur", "Veuillez entrer un message et un crib.")
            return

        # Lancer la simulation dans un thread séparé pour ne pas bloquer l'interface
        decryption_thread = threading.Thread(target=self.run_bombe_simulation, args=(message, crib))
        decryption_thread.start()

    def run_bombe_simulation(self, message, crib):
        decrypted_message = ""
        contradictions_found = []

        for i, letter in enumerate(message):
            rotor_pos = i % len(self.rotor_labels)
            self.update_rotor_status(i, rotor_pos)

            # Si le caractère est une lettre, appliquer le codage
            if letter.isalpha():  # Vérifier si c'est une lettre
                # Application du Plugboard
                letter = self.plugboard_mapping.get(letter, letter)

                # Passage dans les rotors
                letter_index = ord(letter) - ord('A')
                rotor_letter = rotors[rotor_pos][letter_index]

                # Passage dans le réflecteur
                letter_index = ord(rotor_letter) - ord('A')
                reflected_letter = reflector[letter_index]

                # Retour à travers les rotors en sens inverse
                rotor_letter_back = chr(rotors[rotor_pos].index(reflected_letter) + ord('A'))
                decrypted_letter = self.plugboard_mapping.get(rotor_letter_back, rotor_letter_back)

                # Vérification des contradictions
                if crib in decrypted_message:
                    contradictions_found.append(f"Contradiction trouvée: {crib} dans {decrypted_message}")

                decrypted_message += decrypted_letter
            else:
                # Conserver les chiffres ou autres caractères
                decrypted_message += letter

        # Affichage des résultats
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, decrypted_message)
        self.result_text.config(state=tk.DISABLED)

        self.contradictions_text.config(state=tk.NORMAL)
        self.contradictions_text.delete(1.0, tk.END)
        for contradiction in contradictions_found:
            self.contradictions_text.insert(tk.END, contradiction + "\n")
        self.contradictions_text.config(state=tk.DISABLED)

    def update_rotor_status(self, i, rotor_pos):
        for j, label in enumerate(self.rotor_labels):
            if j == rotor_pos:
                label.config(text=f"Pos {i % 26}")  # Mise à jour de la position

    def clear_text(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        self.contradictions_text.config(state=tk.NORMAL)
        self.contradictions_text.delete(1.0, tk.END)
        self.contradictions_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BombeApp(root)
    root.mainloop()
