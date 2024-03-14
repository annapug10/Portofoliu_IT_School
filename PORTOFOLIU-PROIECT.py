import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

# Clasa pentru a reprezenta întrebările și răspunsurile asociate
class Intrebare:
    def __init__(self, intrebare, raspuns):
        self.intrebare = intrebare
        self.raspuns = raspuns

# Clasa pentru gestionarea jocului
class Joc:
    def __init__(self, master):
        self.master = master
        self.master.title("Joc de întrebări generale")
        self.master.geometry("400x300")

        self.bun_venit()

    def bun_venit(self):
        self.frame_bun_venit = tk.Frame(self.master)
        self.frame_bun_venit.pack(pady=50)

        self.label_nume = tk.Label(self.frame_bun_venit, text="Introdu numele tău:", font=("Helvetica", 12))
        self.label_nume.pack()

        self.entry_nume = tk.Entry(self.frame_bun_venit, font=("Helvetica", 12))
        self.entry_nume.pack(pady=5)

        self.buton_start = tk.Button(self.frame_bun_venit, text="Vrei să începem?", command=self.incepe_joc)
        self.buton_start.pack(pady=5)

    def incepe_joc(self):
        nume_jucator = self.entry_nume.get().strip()
        if not nume_jucator:
            messagebox.showwarning("Nume Necompletat", "Te rugăm să introduci numele tău!")
            return

        self.frame_bun_venit.destroy()
        self.intrebari = [
            Intrebare("Ce este capitala Franței?", "Paris"),
            Intrebare("Care este cel mai mare ocean al lumii?", "Pacific"),
            Intrebare("Cine a scris 'Romeo și Julieta'?", ["William Shakespeare", "William"]),
            Intrebare("Care este cel mai lung râu din lume?", "Nilul"),
            Intrebare("Câte continente există pe Pământ?", ["Șapte", "sapte", "Sapte", "7"]),
            Intrebare("Care este elementul chimic cu simbolul 'Fe'?", "Fier"),
            Intrebare("Câte zile are un an bisect?", "366"),
            Intrebare("Cine a pictat Mona Lisa?", "Leonardo da Vinci"),
            # Adaugă mai multe întrebări aici
        ]

        self.punctaj = 0
        self.index_intrebare_curenta = -1
        self.nume_jucator = nume_jucator

        self.creeaza_interfata()

        # Conectăm metoda `verifica_si_urmatoarea` la evenimentul Enter
        self.camp_raspuns.bind("<Return>", self.verifica_si_urmatoarea)

    def creeaza_interfata(self):
        self.eticheta_intrebare = tk.Label(self.master, text=f"{self.nume_jucator}, răspunde la următoarele întrebări:", font=("Helvetica", 12))
        self.eticheta_intrebare.pack(pady=10)

        self.camp_raspuns = tk.Entry(self.master, font=("Helvetica", 12))
        self.camp_raspuns.pack(pady=5)

        self.eticheta_punctaj = tk.Label(self.master, text="Punctaj: 0", font=("Helvetica", 12))
        self.eticheta_punctaj.pack()

        self.eticheta_timp_ramas = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.eticheta_timp_ramas.pack()

        self.culori = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightpink']

        self.urmatoarea_intrebare()

    def rulare_cronometru(self):
        timp_ramas = 10  # Ajustează timpul limită aici
        while timp_ramas > 0:
            self.eticheta_timp_ramas.config(text=f"Timp rămas: {timp_ramas} secunde")
            time.sleep(1)
            timp_ramas -= 1
        messagebox.showinfo("Timpul a expirat!", "Timpul a expirat! Trecem automat la următoarea întrebare.")
        self.verifica_raspuns()

    def urmatoarea_intrebare(self):
        self.index_intrebare_curenta += 1
        if self.index_intrebare_curenta >= len(self.intrebari):
            messagebox.showinfo("Sfârșitul Jocului", f"{self.nume_jucator}, ai răspuns la toate întrebările!\nPunctajul tău final este: {self.punctaj}")
            self.master.destroy()
            return

        random_color = random.choice(self.culori)
        self.master.config(bg=random_color)

        intrebare_curenta = self.intrebari[self.index_intrebare_curenta]
        self.intrebare_curenta = intrebare_curenta.intrebare
        self.raspuns_corect = intrebare_curenta.raspuns

        self.eticheta_intrebare.config(text=self.intrebare_curenta)
        self.camp_raspuns.delete(0, tk.END)

        # Pornim cronometrul pentru întrebarea curentă
        self.cronometru = threading.Thread(target=self.rulare_cronometru)
        self.cronometru.start()

    def verifica_si_urmatoarea(self, event=None):
        self.verifica_raspuns()

        # Oprim cronometrul după verificarea răspunsului
        if self.cronometru.is_alive():
            self.cronometru.join()

        self.eticheta_timp_ramas.config(text="")

        # Trecem automat la următoarea întrebare
        self.urmatoarea_intrebare()

    def verifica_raspuns(self):
        raspuns_utilizator = self.camp_raspuns.get().strip()

        if not raspuns_utilizator:
            messagebox.showwarning("Răspuns Necompletat", "Te rugăm să introduci un răspuns!")
            return

        # Verificăm răspunsul și acordăm punctajul corespunzător
        if isinstance(self.raspuns_corect, list):
            if raspuns_utilizator.lower() in map(str.lower, self.raspuns_corect):
                self.punctaj += 10
                messagebox.showinfo("Răspuns Corect!", "Felicitări, răspunsul este corect!")
            else:
                messagebox.showerror("Răspuns Incorect!", f"Răspunsul corect este: {', '.join(self.raspuns_corect)}")
        elif raspuns_utilizator.lower() == self.raspuns_corect.lower():
            self.punctaj += 10
            messagebox.showinfo("Răspuns Corect!", "Felicitări, răspunsul este corect!")
        else:
            messagebox.showerror("Răspuns Incorect!", f"Răspunsul corect este: {self.raspuns_corect}")

        # Actualizăm eticheta de punctaj
        self.eticheta_punctaj.config(text=f"Punctaj: {self.punctaj}")

        # Asigurăm că punctajul nu poate fi mai mic decât 0
        if self.punctaj < 0:
            self.punctaj = 0

        # Trecem automat la următoarea întrebare
        self.urmatoarea_intrebare()

# Funcția principală care inițializează jocul
def main():
    root = tk.Tk()
    app = Joc(root)
    root.mainloop()

# Verificăm dacă scriptul este rulat direct sau importat ca modul
if __name__ == "__main__":
    main()
