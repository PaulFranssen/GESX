# -*- coding: utf-8 -*-

# liste des couleurs non-utilisées
color_1 = 'wheat1'
color_2 = 'pink'
color_3 = 'blue'
color_4 = 'green'
color_5 = 'yellow'
color_7 = 'purple'
color_8 = 'black'
color_9 = 'white'
color_10 = 'wheat3'
color_11 = 'alice blue'
color_13 = 'wheat2'
color_14 = 'yellow4'
color_15 = 'ivory3'
color_16 = "wheat4"
color_17 = 'khaki3'
color_18 = 'SteelBlue1'
color_19 = 'DarkSeaGreen1'
color_20 = 'VioletRed1'
color_21 = 'VioletRed3'
color_29 = 'grey0'
color_31 = 'grey10'
color_34 = 'grey40'
color_35 = 'grey50'
color_36 = 'grey60'
color_38 = 'grey80'


# largeur des labels et entry
l_code = 15
l_des = 30
l_base = 15
l_baseC = l_base - 8
l_pv = 7
l_min = 4
l_alerte = 2
l_actif = 2
l_contact = 35
l_date = 12             # date sans le jour ou sans l'année
l_date2 = 14            # date avec le jour
l_path = 50
l_filename = 30
l_num = 10
l_descript = 50         # description de la charge
l_prix = 11
l_qte = 6
l_type = 20
l_explication = 52
l_proportion = len(' proportion ')

# largeur button de base
l_button1 = len('enregistrer')+1

# nombre de jours de traçage
n_trace = 14

# titre et bas des colonnes en label, ainsi que largeur de ces labels

ligne_2 = '{:^' + str(l_date) + '}   {:^' + str(l_num) + '}   {:^' + str(l_code) + '}   {:^' + str(l_prix) + '}'
l_2 = len(ligne_2.format('DATE', 'N°PIÈCE', 'TIERS', 'TOTAL'))

# éditer les charges
ligne_3 = '{:^' + str(l_date) + '}   {:^' + str(l_num) + '}   {:^' + str(l_type) + '}   {:^' + str(
    l_code) + '}   {:^' + str(l_prix) + '}   {:^' + '3' + '}'
l_3 = len(ligne_3.format('DATE', 'N°PIÈCE', 'TYPE', 'TIERS', 'MONTANT', ' '*3))

ligne_4 = '{:^' + str(l_date) + '}   {:^' + str(l_code) + '}   {:^' + str(l_prix) + '}'
l_4 = len(ligne_4.format('DATE', 'CAISSIER(ÈRE)', 'TOTAL'))

ligne_5 = '{:^' + str(l_date) + '}   {:^' + str(l_code) + '}   {:^' + str(
    l_qte) + '}   {:^' + str(l_explication) + '}'
l_5 = len(ligne_5.format('DATE', 'CODE', '+/-', 'EXPLICATION'))

ligne_7 = '{:^' + str(l_code) + '}   {:^' + str(l_des) + '}   {:^' + str(l_proportion) + '}'
l_7 = len(ligne_7.format('CODE', 'DÉSIGNATION', 'PROPORTION'))

ligne_8 = '{:^' + str(l_code) + '}   {:^' + str(l_des) + '}   {:^' + str(l_qte) + '}   {:^' + str(l_prix) + '}'
l_8 = len(ligne_8.format('CODE', 'DÉSIGNATION', 'QTÉ', 'PRIX'))

# réglages finaux
taille_4 = 18       # taille des caractères normaux
taille_3 = 16       # taille de l'exercice et de la base en haut à droite et du menu
taille_5 = 22       # taille du titre
taille_7 = 13       # taille petit checkbutton (par défaut)
taille_8 = 100       # taille logo

# distanciation
p_02 = 40
p_03 = 60
p_04 = 10
p_05 = 15

# hauteur de box
h_03 = 20       # listbox choix avec selection et button nouveau en bas
h_15 = 13       # listbox de facture de vente
h_27 = h_15     # idem
h_08 = 23       # lisbox choix avec selevction mais sans button ni comment en bas
h_09 = 5        # lisbox composition
h_10 = 21       # listbox sans button mais avec comment


# couleur
color_32 = 'grey15'         # fond écran
color_37 = 'grey80'         # écriture claire
color_6 = 'tomato'          # sélection
color_33 = 'grey30'         # disabled
color_30 = 'black'          # écriture foncée

# police de caractère
police_1 = "Consolas"

# NOMS DE FICHIERS
f_partage = "share_file.txt"
f_sauvegarde = "save_file.txt"
f_base = "base_file.txt"
f_dirImport = "dirImport_file.txt"
f_dirImportVente = "dirImportVente_file.txt"
f_nameImport = "nameImport_file.txt"
f_ticket = "ticket_file.txt"

# temps d'attente
attenteLongue = 1000
attenteCourte = 700

# réglage distance entre les entry sous les listbox
reglage_1 = 33
reglage_2 = 33
reglage_3 = 65















