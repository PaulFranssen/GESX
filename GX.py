
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# importation des modules

from sqlite3 import *
from random import choice, randint
from os import startfile
from tkinter import *
from time import time
import sys
from vue import *  # vue comprend les différents objets FRAME qui seront affichés
from control import *  # les vues sont contrôlées par la base se trouvant dans control

if __name__ == '__main__':

    # création de la DATABASE
    base = Base()

    # création du cadre principal et du lien : cadre > database
    pf = PF(base=base)

    # fixation du lien : base > cadre_principal
    base.fix_cp(pf)

    # affichage écran d'accueil
    pf.accueil()

    # création éventuelle du système de fichiers, établissement de la base de départ et de l'exercice actuel
    base.create_f()

    # boucle principale (attente des événements)

    pf.mainloop()

