# ------------------------ #
# ** WHEATER SIMULATION ** #
# ------------------------ #
from multiprocessing import Semaphore, Manager, Process
import random
#import matplotlib.pyplot as plt
import threading
from math import *

# -------------------------------------------
# NOTES
"On suppose à t=0 on est le 1er janvier et que à t=365 on est le 31 décembre"
"Certaine données sont imspirées des valeurs métérologiques de la ville de LYON :"
"https://fr.wikipedia.org/wiki/Lyon"

# -------------------------------------------
# CLASSES METEO
class Weather():
    '''
    Arguments: t (int) : jour de l'année
    Méthodes: jourAnnee() : renvoie le jour de l'année
            tempJour() : renvoie la température du jour 
            ensJour() : renvoie le taux d'ensoleillement du jour
            ventJour() : renvoie l'indice de vent du jour
            afficheStatJour() : affiche les statistiques du jour
    '''

    def __init__(self,t):
        self.t = t
    
    #mise à jour paramétres de meteo 
    def dataJour(self, list, sem):

        #print("Starting process dataJour\n")
        
        self.t=list[3]

        waitTemp = Semaphore(0)
        waitWind = Semaphore(0)
        waitSunBeam = Semaphore(0)

        temperature = threading.Thread(target=self.tempJour, args=(list,waitTemp,))
        windSpeed = threading.Thread(target=self.ventJour, args=(list,waitWind,))
        sunbeam = threading.Thread(target=self.ensJour, args=(list,waitSunBeam,))

        temperature.start()
        windSpeed.start()
        sunbeam.start()

        temperature.join()
        windSpeed.join()
        sunbeam.join()

        waitTemp.acquire()
        print("temp OK")
        waitWind.acquire()
        print("wind OK")
        waitSunBeam.acquire()
        print("sun OK")
        sem.release()
        print("waitTemp released")

        #print("Ending process dataJour\n")

    # Définition du jour de l'année en fonction de t
    def jourAnnee(self):
        mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        nbJoursMois = [31,28,31,30,31,30,31,31,30,31,30,31]
        jour = self.t
        for k in range(len(nbJoursMois)):
            if jour > nbJoursMois[k]:
                jour -= nbJoursMois[k]
            else:
                return (jour, mois[k])

    # Définition de la température quotidienne
    "Température en °C"
    def tempJour(self,list,waitData):
        #print("Starting thread:", threading.current_thread().name)
        coefSaison = -sin(2*pi*self.t/365-250)*15 + 14.5 
        bruit = random.random()*5*random.randint(-1,1)
        list[0]= coefSaison + bruit
        waitData.release()
        #print("Ending thread:", threading.current_thread().name)

    # Définition de l'ensoleillement moyen en 24h
    "Taux d'ensoleillement entre 0 et 1"
    def ensJour(self,list,waitData):
        #print("Starting thread:", threading.current_thread().name)
        (heuresEnsAnnee,heureAnnee) = (2001.9, 8760)
        fmoy = heuresEnsAnnee/heureAnnee
        coefsaison = fmoy - 0.1*sin(2*pi*self.t/365-250)
        bruit = random.random()*0.075*random.randint(-1,1)
        list[2] = coefsaison + bruit
        waitData.release()
        #print("Ending thread:", threading.current_thread().name)
    
    # Définition du vent moyen en 24h
    "Indice entre 0 et 10"
    def ventJour(self,list,waitData):
        #print("Starting thread:", threading.current_thread().name)
        coefSaison = 5 + 2*sin(2*pi*self.t/365-250)
        bruit = random.random()*3*random.randint(-1,1)
        list[1]=  coefSaison + bruit
        waitData.release()
        #print("Ending thread:", threading.current_thread().name)
    
    '''
    # Affichage des statistiques du jour
    def afficheStatJour(self):
        print("\nNous sommes le ", self.jourAnnee()[0], " ", self.jourAnnee()[1])
        print("Température : ", round(self.tempJour(),1),"°C")
        print("Taux d'Ensoleillement : ", self.ensJour())
        print("Indice de Vent : ", self.ventJour(), "\n")
        return None
    '''


# -------------------------------------------
'''
# Quelles Stats aujourd'hui ?
Meteo(23).afficheStatJour()

# Graphique vent
X = [k for k in range(365)]
Y=[]
for k in range(365):
    Y.append(Meteo(k).tempJour())
plt.plot(X,Y)
plt.show()
'''