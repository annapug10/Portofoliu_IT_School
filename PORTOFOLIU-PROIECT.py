import tkinter as tk
from tkinter import messagebox
import random

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

        self.label_bun_venit = tk.Label(self.frame_bun_venit, text="Bine ai venit la joc!", font=("Helvetica", 16))
        self.label_bun_venit.pack(pady=10)

        self.buton_start = tk.Button(self.frame_bun_venit, text="Vrei să începem?", command=self.incepe_joc)
        self.buton_start.pack(pady=5)

    def incepe_joc(self):
        self.frame_bun_venit.destroy()
        self.intrebari = [
            Intrebare("Ce este capitala Franței?", "Paris"),
            Intrebare("Care este cel mai mare ocean al lumii?", "Pacific"),
            Intrebare("Cine a scris 'Romeo și Julieta'?", "William Shakespeare"),
            Intrebare("Care este cel mai lung râu din lume?", "Nilul"),
            Intrebare("Câte continente există pe Pământ?", "Șapte"),
            Intrebare("Care este elementul chimic cu simbolul 'Fe'?", "Fier"),
            Intrebare("Câte zile are un an bisect?", "366"),
            Intrebare("Cine a pictat Mona Lisa?", "Leonardo da Vinci"),
            # Adaugă mai multe întrebări aici
        ]

        self.punctaj = 0
        self.index_intrebare_curenta = -1

        self.creeaza_interfata()

    def creeaza_interfata(self):
        self.eticheta_intrebare = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.eticheta_intrebare.pack(pady=10)

        self.camp_raspuns = tk.Entry(self.master, font=("Helvetica", 12))
        self.camp_raspuns.pack(pady=5)

        self.eticheta_punctaj = tk.Label(self.master, text="Punctaj: 0", font=("Helvetica", 12))
        self.eticheta_punctaj.pack()

        self.culori = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightpink']

        self.urmatoarea_intrebare()

    def urmatoarea_intrebare(self):
        self.index_intrebare_curenta += 1
        if self.index_intrebare_curenta >= len(self.intrebari):
            messagebox.showinfo("Sfârșitul Jocului", f"Ai răspuns la toate întrebările!\nPunctajul tău final este: {self.punctaj}")
            self.master.destroy()
            return

        random_color = random.choice(self.culori)
        self.master.config(bg=random_color)

        intrebare_curenta = self.intrebari[self.index_intrebare_curenta]
        self.intrebare_curenta = intrebare_curenta.intrebare
        self.raspuns_corect = intrebare_curenta.raspuns

        self.eticheta_intrebare.config(text=self.intrebare_curenta)
        self.camp_raspuns.delete(0, tk.END)

        # Adăugăm verificarea automată a răspunsului corect
        self.master.bind('<Return>', self.verifica_si_urmatoarea)

    def verifica_si_urmatoarea(self, event):
        self.verifica_raspuns()

        # Dacă răspunsul este corect, trecem automat la următoarea întrebare
        if self.camp_raspuns.get().strip().lower() == self.raspuns_corect.lower():
            self.punctaj += 10
            self.eticheta_punctaj.config(text=f"Punctaj: {self.punctaj}")
            self.urmatoarea_intrebare()

    def verifica_raspuns(self):
        raspuns_utilizator = self.camp_raspuns.get().strip()

        if not raspuns_utilizator:
            messagebox.showwarning("Răspuns Necompletat", "Te rugăm să introduci un răspuns!")
            return

        if raspuns_utilizator.lower() == self.raspuns_corect.lower():
            messagebox.showinfo("Răspuns Corect", "Felicitări, răspunsul este corect!")
            self.punctaj += 10
        else:
            messagebox.showerror("Răspuns Incorect", f"Răspunsul corect este: {self.raspuns_corect}")

        self.eticheta_punctaj.config(text=f"Punctaj: {self.punctaj}")

# Funcția principală care inițializează jocul
def main():
    root = tk.Tk()
    app = Joc(root)
    root.mainloop()

# Verificăm dacă scriptul este rulat direct sau importat ca modul
if __name__ == "__main__":
    main()
