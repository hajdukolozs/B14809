from abc import ABC, abstractmethod
from datetime import date, datetime


class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def get_info(self):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar = 15000, szobaszam = szobaszam)
        self.tipus = "Egyágyas"

    
    def get_info(self):
        return f"Szoba szám: {self.szobaszam}, Típus: {self.tipus}, Ár: {self.ar} Ft"


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar = 25000, szobaszam = szobaszam)
        self.tipus = "Kétágyas"

    def get_info(self):
        return f"Szoba szám: {self.szobaszam}, Típus: {self.tipus}, Ár: {self.ar} Ft"
    

class Szalloda:
    def __init__(self, nev, cim, szobak):
        self.nev = nev
        self.cim = cim
        self.szobak = szobak
        self.foglalasok = []

    def get_szalloda_info(self):
        info = f"Szálloda neve: {self.nev}\nCíme: {self.cim}\nSzobák:\n"
        for szoba in self.szobak:
            info += szoba.get_info() + "\n"
        return info
    
    def foglalas_hozzaadasa(self, foglalas):
        self.foglalasok.append(foglalas)

    def get_foglalasok(self):
        foglalasok_info = [foglalas.get_info() for foglalas in self.foglalasok]
        info = "Foglalások:\n" + "\n".join(foglalasok_info)
        return info
    
    def datum_ervenyes(self, datum):
        return datum > date.today()
    
    def szoba_foglalas(self, nev, szoba_szam, datum):
        if not self.datum_ervenyes(datum):
            return f"A foglalás dátuma érvénytelen. Csak jövőbeni dátumot lehet megadni."
        
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szoba_szam and foglalas.datum == datum:
                return f"A {szoba_szam} számú szoba már foglalt a {datum} dátumra."
        
        for szoba in self.szobak:
            if szoba.szobaszam == szoba_szam:
                uj_foglalas = Foglalas(nev, szoba, datum)
                self.foglalas_hozzaadasa(uj_foglalas)
                return f"A {szoba_szam} számú szoba foglalása sikeres. Ár: {szoba.ar} Ft."

        return f"A {szoba_szam} számú szoba nem található."
    
    def foglalas_lemondasa(self, nev, szoba_szam, datum):
        for foglalas in self.foglalasok:
            if foglalas.nev == nev and foglalas.szoba.szobaszam == szoba_szam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return f"A {szoba_szam} számú szoba foglalása {datum} dátumra le lett mondva."
        return f"Nincs ilyen foglalás: Név: {nev}, Szoba szám: {szoba_szam}, Dátum: {datum}"


class Foglalas:
    def __init__(self, nev, szoba, datum):
        self.nev = nev
        self.szoba = szoba
        self.datum = datum
    
    def get_info(self):
        return f"Név: {self.nev}, Szoba szám: {self.szoba.szobaszam}, Dátum: {self.datum}"


egyAgyasSzobak = [EgyagyasSzoba(1), EgyagyasSzoba(2), EgyagyasSzoba(3), EgyagyasSzoba(4), EgyagyasSzoba(5)]
ketAgyasSzobak = [KetagyasSzoba(6), KetagyasSzoba(7), KetagyasSzoba(8), KetagyasSzoba(9), KetagyasSzoba(10)]

szobak = egyAgyasSzobak + ketAgyasSzobak

szalloda = Szalloda("Hotel Budapest", "1234 Példa utca 5.", szobak)

foglalasok = [("Kiss Péter", 1, date(2024, 7, 20)),
              ("Kovács István", 2, date(2024, 7, 20)),
              ("Tóth Éva", 5, date(2024, 7, 21)),
              ("Nagy Anna", 3, date(2024, 7, 21)),
              ("Kovács Gábor", 6, date(2024, 7, 20))]

for foglalas in foglalasok:
    szalloda.szoba_foglalas(foglalas[0], foglalas[1], foglalas[2])

def menu():
    print("-------------------------------------------------------------------------")
    print("1. Szálloda információ")
    print("2. Foglalások listázása")
    print("3. Szoba foglalása")
    print("4. Foglalás lemondása")
    print("5. Kilépés")
    print("-------------------------------------------------------------------------")

while True:
    menu()
    valasztas = input("Válassz egy lehetőséget: ")

    if valasztas == "1":
        print()
        print(szalloda.get_szalloda_info())
    elif valasztas == "2":
        print()
        print(szalloda.get_foglalasok())
    elif valasztas == "3":
        nev = input("Név: ")
        szoba_szam = int(input("Szoba szám: "))
        datum_input = input("Dátum (YYYY-MM-DD): ")
        datum = datetime.strptime(datum_input, "%Y-%m-%d").date()
        print()
        print(szalloda.szoba_foglalas(nev, szoba_szam, datum))
    elif valasztas == "4":
        nev = input("Név: ")
        szoba_szam = int(input("Szoba szám: "))
        datum_input = input("Dátum (YYYY-MM-DD): ")
        datum = datetime.strptime(datum_input, "%Y-%m-%d").date()
        print()
        print(szalloda.foglalas_lemondasa(nev, szoba_szam, datum))
    elif valasztas == "5":
        break
    else:
        print()
        print("Érvénytelen választás, próbáld újra.")
