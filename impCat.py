# -*- coding: utf-8 -*-

import csv
from sqlite3 import *
from datetime import *

ENCODAGE= 'latin-1'

print('IMPORT')
print('------')
print('1 catégorie')
print('2 article inventorié')
print('3 article composé')
print('')
choix = input('> CHOIX : ')


nameBase = 'BASE/' + input("Nom complet de la base-destination : ") + '.db'
nameFichier = 'BASE/' + input("Nom complet du fichier-source : ") + '.csv'

print(nameBase, nameFichier)

if choix == '1':

    # récupération des catégories dans le fichier
    try:
        with open(nameFichier, 'r', newline='', encoding=ENCODAGE) as f:
            lignes = csv.reader(f)
            liste_categorie = [cat[0] for cat in lignes]
            print(lignes)
            print(liste_categorie)
    except csv.Error as error:
        print(error)
    else:
        # ouverture de la base et insertion dans la base
        try:
            connexion = connect(nameBase, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            connexion.execute("PRAGMA foreign_keys = 1")
            curseur = connexion.cursor()

        except Error as error:
            print("Error while connecting to sqlite", error)
        else:
            for cat in liste_categorie:
                if len(cat)>15:
                    cat = cat[:15]
                chaine = """INSERT INTO categorie (name) VALUES(?)"""
                curseur.execute(chaine, (cat,))
            connexion.commit()
            connexion.close()
elif choix == '2':
    print('choix2')
    # récupération des articles inventoriés  dans le fichier
    try:
        with open(nameFichier, 'r', newline='', encoding=ENCODAGE) as f:
            lignes = csv.DictReader(f, fieldnames=['code', 'des', 'cat', 'pv'])
            liste_article = [dico for dico in lignes]
            print(lignes, liste_article)
    except csv.Error as error:
        print(error)
    else:
        # ouverture de la base et insertion dans la base
        try:
            connexion = connect(nameBase, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            connexion.execute("PRAGMA foreign_keys = 1")
            curseur = connexion.cursor()

        except Error as error:
            print("Error while connecting to sqlite", error)
        else:
            for dico in liste_article:
                # recherche de la catégorie
                cat_id = curseur.execute("""SELECT cat_id FROM categorie WHERE name=?""", (dico['cat'][:15],)).fetchone()[0]
                chaine = """INSERT INTO article (code, des, cat_id, pv, ad) VALUES(?,?,?,?,1)"""
                curseur.execute(chaine, (dico['code'][:15],
                                         dico['des'],
                                         cat_id,
                                         int(float(dico['pv']))))
            connexion.commit()
            connexion.close()

elif choix == '3':
    print('articles composés')
    # récupération des articles inventoriés  dans le fichier
    try:
        with open(nameFichier, 'r', newline='', encoding='ENCODAGE') as f:
            lignes = csv.DictReader(f,
                                    fieldnames=['code', 'des', 'cat', 'pv', 'pa',
                                                'n', 'c1', 'p1', 'c2', 'p2', 'c3', 'p3'])
            liste_article = [dico for dico in lignes]
    except csv.Error as error:
        print(error)
    else:
        # ouverture de la base et insertion dans la base
        try:
            connexion = connect(nameBase, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            connexion.execute("PRAGMA foreign_keys = 1")
            curseur = connexion.cursor()

        except Error as error:
            print("Error while connecting to sqlite", error)
        else:
            erreur = 0
            for dico in liste_article:
                # recherche de la catégorie
                code = dico['code'][:15]
                cat_id = curseur.execute("""SELECT cat_id FROM categorie WHERE name=?""", (dico['cat'][:15],)).fetchone()[0]
                chaine = """INSERT INTO article (code, des, cat_id, pv, ad) VALUES(?,?,?,?,2)"""
                curseur.execute(chaine, (code[:15],
                                         dico['des'],
                                         cat_id,
                                         int(float(dico['pv']))))
                # insertion des composants
                # id de l'article
                compo_id = curseur.execute("""SELECT art_id FROM article WHERE code=?""", (code[:15],)).fetchone()[0]
                
                # composant1
                code = dico['c1'][:15]
                prop = float(dico['p1'])
                result = curseur.execute("""SELECT art_id FROM article WHERE code=?""", (code[:15],)).fetchone()
                if result:
                    component_id=result[0]
                else:
                    print('composant', code, 'inexistant')
                    erreur = 1
                    break
                dat = datetime(2015, 1, 1)
                chaine = """INSERT INTO composition (compo_id, component_id, proportion, dat) VALUES(?,?,?,?)"""
                curseur.execute(chaine, (compo_id,
                                         component_id,
                                         prop,
                                         dat))
                
                # composant2
                code = dico['c2'][:15]
                if not code:
                    continue
                prop = float(dico['p2'])
                result = curseur.execute("""SELECT art_id FROM article WHERE code=?""", (code[:15],)).fetchone()
                if result:
                    component_id=result[0]
                else:
                    print('composant', code, 'inexistant')
                    erreur = 1
                    break
                chaine = """INSERT INTO composition (compo_id, component_id, proportion, dat) VALUES(?,?,?,?)"""
                curseur.execute(chaine, (compo_id,
                                         component_id,
                                         prop,
                                         dat))
                
                # composant3
                code = dico['c3'][:15]
                if not code:
                    continue
                prop = float(dico['p3'])
                result = curseur.execute("""SELECT art_id FROM article WHERE code=?""", (code[:15],)).fetchone()
                if result:
                    component_id=result[0]
                else:
                    print('composant', code, 'inexistant')
                    erreur = 1
                    break
                chaine = """INSERT INTO composition (compo_id, component_id, proportion, dat) VALUES(?,?,?,?)"""
                curseur.execute(chaine, (compo_id,
                                         component_id,
                                         prop,
                                         dat))
            if not erreur:   
                connexion.commit()
            connexion.close()





