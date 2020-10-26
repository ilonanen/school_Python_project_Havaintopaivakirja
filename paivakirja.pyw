import tkinter as tk
import tkinter.scrolledtext
from datetime import date, datetime
from tiedosto import Taulukko

class Kayttoliittyma(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Havaintopäiväkirja')
        self.geometry('600x480')
        
        tanaan = date.today()
        self.tiedostonimi = tanaan.strftime('%Y' + '.csv')
                
        self.taulukko = Taulukko(self.tiedostonimi)
        havainnot = self.taulukko.havainnot()
        
        tk.Label(self, text = 'Syötä uusi havainto').grid(row = 1, column = 1, columnspan = 2, sticky = 'NSWE')
        self.protocol('WM_DELETE_WINDOW', self.sulje)
        
        pvmlabel = tk.Label(self, text = 'Päivämäärä: ')
        pvmlabel.grid(row = 2, column = 1, sticky = 'NSWE')
        
        self.tamapvm = tanaan.strftime('%d.%m.%Y')

        self.pvmkentta = tk.Entry(self, width = 20)
        self.pvmkentta.insert(0, self.tamapvm)
        self.pvmkentta.grid(row = 2, column = 2, sticky = 'NSWE')
        
        paikkalabel = tk.Label(self, text = 'Paikka: ')
        paikkalabel.grid(row = 3, column = 1, sticky = 'NSWE')
        self.paikkakentta = tk.Entry(self, width = 20)
        self.paikkakentta.grid(row = 3, column = 2, sticky = 'NSWE')
        
        lajilabel = tk.Label(self, text = 'Laji: ')
        lajilabel.grid(row = 4, column = 1, sticky = 'NSWE')
        self.lajikentta = tk.Entry(self, width = 20)
        self.lajikentta.grid(row = 4, column = 2, sticky = 'NSWE')
        
        self.tallennabutton = tk.Button(text = 'Tallenna', command = self.tallenna)
        self.tyhjennabutton = tk.Button(text = 'Tyhjennä', command = self.tyhjenna)
        self.tallennabutton.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = 'NSE')
        self.tyhjennabutton.grid(row = 6, column = 2, padx = 5, pady = 5, sticky = 'NSW')
    
        self.paivakirja = tk.scrolledtext.ScrolledText(self)
        self.paivakirja.grid(row = 8, column = 1, columnspan = 4, padx = 10, sticky = 'NSWE')
        self.paivakirja.insert('insert', havainnot)
        
        self.lajimaara = tk.Label(self, text = f'Havaintoja kirjattu tänä vuonna: {self.taulukko.lajimaara()}')
        self.lajimaara.grid(row = 7, column = 1, columnspan = 2, sticky = 'NSWE')
        
        
    def tallenna(self):
        '''lisää tiedot pandas-taulukkoon, jos kaikki kentät on täytetty ja lajia ei vielä löydy taulukosta'''
        pvmteksti = self.pvmkentta.get()
        paikka = self.paikkakentta.get()
        laji = self.lajikentta.get().lower()
        if len(pvmteksti) == 0 or len(paikka) == 0 or len(laji) == 0:
            taytakaikki = tk.Toplevel()
            varoitus = tk.Label(taytakaikki, text = 'Täytä kaikki kentät.')
            varoitus.grid(row = 0)
            nappi = tk.Button(taytakaikki, text = 'OK', command = taytakaikki.destroy)
            nappi.grid(row = 1)
            pass
        
        else:
            pvm = datetime.strptime(pvmteksti, '%d.%m.%Y').date()
            
            aiempipvm = self.taulukko.tarkista(laji)
            
            if aiempipvm:
                samalaji = tk.Toplevel()
                lajivaroitus = tk.Label(samalaji, text = f'{laji} on jo tallennettu {aiempipvm}.')
                lajivaroitus.grid(row = 0)
                OK = tk.Button(samalaji, text = 'OK', command = samalaji.destroy)
                self.lajikentta.delete(0, 'end')
                OK.grid(row = 1)
                
            else:
                self.taulukko.lisaa({'Pvm' : pvm, 'Paikka': paikka, 'Laji': laji})
                self.paivakirja.delete('1.0', 'end')
                self.paivakirja.insert('1.0', self.taulukko.havainnot())
                self.lajikentta.delete(0, 'end')
                self.lajimaara.config(text = f'Havaintoja kirjattu tänä vuonna: {self.taulukko.lajimaara()}')
    
    def tyhjenna(self):
        '''Palauttaa päivämääräkentän arvon syöttöpäiväksi, tyhjentää muut kentät'''
        self.pvmkentta.delete(0, 'end')
        self.pvmkentta.insert(0, self.tamapvm)
        self.paikkakentta.delete(0, 'end')
        self.lajikentta.delete(0, 'end')
        
    def sulje(self):
        '''Tallentaa tiedot tiedostoon ja sulkee ikkunan'''
        self.taulukko.tallennatiedot()
        self.destroy()
        
if __name__ == '__main__':
    Kayttoliittyma().mainloop()