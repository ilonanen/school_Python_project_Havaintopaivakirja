import pandas as pd

class Tiedosto:        
    def hae(self, tiedostonimi):
        '''avaa kuluvan vuoden csv-tiedoston ja vie tiedot pandas-taulukkoon'''
        try:
            tied = open(tiedostonimi, 'r')
            havainnot = pd.read_csv(tiedostonimi)
            tied.close()
        except:
            havainnot = pd.DataFrame(columns = ['Pvm', 'Paikka', 'Laji'])
        return havainnot
        
    def tallenna(self, havainnot, tiedostonimi):
        '''tallentaa pandas-taulukon csv-tiedostoon ilman rivinumeroja'''
        havainnot.to_csv(tiedostonimi, index = False, header = True)
        
        
class Taulukko:
    def __init__(self, tiedostonimi):
        self.tiedostonimi = tiedostonimi
        self.__havainnot = Tiedosto().hae(self.tiedostonimi)
            
    def havainnot(self):
        '''palauttaa havaintotaulukon ilman rivinumeroja tai tyhjän, jos taulukossa ei ole sisältöä'''
        if self.__havainnot.empty:
            return ''
        else:
            return self.__havainnot.to_string(index = False, header = True)

    def lajimaara(self):
        '''palauttaa tallennettujen lajien määrän'''
        return self.__havainnot['Laji'].count()

    def tarkista(self, laji):
        '''tarkistaa, onko laji jo taulukossa, ja palauttaa aiemman havaintopäivämäärän'''
        if len(self.__havainnot[self.__havainnot['Laji'] == laji]) > 0:
            havaitut = self.__havainnot[self.__havainnot['Laji'] == laji]
            aiempipvm = havaitut.iat[0, 0]
            return aiempipvm
        else:
            return None
            
    def lisaa(self, tiedot):
        '''lisää tallennetut tiedot uutena rivinä taulukkoon ja järjestää sen päivämäärien mukaan'''
        uusirivi = pd.DataFrame(tiedot, index = [0])
        havainnot = pd.concat([uusirivi, self.__havainnot]).reset_index(drop = True)
        self.__havainnot = havainnot
        self.__havainnot['Pvm'] = pd.to_datetime(self.__havainnot['Pvm'])
        self.__havainnot.sort_values(by = ['Pvm'], inplace = True, ascending = False)
        
    def tallennatiedot(self):
        '''järjestää taulukon ja lähettää Tiedosto-luokalle tallennettavaksi tiedostoon'''
        self.__havainnot.sort_values(by = ['Pvm'], inplace = True, ascending = False)
        Tiedosto().tallenna(self.__havainnot, self.tiedostonimi)