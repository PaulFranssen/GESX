# -*- coding: utf-8 -*-

# importation des modules

from datetime import *
from constants import *
import csv
from calendar import monthrange



f = lambda x: int(x) if x == int(x) else x  # renvoie un integer si x est un integer



def func_2(x):
    """détermine la nature entière et positive de x

    Args:
        x (str): valeur introduite par l'utilisateur

    Returns:
        bool: True si x est la chaine vide ou contient un entier positif, False sinon
    """    
    if not x:
        return True
    else:
        try:
            x = int(x)
        except:
            return False

        return x >= 0

def func_1(x):
    try:
        x = int(x)
    except:
        return False

    return x >= 0

def func_18(x):
    """majore une date

    Args:
        x (datetime): date

    Returns:
        datetime: date du jour suivant x
    """
    x = datetime(x.year, x.month, x.day)+timedelta(days=1)
    return x

def func_20(x):
    """minore une date

    Args:
        x (datetime): date à minorer

    Returns:
        datetime: date du jour précédent x 
    """
    x = datetime(x.year, x.month, x.day)-timedelta(days=1)
    return x

def func_19(x):

    p = '{:#0.0%}'.format(x)
    return p.replace('.', '')

def func_10(x):
    """renvoie True si x est un réel positif"""
    try:
        x = float(x)
    except:
        return False

    return x >= 0


def func_11(xx):
    pass


def func_12(x, y):
    com = ''
    try:
        with open(y, 'w', newline='', encoding='utf-8') as fichier:
            fiche = csv.writer(fichier, delimiter=";")
            fiche.writerows(x)
    except OSError as err:
        com = 'ERREUR création du fichier refusée' + err
    return com


def func_13(x):
    try:
        x = int(x)
    except ValueError:
        return False
    return x > 0


def func_14(x, year):
    if not x:
        return datetime(year, 1, 1), datetime(year, 12, 31)

    if len(x) < 4:
        month = func_15(x)
        if month:
            last_day = monthrange(year, month)[1]
            first = datetime(year, month, 1)
            last = datetime(year, month, last_day)
            return first, last
        else:
            return False
    else:
        d = func_7(x) or func_7(x + ' ' + str(year))
        if not d:
            return False
        elif not d.year == year:
            return False
        else:
            return d, d


def func_15(x):
    try:
        m = datetime.strptime(x, "%b")
    except ValueError:
        return False
    else:
        return m.month


def func_16(x, year):
    x = x.strip()
    if len(x) < 7:
        x += ' ' + str(year)
    d = func_7(x)
    if not d:
        return False
    elif not d.year != year:
        return False
    else:
        return d


def func_3(x):
    try:
        x = float(x)
    except ValueError:
        return False

    return x > 0


def func_4(x):
    if x:
        return int(x)
    else:
        return 0


def ligne(code, des, qte, prix):
    """renvoie une ligne formatée comprenant le code, la description, la quantité et le prix"""
    global l_box_1

    l_box_1 = l_code

    return "{:^19}{:^33}{:>8}{:>16}".format(code, des, qte, prix)

def func_7(x):
    """à partir d'une chaine, renvoie un objet datetime ou False si la date n'est pas conforme"""
    try:
        y = datetime.strptime(x, "%d %b %Y")
    except:
        return False
    return y


def func_9(x):
    """modifie le type d'une date

    Args:
        x (datetime.datetime): date 

    Returns:
        str or False: date sous forme de str (exemple : Lu 04 Jan 2021)
    """
    try:
        y = datetime.strftime(x, "%a %d %b %Y")
    except:
        print('erreur date dane le fichier date')
        return False
    return y

def func_21(x):
    try:
        y = datetime.strftime(x, "%a %d %b %Y (%H:%M)")
    except:
        print('erreur date dane le fichier date')
        return False
    return y


def func_8(x):
    """à partir d'une date, renvoie une date ou false si la date de base n'est pas conforme"""
    try:
        y = datetime.strftime(x, "%d %b %Y")
    except:
        return False
    return y


def print_dict_csv(file_name, lis):
    """enregistre un fichier csv, de nom file, de 2 colonnes à partir d'une liste de dictionnaire lis"""
    with open(file_name, 'w', newline='', encoding = "utf-8") as file:
        fi = csv.DictWriter(file, fieldnames=[1, 2], delimiter=";")
        fi.writerows(lis)


def func_5(x):
    form = '{:>' + str(l_prix - 1) + ',}'
    return form.format(int(x)).replace(',', '.') + ' '


def func_6(x):
    x = round(float(x), 2)
    if x == int(x):
        return str(int(x))
    else:
        return (str(x)).replace('.', ',')


def func_17(x, y):
    a = '{:^' + str(y) + '}'
    return a.format(x)


