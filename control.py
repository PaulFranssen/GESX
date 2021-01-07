#!/usr/bin/env python

# -*- coding: utf-8 -*-

# importation des modules

from sqlite3 import *
from random import choice, randint, randrange
from os import startfile, listdir, getcwd, mkdir, rename
from os.path import isdir, join, exists, splitext, isfile
import shutil
from tkinter import *
from time import time
from datetime import *
from collections import OrderedDict
import sys

from vue import *

class E(Exception):
    pass

class Base:

    def __init__(self):

        self.exercice = None
        self.database = None
        self.database_path = None
        self.connexion = None
        self.curseur = None
        self.cp = None

    def fix_cp(self, cp):
        self.cp = cp
        self.fix_exercice(date.today().year)

    def fix_exercice(self, year):
        self.exercice = year
        self.cp.fix_exercice(year)

    def get_exercice(self):
        return self.exercice

    def fix_database(self, database):

        # fixer le nom de la database et le path
        self.database = database
        self.database_path = join('BASE', database + '.db')

        # afficher le nom à l'écran
        self.cp.fix_database(self.database)

        # création de la database ou ouverture simple
        self.ouvrir()

        # création éventuelle des tables
        self.create_cat()
        self.create_type()
        self.create_article()
        self.create_composition()
        self.create_tiers()
        self.create_workers()
        self.create_charge()
        self.create_factureA()
        self.create_recordA()
        self.create_vente()
        self.create_recordV()
        self.create_stocloture()
        self.create_correction()
        self.create_ponderation()
        self.create_fixecat()
        self.create_limitation()
        self.create_trace()

        # effacement des traces au delà de n_trace jour
        dat = date.today() - timedelta(days=n_trace - 1)
        chaine = """DELETE FROM trace WHERE dat<?"""
        self.curseur.execute(chaine, (dat,))
        self.enregistrer()

        # fermeture de la database
        self.fermer()

        # enregistrement dans le fichier f_base de la databse de lancement
        with open(f_base, 'w', encoding='utf-8') as f:
            f.write(self.database)

    def get_database(self):
        return self.database

    def get_curseur(self):
        return self.curseur

    def ouvrir(self):
        try:
            self.connexion = connect(self.database_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            self.connexion.execute("PRAGMA foreign_keys = 1")
            self.curseur = self.connexion.cursor()

        except Error as error:
            print("Error while connecting to sqlite", error)

        else:
            if self.connexion:
                # connexion à la base de données
                pass

    def enregistrer(self):
        self.connexion.commit()

    def fermer(self):
        self.connexion.close()

    def create_f(self):

        # fixation de l'execice
        self.fix_exercice(date.today().year)

        # création des fichiers txt
        try:
            if not exists('BASE'):
                mkdir('BASE')
            elif not isdir('BASE'):
                mkdir('BASE')
            if not exists('MEM_file'):
                mkdir('MEM_file')
            elif not isdir('MEM_file'):
                mkdir('MEM_file')
            if not exists(f_partage):
                with open(f_partage, 'w', encoding='utf-8') as f:
                    f.write('')
            if not exists(f_sauvegarde):
                with open(f_sauvegarde, 'w', encoding='utf-8') as f:
                    f.write('')
            if not exists(f_dirImport):
                with open(f_dirImport, 'w', encoding='utf-8') as f:
                    f.write('')
            if not exists(f_dirImportVente):
                with open(f_dirImportVente, 'w', encoding='utf-8') as f:
                    f.write('')
            if not exists(f_nameImport):
                with open(f_nameImport, 'w', encoding='utf-8') as f:
                    f.write('')
            if not exists(f_ticket):
                with open(f_ticket, 'w', encoding='utf-8') as f:
                    f.write('')
            if not exists(f_base):
                with open(f_base, 'w', encoding='utf-8') as f:
                    f.write('baseX')
            with open(f_base, 'r', encoding='utf-8') as f:
                nom = f.readline()
            if not nom.strip():
                nom = "baseX"

        except OSError as error:
            print(error)
            # a revoir commentaire avant de débuter
            return False
        else:
            # database initiale
            self.fix_database(nom)

    def create_article(self):
        chaine = """CREATE TABLE IF NOT EXISTS article (
                    art_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    code TEXT,
                    des TEXT,
                    cat_id INTEGER,        
                    pv INTEGER,
                    stockmin INTEGER DEFAULT 0,
                    envente INTEGER DEFAULT 1,
                    ad INTEGER,
                    FOREIGN KEY(cat_id) REFERENCES categorie(cat_id))"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_tiers(self):
        chaine = """CREATE TABLE IF NOT EXISTS tiers (
                            tiers_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            nom TEXT UNIQUE,
                            contact TEXT)"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_workers(self):
        chaine = """CREATE TABLE IF NOT EXISTS workers (
                            worker_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            nom TEXT UNIQUE,
                            contact TEXT)"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_composition(self):
        chaine = """CREATE TABLE IF NOT EXISTS composition (
                        rec_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        compo_id INTEGER,
                        component_id INTEGER,
                        proportion FLOAT,
                        dat timestamp,
                        FOREIGN KEY(compo_id) REFERENCES article (art_id),
                        FOREIGN KEY(component_id) REFERENCES article (art_id))"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_cat(self):

        chaine = """CREATE TABLE IF NOT EXISTS categorie (
                            cat_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            name TEXT UNIQUE)"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_type(self):

        chaine = """CREATE TABLE IF NOT EXISTS type (
                            type_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            name TEXT UNIQUE)"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_factureA(self):
        chaine = """CREATE TABLE IF NOT EXISTS factureA (
                                    fact_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    num TEXT,
                                    tiers_id INTEGER,
                                    dat timestamp,
                                    remise INTEGER,
                                    total INTEGER,
                                    FOREIGN KEY(tiers_id) REFERENCES tiers (tiers_id))"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_vente(self):
        chaine = """CREATE TABLE IF NOT EXISTS vente (
                                        vente_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,                                
                                        dat timestamp,
                                        caisse_id INTEGER,
                                        total INTEGER,
                                        FOREIGN KEY(caisse_id) REFERENCES workers (worker_id))"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_stock(self):
        chaine = """CREATE TABLE IF NOT EXISTS stock (
                                        stock_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,                                
                                        art_id TEXT,
                                        pa FLOAT,
                                        stk FLOAT,
                                        dat timestamp,
                                        FOREIGN KEY(art_id) REFERENCES article (art_id)
                                        )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_stocloture(self):
        chaine = """CREATE TABLE IF NOT EXISTS stocloture (
                                        stock_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,                                
                                        art_id TEXT,
                                        pa FLOAT,
                                        stk FLOAT,
                                        year INTEGER,
                                        FOREIGN KEY(art_id) REFERENCES article (art_id)
                                        )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_trace(self):
        chaine = """CREATE TABLE IF NOT EXISTS trace (
                                        trace_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,                                
                                        dat timestamp,
                                        info1 TEXT,
                                        info2 TEXT,
                                        info3 TEXT,
                                        info4 TEXT,
                                        info5 TEXT
                                        )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_correction(self):
        chaine = """CREATE TABLE IF NOT EXISTS correction (
                                        corr_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,                                
                                        art_id TEXT,
                                        theorique FLOAT,
                                        physique FLOAT,
                                        dat timestamp,
                                        explication TEXT,
                                        FOREIGN KEY(art_id) REFERENCES article (art_id)
                                        )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_charge(self):
        chaine = """CREATE TABLE IF NOT EXISTS charge (
                                    charge_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    dat timestamp,
                                    num TEXT,
                                    type_id INTEGER,
                                    tiers_id INTEGER,
                                    des TEXT,
                                    montant INTEGER,
                                    dif TEXT,
                                    debut timestamp,
                                    mois INTEGER,
                                    FOREIGN KEY(type_id) REFERENCES type (type_id),
                                    FOREIGN KEY(tiers_id) REFERENCES tiers (tiers_id)
                                    )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_recordA(self):
        chaine = """CREATE TABLE IF NOT EXISTS recordA (
                                    rec_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    fact_id INTEGER,
                                    art_id INTEGER,
                                    qte REAL,
                                    prix INTEGER,
                                    FOREIGN KEY(fact_id) REFERENCES factureA (fact_id),
                                    FOREIGN KEY(art_id) REFERENCES article (art_id))"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_recordV(self):
        chaine = """CREATE TABLE IF NOT EXISTS recordV (
                                        v_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                        vente_id INTEGER,
                                        codeV_id INTEGER,
                                        qte REAL,
                                        prix INTEGER,
                                        FOREIGN KEY(codeV_id) REFERENCES article (art_id),
                                        FOREIGN KEY(vente_id) REFERENCES vente (vente_id)
                                        )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_ponderation(self):
        chaine = """CREATE TABLE IF NOT EXISTS ponderation (
                                            pond_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            jour INTEGER UNIQUE,
                                            weighting INTEGER DEFAULT 1
                                            )"""
        self.curseur.execute(chaine)
        self.enregistrer()
        
    def create_fixecat(self):
        chaine = """CREATE TABLE IF NOT EXISTS fixecat (
                                            c_id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            cat_id INTEGER NOT NULL,
                                            pc FLOAT,
                                            couplage INTEGER DEFAULT 0,
                                            FOREIGN KEY(cat_id) REFERENCES categorie (cat_id)
                                            )"""
        self.curseur.execute(chaine)
        self.enregistrer()

    def create_limitation(self):
        chaine = """CREATE TABLE IF NOT EXISTS limitation (
                                            lim_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            jour INTEGER UNIQUE,
                                            limite INTEGER DEFAULT NULL
                                            )"""
        self.curseur.execute(chaine)
        
        # initialisation des limites à None pour chaque jour
        if not self.curseur.execute("""SELECT lim_id FROM limitation"""):
            for jour in range(7):
                    self.insert_limitation(jour)
                               
        self.enregistrer()
        
    def insert_ponderation(self, jour):
        chaine = """INSERT INTO ponderation (jour) VALUES(?)"""
        self.curseur.execute(chaine, (jour,))
        
        
    def insert_fixecat(self, tup):
        chaine = """INSERT INTO fixecat (cat_id, pc, couplage) VALUES(?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_limitation(self, jour):
        chaine = """INSERT INTO limitation (jour) VALUES(?)"""
        self.curseur.execute(chaine, (jour,))

    def insert_stock(self, tup):
        chaine = """INSERT INTO stock (art_id, pa, stk, dat) VALUES(?,?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_stocloture(self, tup):
        chaine = """INSERT INTO stocloture (art_id, pa, stk, year) VALUES(?,?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_article(self, tup):
        chaine = """INSERT INTO article (code,des,cat_id,pv,stockmin,envente,ad) VALUES(?,?,?,?,?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_composition(self, tup):
        chaine = """INSERT INTO composition (compo_id, component_id, proportion, dat) VALUES(?,?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_tiers(self, tup):
        chaine = """INSERT INTO tiers (nom,contact) VALUES(?,?)"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def insert_trace(self, tup):
        chaine = """INSERT INTO trace (dat,info1, info2, info3, info4, info5) VALUES(?,?,?,?,?,?)"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def insert_workers(self, tup):
        chaine = """INSERT INTO workers (nom,contact) VALUES(?,?)"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def insert_correction(self, tup):
        chaine = """INSERT INTO correction (art_id,theorique, physique ,dat,explication) VALUES(?,?,?,?,?)"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def insert_factureA(self, tup=(None, None, None, None, None)):

        chaine = """INSERT INTO factureA (num,tiers_id,dat,remise,total) VALUES(?,?,?,?,?)"""
        self.curseur.execute(chaine, tup)

        # chaine = """SELECT fact_id FROM factureA"""
        # return self.curseur.execute(chaine).fetchall()[-1][0]

    def insert_charge(self, tup=(None, None, None, None, None, None, None, None, None)):

        chaine = """INSERT INTO charge (dat, num, type_id, tiers_id, des, montant, dif, debut, mois) 
                    VALUES(?,?,?,?,?,?,?,?,?)"""
        self.curseur.execute(chaine, tup)

        chaine = """SELECT charge_id FROM charge """
        return self.curseur.execute(chaine).fetchall()[-1][0]

    def insert_vente(self, tup=(None, None, None)):

        chaine = """INSERT INTO vente (dat, caisse_id, total) VALUES(?,?,?)"""
        self.curseur.execute(chaine, tup)

        chaine = """SELECT vente_id FROM vente"""
        return self.curseur.execute(chaine).fetchall()[-1][0]

    def insert_recordA(self, tup):
        chaine = """INSERT INTO recordA (fact_id,art_id,qte,prix) VALUES(?,?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_recordV(self, tup):
        chaine = """INSERT INTO recordV (vente_id, codeV_id, qte, prix) VALUES(?,?,?,?)"""
        self.curseur.execute(chaine, tup)

    def insert_categorie(self, name):
        chaine = """INSERT INTO categorie (name) VALUES(?)"""
        self.curseur.execute(chaine, (name,))
        self.enregistrer()

    def insert_type(self, name):
        chaine = """INSERT INTO type (name) VALUES(?)"""
        self.curseur.execute(chaine, (name,))
        self.enregistrer()

    def update_type(self, tup):
        chaine = """UPDATE type
                    SET name=?
                    WHERE type_id=?"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def update_article(self, tup):

        chaine = """UPDATE article 
                SET code=?, des=?, cat_id=?, pv=?, stockmin=?, envente=?, ad=? 
                WHERE art_id=?"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def update_categorie(self, tup):

        chaine = """UPDATE categorie 
                SET name=?
                WHERE cat_id=?"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def update_tiers(self, tup):

        chaine = """UPDATE tiers 
                SET nom=?, contact=?
                WHERE tiers_id=?"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def update_workers(self, tup):

        chaine = """UPDATE workers 
                SET nom=?, contact=?
                WHERE worker_id=?"""
        self.curseur.execute(chaine, tup)
        self.enregistrer()

    def update_factureA(self, tup):
        chaine = """UPDATE factureA SET num=?,tiers_id=?,dat=?,remise=?,total=? WHERE fact_id=?"""
        self.curseur.execute(chaine, tup)

    def update_vente(self, tup):
        chaine = """UPDATE vente SET dat=?,caisse_id=?,total=? WHERE vente_id=?"""
        self.curseur.execute(chaine, tup)

    def update_ponderation(self, tup):
        chaine = """UPDATE ponderation SET weighting=?  WHERE jour=?"""
        self.curseur.execute(chaine, tup)
        
    def update_fixecat(self, tup):
        self.curseur.execute("""DELETE FROM fixecat""")
        self.insert_fixecat(tup)

    def update_limitation(self, tup):
        print(tup)
        chaine = """UPDATE limitation SET limite=?  WHERE jour=?"""
        self.curseur.execute(chaine, tup)

    def update_charge(self, tup):
        chaine = """UPDATE charge SET dat=?, num=?, type_id=?, tiers_id=?, des=?, montant=?, dif=?, debut=?, mois=? 
                WHERE charge_id=?"""
        self.curseur.execute(chaine, tup)

    def action_47(self, **kw):
        # récupérer les variables
        comment = kw['comment']
        nom = kw['nom'].get().strip()

        # test
        com = ''
        liste = listdir('BASE')
        filename = nom + '.db'
        if not nom:
            com = "ERREUR database (vide)"
        elif len(nom) > l_baseC:
            com = "ERREUR database (limite : " + str(l_baseC) + " caractères)"
        elif not nom.isalnum():
            com = "ERREUR database (catactère non-alphanumérique)"
        elif filename in liste:
            com = 'ERREUR database (déjà existante)'
        comment.set(com)
        if com:
            return False

        self.fix_database(nom)
        comment.set(nom + ' créée')
        return True

    def action_46(self, **kw):

        def test():
            com = ''
            year = self.exercice

            if not (d_i and d_f):
                com = "ERREUR date (non conforme)"
            elif d_f < d_i:
                com = "ERREUR date (non conforme)"
            elif d_f.year != year or d_f.year != year:
                com = "ERREUR date (année non conforme)"
            elif not func_1(montant):
                com = "ERREUR montant total (non conforme)"
            elif not func_1(vente_nulle):
                com = "ERREUR ventes nulles (non conforme)"
            elif not (0 <= int(vente_nulle) <= 100):
                com = "ERREUR ventes nulles (doit être entre 0 et 100)"
            elif not caisse:
                com = "ERREUR caissier(ère) (vide)"
            elif not self.function_12(caisse):
                com = "ERREUR caissier(ère) (inconnu)"
            return com

        def f_1(x, y):
            """détermine les stocks disponibles des articles inventoriés

            Args:
                x (datetime): date initiale de la vente
                y (datetime): date finale de la vente

            Returns:
                dict: clé: art_id (articles inventoriés) valeurs: stock disponible pour la vente
            """            
            # récupération des art_id des articles inventoriés
            chaine = """SELECT art_id FROM article WHERE ad=?"""
            result = self.curseur.execute(chaine, (1,)).fetchall()
            
            # initailisation du dico
            dico = {}
        
            if result:
                for tup in result:
                    # stock de chaque article avant le premier jour de vente
                    dico[tup[0]] = self.function_46(tup[0], func_20(x))
                    
                # augmentation du stock suite aux achats entre les la date initiale inculuse et le dernier jour de génération   
                chaine = """SELECT art_id, qte FROM recordA, factureA
                            WHERE recordA.fact_id=factureA.fact_id
                            AND dat>=?
                            AND dat<?"""
                res = self.curseur.execute(chaine, (x, func_18(y)))
                if res:
                    # ajout des quantités achetées dans le dictionnaire
                    for tup in res:
                        dico[tup[0]] += tup[1]
            return dico

        def f_2(dico, dat):
            """détermine la liste des articles seront choisis

            Args:
                dico (dict ): dictionnaire des articles inventoriés
                dat (datetime): date de création de la liste

            Returns:
                list: liste de tuples (art_id, cat_id, pv)
            """      
            # sélection des articles en vente, des PV, de la catégorie, du type (composé ou inventorié)
            chaine = """SELECT art_id, cat_id, pv, ad FROM article WHERE envente=?"""
            result = self.curseur.execute(chaine, (1,)).fetchall()
            liste = []
            if result:
                for tup in result:
                    art_id, cat_id, pv, ad = tup
                    if ad == 1:
                        # article inventorié : le poids est égal au stock
                        weight = dico[art_id]
                    else:
                        list_c = self.function_15(art_id, dat)
                        weight = 0
                        if list_c:
                            for tupl in list_c:
                                a_id, proportion = tupl
                                # reglage du poids des composés
                                weight += dico[a_id] * max(coef_compose, proportion)
                        else:
                            # le composé n'était pas créé à cette date
                            continue
                    # on ajoute autant d'articles art_id que son poids à la liste
                    for i in range(round(weight)):
                        liste.append((art_id, cat_id, pv))
            return liste

        def f_6(x, y):
            """construit la liste des jours de vente

            Args:
                x (datetime): premier jour de vente
                y (datetime): dernier jour de vente

            Returns:
                list: liste 
            """            
            day = x
            liste = []
            while day <= y:
                nbr = self.function_65(day)
                print(nbr, 'fonction_65(day)')
                liste += [day for j in range(self.function_65(day))]
                day += timedelta(days=1)
            return liste

        def f_3(dico, x, y, dico_quota):
            """détermine la validité des choix

            Args:
                dico (dict): dictionnaire des stocks
                x (tuple): (art_id, cat_id, pv)
                y (datetime): jour choisi
                dico_quota(dict): dictionnaire des quotas

            Returns:
                bool: True si le choix est bon, false sinon
            """            
            art_id, cat_id, pv = x                 
            res = True
            
            # vérification non dépassement de limite du jour
            chaine = """SELECT limite FROM limitation WHERE jour=?"""
            result = self.curseur.execute(chaine, (y.weekday(),)).fetchone()
            if result:
                limite = result[0] 
                if limite is not None and pv >= limite:
                    res = False           
            if res:   
                # verification non-dépassement des quotas de catégories
                if cat_id in dico_quota:                   
                    if dico_quota[cat_id][1] > dico_quota[cat_id][0]: 
                        # dépassement dans une catégorie fixée           
                        res = False  
                        # suppression des éléments de cette catégorie
                        i = 0
                        while i<len(list_choix):
                            if list_choix[i][1] == cat_id:
                                del list_choix[i]
                            else:
                                i +=1
                            
                elif dico_quota[0][1] > dico_quota[0][0]:
                    # dépassement dans le reste des catégories
                    res = False    
                    # suppression des éléments des autres catégories
                    i = 0
                    while i<len(list_choix):
                        if list_choix[i][1] not in dico_quota:
                            del list_choix[i]
                        else:
                            i +=1                  
            if res:
                # vérification de non stock négatifs (et retrait des stocks)
                chaine = """SELECT ad FROM article WHERE art_id=?"""
                result = self.curseur.execute(chaine, (art_id,)).fetchone()
                ad = result[0]
                if ad == 1:
                    # article inventorié
                    if dico[art_id] - 1 < 0:
                        res = False
                    else:
                        # retrait des stocks
                        dico[art_id] -= 1
                else:
                    # articles composés
                    liste = self.function_15(art_id, y)
                    for tup in liste:
                        component_id, proportion = tup
                        if dico[component_id] - proportion < 0:
                            res = False
                    # retrait des stocks
                    for tup in liste:
                        component_id, proportion = tup
                        dico[component_id] -= proportion        
            return res
          
        def f_4(dico, x, y, nulle, dico_quota):
            """ajout de l'article dans le dictionnaire des ventes et des quotas

            Args:
                dico (dict): dictionnaire des ventes
                x (tuple): (art_id, cat_id, pv) relatif à l'article vendu
                y (datetime): date de la vente
                nulle (float): pourcentage de vente nulle

            Returns:
                int: prix de vente
            """
            art_id, cat_id, pv = x
            facteur = (lambda z: 1 if randint(0, 100) >= z else 0)(nulle)
            pv = facteur * pv
            
            # complétion du dictionnaire des catégories
            if cat_id in dico_quota:
                dico_quota[cat_id][1] += pv
            else:
                dico_quota[0][1] += pv 
                
            # ajout dans le dictionnaire de vente
            if y not in dico:
                dico[y] = ({art_id: [1, pv]})
            elif art_id not in dico[y]:
                dico[y][art_id] = [1, pv]
            else:
                dico[y][art_id][0] += 1
                dico[y][art_id][1] += pv
            return pv

        def f_5(dico, caisse):
            """transfert des ventes dans la base de données

            Args:
                dico (dict): clé: (datetime) date de la vente / valeur : dict: clé : art_id, valeur : (qte, pv)
                caisse (str): caissier
            """
            for dat in dico:

                # calcul du total pour la date dat
                total = 0
                for art_id in dico[dat]:
                    total += dico[dat][art_id][1]

                # insertion de la vente
                vente_id = self.insert_vente(tup=(dat, self.function_12(caisse), total))

                # insertion des record vente
                for art_id in dico[dat]:
                    qte = dico[dat][art_id][0]
                    prix = dico[dat][art_id][1]
                    self.insert_recordV(tup=(vente_id, art_id, qte, prix))

        def f_7(begin, end):
            """suppression des ventes 

            Args:
                begin (datetime): date de début des ventes
                end (datetime): dernier jour des ventes
            """            
            chaine = """SELECT vente_id FROM vente WHERE dat>=? and dat<?"""
            result = self.curseur.execute(chaine, (begin, func_18(end))).fetchall()
            if result:
                for tup in result:
                    chaine = """DELETE FROM recordV WHERE vente_id=?"""
                    self.curseur.execute(chaine, tup)
                    chaine = """DELETE FROM vente WHERE vente_id=?"""
                    self.curseur.execute(chaine, tup)
        
        def f_8(dico, montant):
            """construit le dictionnaire des quotas de la catégorie

            Args:
                dico (dict): clé: cat_id ou 0 (autres) ;valeurs: (montant de la catégorie, montant vendu actualisé)
                montant (int): total des biens vendus
            Returns:
                None
            """
            # récupération des montants dans la databse
            chaine = """SELECT cat_id, pc FROM fixecat"""
            result = self.curseur.execute(chaine)
            total_pc = 0
            if result:
                for (cat_id, pc) in result:
                    dico[cat_id] = [pc*montant/100, 0]
                    total_pc += pc
            dico[0] = [montant - total_pc*montant/100, 0]               
            print('dico_quotas', dico)
            
        ### corps principal ###
        
        # récupération des variables
        comment = kw['comment']
        d_i = func_7(kw['dat_i'].get().strip())
        d_f = func_7(kw['dat_f'].get().strip())
        montant = kw['montant'].get().strip()
        vente_nulle = kw['vente_nulle'].get().strip()
        caisse = kw['caisse'].get().strip()

        # test
        com = test()
        comment.set(com)
        if com:
            return False
        montant = int(montant)
        vente_nulle = int(vente_nulle)

        # dictionnaire des stocks
        dico_stock = f_1(d_i, d_f)
        if not len(dico_stock):
            comment.set("ERREUR pas d'articles inventoriés")
            return False

        # liste de choix de l'article
        list_choix = f_2(dico_stock, d_i)
        if not len(list_choix):
            comment.set("ERREUR pas d'articles en vente")
            return False
        
        print('list_choix', list_choix)

        # liste des jours
        list_jour = f_6(d_i, d_f)
        if not len(list_jour):
            comment.set("ERREUR pas de dates programmées")
            return False
        
        # construction du dictionnaire de quotas (catégories) clés cat_id des catégories ou 0 (autres)
        #   valeurs : couple (montant d'achat, montant actuel vendu)
        
        dico_quota ={}
        f_8(dico_quota, montant)
        
        # suppression dans la liste articles ceux dont la catégorie est pc=0
        liste = [cat_id for cat_id in dico_quota if cat_id !=0] # ltste des catégories fixées
        pc = 100 - sum([dico_quota[cat_id][0] for cat_id in liste]) # pourcentage de la catégorie 0
        if pc == 0:
            # conservation des articles de catégorie dans la liste
            list_choix = [elem for elem in list_choix if elem[1] in liste]
        ## conservation des catégories ne se trouvant pas dans la liste ou, si elle s'y trouve, n'est pas à 0
        list_choix = [elem for elem in list_choix if (elem[1] in liste and dico_quota[elem[1]][0] != 0) or (elem[1] not in liste)]
        
        # initialisation de la boucle de choix
        dico_vente = {}
        t = 0
        iteration = 0
        comment.set('en cours...')

        # boucle principale     
        while t < montant and len(list_choix) and iteration < max_iteration:
            
            # choix aléatoire de l'article et du jour
            article = choice(list_choix)  # article est un triplet (art_id, cat_id, pv)
            jour = choice(list_jour)

            # validité des choix          
            if not f_3(dico_stock, article, jour, dico_quota):
                iteration +=1
                continue

            # ajout du choix dans le dictionnaire de vente et incrémentation du total
            t += f_4(dico_vente, article, jour, vente_nulle, dico_quota)

            # retrait de l'article choisi de la liste
            list_choix.remove(article) 

        # fin de boucle >
        # vérification des raisons de sortie de boucle
        if iteration == max_iteration:
            comment.set(f"ERREUR : itérations excessives({iteration})")
            return False
        if not len(list_choix):
            comment.set(f"ERREUR : manque d'articles en vente selon les critères")
            return False
        
        # suppression des ventes entre les dates
        f_7(d_i, d_f)


        # transfert du dico_vente dans la database
        f_5(dico_vente, caisse)

        # enregistrement des modifications de la base
        self.enregistrer()
        comment.set(f"Total généré : {func_6(t)}")
        return True

    def display_11(self, **kw):

        art_id = kw['art_id']

        chaine = """SELECT des, cat_id, pv, stockmin, envente FROM article 
                    WHERE art_id=?"""
        result = self.curseur.execute(chaine, (art_id,)).fetchone()
        chaine = """SELECT name FROM categorie 
                    WHERE cat_id=?"""
        result2 = self.curseur.execute(chaine, (result[1],)).fetchone()
        kw['des'].set(result[0])
        kw['cat'].set(result2[0])
        kw['pv'].set(result[2])
        kw['stockmin'].set(result[3])
        envente = result[4]
        kw['envente'].set(envente)
        if envente:
            kw['pv_widget'].configure(state='normal')
        else:
            kw['pv_widget'].configure(state='disabled')
        kw['comment'].set('')

    def display_21(self, **kw):

        spin = kw['spin']
        var_spin = kw['var_spin']
        comment = kw['comment']
        try:
            path = join(getcwd(), 'BASE')
            liste = listdir(path)
            liste = [splitext(b)[0] for b in liste]

        except OSError as error:
            comment.set(error)
        else:
            spin.config(values=liste)
            var_spin.set(self.database)

    def display_34(self, **kw):

        non_id = kw['non_id']
        code = self.function_29(non_id)
        kw['des'].set(self.function_3(code))
        cat_id = self.function_33(code)
        kw['cat'].set(self.function_32(cat_id))
        kw['comment'].set('')

    def display_26(self, **kw):

        arg = kw['arg']
        kw['code'].set(arg)
        chaine = """SELECT contact FROM tiers 
                    WHERE nom=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()
        if result:
            kw['des'].set(result[0])
        kw['comment'].set('')

    def display_24(self, **kw):

        compo_id = kw['compo_id']

        chaine = """SELECT des, cat_id, pv, envente 
                    FROM article 
                    WHERE art_id=?"""
        result = self.curseur.execute(chaine, (compo_id,)).fetchone()
        chaine = """SELECT name FROM categorie 
                           WHERE cat_id=?"""
        result2 = self.curseur.execute(chaine, (result[1],)).fetchone()
        kw['des'].set(result[0])
        kw['cat'].set(result2[0])
        kw['pv'].set(result[2])

        envente = result[3]
        kw['envente'].set(envente)
        if envente:
            kw['pv_widget'].configure(state='normal')
        else:
            kw['pv_widget'].configure(state='disabled')

        # display composition

        list_box = kw['list_box']
        list_ref = kw['list_ref']

        dat = self.function_40(compo_id, datetime.now())
        chaine = """SELECT component_id, proportion 
                    FROM composition
                    WHERE compo_id=?
                    AND dat=?"""
        result = self.curseur.execute(chaine, (compo_id, dat)).fetchall()

        for tup in result:
            code = self.function_6(tup[0])
            des = self.function_3(code)
            proportion = tup[1]
            list_ref.append({'code': code, 'proportion': proportion})
            list_box.append(ligne_7.format(code, des, proportion))

        kw['var_box'].set(list_box)
        kw['comment'].set('')

    def display_27(self, **kw):

        arg = kw['arg']

        # récupérer les éléments de la facture dans la base de données

        chaine = """SELECT num, tiers_id, dat, remise, total 
                    FROM factureA 
                    WHERE fact_id=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()

        kw['num'].set(result[0])
        kw['tiers'].set(self.function_11(result[1]))
        kw['dat'].set(func_8(result[2]))
        kw['remise'].set('')
        if result[3]:
            kw['remise'].set(func_5(result[3]))
        kw['total'].set(func_5(result[4]))

        # recupérer les enregistrements et les ajouter dans la boite

        chaine = """SELECT art_id, qte, prix 
                    FROM recordA  
                    WHERE fact_id = ?"""
        result = self.curseur.execute(chaine, (arg,)).fetchall()

        for tup in result:
            code = self.function_29(tup[0])
            des = self.function_3(code)
            qte = func_6(tup[1])
            prix = tup[2]
            kw['list_ref'].append({'code': code, 'qte': qte, 'prix': prix})
            kw['list_box'].append(ligne_8.format(code, des, qte, func_5(prix)))
        kw['var_box'].set(value=kw['list_box'])
        return

    def display_15(self, **kw):

        arg = kw['arg']

        # récupérer les éléments de la facture dans la base de données

        chaine = """SELECT dat,caisse_id,total 
                    FROM vente 
                    WHERE vente_id=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()

        kw['caisse'].set(self.function_14(result[1]))
        kw['dat'].set(func_8(result[0]))
        kw['total'].set(func_5(result[2]))

        # recupérer les enregistrements et les ajouter dans la boite

        chaine = """SELECT codeV_id, qte, prix 
                        FROM recordV 
                        WHERE vente_id = ?"""
        result = self.curseur.execute(chaine, (arg,)).fetchall()

        for tup in result:
            code = self.function_29(tup[0])
            des = self.function_3(code)
            qte = func_6(tup[1])
            prix = tup[2]
            kw['list_ref'].append({'code': code, 'qte': qte, 'prix': prix})
            kw['list_box'].append(ligne_8.format(code, des, qte, func_5(prix)))
        kw['var_box'].set(value=kw['list_box'])
        return

    def display_18(self, **kw):

        code = kw['code'].get()
        kw['des'].set(self.function_3(code))
        kw['theorique'].set(self.function_23(code))
        kw['explication'].set('')

    def display_29(self, **kw):

        arg = kw['arg']
        kw['code'].set(arg)
        chaine = """SELECT contact FROM workers 
                    WHERE nom=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()
        if result:
            kw['des'].set(result[0])
        kw['comment'].set('')

    def display_30(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' inventaire')
        kw['comment'].set('')

    def display_43(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' bilan')
        kw['comment'].set('')

    def display_51(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' bilan annuel ' + str(self.exercice))
        kw['comment'].set('')

    def display_52(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' traçage')
        kw['comment'].set('')

    def display_42(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' articles')
        kw['comment'].set('')

    def display_44(self, **kw):
        p = kw['p']
        comment = kw['comment']
        com = ''

        chaine = """SELECT jour, weighting FROM ponderation"""
        result = self.curseur.execute(chaine).fetchall()
        if result:
            for tup in result:
                p[tup[0]].set(tup[1])
        else:
            for jour in range(7):
                self.insert_ponderation(jour)
                p[jour].set('1')
            self.enregistrer()
            
    def display_55(self, **kw):
      
        n = kw['n']
        cat = kw['cat']
        pc = kw['pc']
        couplage = kw['couplage']
        
        
        # effacement
        couplage.set(0)
        kw['comment'].set('')
        for i in range(n):
            cat[i].set('')
            pc[i].set('') 
                       
        # récupération des enregistrements dans result
        chaine = """SELECT cat_id, pc, couplage FROM fixecat"""
        result = self.curseur.execute(chaine).fetchall()
        if result:
            for i, tup in enumerate(result):
                cat_id, percent, couple = tup
                # placement des valeurs de la base dans les variables dynamiques
                cat[i].set(self.function_32(cat_id))
                pc[i].set(int(percent) if percent == int(percent) else percent) 
                if i == 0:
                    couplage.set(couple)               
            
    def display_45(self, **kw):
        p = kw['p']
        comment = kw['comment']
        com = ''
        chaine = """SELECT jour, limite FROM limitation"""
        result = self.curseur.execute(chaine).fetchall()
        if result:
            for tup in result:
                if tup[1] is not None:
                    p[tup[0]].set(tup[1])
                else:
                    p[tup[0]].set('')
        else:
            com = "Erreur database (limitation)"
        
        comment.set(com)
        
    def display_31(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' alertes-stock')
        kw['comment'].set('')

    def validate_23(self, **kw):

        list_box = kw['list_box']
        list_ref = kw['list_ref']
        var_box = kw['var_box']

        code_i = kw['code_i'].get().strip()
        p = kw['proportion'].get().strip()

        com = ''

        if not (code_i or p):
            return True
        elif not code_i:
            com = 'ERREUR composition (code absent)'
        elif not self.function_2(code_i):
            com = 'ERREUR composition (code erroné)'
        else:
            try:
                proportion = float(eval(p))
                proportion = round(proportion, 2)
                if proportion < 0:
                    com = 'ERREUR composition (proportion non conforme)'
            except:
                com = 'ERREUR composition (proportion non conforme)'

        if com:
            kw['comment'].set(com)
            return False

        list_box.append(ligne_7.format(code_i, kw['des_i'].get(), proportion))
        var_box.set(list_box)
        list_ref.append({'code': code_i, 'proportion': proportion})

        kw['code_i'].set('')
        kw['des_i'].set('')
        kw['proportion'].set('')
        kw['comment'].set('')
        return True

    def validate_27(self, **kw):

        remise = kw['remise'].get().strip().replace('.', '')
        code = kw['code'].get().strip()
        qte = kw['qte'].get().strip().replace(',', '.')
        prix = kw['prix'].get().strip().replace('.', '')

        list_box = kw['list_box']
        list_ref = kw['list_ref']
        var_box = kw['var_box']

        com = ''

        code_id = self.function_5(code)

        # contrôle de la zone d'encodage
        if code or qte or prix:

            if not code:
                com = 'ERREUR code (vide)'
            elif not code_id:
                com = 'ERREUR code (inconnu)'
            elif self.function_7(code_id):
                com = 'ERREUR code (article composé)'
            elif not func_3(qte):
                com = 'ERREUR qté (non conforme)'
            elif not func_1(prix):
                com = 'ERREUR prix (non conforme)'

        kw['comment'].set(com)
        if com:
            return False

        # vérification remise

        if not func_2(remise):
            com = 'ERREUR remise (non conforme)'

        kw['comment'].set(com)

        if com:
            return False

        # calcul du total

        tot = 0
        for dico in list_ref:
            tot += int(dico['prix'])

        tot = tot + func_4(prix) - func_4(remise)
        kw['total'].set(func_5(tot))
        if remise:
            kw['remise'].set(func_5(remise))

        # retour si pas d'encodage

        if not (code and qte and prix):
            return True

        # ajout à la box

        qte = func_6(float(qte))
        list_ref.append({'code': code, 'qte': qte, 'prix': prix})
        list_box.append(ligne_8.format(code, self.function_3(code), qte, func_5(int(prix))))
        var_box.set(value=list_box)

        # suppression de l'encodage et du commentaire
        kw['code'].set('')
        kw['des'].set('')
        kw['qte'].set('')
        kw['prix'].set('')
        kw['comment'].set('')

        return True

    def display_54(self, **kw):

        repertoire = kw['repertoire']
        d_i = kw['d_i']
        d_f = kw['d_f']
        comment = kw['comment']
        kw['def_rep'].set(0)

        comment.set('')

        try:
            with open(f_ticket, "r", encoding="utf-8") as f:
                p = f.readline()
        except OSError as error:
            comment.set(error)
            return
        repertoire.set(p)

    def display_38(self, **kw):

        partage = kw['partage']
        sauvegarde = kw['sauvegarde']
        kw['partage'].set(0)
        kw['def_sauvegarde'].set(0)
        comment = kw['comment']
        comment.set('')

        try:
            with open(f_partage, "r", encoding="utf-8") as f:
                p = f.readline()
                partage.set(p)
        except OSError as error:
            comment.set(error)
            return False

        try:
            with open(f_sauvegarde, "r", encoding="utf-8") as f:
                p = f.readline()
                sauvegarde.set(p)
        except OSError as error:
            comment.set(error)
            return False
        return True

    def display_49(self, **kw):

        importe = kw['importe']
        nom = kw['nom']
        comment = kw['comment']
        kw['def_importe'].set(0)
        kw['def_nom'].set(0)

        comment.set('')

        try:
            with open(f_dirImport, "r", encoding="utf-8") as f:
                p = f.readline()
        except OSError as error:
            comment.set(error)
            return
        importe.set(p)

        try:
            with open(f_nameImport, "r", encoding="utf-8") as f:
                p = f.readline()
        except OSError as error:
            comment.set(error)
            return
        nom.set(p)

    def display_58(self, **kw):

        importe = kw['importe']
        nom = kw['nom']
        comment = kw['comment']
        kw['def_importe'].set(0)

        comment.set('')

        try:
            with open(f_dirImportVente, "r", encoding="utf-8") as f:
                p = f.readline()
        except OSError as error:
            comment.set(error)
            return
        importe.set(p)

    def display_59(self, **kw):

        x = getcwd()
        y = join(x, 'DOCUMENTS')
        if not isdir(y):
            mkdir(y)
        kw['path'].set(y)
        kw['filename'].set(str(date.today()) + ' données')
        kw['comment'].set('')

    def display_39(self, **kw):
        arg = kw['arg']
        dat = kw['dat']
        code = kw['code']
        des = kw['des']
        ph = kw['ph']
        th = kw['th']
        corr = kw['corr']
        explication = kw['explication']
        comment = kw['comment']

        try:
            chaine = """SELECT dat, art_id, theorique, physique, explication 
                        FROM correction
                        WHERE corr_id=?"""
            result = self.curseur.execute(chaine, (arg,)).fetchone()
        except Error as error:
            kw['comment'].set(error)
            return False
        else:
            if result:
                dat.set(func_9(result[0]))
                c = self.function_6(result[1])
                code.set(c)
                des.set(self.function_3(c))
                ph.set(func_6(result[3]))
                th.set(func_6(result[2]))
                c = result[3] - result[2]
                explication.set(result[4])
                if c > 0:
                    corr.set('+' + func_6(c))
                else:
                    corr.set(func_6(c))
            comment.set('')
            return True

    def validate_15(self, **kw):

        code = kw['code'].get().strip()
        qte = kw['qte'].get().strip().replace(',', '.')
        prix = kw['prix'].get().strip().replace('.', '')
        list_box = kw['list_box']
        list_ref = kw['list_ref']
        var_box = kw['var_box']
        com = ''
        code_id = self.function_5(code)

        # contrôle de la zone d'encodage

        if code or qte or prix:
            if not code:
                com = 'ERREUR code (vide)'
            elif not code_id:
                com = 'ERREUR code (inconnu)'
            elif not self.function_20(code):
                com = 'ERREUR code (pas en vente)'
            elif not func_3(qte):
                com = 'ERREUR qté (non conforme)'
            elif not func_1(prix):
                com = 'ERREUR prix (non conforme)'

        kw['comment'].set(com)
        if com:
            return False

        # calcul du total

        tot = 0
        for dico in list_ref:
            tot += int(dico['prix'])

        tot = tot + func_4(prix)
        kw['total'].set(func_5(tot))

        # retour si pas d'encodage

        if not (code and qte and prix):
            return True

        # ajout à la box
        qte = func_6(float(qte))
        list_ref.append({'code': code, 'qte': qte, 'prix': prix})
        list_box.append(ligne_8.format(code, self.function_3(code), qte, func_5(int(prix))))
        var_box.set(value=list_box)

        # suppression de l'encodage et du commentaire
        kw['code'].set('')
        kw['des'].set('')
        kw['qte'].set('')
        kw['prix'].set('')
        kw['comment'].set('')

        return True

    def display_14(self, **kw):

        arg = kw['arg']
        chaine = """SELECT dat, num, name, nom, des, montant, dif, debut, mois
                    FROM charge, type, tiers
                    WHERE charge.type_id=type.type_id
                    AND charge.tiers_id=tiers.tiers_id
                    AND charge_id=?"""
        r = self.curseur.execute(chaine, (arg,)).fetchone()

        if r:
            kw['dat'].set(func_8(r[0]))
            kw['num'].set(r[1])
            kw['type'].set(r[2])
            kw['tiers'].set(r[3])
            kw['des'].set(r[4])
            kw['montant'].set(r[5])
            if r[6]:
                kw['debut_w'].config(state='normal')
                kw['mois_w'].config(state='normal')
                kw['debut'].set(func_8(r[7]))
                kw['mois'].set(r[8])
                if r[6] == 'A':
                    kw['amor'].set(1)
                elif r[6] == 'R':
                    kw['repart'].set(1)
        else:
            kw['comment'].set('ERREUR base de données (charge absente)')

    def record_4(self, **kw):

        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        cat = kw['cat'].get().strip()
        pv = kw['pv'].get().strip()
        envente = kw['envente'].get()
        stockmin = kw['stockmin'].get().strip()

        com = ''
        if not code:
            com = "ERREUR code (vide)"
        elif not code.isalnum():
            com = "ERREUR code (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR code (limite = " + str(l_code) + " caractères)"
        elif code in self.function_28():
            com = "ERREUR code (déjà utilisé)"
        elif not des:
            com = "ERREUR désignation (vide)"
        elif len(des) > l_des:
            com = "ERREUR désignation (limite = " + str(l_des) + " caractères)"
        elif not self.function_8(cat):
            com = "ERREUR catégorie (inexistante)"
        elif not func_2(pv):
            com = "ERREUR prix de vente"
        elif not func_1(stockmin):
            com = "ERREUR stock minimum"

        kw['comment'].set(com)
        if com:
            return False
        else:
            cat_id = self.function_8(cat)
            self.insert_article((code, des, cat_id, pv, stockmin, envente, 1))

            tup = (datetime.now(), 'ajout', 'article', code, des, cat)
            self.insert_trace(tup)

            self.enregistrer()
            return code

    def record_33(self, **kw):

        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        cat = kw['cat'].get().strip()

        com = ''
        cat_id = self.function_8(cat)

        if not code:
            com = "ERREUR code (vide))"
        elif not code.isalnum():
            com = "ERREUR code (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR code (limite = " + str(l_code) + " caractères)"
        elif not cat:
            com = "ERREUR catégorie (vide)"
        elif not cat_id:
            com = "ERREUR catégorie (inexistante)"
        elif not des:
            com = "ERREUR désignation (vide)"
        elif len(des) > l_des:
            com = "ERREUR désignation (limite = " + str(l_des) + " caractères)"

        kw['comment'].set(com)
        if com:
            return False
        else:
            self.insert_article((code, des, cat_id, None, None, 0, 0))

            tup = (datetime.now(), 'ajout', 'article', code, des, cat)
            self.insert_trace(tup)
            self.enregistrer()
            return code

    def record_7(self, **kw):
        code = kw['code'].get().strip()
        com = ''
        if not code:
            com = "ERREUR nom (vide)"
        elif not code.isalnum():
            com = "ERREUR nom (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR nom (limite = " + str(l_code) + " caractères)"
        elif self.function_8(code):
            com = "ERREUR nom (déjà utilisé)"

        kw['comment'].set(com)
        if com:
            return False
        else:
            self.insert_categorie(code)
            self.enregistrer()
            return code

    def record_36(self, **kw):

        code = kw['code'].get().strip()

        com = ''
        if not code:
            com = "ERREUR nom (vide)"
        elif not code.isalnum():
            com = "ERREUR nom (non alphanumérique)"
        elif len(code) > l_type:
            com = "ERREUR nom (limite = " + str(l_type) + " caractères)"
        elif self.function_30(code):
            com = "ERREUR nom (déjà utilisé)"

        kw['comment'].set(com)
        if com:
            return False
        else:
            self.insert_type(code)
            self.enregistrer()
            return code

    def record_8(self, **kw):

        nom = kw['code'].get().strip()
        contact = kw['des'].get().strip()

        com = ''
        if not nom:
            com = "ERREUR nom (vide)"

        elif self.function_9(nom):
            com = "ERREUR nom (déjà utilisé)"

        elif len(nom) > l_code:
            com = "ERREUR nom (limite = " + str(l_code) + " caractères)"

        kw['comment'].set(com)

        if not com:
            self.insert_tiers((nom, contact))
            return nom
        else:
            return False

    def record_28(self, **kw):

        nom = kw['code'].get().strip()
        contact = kw['des'].get().strip()

        com = ''
        if not nom:
            com = "ERREUR nom (vide)"

        elif self.function_12(nom):
            com = "ERREUR nom (déjà utilisé)"

        elif len(nom) > l_code:
            com = "ERREUR nom (limite = " + str(l_code) + " caractères)"

        kw['comment'].set(com)

        if not com:
            self.insert_workers((nom, contact))
            return nom
        else:
            return False

    def record_11(self, **kw):

        art_id = kw['art_id']
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        cat = kw['cat'].get().strip()
        pv = kw['pv'].get().strip()
        stockmin = kw['stockmin'].get().strip()
        envente = kw['envente'].get()

        com = ''
        if not code:
            com = "ERREUR code (vide)"
        elif not code.isalnum():
            com = "ERREUR code (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR code (limite = " + str(l_code) + " caractères)"
        elif code in self.function_28() and self.function_5(code) != art_id:
            com = "ERREUR code (déjà utilisé)"
        elif not des:
            com = "ERREUR désignation (vide)"
        elif len(des) > l_des:
            com = "ERREUR désignation (limite = " + str(l_des) + " caractères)"
        elif not self.function_8(cat):
            com = "ERREUR catégorie (inconnue)"
        elif not func_2(pv):
            com = "ERREUR prix de vente"
        elif not func_1(stockmin):
            com = "ERREUR stock minimum"

        kw['comment'].set(com)

        if not com:
            cat_id = self.function_8(cat)
            self.update_article(tup=(code, des, cat_id, pv, stockmin, envente, 1, art_id))

            tup = (datetime.now(), 'édition', 'article', code, des, cat)
            self.insert_trace(tup)

            self.enregistrer()
            return code

        else:
            return False

    def record_34(self, **kw):

        non_id = kw['non_id']
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        cat = kw['cat'].get().strip()

        com = ''
        cat_id = self.function_8(cat)

        if not code:
            com = "ERREUR code (vide)"
        elif not code.isalnum():
            com = "ERREUR code (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR code (limite = " + str(l_code) + " caractères)"
        elif code in self.function_28() and self.function_5(code) != non_id:
            com = "ERREUR code (déjà utilisé)"
        elif not cat:
            com = "ERREUR catégorie (vide)"
        elif not cat_id:
            com = "ERREUR catégorie (inexistante)"
        elif not des:
            com = "ERREUR désignation (vide)"
        elif len(des) > l_des:
            com = "ERREUR désignation (limite = " + str(l_des) + " caractères)"
        kw['comment'].set(com)

        if not com:
            self.update_article(tup=(code, des, cat_id, None, None, 0, 0, non_id))
            tup = (datetime.now(), 'édition', 'article', code, des, cat)
            self.insert_trace(tup)
            self.enregistrer()
            return True
        else:
            return False

    def record_18(self, **kw):

        if self.exercice != date.today().year:
            com = "ERREUR exercice (non actuel)"
            kw['comment'].set(com)
            return False

        code = kw['code'].get()
        th = kw['theorique'].get().strip().replace(',', '.')
        ph = kw['physique'].get().strip().replace(',', '.')
        expl = kw['explication'].get().strip()

        if not func_10(ph):
            com = 'ERREUR stock physique (non conforme)'
            kw['comment'].set(com)
            return False

        ph = round(float(ph), 2)

        art_id = self.function_2(code)
        self.insert_correction(tup=(art_id, th, ph, datetime.now(), expl))

        tup = (datetime.now(), 'correction', code, 'théorique: ' + func_6(th),
               'physique: ' + func_6(ph), '')
        self.insert_trace(tup)

        self.enregistrer()
        return True

    def record_25(self, **kw):

        arg = kw['arg']
        code = kw['code'].get().strip()

        cat_id = self.function_8(arg)

        com = ''

        if not code:
            com = "ERREUR nom (vide)"
        elif not code.isalnum():
            com = "ERREUR nom (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR nom (limite = " + str(l_code) + " caractères)"
        elif self.function_8(code) and self.function_8(code) != cat_id:
            com = "ERREUR nom (déjà utilisé)"

        kw['comment'].set(com)

        if not com:
            self.update_categorie(tup=(code, cat_id))
            return True

        else:
            return False

    def erase_25(self, **kw):

        arg = kw['arg']
        code = kw['code'].get().strip()

        cat_id = self.function_8(code)

        com = ''

        if not code:
            com = "ERREUR catégorie (vide)"
        elif not cat_id:
            com = "ERREUR catégorie (inexistante)"
        elif self.function_47(code):
            com = "ERREUR catégorie (contient des articles)"

        kw['comment'].set(com)

        if not com:
            self.curseur.execute("""DELETE FROM fixecat WHERE cat_id=?""", (cat_id,))
            self.curseur.execute("""DELETE FROM categorie WHERE cat_id=?""", (cat_id,))    
            self.enregistrer()
            return True
        else:
            return False

    def record_37(self, **kw):

        arg = kw['arg']
        code = kw['code'].get().strip()

        cat_id = self.function_30(arg)

        com = ''

        if not code:
            com = "ERREUR nom (vide)"
        elif not code.isalnum():
            com = "ERREUR nom (non alphanumérique)"
        elif len(code) > l_type:
            com = "ERREUR nom (limite = " + str(l_type) + " caractères)"
        elif self.function_30(code) and self.function_30(code) != cat_id:
            com = "ERREUR code (déjà utilisé)"

        kw['comment'].set(com)

        if not com:
            self.update_type(tup=(code, cat_id))
            return True

        else:
            return False

    def record_26(self, **kw):

        arg = kw['arg']
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()

        tiers_id = self.function_9(arg)
        code_id = self.function_9(code)

        com = ''

        if not code:
            com = "ERREUR nom (vide)"

        elif len(code) > l_code:
            com = "ERREUR nom (limite = " + str(l_code) + " caractères)"
        elif (code_id != tiers_id) and code_id:
            com = "ERREUR nom (déjà utilisé)"

        kw['comment'].set(com)

        if not com:
            self.update_tiers(tup=(code, des, tiers_id))
            return True

        else:
            return False

    def record_29(self, **kw):

        arg = kw['arg']
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()

        worker_id = self.function_12(arg)
        code_id = self.function_12(code)

        com = ''

        if not code:
            com = "ERREUR nom (vide)"

        elif len(code) > l_code:
            com = "ERREUR nom (limite = " + str(l_code) + " caractères)"
        elif (code_id != worker_id) and code_id:
            com = "ERREUR nom (déjà utilisé)"

        kw['comment'].set(com)

        if not com:
            self.update_workers(tup=(code, des, worker_id))
            return True

        else:
            return False

    def record_23(self, **kw):

        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        cat = kw['cat'].get().strip()
        pv = kw['pv'].get().strip()
        code_i = kw['code_i'].get().strip()
        des_i = kw['des_i'].get().strip()
        proportion = kw['proportion'].get().strip()
        envente = kw['envente'].get()
        list_ref = kw['list_ref']

        com = ''

        # test du code
        if not code:
            com = "ERREUR code (vide)"
        elif not code.isalnum():
            com = "ERREUR code (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR code (limite = " + str(l_code) + " caractères)"
        elif code in self.function_28():
            com = "ERREUR code (déjà utilisé)"

        # test des
        elif not des:
            com = "ERREUR désignation (vide)"
        elif len(des) > l_des:
            com = "ERREUR désignation (limite = " + str(l_des) + " caractères)"

        # test de la catégorie
        elif not self.function_8(cat):
            com = "ERREUR catégorie (inconnue)"

        # test du prix de vente

        elif not func_2(pv):
            com = "ERREUR prix de vente"

        # test de la composition
        elif not list_ref:
            com = 'ERREUR : composition (vide)'

        elif code_i or des_i or proportion:
            com = "ERREUR composition (zone d'encodage non vide)"

        # enregistrement dans la base si pas d'erreurs
        kw['comment'].set(com)
        if com:
            return False
        else:
            # insertion du compose
            cat_id = self.function_8(cat)
            self.insert_article((code, des, cat_id, pv, None, envente, 2))

            # insertion des composants
            dat = datetime.now()
            for dico in list_ref:
                compo_id = self.function_5(code)
                proportion = dico['proportion']
                self.insert_composition(tup=(compo_id, self.function_5(dico['code']), proportion, dat))

            # enregistrement
            tup = (datetime.now(), 'ajout', 'article', code, des, cat)
            self.insert_trace(tup)

            self.enregistrer()
            return code

    def record_24(self, **kw):

        compo_id = kw['compo_id']
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        cat = kw['cat'].get().strip()
        pv = kw['pv'].get().strip()
        code_i = kw['code_i'].get().strip()
        des_i = kw['des_i'].get().strip()
        proportion = kw['proportion'].get().strip()
        envente = kw['envente'].get()
        list_ref = kw['list_ref']

        com = ''

        # test du code
        if not code:
            com = "ERREUR code (vide)"
        elif not code.isalnum():
            com = "ERREUR code (non alphanumérique)"
        elif len(code) > l_code:
            com = "ERREUR code (limite = " + str(l_code) + " caractères)"
        elif code in self.function_28() and self.function_5(code) != compo_id:
            com = "ERREUR code (déjà utilisé)"

        # test des
        elif not des:
            com = "ERREUR désignation (vide)"
        elif len(des) > l_des:
            com = "ERREUR désignation (limite = " + str(l_des) + " caractères)"

        # test de la catégorie
        elif not self.function_8(cat):
            com = "ERREUR catégorie (inconnue)"

        # test du prix de vente
        elif not func_2(pv):
            com = "ERREUR prix de vente (non entier positif)"

        # test de la composition
        elif not list_ref:
            com = 'ERREUR composition (vide)'

        elif code_i or des_i or proportion:
            com = "ERREUR composition (zone d'encodage non vide)"

        # enregistrement dans la base si pas d'erreurs
        kw['comment'].set(com)
        if com:
            return False
        else:
            # update du compose
            cat_id = self.function_8(cat)
            self.update_article((code, des, cat_id, pv, None, envente, 2, compo_id))

            # insertion des composants
            dat = datetime.now()
            for dico in list_ref:
                compo_id = self.function_5(code)
                proportion = dico['proportion']
                self.insert_composition(tup=(compo_id, self.function_5(dico['code']), proportion, dat))

            tup = (datetime.now(), 'édition', 'article', code, des, cat)
            self.insert_trace(tup)
            self.enregistrer()
            return code

    def record_27(self, **kw):

        arg = kw['arg']
        num = kw['num'].get().strip()
        dat = kw['dat'].get().strip()
        d = func_7(dat)
        tiers = kw['tiers'].get().strip()
        remise = kw['remise'].get().strip().replace('.', '')
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        qte = kw['qte'].get().strip()
        prix = kw['prix'].get().strip()

        list_box = kw['list_box']
        list_ref = kw['list_ref']

        com = ''

        num_id = self.function_10b(num)
        n_prim = self.function_34b(num)

        if not d:
            com = 'ERREUR date (non conforme)'
        elif d.year != self.exercice:
            com = "ERREUR date (année incorrecte)"
        elif not num:
            com = 'ERREUR n°pièce (vide)'
        elif not arg and (num_id or n_prim):
            com = 'ERREUR n°pièce (déjà utilisé)'
        elif arg and not ((num_id == arg or not num_id) and not n_prim):
            com = 'ERREUR n°pièce (déjà utilisé)'
        elif not tiers:
            com = 'ERREUR tiers (vide)'
        elif not self.function_9(tiers):
            com = 'ERREUR tiers (inconnu)'
        elif not func_2(remise):
            com = 'ERREUR remise (non conforme)'
        elif code or des or qte or prix:
            com = "ERREUR zone d'encodage article (non vide)"
        elif not list_box:
            com = "ERREUR liste d'achat (vide)"

        kw['comment'].set(com)

        if com:
            return None

        # mise en forme et valeur de la remise

        if remise:
            remise = int(remise)
            kw['remise'].set(func_5(remise))
        else:
            remise = 0

        # calcul du total
        tot = 0
        for dico in list_ref:
            tot += int(dico['prix'])

        tot = tot - func_4(remise)
        kw['total'].set(func_5(tot))

        if tot < 0:
            com = 'ERREUR total (négatif)'
            kw['comment'].set(com)
            return None

        # enregistrement de la facture d'achat
        tup = (num, self.function_9(tiers), d, remise, tot)
        if arg:
            self.update_factureA(tup + (arg,))
        else:
            self.insert_factureA(tup)

        # détermination de fact_id
        if not arg:
            fact_id = self.function_10b(num)
        else:
            fact_id = arg

        # suppression dans la bas des enregistrements
        chaine = """DELETE FROM recordA WHERE fact_id=?"""
        self.curseur.execute(chaine, (fact_id,))

        # enregistrement des articles de la liste
        for dico in list_ref:
            self.insert_recordA(
                tup=(fact_id, self.function_5(dico['code']), dico['qte'].replace(',', '.'), dico['prix']))
        if not arg:
            t = 'ajout'
        else:
            t = 'édition'
        tup = (datetime.now(), t, 'achat ' + num, tiers, 'total: ' + str(tot), dat)
        self.insert_trace(tup)

        self.enregistrer()

        return fact_id

    def record_15(self, **kw):

        arg = kw['arg']
        dat = kw['dat'].get().strip()
        d = func_7(dat)
        caisse = kw['caisse'].get().strip()
        code = kw['code'].get().strip()
        des = kw['des'].get().strip()
        qte = kw['qte'].get().strip()
        prix = kw['prix'].get().strip()

        list_box = kw['list_box']
        list_ref = kw['list_ref']

        com = ''
        dat_id = self.function_73(d)

        if not d:
            com = 'ERREUR date (non conforme)'
        elif d.year != self.exercice:
            com = "ERREUR date (année incorrecte)"
        elif not arg and self.function_73(d):
            com = "ERREUR date (déjà existante)"
        elif arg and dat_id and arg != dat_id:
            com = "ERREUR date (déjà existante)"
        elif not caisse:
            com = 'ERREUR caissier(ère) (vide)'
        elif not self.function_12(caisse):
            com = 'ERREUR caissier(ère) (inconnu(e))'
        elif code or des or qte or prix:
            com = "ERREUR zone d'encodage article (non vide)"
        elif not list_box:
            com = "ERREUR liste de vente (vide)"

        kw['comment'].set(com)

        if com:
            return False

        # mise en forme et valeur de la remise

        # calcul du total

        tot = 0
        for dico in list_ref:
            tot += int(dico['prix'])

        kw['total'].set(func_5(tot))

        if tot < 0:
            com = 'ERREUR total (négatif)'
            kw['comment'].set(com)
            return False

        # enregistrement de la facture de vente

        tup = (d, self.function_12(caisse), tot)

        if arg:
            self.update_vente(tup + (arg,))
            vente_id = arg
            # suppression des enregistrements
            chaine = """DELETE FROM recordV WHERE vente_id=?"""
            self.curseur.execute(chaine, (vente_id,))
        else:
            vente_id = self.insert_vente(tup)

        # enregistrement des articles de la liste

        for dico in list_ref:
            art_id = self.function_5(dico['code'])
            # vérification qu'un composé possède des composants à la date d
            if self.function_7(art_id):
                if not self.function_40(art_id, d):
                    com = "ERREUR " + dico['code'] + " non défini à cette date"
                    break
            self.insert_recordV(tup=(vente_id,
                                     art_id,
                                     dico['qte'].replace(',', '.'),
                                     dico['prix']))
        if com:
            kw['comment'].set(com)
            self.fermer()
            self.ouvrir()
            return False

        # traçage de l'enregistrement
        if not arg:
            t = 'ajout'
        else:
            t = 'édition'
        tup = (datetime.now(), t, 'vente', caisse, 'total: ' + str(tot), dat)
        self.insert_trace(tup)

        # enregistrement dans la DB
        self.enregistrer()

        # vente_id est NOT NULL
        return vente_id

    def record_39(self, **kw):

        arg = kw['arg']
        explication = kw['explication'].get().strip()

        if len(explication) > l_explication:
            kw["comment"].set('ERREUR explication (limite = ' + str(l_explication) + ' caractères)')
            return False
        else:
            try:
                chaine = """UPDATE correction
                            SET explication=?
                            WHERE corr_id=?"""
                self.curseur.execute(chaine, (explication, arg))
                self.enregistrer()

            except sqlite3.Error as error:
                kw['comment'].set(error)
                return False

            else:
                return True

    def record_44(self, **kw):
        p = kw['p']
        comment = kw['comment']
        com = ''
        for jour in range(7):
            if not func_1(p[jour].get().strip()):
                com = "ERREUR pondération"
        comment.set(com)

        if not com:
            for jour in range(7):
                weighting = p[jour].get().strip()
                self.update_ponderation(tup=(weighting, jour))
            self.enregistrer()
            comment.set('OK')
            return True
        else:
            return False

    def record_45(self, **kw):
        p = kw['p']
        print(p)    
        comment = kw['comment']
        com = ''
        
        # test 
        for jour in range(7):
            if not func_2(p[jour].get().strip()):
                com = "ERREUR prix non conforme"
        comment.set(com)

        if not com:
            # update 
            for jour in range(7):
                limite = p[jour].get().strip()
                if limite == '':
                    limite = None
                self.update_limitation(tup=(limite, jour))
            self.enregistrer()
            comment.set('OK')
            return True
        else:
            return False

    def record_14(self, **kw):
        arg = kw['arg']
        num = kw['num'].get().strip()
        type = kw['type'].get().strip()
        tiers = kw['tiers'].get().strip()
        des = kw['des'].get().strip()
        montant = kw['montant'].get().strip()
        amor = kw['amor'].get()
        repart = kw['repart'].get()
        mois = kw['mois'].get().strip()

        d = func_7(kw['dat'].get().strip())
        n = self.function_34b(num)  # n est l'id de la charge corresondant à num
        n_prim = self.function_10b(num)  # n' est l'id de la factureA correspondant à num

        ty = self.function_30(type)
        ti = self.function_9(tiers)
        debut = func_7(kw['debut'].get().strip())

        comment = kw['comment']
        com = ''

        if not d:
            com = 'ERREUR date (non conforme)'
        elif not num:
            com = 'ERREUR N° PIÈCE (vide)'
        elif len(num) > l_num:
            com = 'ERREUR N° PIÈCE (limite = ' + str(l_num) + ' caractères)'
        elif not arg and (n or n_prim):
            com = 'ERREUR N° PIÈCE (déjà utilisé)'
        elif arg and not ((n == arg or not n) and not n_prim):
            print('arg', arg, 'n', n, 'nprim', n_prim)
            com = 'ERREUR N° PIÈCE (déjà utilisé)'
        elif not montant:
            com = "ERREUR montant (vide)"
        elif not func_1(montant):
            com = "ERREUR montant(non conforme)"
        elif not type:
            com = 'ERREUR type (vide)'
        elif not ty:
            com = 'ERREUR type (inconnu)'
        elif not tiers:
            com = 'ERREUR tiers (vide)'
        elif not ti:
            com = 'ERREUR tiers (inconnu)'
        elif not des:
            com = 'ERREUR description (vide)'
        elif amor or repart:
            if not debut:
                com = 'ERREUR date de début (non conforme)'
            elif debut.day not in {1, 15}:
                com = 'ERREUR date de début (accepté : le 1er ou le 15)'
            elif not func_13(mois):
                com = 'ERREUR #mois (non conforme)'
        comment.set(com)
        if com:
            return None
        if amor:
            dif = ('A', debut, mois)
        elif repart:
            dif = ('R', debut, mois)
        else:
            dif = ('', None, None)
        if arg:
            self.update_charge(tup=(d, num, ty, ti, des, montant, dif[0], dif[1], dif[2], arg))
        else:
            charge_id = self.insert_charge(tup=(d, num, ty, ti, des, montant, dif[0], dif[1], dif[2]))

        if not arg:
            t = 'ajout'
        else:
            t = 'édition'

        tup = (datetime.now(), t, 'charge ' + num, tiers, 'montant: ' + str(montant), func_8(d))
        self.insert_trace(tup)
        self.enregistrer()

        if not arg:
            return charge_id
        else:
            return arg

    def record_38(self, **kw):

        arg = kw['arg']
        comment = kw['comment']
        com = ''
        comment.set(com)

        if arg == 'PARTAGE':
            partage = kw['partage'].get().strip()
            if not isdir(partage):
                com = 'ERREUR répertoire de partage (non conforme)'
                comment.set(com)
            else:
                dst = join(partage, self.database + '.db')
                comment.set('Partage en cours...')
                src = self.database_path
                try:
                    shutil.copyfile(src, dst)
                except shutil.Error as com:
                    comment.set(com)
                else:
                    comment.set('Partage effectué')
                    if kw['def_partage'].get():
                        try:
                            with open(f_partage, 'w', encoding='utf-8') as f:
                                f.write(partage)
                        except OSError as com:
                            comment.set(com)

        else:
            # sauvegarde
            sauvegarde = kw['sauvegarde'].get().strip()

            if not isdir(sauvegarde):
                com = 'ERREUR répertoire de sauvegarde (non conforme)'
                comment.set(com)
            else:
                dst = join(sauvegarde,
                           datetime.strftime(datetime.now(), "%Y%m%d") + self.database + '.db')
                comment.set('Sauvegarde en cours...')
                src = self.database_path
                try:
                    shutil.copyfile(src, dst)
                except shutil.Error as com:
                    comment.set(com)
                else:
                    comment.set('Sauvegarde effectuée')
                    if kw['def_sauvegarde'].get():
                        try:
                            with open(f_sauvegarde, 'w', encoding='utf-8') as f:
                                f.write(sauvegarde)
                        except OSError as com:
                            comment.set(com)
        if com:
            return False
        else:
            return True

    def ticket(self, dat, caissier, dicoVente, nomF, total):

        etoile = '*' * 31
        NomBar = ' T G V   L O U N G E   B A R '
        tiret = '-' * 31
        barre = "_" * 31

        dicoVenteTrie = OrderedDict(sorted(dicoVente.items(), key=lambda t: t[0]))
        print(dicoVente, dicoVenteTrie)

        with open(nomF, 'w', encoding='utf-8') as fichier:

            fichier.write('{:^31}'.format(etoile))
            fichier.write('\n{:^31}'.format(NomBar))
            fichier.write('\n{:^31}'.format(etoile))
            fichier.write('\n\n' + '{:^31}'.format('TICKET DE CLOTURE'))
            fichier.write('\n' + barre + '\n')

            nbr = randrange(3)
            signe = randrange(2) * 2 - 1

            if nbr:
                totalM = signe * randrange(12) * 1000
            else:
                totalM = 0

            nbr = str(nbr)
            totalM = '{:+,}'.format(totalM).replace(',', '.')
            fichier.write('\n' + '{:^31}'.format(nbr + ' FACT.MODIF.: ' + totalM))
            fichier.write('\n' + barre + '\n')
            # total = 0
            if dicoVente:
                fichier.write('\n{:<16}{:^3}{:>12}'.format('  REF', 'QTE', 'TTC  ') + '\n')
                for cle, valeur in dicoVenteTrie.items():
                    print(cle, valeur)
                    quant = int(float(valeur['QUANT']))
                    quant = '{:,}'.format(quant).replace(',', '.')
                    prix = int(float(valeur['PRIX']))
                    # total += prix
                    prix = '{:,}'.format(prix).replace(',', '.')
                    fichier.write('\n{:16}{:>3}{:>12}'.format(cle[:15], quant, prix))
                fichier.write('\n' + tiret)
            total = '{:,}'.format(total).replace(',', '.')
            fichier.write('\n' + '  {:>17}{:>12}'.format('TOTAL TTC ', total.strip()))
            fichier.write('\n' + tiret)
            fichier.write('\n' + '{:^31}'.format('Caisse : ' + caissier.capitalize()))
            # date sous format 2019-11-09 21:49:12
            datum = dat[8:10] + '/' + dat[5:7] + '/' + dat[0:4] + '   ' + dat[11:16]
            fichier.write('\n' + '{:^31}'.format(datum))

    def document_54(self, **kw):
        # variables
        repertoire = kw['repertoire'].get().strip()
        d_i = func_7(kw['d_i'].get().strip())
        d_f = func_7(kw['d_f'].get().strip())
        def_rep = kw['def_rep']
        comment = kw['comment']
        comment.set('')

        # test
        year = self.exercice
        com = ''
        if not isdir(repertoire):
            com = 'ERREUR répertoire-cible (non conforme)'
        elif not (d_i and d_f):
            com = "ERREUR date (non conforme)"
        elif d_f < d_i:
            com = "ERREUR date (non conforme)"
        elif d_f.year != year or d_f.year != year:
            com = "ERREUR date (année non conforme)"
        comment.set(com)
        if com:
            return False

        if def_rep.get():
            with open(f_ticket, 'w', encoding='utf-8') as fichier:
                fichier.write(repertoire)

        # fabrication des tickets txt
        jour = d_i
        while jour <= d_f:
            # récupération de la vente éventuelle à la date j, du caissier et du total
            chaine = """SELECT vente_id, caisse_id, total
                        FROM vente
                        WHERE dat=?"""
            result = self.curseur.execute(chaine, (jour,)).fetchone()
            if result:
                vente_id, caisse_id, total = result
                caissier = self.function_14(caisse_id)
            else:
                jour += timedelta(days=1)
                continue

            # création du dicoVente
            chaine = """SELECT codeV_id, qte, prix
                        FROM recordV
                        WHERE vente_id = ?"""
            result = self.curseur.execute(chaine, (vente_id,)).fetchall()
            dicoVente = dict()
            if result:
                for tup in result:
                    code = self.function_29(tup[0])
                    qte = tup[1]
                    prix = tup[2]
                    dicoVente[code] = dict(QUANT=qte, PRIX=prix)

            # fabrication de la date de cloture
            if jour.weekday() in {4, 5}:
                h = '0' + str(randint(5, 6))
            else:
                h = '0' + str(randint(3, 5))
            m = randrange(60)
            if m < 10:
                m = '0' + str(m)
            else:
                m = str(m)
            d = datetime.strftime(jour + timedelta(days=1), "%Y-%m-%d")
            dat = d + ' ' + h + ':' + m

            # création du ticket
            d = datetime.strftime(jour, "%Y-%m-%d")
            self.ticket(dat, caissier, dicoVente, join(repertoire, d + ' TICKET'), total)

            # répétition de la boucle
            jour += timedelta(days=1)

    def action_49(self, **kw):
        comment = kw['comment']
        comment.set('')
        com = ''

        importe = kw['importe'].get().strip()
        nom = kw['nom'].get().strip()

        src = join(importe, nom + '.db')
        if not isdir(importe):
            com = "ERREUR répertoire-source (non conforme)"
            comment.set(com)
        elif not nom:
            com = "ERREUR nom (vide)"
        elif not nom.isalnum():
            com = "ERREUR nom (non alphanumérique)"

        elif not isfile(src):
            com = "ERREUR nom (introuvable)"

        elif len(nom) > l_base:
            com = 'ERREUR nom (limite : ' + str(l_base) + ' caractères'
        comment.set(com)

        if com:
            return False
        else:
            dst = join(getcwd(), 'BASE')

            if kw['def_importe'].get():
                try:
                    with open(f_dirImport, 'w', encoding='utf-8') as f:
                        f.write(importe)
                except OSError as com:
                    comment.set(com)
                    return False

            if kw['def_nom'].get():
                try:
                    with open(f_nameImport, 'w', encoding='utf-8') as f:
                        f.write(nom)
                except OSError as com:
                    comment.set(com)
                    return False
            try:
                comment.set('Importation en cours...')
                shutil.copy2(src, dst)
            except shutil.Error as com:
                comment.set(com)
                return False
            else:
                self.fix_database(nom)
                return True

    def action_58(self, **kw):

        # récupération des variables
        comment = kw['comment']
        importe = kw['importe'].get().strip()
        nom = kw['nom'].get().strip()
        com = ''
        comment.set(com)

        # importation
        src = join(importe, nom + '.csv')
        if not isdir(importe):
            com = "ERREUR répertoire-source (non conforme)"
            comment.set(com)
        elif not nom:
            com = "ERREUR nom (vide)"
        elif not isfile(src):
            com = "ERREUR nom (incorrect)"
        comment.set(com)
        if com:
            return False
        else:
            if kw['def_importe'].get():
                try:
                    with open(f_dirImportVente, 'w', encoding='utf-8') as f:
                        f.write(importe)
                except OSError as com:
                    comment.set(com)
                    return False
            try:
                comment.set('Importation en cours...')
                # lire le fichier csv
                with open(src, 'r', newline='', encoding='utf-8') as f:
                    fi = csv.DictReader(f, fieldnames=['code', 'qte', 'prix'])
                    liste = [dico for dico in fi]
            except csv.Error as com:
                comment.set(com)
                return False

            ## vérification du fichier
            if len(liste) == 0:
                com = "Erreur fichier (vide)"
                comment.set(com)
                return False

            # liste0 : date et caissier et total
            dat = liste[0]['code'].strip()
            d = func_7(dat)
            caissier = liste[0]['qte'].strip()
            caisse_id = self.function_12(caissier)
            total = liste[0]['prix'].strip()

            if not d:
                com = 'ERREUR fichier (date non conforme)'
            elif d.year != self.exercice:
                com = 'ERREUR fichier (année non conforme)'
            elif not caisse_id:
                com = 'ERREUR fichier (caissier(ère) inconnu)'
            elif not func_1(total):
                com = 'ERREUR fichier (total non conforme)'

            if com:
                comment.set(com)
                return False
            del liste[0]

            # code, qte, prix
            tt = 0
            for dico in liste:
                code, qte, prix = dico.values()
                if not code:
                    com = 'ERREUR fichier (code vide)'
                elif not self.function_5(code):
                    com = "ERREUR fichier (code '" + code + "' inconnu)"
                elif not self.function_20(code):
                    com = "ERREUR fichier (code '" + code + "' pas en vente)"
                elif not func_3(qte):
                    com = "ERREUR fichier (quantité '" + qte + "' non conforme)"
                elif not func_1(prix):
                    com = "ERREUR fichier (prix '" + prix + "' non conforme)"
                if com:
                    break
                tt += int(prix)

            if com:
                comment.set(com)
                return False

            if tt != int(total):
                com = "ERREUR fichier (total inexact)"
                comment.set(com)
                return False

            ## enregistrement de la vente
            # suppression de la vente éventuelle à cette date
            chaine = """SELECT vente_id FROM vente WHERE dat=?"""
            result = self.curseur.execute(chaine, (d,)).fetchone()
            if result:
                vente_id = result[0]
                chaine = """DELETE FROM recordV WHERE vente_id=?"""
                self.curseur.execute(chaine, (vente_id,))
                chaine = """DELETE FROM vente WHERE vente_id=?"""
                self.curseur.execute(chaine, (vente_id,))

            # enregistrement
            vente_id = self.insert_vente(tup=(d, caisse_id, int(total)))
            for dico in liste:
                code, qte, prix = dico.values()
                self.insert_recordV(tup=(vente_id, self.function_5(code), float(qte), int(prix)))

            # traçage de l'enregistrement
            tup = (datetime.now(), 'import', 'vente', caissier, 'total: ' + str(total), dat)
            self.insert_trace(tup)

            self.enregistrer()
            comment.set('Importation effectuée')
            return vente_id

    def action_50(self, **kw):
        comment = kw['comment']
        comment.set('')
        com = ''

        name = kw['name'].get().strip()
        director = join(getcwd(), 'BASE')
        old = self.database_path
        new = join(director, name + '.db')

        if not name:
            com = "ERREUR nom (vide)"
        elif not name.isalnum():
            com = "ERREUR nom (non alphanumérique)"
        elif len(name) > l_baseC:
            com = "ERREUR nom (limite : " + str(l_baseC) + " caractères"
        elif name + '.db' in listdir(director):
            com = "ERREUR nom (déjà existant)"
        comment.set(com)
        if com:
            return False
        else:
            try:
                rename(old, new)
                with open(f_base, 'w', encoding='utf-8') as f:
                    f.write(name)
            except OSError as com:
                comment.set(com)
                return False
            else:
                self.fix_database(name)
                return True

    def document_52(self, **kw):
        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']

        com = ''

        year = self.exercice

        if not isdir(path):
            com = "ERREUR répertoire"

        comment.set(com)
        if com:
            return False
        else:
            f = join(path, filename + '.csv')
            com = func_12(x=self.function_67(), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def select_23(self, **kw):
        # ne concerne pas le code 23
        list_ref = kw['list_ref']
        indice = kw['indice']

        art_id = self.function_2(list_ref[indice]['code'])

        chaine = """SELECT rec_id, art_id, component_id, proportion 
                       FROM composition
                       WHERE rec_id=?"""

        result = self.curseur.execute(chaine, (rec_id,)).fetchone()

        code = self.set(result[0])
        kw['code'].set(code)
        kw['des'].set(self.function_3(code))
        kw['qte'].set(result[1])
        kw['prix'].set(result[2])

        del list_box[indice]
        del list_rec_id[indice]
        var_box.set(list_box)
        chaine = """DELETE FROM recordA where rec_id=?"""
        self.curseur.execute(chaine, (rec_id,))

        tot = self.total_factureA(fact_id, remise)
        chaine = """UPDATE  factureA  SET total=?  WHERE fact_id=?"""
        self.curseur.execute(chaine, (tot, fact_id))
        total.set(tot)

    def select_24(self, **kw):

        list_ref = kw['list_ref']
        list_box = kw['list_box']
        indice = kw['indice']

        code_i, proportion = list_ref[indice]['code'], list_ref[indice]['proportion']
        kw['code_i'].set(code_i)
        kw['des_i'].set(self.function_3(code_i))
        kw['proportion'].set(proportion)

        del list_box[indice]
        del list_ref[indice]
        kw['var_box'].set(list_box)

    def select_27(self, **kw):

        list_ref = kw['list_ref']
        list_box = kw['list_box']
        total = kw['total'].get().replace('.', '')
        indice = kw['indice']

        code, qte, prix = list_ref[indice]['code'], list_ref[indice]['qte'], list_ref[indice]['prix']
        kw['code'].set(code)
        kw['des'].set(self.function_3(code))
        kw['qte'].set(qte)
        kw['prix'].set(prix)

        del list_box[indice]
        del list_ref[indice]
        kw['var_box'].set(list_box)

        # calcul du total
        kw['total'].set(func_5(int(total) - int(prix)))

    def list_22(self, **kw):

        code_entry = kw['code'].get().strip()
        chaine = """SELECT code 
                    FROM article 
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (2,)).fetchall()

        li_code = list_code = []
        if result:

            for c in result:
                code = c[0]

                if not code_entry:
                    li_code.append(code)
                    continue

                length = len(code_entry)
                if len(code) < length:
                    continue

                if code[0:length] == code_entry:
                    li_code.append(code)

            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]

        kw['list_box'].clear()
        kw['list_box'] += list_code
        kw['var_box'].set(list_code)

        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)

        return len(list_code)

    def list_6(self, **kw):
        code_entry = kw['code'].get().strip()
        chaine = """SELECT name FROM categorie"""
        result = self.curseur.execute(chaine).fetchall()
        li_code = list_code = []
        if result:

            for c in result:
                code = c[0]

                if not code_entry:
                    li_code.append(code)
                    continue

                length = len(code_entry)
                if len(code) < length:
                    continue

                if code[0:length] == code_entry:
                    li_code.append(code)
            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]
        kw['list_box'].clear()
        kw['list_box'] += list_code
        kw['var_box'].set(list_code)
        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)
        return len(list_code)

    def list_35(self, **kw):
        code_entry = kw['code'].get().strip()
        chaine = """SELECT name FROM type"""
        result = self.curseur.execute(chaine).fetchall()
        li_code = list_code = []

        if result:
            for c in result:
                code = c[0]

                if not code_entry:
                    li_code.append(code)
                    continue

                length = len(code_entry)
                if len(code) < length:
                    continue

                if code[0:length] == code_entry:
                    li_code.append(code)
            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]

        kw['list_box'].clear()
        kw['list_box'] += list_code
        kw['var_box'].set(list_code)

        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)
        return len(list_code)

    def list_10(self, **kw):

        list_box = kw['list_box']
        list_box.clear()
        var_box = kw['var_box']
        box = kw['box']

        code_entry = kw['code'].get().strip()
        chaine = """SELECT code 
                    FROM article
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (1,)).fetchall()
        li_code = list_code = []

        if result:
            for c in result:
                code = c[0]
                if not code_entry:
                    li_code.append(code)
                    continue
                length = len(code_entry)
                if len(code) < length:
                    continue
                if code[0:length] == code_entry:
                    li_code.append(code)
            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]

        list_box += list_code
        var_box.set(list_code)

        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            box.selection_clear(0, END)
            box.selection_set(indice)

        return len(list_code)

    def list_32(self, **kw):

        code_entry = kw['code'].get().strip()
        chaine = """SELECT code 
                    FROM article
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (0,)).fetchall()
        li_code = list_code = []
        if result:

            for c in result:
                code = c[0]

                if not code_entry:
                    li_code.append(code)
                    continue

                length = len(code_entry)
                if len(code) < length:
                    continue

                if code[0:length] == code_entry:
                    li_code.append(code)
            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]

        kw['list_box'].clear()
        kw['list_box'] += list_code
        kw['var_box'].set(list_code)

        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)

        return len(list_code)

    def list_5(self, **kw):

        code_entry = kw['code'].get().strip()
        chaine = """SELECT nom FROM tiers"""
        result = self.curseur.execute(chaine).fetchall()
        li_code = list_code = []
        if result:

            for c in result:
                code = c[0]

                if not code_entry:
                    li_code.append(code)
                    continue

                length = len(code_entry)
                if len(code) < length:
                    continue

                if code[0:length] == code_entry:
                    li_code.append(code)
            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]

        kw['list_box'].clear()
        kw['list_box'] += list_code
        kw['var_box'].set(list_code)
        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)
        return len(list_code)

    def list_13(self, **kw):
        code_entry = kw['code'].get().strip()
        chaine = """SELECT nom FROM workers"""
        result = self.curseur.execute(chaine).fetchall()

        li_code = list_code = []
        if result:
            for c in result:
                code = c[0]

                if not code_entry:
                    li_code.append(code)
                    continue

                length = len(code_entry)
                if len(code) < length:
                    continue

                if code[0:length] == code_entry:
                    li_code.append(code)
            li_code.sort()
            list_code = [' {}'.format(x) for x in li_code]

        kw['list_box'].clear()
        kw['list_box'] += list_code
        kw['var_box'].set(list_code)
        arg = kw['arg']
        if arg:
            indice = li_code.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)
        return len(list_code)

    def list_12(self, **kw):

        list_ref = kw['list_ref']
        list_ref.clear()
        list_box = kw['list_box']
        list_box.clear()
        var_box = kw['var_box']
        filtre = kw['filtre'].get().strip()

        # fabrication de list_ref
        tup = func_14(filtre, self.exercice)
        if tup:
            list_ref += self.function_37(tup)
        else:
            # ajout des factures d'un tiers = filtre (liste vide éventuelle)
            list_ref += self.function_68(filtre)

        # fabrication de la list_box
        for tup in list_ref:
            dat = func_9(tup[0])
            num = tup[2]
            tiers = self.function_11(tup[3])
            total = func_5(tup[4])
            list_box.append(ligne_2.format(dat[:-5], num, tiers, total))
        var_box.set(list_box)

        return len(list_box)

    def list_3(self, **kw):

        list_ref = kw['list_ref']
        list_ref.clear()
        list_box = kw['list_box']
        list_box.clear()
        var_box = kw['var_box']
        filtre = kw['filtre'].get().strip()

        # fabrication de list_ref
        tup = func_14(filtre, self.exercice)
        if tup:
            list_ref += self.function_36(tup)

        # fabrication de la list_box
        for tup in list_ref:
            dat = func_9(tup[0])
            caisse = self.function_14(tup[2])
            total = func_5(tup[3])
            list_box.append(ligne_4.format(dat[:-5], caisse, total))
        var_box.set(list_box)

        """
        arg = kw['arg']

        if arg:
            liste = [e[1] for e in list_ref]
            indice = liste.index(arg)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)
        """
        return len(list_box)

    def list_9(self, **kw):

        list_ref = kw['list_ref']
        list_ref.clear()
        list_box = kw['list_box']
        list_box.clear()
        var_box = kw['var_box']
        filtre = kw['filtre'].get().strip()

        # fabrication de list_ref
        tup = func_14(filtre, self.exercice)
        if tup:
            list_ref += self.function_38(tup)
        else:
            # autre filtre : tiers, type, A ou R
            list_ref += self.function_69(filtre)

        for tup in list_ref:
            dat = func_9(tup[0])
            charge_id = tup[1]
            num = tup[2]
            type = self.function_31(tup[3])
            tiers = self.function_11(tup[4])
            montant = func_5(tup[6])
            dif = tup[7]
            if not dif:
                dif = ' '
                print(dat[:-5], num, type, tiers, montant, dif)
            list_box.append(ligne_3.format(dat[:-5], num, type, tiers, montant, dif))
        var_box.set(list_box)

        arg2 = kw['arg2']
        if arg2 is not None:
            liste = [e[1] for e in list_ref]
            indice = liste.index(arg2)
            kw['box'].selection_clear(0, END)
            kw['box'].selection_set(indice)

        return len(list_box)

    def erase_27(self, arg):
        chaine = """SELECT num, tiers_id, total, dat
                    FROM factureA
                    WHERE fact_id=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()
        num, tiers_id, total, dat = result

        chaine = """DELETE FROM recordA WHERE fact_id=?"""
        self.curseur.execute(chaine, (arg,))
        chaine = """DELETE FROM factureA WHERE fact_id=?"""
        self.curseur.execute(chaine, (arg,))

        tup = (datetime.now(), 'suppression', 'achat ' + num, self.function_11(tiers_id),
               'total: ' + str(total), func_8(dat))
        self.insert_trace(tup)
        self.enregistrer()

    def erase_14(self, arg):
        chaine = """SELECT num, tiers_id, montant, dat
                    FROM charge
                    WHERE charge_id=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()
        num, tiers_id, montant, dat = result

        chaine = """DELETE FROM charge WHERE charge_id=?"""
        self.curseur.execute(chaine, (arg,))

        tup = (datetime.now(), 'suppression', 'charge ' + num, self.function_11(tiers_id),
               'montant: ' + str(montant), func_8(dat))
        self.insert_trace(tup)
        self.enregistrer()

    def erase_15(self, arg):

        if not arg:
            return False

        # récupération d'éléments avant suppression pour traçage
        chaine = """SELECT caisse_id, total, dat
                           FROM vente
                           WHERE vente_id=?"""
        result = self.curseur.execute(chaine, (arg,)).fetchone()
        caisse_id, total, dat = result

        # effacement
        chaine = """DELETE FROM recordV WHERE vente_id=?"""
        self.curseur.execute(chaine, (arg,))
        chaine = """DELETE FROM vente WHERE vente_id=?"""
        self.curseur.execute(chaine, (arg,))

        # traçage
        tup = (datetime.now(), 'suppression', 'vente', self.function_14(caisse_id),
               'total: ' + str(total), func_8(dat))
        self.insert_trace(tup)

        # enregistrement
        self.enregistrer()
        return True

    def document_30(self, **kw):
        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']

        com = ''
        if not isdir(path):
            com = "ERREUR répertoire"

        comment.set(com)
        if com:
            return False
        else:
            f = join(path, filename + '.csv')
            com = func_12(x=self.function_24(), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def document_53(self, **kw):

        filename = kw['filename']
        comment = kw['comment']
        comment.set('')
        f = join('DOCUMENTS', filename)

        try:
            startfile(f)
        except OSError as com:
            comment.set(com)
            return False
        else:
            return True

    def document_42(self, **kw):

        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']

        com = ''
        if not isdir(path):
            com = "ERREUR répertoire"

        comment.set(com)
        if com:
            return False
        else:
            f = join(path, filename + '.csv')
            com = func_12(x=self.function_49(), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def document_43(self, **kw):

        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']
        d_i = func_7(kw['d_i'].get().strip())
        d_f = func_7(kw['d_f'].get().strip())
        com = ''
        year = self.exercice

        if not isdir(path):
            com = "ERREUR répertoire"
        elif not (d_i and d_f):
            com = "ERREUR date (non conforme)"
        elif d_f < d_i:
            com = "ERREUR date (non conforme)"
        elif d_i.year != year or d_f.year != year:
            com = "ERREUR date (année non conforme)"

        comment.set(com)
        if com:
            return False
        else:
            f = join(path, filename + '.csv')
            com = func_12(x=self.function_55(d_i, d_f), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def document_51(self, **kw):

        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']

        com = ''

        year = self.exercice

        if not isdir(path):
            com = "ERREUR répertoire"

        comment.set(com)
        if com:
            return False
        else:
            d_i = datetime(year, 1, 1)
            d_f = datetime(year, 12, 31)
            f = join(path, filename + '.csv')
            com = func_12(x=self.function_55(d_i, d_f, final=" ANNUEL " + str(year)), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def document_31(self, **kw):

        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']

        com = ''
        if not isdir(path):
            com = "ERREUR répertoire"

        comment.set(com)
        if com:
            return False
        else:
            f = join(path, filename + '.csv')
            com = func_12(x=self.function_25(), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def document_59(self, **kw):
        def f_2():
            dicoPaInit = {}
            chaine = """SELECT art_id
                                FROM article
                                WHERE ad=?"""
            result = self.curseur.execute(chaine, (1,)).fetchall()
            if result:
                dat = datetime.now()
                year = self.exercice
                self.fix_exercice(dat.year)
                for tup in result:
                    art_id = tup[0]
                    qInit = self.function_46(art_id, dat)
                    pInit = self.function_43(art_id, dat)
                    dicoPaInit[art_id] = (qInit, pInit)
            self.fix_exercice(year)
            return dicoPaInit

        def f_1():
            v = []
            liste = []
            liste.append(['DONNÉES', self.database])
            liste.append(v)
            liste.append([func_9(date.today())])

            chaine = """SELECT name FROM categorie"""
            result = self.curseur.execute(chaine).fetchall()
            if result:
                liste_categorie = [c[0] for c in result]
                liste_categorie.sort()
            else:
                liste_categorie = []

            if kw['cat'].get():
                liste.append(v)
                liste.append(['catégories'.upper()])
                if liste_categorie:
                    liste += [[c] for c in liste_categorie]

            if kw['inv'].get():
                liste.append(v)
                liste.append(['ARTICLES INVENTORIÉS'])
                if liste_categorie:
                    liste.append(['CODE', 'DÉSIGNATION', 'MIN', 'STOCK', 'PA', '', 'PV'])
                for categorie in liste_categorie:
                    chaine = """SELECT art_id, code, des,  pv, stockmin, envente
                                FROM article
                                WHERE ad=1
                                AND cat_id = ?"""
                    result = self.curseur.execute(chaine, (self.function_8(categorie),)).fetchall()
                    if result:
                        dic = f_2()
                        liste.append([])
                        liste.append([categorie.upper()])
                        l_result = list(result)
                        l_result.sort()
                        for tup in l_result:
                            art_id, code, des, pv, stockmin, envente = tup
                            stock, pa = dic[art_id]
                            liste.append([code, des, stockmin, stock, pa, (lambda k: 'V' if k == 1 else '')(envente), pv])

            if kw['comp'].get():
                liste.append(v)
                liste.append(['ARTICLES COMPOSÉS'])
                if liste_categorie:
                    liste.append(['CODE', 'DÉSIGNATION', '', 'PV', 'COMPOSITION'])
                for categorie in liste_categorie:
                    chaine = """SELECT code, des,  pv, envente
                                FROM article
                                WHERE ad=2
                                AND cat_id = ?"""
                    result = self.curseur.execute(chaine, (self.function_8(categorie),)).fetchall()
                    if result:
                        liste.append([])
                        liste.append([categorie.upper()])
                        l_result = list(result)
                        l_result.sort()
                        for tup in l_result:
                            code, des, pv, envente = tup
                            # ajout des compostions via liste_compo
                            liste_c = self.function_15(self.function_5(code), datetime.now())
                            liste_compo = []
                            if liste_c:
                                for tu in liste_c:
                                    liste_compo += [self.function_6(tu[0]), func_6(tu[1])]
                            liste.append([code, des, (lambda k: 'V' if k == 1 else '')(envente), pv] + liste_compo)

            if kw['non'].get():
                liste.append(v)
                liste.append(['ARTICLES COMPOSÉS'])
                if liste_categorie:
                    liste.append(['CODE', 'DÉSIGNATION'])
                for categorie in liste_categorie:
                    chaine = """SELECT code, des FROM article
                                WHERE ad=0
                                AND cat_id = ?"""
                    result = self.curseur.execute(chaine, (self.function_8(categorie),)).fetchall()
                    if result:
                        liste.append([])
                        liste.append([categorie.upper()])
                        l_result = list(result)
                        l_result.sort()
                        for tup in l_result:
                            code, des = tup
                            liste += [[code, des]]

            if kw['ven'].get():
                liste.append(v)
                liste.append(['ARTICLES EN VENTE'])
                if liste_categorie:
                    liste.append(['CODE', 'DÉSIGNATION', 'PV'])
                for categorie in liste_categorie:
                    chaine = """SELECT code, des, pv FROM article
                                WHERE envente=1
                                AND cat_id = ?"""
                    result = self.curseur.execute(chaine, (self.function_8(categorie),)).fetchall()
                    if result:
                        liste.append([])
                        liste.append([categorie.upper()])
                        l_result = list(result)
                        l_result.sort()
                        for tup in l_result:
                            code, des, pv = tup
                            liste += [[code, des, pv]]

            if kw['tie'].get():
                liste.append(v)
                liste.append(['TIERS'])
                chaine = """SELECT nom FROM tiers"""
                result = self.curseur.execute(chaine).fetchall()
                if result:
                    l_result = list(result)
                    l_result.sort()
                    liste += [[t[0]] for t in l_result]

            if kw['emp'].get():
                liste.append(v)
                liste.append(['TIERS'])
                chaine = """SELECT nom FROM workers"""
                result = self.curseur.execute(chaine).fetchall()
                if result:
                    l_result = list(result)
                    l_result.sort()
                    liste += [[t[0]] for t in l_result]

            if kw['typ'].get():
                liste.append(v)
                liste.append(['types de charges'.upper()])
                chaine = """SELECT name FROM type"""
                result = self.curseur.execute(chaine).fetchall()
                if result:
                    l_result = list(result)
                    l_result.sort()
                    liste += [[t[0]] for t in l_result]

            return liste

        path = kw['path'].get().strip()
        filename = kw['filename'].get().strip()
        comment = kw['comment']
        com = ''
        if not isdir(path):
            com = "ERREUR répertoire"

        comment.set(com)
        if com:
            return False
        else:
            f = join(path, filename + '.csv')
            com = func_12(x=f_1(), y=f)
            if com:
                comment.set(com)
                return False
            else:
                startfile(f)
                return True

    def function_1(self):
        chaine = """SELECT art_id 
                    FROM article
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (2,)).fetchall()

        if result:
            return [x[0] for x in result]
        else:
            return []

    def function_2(self, x):
        chaine = """SELECT art_id 
                    FROM article 
                    WHERE code=?
                    AND ad=?"""
        result = self.curseur.execute(chaine, (x, 1)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_3(self, x):

        chaine = """SELECT des 
                        FROM article 
                        WHERE code=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return ''

    def function_4(self, c):

        chaine = """SELECT art_id 
                       FROM article 
                       WHERE code=?
                       AND ad=?"""
        result = self.curseur.execute(chaine, (c, 2)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_5(self, c):
        chaine = """SELECT art_id 
                    FROM article 
                    WHERE code=?"""
        result = self.curseur.execute(chaine, (c,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_6(self, x):
        chaine = """SELECT code 
                    FROM article 
                    WHERE art_id=?
                    AND ad=?"""
        result = self.curseur.execute(chaine, (x, 1)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_7(self, x):
        chaine = """SELECT code 
                    FROM article 
                    WHERE art_id=?
                    AND ad=?"""
        result = self.curseur.execute(chaine, (x, 2)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_8(self, x):
        chaine = """SELECT cat_id FROM categorie WHERE name=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_9(self, x):
        chaine = """SELECT tiers_id FROM tiers WHERE nom=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_10(self, x):
        chaine = """SELECT fact_id FROM factureA
                    WHERE num=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()

        if not result:
            return False
        else:
            return result[0]

    def function_10b(self, x):
        begin = datetime(self.exercice, 1, 1)
        end = datetime(self.exercice + 1, 1, 1)
        chaine = """SELECT fact_id FROM factureA WHERE num=? AND dat>=? AND dat<?"""
        result = self.curseur.execute(chaine, (x, begin, end)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_11(self, x):

        chaine = """SELECT nom 
                    FROM tiers 
                    WHERE tiers_id=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_12(self, x):
        chaine = """SELECT worker_id FROM workers WHERE nom=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_13(self, x):
        chaine = """SELECT vente_id FROM vente
                    WHERE dat=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if not result:
            return False
        else:
            return result[0]

    def function_14(self, x):
        chaine = """SELECT nom FROM workers WHERE worker_id=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_15(self, art_id, dat):
        """détermine les composants d'un article composé à une certaine date de vente

        Args:
            art_id (int): id du composant
            dat (datetime): date de vente

        Returns:
            tuple or False: tuple de (component_id, proportion) du composé art_id ou False si le composé n'existait pas
        """      
        dat = self.function_40(art_id, dat)
        if not dat:
            res = False
        else:
            chaine = """SELECT component_id, proportion
                        FROM composition
                        WHERE compo_id=?
                        AND dat=?"""
            result = self.curseur.execute(chaine, (art_id, dat)).fetchall()
            res = () if not result else result
            
        print('liste des composants de', art_id, res, dat)
        return res

    def function_16(self, art_id, dat):
        """détermine la quantité vendue d'un article inventorié art_id 
        pendant l'exercice jusqu'à une date donnée

        Args:
            art_id (int): id de l'article inventorié
            dat (datetime): date limite pour la vente

        Returns:
            float: quantité vendue de l'article art_id jusqu'à la date y
        """        
        if dat.year < self.exercice:
            # cas où la date initiale est le 1er janvier, donc x est le 31 decembre de l'année pécédente
            return 0
        
        # dates initiales et finales
        end = dat
        begin = datetime(dat.year, 1, 1)
        
        # récupération de toutes les ventes avec leurs quantités et la date de vente
        chaine = """SELECT codeV_id, qte, dat 
                    FROM recordV, vente 
                    WHERE  recordV.vente_id=vente.vente_id 
                    AND dat>=? 
                    AND dat<?"""
        result = self.curseur.execute(chaine, (begin, func_18(end))).fetchall()
        
        # calcule de la quantité q vendue
        q = 0
        if result:
            for code_id, qte, dat in result:
                if code_id == art_id:  # code_id est l'article recherché
                    q += qte
                elif self.function_6(code_id):  # l'article est un autre article inventorié
                    continue
                elif self.function_7(code_id):  # code_id est un composé
                    liste = self.function_15(code_id, dat)
                    if not liste:
                        continue # composé sans composants
                    else:
                        for cod, prop in liste:
                            if cod == art_id:
                                q += prop * qte
                else:  # code_id est non-inventorié et non-composé
                    print('cet article ne devrait pas se trouvé dans  vente')
                    continue
        return q

    def function_16b(self, art_id, y, z):
        """détermine la quantité vendue d'un article inventorié donné entre 2 dates.
        cet article a peut se trouvé dans un composé

        Args:
            art_id (int): id de l'article inventorié
            y (datetime): date initiale
            z (datetime): datefinale

        Returns:
            float: quantité vendue de l'article
        """        
    
        chaine = """SELECT codeV_id, qte, dat 
                    FROM recordV, vente 
                    WHERE  recordV.vente_id=vente.vente_id 
                    AND dat>=? 
                    AND dat<?"""
                    
        result = self.curseur.execute(chaine, (y, func_18(z))).fetchall()
        q = 0
        if result:
            # result contient les tuples (code_id, qte, dat) des ventes
            for code_id, qte, dat in result:
                if code_id == art_id:  # code_id est l'article recherché
                    q += qte
                    print('article comptaboilisé', art_id, qte, dat)
                elif self.function_6(code_id):  # l'article est un autre article inventorié
                    continue
                elif self.function_7(code_id):  # code_id est un composé
                    liste = self.function_15(code_id, dat)
                    if not liste:
                        print('ici considéré nul, composé sans composants connus à cette date')
                    else:
                        for cod, prop in [tup for tup in liste if tup[0] == art_id]:
                                q += prop * qte
                else:  # code_id est non-inventorié
                    print('cet article ne devrait pas se trouvé dans  vente')
                    continue
        
        return q

    def function_17(self, art_id, dat):
        if dat.year < self.exercice:
            return 0
        end = dat
        begin = datetime(dat.year, 1, 1)
        chaine = """SELECT qte  from recordA, factureA 
                    WHERE  art_id=?
                    AND factureA.fact_id=recordA.fact_id 
                    AND dat >= ?
                    AND dat < ?
                    """
        result = self.curseur.execute(chaine, (art_id, begin, func_18(end))).fetchall()
        q = 0
        if result:
            for tup in result:
                q += tup[0]
        return q

    def function_17b(self, art_id, y, z):
        """détermine la quantité achetée d'un article entre 2 dates

        Args:
            art_id (int): id de l'article
            y (datetime): date initiale
            z (datetime): date finale

        Returns:
            int: quantité achetée entre les dates x et y
        """ 
        
        chaine = """SELECT qte  from recordA, factureA 
                    WHERE  art_id=?
                    AND factureA.fact_id=recordA.fact_id 
                    AND dat >= ?
                    AND dat < ?
                    """
        result = self.curseur.execute(chaine, (art_id, y, func_18(z))).fetchall()
       
        return 0 if not result else sum([tup[0] for tup in result])

    def function_18(self, art_id, dat):
        if dat.year < self.exercice:
            return 0
        begin = datetime(dat.year, 1, 1)
        end = dat
        chaine = """SELECT theorique, physique 
                    FROM correction
                    WHERE art_id=?
                    AND dat>=?
                    and dat<?"""
        result = self.curseur.execute(chaine, (art_id, begin, func_18(end))).fetchall()
        cor = 0
        if result:
            for tup in result:
                cor += tup[1] - tup[0]
        return cor

    def function_18b(self, art_id, x, y):
        begin = x
        end = y
        chaine = """SELECT theorique, physique 
                    FROM correction
                    WHERE art_id=?
                    AND dat>=?
                    and dat<?"""
        result = self.curseur.execute(chaine, (art_id, begin, func_18(end))).fetchall()
        cor = 0
        if result:
            for tup in result:
                cor += tup[1] - tup[0]
        return cor

    def function_19(self, art_id, dat):
        if dat.year < self.exercice:
            year = dat.year
        else:
            year = dat.year - 1

        chaine = """SELECT stk
                    FROM stocloture
                    WHERE art_id=?
                    AND year=?"""
        result = self.curseur.execute(chaine, (art_id, year)).fetchone()
        if result:
            stock = result[0]
        else:
            stock = 0
        return stock

    def function_20(self, x):
        chaine = """SELECT CODE
                    FROM article
                    WHERE envente=?"""
        result = self.curseur.execute(chaine, (1,)).fetchall()
        if (x,) in result:
            return True
        else:
            return False

    def function_21(self):
        liste = []
        chaine = """SELECT name
                    FROM categorie"""
        result = self.curseur.execute(chaine).fetchall()
        if result:
            for tup in result:
                liste.append(tup[0])
            liste.sort()
        return liste

    def function_22(self, x):
        liste = []
        chaine = """SELECT code
                    FROM article
                    WHERE cat_id=?
                    AND ad=?"""
        result = self.curseur.execute(chaine, (self.function_8(x), 1))
        if result:
            for tup in result:
                liste.append(tup[0])
            liste.sort()
        return liste

    def function_23(self, x):
        art_id = self.function_2(x)
        v = self.function_16(art_id, datetime.now())
        a = self.function_17(art_id, datetime.now())
        c = self.function_18(art_id, datetime.now())
        s = self.function_19(art_id, datetime.now())
        return func_6(s + a + c - v)

    def function_24(self):
        v = []
        liste = []
        liste.append(['INVENTAIRE', self.database])
        liste.append(v)
        liste.append([func_9(date.today())])

        liste.append(v)
        liste.append(['CODE', 'DÉSIGNATION', 'TH.', 'PHYSIQUE'])

        liste1 = self.function_21()
        for name in liste1:
            passage = True
            liste2 = self.function_22(name)
            for code in liste2:
                if passage:
                    liste.append(v)
                    liste.append([name.upper()])
                    passage = False
                liste.append([code, self.function_3(code), self.function_23(code)])

        return liste

    def function_25(self):
        v = []
        liste = [['ALERTES-STOCK', self.database], v, [func_9(date.today())], v,
                 ['CODE', 'DÉSIGNATION', 'MIN', 'STOCK']]

        liste1 = self.function_21()
        for name in liste1:
            liste2 = self.function_22(name)
            passage = True
            for code in liste2:
                min = self.function_26(code)
                stock = self.function_23(code)
                if float(stock.replace(',', '.')) < min:
                    if passage:
                        liste.append(v)
                        liste.append([name.upper()])
                        passage = False
                    liste.append([code, self.function_3(code), func_6(min), stock])
        return liste

    def function_26(self, x):
        chaine = """SELECT stockmin
                    FROM article
                    WHERE art_id=?"""
        result = self.curseur.execute(chaine, (self.function_2(x),)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_27(self, x):
        chaine = """SELECT art_id 
                    FROM article
                    WHERE code=?
                    AND ad=?"""
        result = self.curseur.execute(chaine, (x, 0)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_28(self):
        chaine = "SELECT code FROM article"
        ensemble = set()
        result = self.curseur.execute(chaine).fetchall()
        if result:
            for tup in result:
                ensemble = ensemble | {tup[0]}
        return ensemble

    def function_29(self, x):
        chaine = """SELECT code 
                    FROM article
                    WHERE art_id=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_30(self, x):
        chaine = """SELECT type_id 
                    FROM type
                    WHERE name=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_31(self, x):
        chaine = """SELECT name 
                    FROM type
                    WHERE type_id=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_32(self, x):
        chaine = """SELECT name
                    FROM categorie
                    WHERE cat_id=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_33(self, x):
        chaine = """SELECT cat_id
                    FROM article
                    WHERE code=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_34(self, x):
        chaine = """SELECT charge_id 
                    FROM charge 
                    WHERE num=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if not result:
            return False
        else:
            return result[0]

    def function_34b(self, x):
        begin = datetime(self.exercice, 1, 1)
        end = datetime(self.exercice + 1, 1, 1)
        chaine = """SELECT charge_id FROM charge 
                           WHERE num=? AND dat>=? AND dat<?"""
        result = self.curseur.execute(chaine, (x, begin, end)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_36(self, tup):

        chaine = """SELECT dat, vente_id, caisse_id, total
                    FROM vente
                    WHERE dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (tup[0], func_18(tup[1]))).fetchall()
        if not result:
            liste = []
        else:
            liste = list(result)
            liste.sort(reverse=True)

        return liste

    def function_37(self, tup):

        chaine = """SELECT dat, fact_id, num, tiers_id, total
                    FROM factureA
                    WHERE dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (tup[0], func_18(tup[1]))).fetchall()

        if not result:
            liste = []
        else:
            liste = list(result)
            liste.sort(reverse=True)

        return liste

    def function_38(self, tup):

        chaine = """SELECT dat, charge_id, num, type_id, tiers_id, des, montant, dif, debut, mois
                    FROM charge
                    WHERE dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (tup[0], func_18(tup[1]))).fetchall()

        if not result:
            liste = []
        else:
            liste = list(result)
            liste.sort(reverse=True)

        return liste

    def function_39(self, tup):

        chaine = """SELECT dat, corr_id, art_id, theorique, physique, explication
                    FROM correction
                    WHERE dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (tup[0], func_18(tup[1]))).fetchall()

        if not result:
            liste = []
        else:
            liste = list(result)
            liste.sort(reverse=True)

        return liste

    def function_40(self, art_id, y):
        """détermine la date s'un composé pour une date de vente y

        Args:
            art_id (int): id du composé
            y (datetime): date de vente du composé

        Returns:
            datetime: date du composé (les compositions peuvent en effet varier avec des modifications temporelles)
        """        
        chaine = """SELECT dat
                    FROM composition
                    WHERE compo_id=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (art_id, func_18(y))).fetchall()
        if result:
            print('date compo', art_id, max(result)[0])
            return max(result)[0] 
        else:
            return False

    def function_41(self, x, y):
        if y.year < self.exercice:
            return 0
        tot = 0
        chaine = """SELECT prix, remise, total
                    FROM recordA, factureA
                    WHERE recordA.fact_id=factureA.fact_id
                    AND art_id=?
                    AND dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (x, datetime(y.year, 1, 1), func_18(y))).fetchall()
        if result:
            for tup in result:
                prix, remise, total = tup
                if not total:
                    continue
                elif remise:
                    percent = 1 - remise / (total + remise)
                    tot += prix * percent
                else:
                    tot += prix
        return round(tot)

    def function_41b(self, art_id, y, z):
        """détermine le montant de l'achat d'un article entre deux dates

        Args:
            art_id ([type]): id de l'article
            y (date initiale): [description]
            z (date finale): [description]

        Returns:
            int: montant de l'achat l'article entre les dates y et z
        """        
        tot = 0
        chaine = """SELECT prix, remise, total
                    FROM recordA, factureA
                    WHERE recordA.fact_id=factureA.fact_id
                    AND art_id=?
                    AND dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (art_id, y, func_18(z))).fetchall()
        if result:
            for tup in result:
                prix, remise, total = tup
                if not total:
                    continue
                elif remise:
                    percent = 1 - remise / (total + remise)
                    tot += prix * percent
                else:
                    tot += prix
        return round(tot)

    def function_42(self, art_id, y, dicoPa):
        """détermine le Pa d'un composé vendu à la date y

        Args:
            art_id (int): id de l'article composé
            y (datetime): date de vente du composé
            dicoPa (dict): clé: id d'un article/valeur: (stock, Pa)

        Returns:
            int: prix d'achat du composé
        """        
        pA = 0
        dat = self.function_40(art_id, y)
        if dat:
            chaine = """SELECT component_id, proportion
                        FROM composition
                        WHERE compo_id=?
                        AND dat=?"""
            result = self.curseur.execute(chaine, (art_id, dat)).fetchall()
            if result:
                for article_id, proportion in result:
                    
                    pA += proportion * dicoPa[article_id][1]
        else:
            print("erreur : le commposant n'existait pas à la date supposée de sa vente...")
        return round(pA)

    def function_43(self, art_id, y):
        """détermine le pa d'un article à une date y 

        Args:
            art_id (int): id de l'article
            y (datetime): date pour laquelle on détermine le pa

        Returns:
            int: pa de l'article
        """
        
        num = max(self.function_44(art_id, y), 0) + self.function_41(art_id, y) # somme des pa*qa
        den = max(self.function_19(art_id, y), 0) + self.function_17(art_id, y) # somme des qa

        if den:
            return round(num / den)
        else:
            # pa du stock de cloture précédent
            return self.function_44b(art_id, y)

    def function_44(self, x, y):
        if y.year < self.exercice:
            year = y.year
        else:
            year = y.year - 1
        tot = 0
        chaine = """SELECT pa, stk
                    FROM stocloture
                    WHERE art_id=?
                    AND year=?"""
        result = self.curseur.execute(chaine, (x, year)).fetchone()
        if result:
            tot = result[0] * result[1]
        return round(tot)

    def function_44b(self, x, y):
        if y.year < self.exercice:
            year = y.year
        else:
            year = y.year - 1
        tot = 0
        chaine = """SELECT pa
                    FROM stocloture
                    WHERE art_id=?
                    AND year=?"""
        result = self.curseur.execute(chaine, (x, year)).fetchone()
        if result:
            p = round(result[0])
        else:
            p = 0
        return p

    def function_45(self, x, y):

        return self.function_43(x, y) * self.function_46(x, y)

    def function_46(self, art_id, y):
        """détermine le stock d un article à une date donnée

        Args:
            x (int): art_id de l article
            y (datetime): date à laquelle on cherche le stock

        Returns:
            float: quantité de l article art_id à la date y
        """

        v = self.function_16(art_id, y)  # q vendue à une date <= y de l'exercice
        a = self.function_17(art_id, y)  # q achetée à une date <= y de l'exercice
        c = self.function_18(art_id, y)  # q corrigée à une date <= y de l'exercice
        s = self.function_19(art_id, y)  # q su stock de cloture de l'année précédente la date y

        return s + a + c - v

    def function_47(self, x):
        liste = []
        chaine = """SELECT code, art_id, des, stockmin, envente, pv, ad
                    FROM article
                    WHERE cat_id=?"""

        result = self.curseur.execute(chaine, (self.function_8(x),))
        if result:
            liste = list(result)
            liste.sort()
        return liste

    def function_48(self):
        liste = []
        chaine = """SELECT art_id
                    FROM article"""
        result = self.curseur.execute(chaine).fetchall()
        if result:
            liste = [tup[0] for tup in result]
        return liste

    def function_49(self):
        dat = datetime.now()
        liste = []
        v = ''
        line = []

        liste += [['ARTICLES', self.database], line, [func_9(date.today())], line]
        titre = ['CODE', 'désignation'.upper(), 'MIN', 'STOCK', '', 'PA', 'PV']

        liste.append(titre)
        list_categorie = self.function_21()

        for categorie in list_categorie:
            liste.append(line)
            liste.append([categorie.upper()])
            list_article = self.function_47(categorie)
            for article in list_article:
                code, art_id, des, mini, envente, pv, ad = article
                if ad == 1:
                    pa = self.function_43(art_id, dat)
                    stock = func_6(self.function_46(art_id, dat))
                    mini = func_6(mini)
                elif ad == 2:
                    pa = self.function_42(art_id, dat)
                    stock = v
                else:
                    pa = v
                    pv = v
                    stock = v
                if envente:
                    envente = 'V'
                else:
                    envente = v
                liste.append([code, des, mini, stock, envente, pa, pv])

        return liste

    def function_50(self, x, y, z):
        tot = qte = 0
        chaine = """SELECT qte, prix
                    FROM recordV, vente
                    WHERE recordV.vente_id=vente.vente_id
                    AND codeV_id=?
                    AND dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (x, y, func_18(z)))
        if result:
            for tup in result:
                qte += tup[0]
                tot += tup[1]
        return qte, tot

    def function_51(self, x, y):
        tot = 0
        chaine = """SELECT total
                    FROM vente
                    WHERE dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (x, func_18(y)))
        if result:
            for tup in result:
                tot += tup[0]
        return tot

    def function_52(self, x, y):
        tot = 0
        chaine = """SELECT total
                    FROM factureA
                    WHERE dat>=?
                    AND dat<?"""
        result = self.curseur.execute(chaine, (x, func_18(y)))
        if result:
            for tup in result:
                tot += tup[0]
        return tot

    def function_53(self, x):
        tot = 0
        chaine = """SELECT pa, stk
                    FROM stocloture
                    WHERE year=?"""
        result = self.curseur.execute(chaine, (x.year - 1,)).fetchall()
        if result:
            for tup in result:
                tot += max(tup[0] * tup[1], 0)
        return tot

    def function_54(self, x):
        tot = 0
        chaine = """SELECT art_id
                    FROM article
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (1,)).fetchall()
        if result:
            for tup in result:
                # print('pa, qte', self.function_43(tup[0], x), self.function_46(tup[0], x))
                tot += self.function_43(tup[0], x) * self.function_46(tup[0], x)
        return tot

    def function_54b(self, x, y, final=''):
        """détermine la situation initiale (stock et Pa) et la situation finale (stock et Pa)
        pour tous les articles inventoriés

        Args:
            x (datetime): date initiale
            y (datetime): date finale
            final (str, optional): année de cloture. Defaults to ''.

        Returns:
            tuple: stockInitial(valeur), deltaStock(valeur), stockFinal(valeur), dicoPa(stock, Pa), dicoPaInit(stock, Pa)
        """        
        
        # initialisation
        deltaStock = stockInitial = 0
        dicoPaInit = {}
        dicoPa = {}
        # sélection des articles inventoriés (ad=1)
        chaine = """SELECT art_id
                    FROM article
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (1,)).fetchall()
        if result:
            for tup in result:
                art_id = tup[0]
                
                # calcul du prix d'achat et stock initiaux
                qInit = self.function_46(art_id, func_20(x))
                pInit = self.function_43(art_id, func_20(x))
                dicoPaInit[art_id] = (qInit, pInit)
                stockInitial += pInit * qInit
                
                # calcul du prix d'achat et quantité achetée entre les dates x et y 
                montantAchat = self.function_41b(art_id, x, y)
                qA = self.function_17b(art_id, x, y)              
                pA = pInit if not (qInit + qA) else round((pInit * qInit + montantAchat) / (qInit + qA))      
                q = self.function_46(art_id, y)
                dicoPa[art_id] = (q, pA)
                
                # calcul de la valeur du stock
                qVendue = self.function_16b(art_id, x, y)
                qCorr = self.function_18b(art_id, x, y)
                deltaStock += montantAchat - pA * (qVendue - qCorr)
            return round(stockInitial), round(deltaStock), round(stockInitial) + round(deltaStock), dicoPa, dicoPaInit
        else:
            return 0, 0, 0, {}, {}

    def function_55(self, x, y, final=''):
        """Détermine le bilan entre deux dates

        Args:
            x (datetime.datetime): date initiale
            y (datetime.datetime): date finale  
            
            final (str, optional): année du bilan final. Defaults to ''.

        Returns:
            [list]: liste prête à l'impression
        """
        v = []
        liste = [['BILAN' + final], v, [self.database], v, [func_9(x)], ['> ' + func_9(y)]]
        recette = self.function_51(x, y)
        achat = self.function_52(x, y)
        
        stock_initial, delta_stock, stock_final, dicoPa, dicoPaInit = self.function_54b(x, y, final)
        
        marge_brute, dicoMarge = self.function_61(x, y, dicoPa)
      
        
        # encore à vérifié ci-dessous
        charge = self.function_56(x, y)
        resultat_net = recette - achat - charge + delta_stock

        if recette:
            marge_nette = func_19(resultat_net / recette)
        else:
            marge_nette = ''

        liste += [v, ['RÉSULTATS GLOBAUX'], v]
        liste += [['RECETTES', func_6(recette)],
                  ['ACHATS', func_6(achat)],
                  ['VARIATION DE STOCK', func_6(delta_stock)],
                  ['MARGE BRUTE', func_6(marge_brute)],
                  ['CHARGES', func_6(charge)],
                  ['RÉSULTAT NET', func_6(resultat_net)],
                  ['MARGE NETTE', marge_nette]]

        liste += [v, ['Résultats SELON CATÉGORIE'.upper()]]
        for c in self.function_21():
            recette, marge, qte = dicoMarge[self.function_8(c)]
            # self.function_60(c, x, y, dicoPa)

            liste += [v, [c.upper()],
                      ['Quantité vendue', func_6(qte)],
                      ['Recette', func_6(recette)],
                      ['Marge brute', func_6(marge)]]

        liste += [v, ['CHARGES SELON TYPE']]
        for tup in self.function_62():
            liste += [[tup[0], func_6(self.function_63(tup[1], x, y))]]
            amortissement = self.function_64(tup[1], x, y, 'A')
            repartition = self.function_64(tup[1], x, y, 'R')
            if amortissement:
                liste += [['>amortissement', func_6(amortissement)]]
            if repartition:
                liste += [['>répartition', func_6(repartition)]]

        liste += [v, ['VALEUR STOCK'], ['Initial', func_6(stock_initial)],
                  ['Final', func_6(stock_final)]]

        liste += [v, ['DÉTAILS STOCKS']]
        liste += [['CODE', 'INITIAL', 'PA', 'FINAL', 'PA']]
        if final:
            self.function_66(self.exercice)  # effacement des enregistrements de cloture
        for name in self.function_21():
            passage = True
            for code in self.function_22(name):
                if passage:
                    liste.append(v)
                    liste.append([name.upper()])
                    passage = False
                art_id = self.function_2(code)
                
                d_i, d_f = func_20(x), y 

                pa_final = dicoPa[art_id][1]
                stk_final = dicoPa[art_id][0]

                liste += [[code,
                           func_6(dicoPaInit[art_id][0]),
                           func_6(dicoPaInit[art_id][1]),
                           func_6(stk_final),
                           func_6(pa_final)]]
                if final:
                    self.insert_stocloture(tup=(art_id, pa_final, stk_final, self.exercice))
        if final:
            self.enregistrer()
        return liste

    def function_56(self, x, y):
        tot = 0
        chaine = """SELECT montant
                    FROM charge
                    WHERE dif=?
                    AND DAT>=?
                    AND DAT<?"""
        result = self.curseur.execute(chaine, ('', x, func_18(y))).fetchall()
        if result:
            for tup in result:
                tot += tup[0]
        tot += self.function_57(x, y, 'A')
        tot += self.function_57(x, y, 'R')
        return tot

    def function_57(self, x, y, dif):
        tot = 0
        chaine = """SELECT montant, debut, mois
                    FROM charge
                    WHERE dif=?"""
        result = self.curseur.execute(chaine, (dif,)).fetchall()
        if result:
            for tup in result:
                montant, debut, mois = tup
                part = montant / mois
                for e in range(mois):
                    if not e:
                        dat = debut
                    else:
                        dat = dat + timedelta(days=monthrange(dat.year, dat.month)[1])
                    if x <= dat < func_18(y):
                        tot += part
        return tot

    def function_58(self, art_id, y, z, dicoPa):
        """détermine la recette, la margeB et la qte d'un article vendu entre 2 dates

        Args:
            art_id (int): id de l'article
            y (datetime): date initiale
            z (datetime): date finale
            dicoPa (dict): clé: art_id/valeur:(stock, Pa)

        Returns:
            tuple: recette, margeBrute, qte vendue entre les dates y et z
        """        
        tot = qte = marge = 0
        ad = self.function_59(art_id)
        if ad:
            # article composé ou inventorié
            chaine = """SELECT qte, prix, dat
                           FROM recordV, vente
                           WHERE recordV.vente_id=vente.vente_id
                           AND codeV_id=?
                           AND dat>=?
                           AND dat<?"""
            result = self.curseur.execute(chaine, (art_id, y, func_18(z))).fetchall()

            if result:
                for quantity, price, dat in result:
                    # détermination du Pa
                    if ad == 1:
                        # article inventorié
                        # pa = self.function_43(x, dat)
                        pa = dicoPa[art_id][1]
                    else:
                        # article composé
                        pa = self.function_42(art_id, dat, dicoPa)
                    
                    # incrémentation
                    marge += price - pa * quantity
                    qte += quantity
                    tot += price

        else:
            # situation abandonnée
            print("ad=0 calcul de la marge brute")
            # article non-inventorié (rechercher la quantité achetée)
            marge -= self.function_41b(art_id, y, z)

        return tot, marge, qte

    def function_59(self, x):
        chaine = """SELECT ad
                    FROM article
                    WHERE art_id=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False
    """
    def function_60(self, x, y, z):
        recette = marge = qte = 0
        li = self.function_47(x)

        if li:
            list_code = [c[0] for c in li]
        else:
            list_code = []

        for code in list_code:
            v, m, q = self.function_58(self.function_5(code), y, z)
            recette += v
            marge += m
            qte += q

        return recette, marge, qte
    """
    def function_61(self, x, y, dicoPa):
        """détermine la marge brute (montant des articles vendus - la valeur de ces articles en Pa)
        entre kles dates x et y

        Args:
            x (datetime): date initiale
            y (datetime): date finale
            dicoPa (dict): clé:     art_id
                           valeur:  stock, Pa de l'article 

        Returns:
            tuple: (int, dict): margeBrute et dictionnaire (clé: cat_id / valeur: recette, marge, qte vendue)
        """        
      
        chaine = """SELECT cat_id FROM categorie"""
        result = self.curseur.execute(chaine).fetchall()   
        dicoMarge, margeB = {}, 0
        if result:
            for c in result:
                cat_id = c[0]
                recette, marge, qte = self.function_61b(cat_id, x, y, dicoPa)
                dicoMarge[cat_id] = (recette, marge, qte)
                margeB += marge
        return margeB, dicoMarge

    def function_61b(self, cat_id, x, y, dicoPa):
        """détermine la recette, la margeBrute, la qte vendue pour une catégorie, entre 2 dates

        Args:
            cat_id (int): id de la catégorie
            x (datetime): date initiale
            y (datetime): date finale
            dicoPa (dict): clé: art_id / valeur: (stock,Pa)

        Returns:
            tuple: recette, margeBrute, qunantité vendue entre les dates x et y
        """        
        marge = recette = qte = 0
        chaine = """SELECT art_id FROM article WHERE cat_id=?"""
        result = self.curseur.execute(chaine, (cat_id,)).fetchall()
        if result:
            for c in result:
                art_id = c[0]
                tup = self.function_58(art_id, x, y, dicoPa)
                recette += tup[0]
                marge += tup[1]
                qte += tup[2]

        return recette, marge, qte

    def function_62(self):
        liste = []
        chaine = """SELECT name, type_id
                    FROM type
                    """
        result = self.curseur.execute(chaine)
        if result:
            liste = list(result)
            liste.sort()
        return liste

    def function_63(self, x, y, z):
        tot = 0
        chaine = """SELECT montant
                           FROM charge
                           WHERE dif=?
                           AND type_id=?
                           AND DAT>=?
                           AND DAT<?"""
        result = self.curseur.execute(chaine, ('', x, y, func_18(z))).fetchall()
        if result:
            for tup in result:
                tot += tup[0]
        return tot

    def function_64(self, x, y, z, dif):
        tot = 0
        chaine = """SELECT montant, debut, mois
                    FROM charge
                    WHERE dif=?
                    AND type_id=?"""
        result = self.curseur.execute(chaine, (dif, x)).fetchall()
        if result:
            for tup in result:
                montant, debut, mois = tup
                part = montant / mois
                for e in range(mois):
                    if not e:
                        dat = debut
                    else:
                        dat = dat + timedelta(days=monthrange(dat.year, dat.month)[1])
                    if y <= dat < func_18(z):
                        tot += part
        return tot

    def function_65(self, x):
        chaine = """SELECT weighting FROM ponderation WHERE jour=?"""
        result = self.curseur.execute(chaine, (x.weekday(),)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def function_66(self, x):
        chaine = """DELETE from stocloture WHERE year=?"""
        self.curseur.execute(chaine, (x,))

    def function_67(self):
        v = []
        end = datetime.now()
        b = end - timedelta(days=n_trace - 1)
        begin = datetime(b.year, b.month, b.day)
        liste = [['traçage'.upper()], v, [self.database], v, [func_9(begin)], ['> ' + func_9(end)]]

        chaine = """SELECT dat, info1, info2, info3, info4, info5 
                    FROM trace 
                    WHERE dat>=? and dat<?"""
        result = self.curseur.execute(chaine, (begin, end)).fetchall()
        if result:
            li = list(result)
            li.sort(reverse=True)
            liste.append(v)
            liste.append(['DATE', 'INFOS'])
            liste.append(v)
            for tup in li:
                dat, info1, info2, info3, info4, info5 = tup
                liste.append([func_21(dat), info1, info2, info3, info4, info5])
        return liste

    def function_68(self, x):
        chaine = "SELECT dat, fact_id, num, tiers_id, total FROM factureA WHERE tiers_id=? AND dat>=? AND dat<?"
        tiers_id = self.function_9(x)
        tup = tiers_id, datetime(self.exercice, 1, 1), datetime(self.exercice + 1, 1, 1)
        result = self.curseur.execute(chaine, tup).fetchall()
        if result:
            liste = list(result)
            liste.sort(reverse=True)
        else:
            liste = []

        # liste = [tup for tup in list_ref1 if tup[3] == tiers_id]
        # liste.sort(reverse=True)

        return liste

    def function_69(self, x):
        chaine = """SELECT dat, charge_id, num, type_id, tiers_id, des, montant, dif, debut, mois
                    FROM charge
                    WHERE (tiers_id=? OR type_id=? OR dif=?)
                    AND dat >= ?
                    AND dat < ?"""
        begin, end = datetime(self.exercice, 1, 1), datetime(self.exercice + 1, 1, 1)
        tiers_id, type_id = self.function_9(x), self.function_30(x)
        tup = (tiers_id, type_id, x, begin, end)
        result = self.curseur.execute(chaine, tup).fetchall()
        if result:
            liste = list(result)
            # begin, end = datetime(self.exercice, 1, 1), datetime(self.exercice+1, 1, 1)
            # liste = [e for e in liste if begin<= e[0] < end]
            liste.sort(reverse=True)
        else:
            liste = []

        return liste

    def function_70(self, x):

        # obtention de list_code à partir de x (filtre fragment de code)
        chaine = """SELECT code 
                    FROM article
                    WHERE ad=?"""
        result = self.curseur.execute(chaine, (1,)).fetchall()
        if result:
            li_code = []
            for c in result:
                code = c[0]
                if not x:
                    li_code.append(code)
                    continue
                length = len(x)
                if len(code) < length:
                    continue
                if code[0:length] == x:
                    li_code.append(code)
            list_code = [' {}'.format(y) for y in li_code]
            list_code.sort()
            list_id = [self.function_2(z.strip()) for z in list_code]
        else:
            list_code = []
            list_id = []
        print(list_id)

        # sélection à l'aide de list_id
        liste = []
        begin = datetime(self.exercice, 1, 1)
        end = datetime(self.exercice + 1, 1, 1)
        for art_id in list_id:

            chaine = """SELECT dat, corr_id, art_id, theorique, physique, explication
                        FROM correction
                        WHERE art_id = ?
                        AND dat>=?
                        AND dat<?"""
            result = self.curseur.execute(chaine, (art_id, begin, end)).fetchall()
            if result:
                liste += list(result)

        liste.sort(reverse=True)
        return liste

    def function_71(self, tup):

        begin = tup[0]
        end = tup[1] + timedelta(days=1)

        liste = listdir(join(getcwd(), 'DOCUMENTS'))
        liste.sort(reverse=True)

        li = []
        for file in liste:
            try:
                dat = datetime.strptime(file[0:10], "%Y-%m-%d")
            except ValueError:
                continue
            else:
                if begin <= dat < end:
                    li.append(' {}'.format(file))
        return li

    def function_72(self, x):
        begin = datetime(self.exercice, 1, 1)
        end = datetime(self.exercice + 1, 1, 1)

        liste = listdir(join(getcwd(), 'DOCUMENTS'))
        liste.sort(reverse=True)

        li = []
        for file in liste:
            if x in file:
                try:
                    dat = datetime.strptime(file[0:10], "%Y-%m-%d")
                    rep = begin <= dat < end
                except ValueError:
                    rep = True
                if rep:
                    li.append(' {}'.format(file))
        return li

    def function_73(self, x):
        chaine = """SELECT vente_id FROM vente WHERE dat=?"""
        result = self.curseur.execute(chaine, (x,)).fetchone()
        if result:
            return result[0]
        else:
            return False

    def record_55(self, **kw):
        
        # initialisation
        cat = [elem for elem in kw['cat']]
        pc = [elem for elem in kw['pc']]
        n = kw['n']
        couplage = kw['couplage'].get()
        com = ''
        cat_id =[False for _ in range(n)]
        
        # vérification de chaque encodage
        i = 0
        while i < n and not com:
            encode1 = encode2 = False
            if pc[i].get().strip():
                try:
                    pc[i] = float(pc[i].get().strip())
                    if not (0<= pc[i] <= 100):
                        raise E
                except:
                    com = "ERREUR pourcentage"
                else:
                    encode1 = True
            if cat[i].get().strip():  
                try:
                    cat_id[i] = self.function_8(cat[i].get().strip())
                    if not cat_id[i]:
                        raise E
                except: 
                    com = "EREUR catégorie"
                else:
                    encode2 = True
            if not com and encode1 != encode2:
                com = "ERREUR encodage"
            i += 1 
        # vérification collective
        ## catégories doivent être toutes différentes ou toutes vides
        if not com:
            liste = [elem for elem in cat_id if elem is not False]
            test = liste == [] or  len(set(liste)) == len(liste)
            if not test:
                com = "Erreur encodage (catégories identiques)"
        ## somme des pc doit être <= 100
        if not com:
            if sum([pc[i] for i in range(n) if type(pc[i])==float]) > 100:
                com = "ERREUR pourcentage"                      
        if not com:
            # suppression des enregistrements
            self.curseur.execute("""DELETE FROM fixecat""")
                
            # enregistrements des nouvelles contraintes
            for i in range(n):
                if cat_id[i]:
                    self.insert_fixecat(tup = (cat_id[i], pc[i], 0 if i>0 else couplage))
            self.enregistrer()  
            com = 'OK'
        
        # message d'erreur   
        kw['comment'].set(com) 
        return True if com == 'OK' else False
        
    def list_19(self, **kw):

        list_ref = kw['list_ref']
        list_ref.clear()
        list_box = kw['list_box']
        list_box.clear()
        var_box = kw['var_box']
        filtre = kw['filtre'].get().strip()

        # création de la liste ordonnée de couple (date, fact_id)

        tup = func_14(filtre, self.exercice)
        if tup:
            list_ref += self.function_39(tup)
        else:
            list_ref += self.function_70(filtre)

        # fabrication de la list_box

        for tup in list_ref:
            dat = func_9(tup[0])
            code = self.function_6(tup[2])
            corr = tup[4] - tup[3]
            explication = tup[5]

            if corr > 0:
                corr = '+' + func_6(corr)
            else:
                corr = func_6(corr)

            list_box.append(ligne_5.format(dat[:-5], code, corr, explication))
        var_box.set(list_box)

        return len(list_box)

    def list_53(self, **kw):

        list_ref = kw['list_ref']
        list_ref.clear()
        list_box = kw['list_box']
        list_box.clear()
        var_box = kw['var_box']
        filtre = kw['filtre'].get().strip()

        # création de la liste ordonnée de couple (date, filename)

        tup = func_14(filtre, self.exercice)
        if tup:
            list_ref += self.function_71(tup)
        else:
            list_ref += self.function_72(filtre)

        # fabrication de la list_box
        list_box += list_ref
        var_box.set(list_box)

        return len(list_box)

    def select_19(self, **kw):

        indice = kw['indice']
        list_ref = kw['list_ref']

        dat = kw['dat']
        code = kw['code']
        phth = kw['phth']
        corr = kw['corr']
        explication = kw['explication']

        corr_id = list_ref[indice]

        chaine = """SELECT dat, art_id, theorique, physique, explication 
                    FROM correction
                     WHERE corr_id=?"""
        result = self.curseur.execute(chaine, (corr_id,)).fetchone()

        dat.set(func_9(result[0]))
        code.set(self.function_6(result[1]))
        phth.set(func_6(result[3]) + '/' + func_6(result[2]))
        correction = result[3] - result[2]
        explication.set(result[4])

        if correction > 0:
            corr.set('+' + func_6(correction))
        else:
            corr.set(func_6(correction))
        return
