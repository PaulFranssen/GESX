# -*- coding: utf-8 -*-

# importation des modules

from constants import *
from model import *


class PF(Frame):
    def __init__(self, base, boss=None):
        Frame.__init__(self, boss)
        self.master.colormap = 'red'
        self.master.configure(**kw_master)
        self.configure(**kw_pf)
        self.pack(**pad_pf)

        # variables
        self.base = base
        self.an = IntVar()
        self.database = StringVar()
        
        # childs
        self.frame1 = Frame1(self)
        self.frame1.pack(**pad_f1)
        self.frame2 = Frame2(self, self.frame1)
        self.frame2.pack(**pad_f2)
        
        # dimensionnement
        self.master.wm_attributes('-fullscreen', 'true')
        self.master.resizable(width=False, height=False)
        
        """
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        merge_x, merge_y = int((w - 1500) / 2), int((h - 800) / 2)
        if merge_x < 0 or merge_y < 0:
            print('écran non conforme')
            # exit(0)
        # dim = "{}x{}+{}+{}".format(1500, 800, merge_x, merge_y)      
        # self.master.geometry(dim)
        # self.master.overrideredirect(True)
        """
    def fix_exercice(self, year):
        self.an.set(year)
        # active ou désactive les items du menu lors du changement d'exercices
        self.frame1.active(year)

    def fix_database(self, database):
        self.database.set(database)

    def accueil(self):
        self.frame1.command0()


class Frame1(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_f1)

        # variables
        self.g = IntVar()
        self.var_spin = IntVar(value=self.master.an)
        self.num_display = 0
        
        # enfants
        self.list_display = [None] * 60

        # MENU
        # ARTICLES
        mb = Menubutton(self, text="données".upper(), **kw_1)
        mb.pack(**pad_1)
        Label(self, **kw_50).pack(side='left')
        me = Menu(mb, **kw_3)
        me.add_command(label="Catégories d'articles", command=self.command6, **kw_2)
        me.add_separator()
        me.add_command(label='Articles inventoriés', underline=0, command=self.command10, **kw_2)
        me.add_command(label='Articles composés', command=self.command22, **kw_2)
        #me.add_command(label='Articles non-inventoriés', command=self.command32, **kw_2)
        me.add_separator()

        me.add_command(label='Tiers', command=self.command5, **kw_2)
        me.add_command(label='Employés', command=self.command13, **kw_2)
        me.add_command(label='Types de charges', underline=0, command=self.command35, **kw_2)
        me.add_separator()
        me.add_command(label='Imprimer les données', underline=0, command=self.command59, **kw_2)
        mb.configure(menu=me)

        # ENCODAGE
        mb = Menubutton(self, text="ENCODAGE", **kw_1)
        mb.pack(**pad_1)
        Label(self, **kw_50).pack(side='left')
        me = Menu(mb, **kw_3)
        me.add_command(label='Ventes', underline=0, command=self.command3, **kw_2)
        me.add_command(label='Achats', underline=0, command=self.command12, **kw_2)
        me.add_command(label='Charges', underline=0, command=self.command9, **kw_2)
        mb.configure(menu=me)

        # PARAMETRES
        mb = Menubutton(self, text="paramètres".upper(), **kw_1)
        mb.pack(**pad_1)
        Label(self, **kw_50).pack(side='left')
        me = Menu(mb, **kw_3)
        me.add_command(label="Changer d'exercice", underline=0, command=self.command16, **kw_2)
        me.add_checkbutton(label="Afficher G", variable=self.g, command=self.command48, selectcolor=kw_54['col_spec'], **kw_2)
        mb.configure(menu=me)

        # STOCK
        mb = Menubutton(self, text="STOCKS", **kw_1)
        mb.pack(**pad_1)
        Label(self, **kw_50).pack(side='left')
        self.me1 = Menu(mb, **kw_3)
        self.me1.add_command(label="Corriger les stocks", underline=0, command=self.command17, state=NORMAL, **kw_2)
        self.me1.add_command(label="Expliquer les corrections", command=self.command19, state=NORMAL, **kw_2)
        self.me1.add_separator()
        self.me1.add_command(label="Inventaire", underline=0, command=self.command30, state=NORMAL, **kw_2)
        self.me1.add_separator()
        self.me1.add_command(label="Alertes-stock", underline=0, command=self.command31, state=NORMAL, **kw_2)
        mb.configure(menu=self.me1)

        # ANALYSE
        mb = Menubutton(self, text="ANALYSE", **kw_1)
        mb.pack(**pad_1)
        Label(self, **kw_50).pack(side='left')
        self.me2 = Menu(mb, **kw_3)

        self.me2.add_command(label="Analyse des articles", underline=0, command=self.command42,
                             state=NORMAL, **kw_2)
        self.me2.add_command(label="Traçage des enregistrements", underline=0, command=self.command52,
                             state=NORMAL, **kw_2)
        self.me2.add_command(label="Ouvrir un document", underline=0, command=self.command53,
                             state=NORMAL, **kw_2)
        self.me2.add_separator()
        self.me2.add_command(label="Bilan intermédiaire", underline=0, command=self.command43, state=NORMAL, **kw_2)
        self.me2.add_separator()
        self.me2.add_command(label="Bilan annuel", underline=0, command=self.command51, state=NORMAL, **kw_2)
        # me.add_command(label="Accéder à un document", underline=0, command=self.command42, **kw_2)
        mb.configure(menu=self.me2)

        # DATABASE
        mb = Menubutton(self, text="DATABASE", **kw_1)
        mb.pack(**pad_1)
        sep = Label(self, **kw_50).pack(side=LEFT)
        me = Menu(mb, **kw_3)
        me.add_command(label="Partager", underline=0, command=self.command38, **kw_2)
        me.add_command(label="Sauvegarder", underline=0, command=self.command56, **kw_2)
        me.add_separator()
        me.add_command(label="Sélectionner", underline=0, command=self.command21, **kw_2)
        me.add_separator()
        me.add_command(label="Importer", underline=0, command=self.command49, **kw_2)
        me.add_command(label="Créer", underline=0, command=self.command47, **kw_2)
        me.add_command(label="Clôner", underline=0, command=self.command57, **kw_2)
        me.add_command(label="Renommer", underline=0, command=self.command50, **kw_2)
        mb.configure(menu=me)

        # G
        self.mb_g = Menubutton(self, text="G", **kw_1)
        self.mb_g['foreground'] = kw_54['col_spec']
        self.sep_g = Label(self, **kw_50)

        me = Menu(self.mb_g, **kw_3)
        me.add_command(label="Pondérer les jours", underline=0, command=self.command44, **kw_2)
        me.add_command(label="Limiter le prix des articles", underline=0, command=self.command45, **kw_2)
        me.add_command(label="Fixer des catégories", underline=0, command=self.command55, **kw_2)
        me.add_separator()
        me.add_command(label="Générer les ventes", underline=0, command=self.command46, **kw_2)
        me.add_command(label="Imprimer les tickets", underline=0, command=self.command54, **kw_2)
        self.mb_g.configure(menu=me)

        # EXIT
        b1 = Button(self, text="X ", command=self.command40, **kw_51)
        b1.pack(padx=5, side=RIGHT)
        b2 = Button(self, text=" —", command=self.command41, **kw_51)
        b2.pack(padx=5, side=RIGHT)

        # EXERCICE et # DATABASE
        # cadre englobant
        globe = Frame(self, **kw_53)
        globe.pack(side=RIGHT, **pad_53)

        # cadre autour de l'exercice
        encadre = LabelFrame(globe, **kw_53)
        encadre.pack(side=RIGHT, padx=30)

        # exercice et database
        Label(encadre, textvariable=self.master.an, width=5, **kw_52).pack()
        Label(globe, textvariable=self.master.database, **kw_52b).pack(side=LEFT)

    def active(self, year):
        if year != date.today().year:
            # le premier paramètre me donne l'indice de l'élément dans le menu
            self.me1.entryconfig(0, foreground=color_33, activeforeground=color_33)
            self.me1.entryconfig(3, foreground=color_33, activeforeground=color_33)
            self.me1.entryconfig(5, foreground=color_33, activeforeground=color_33)
            self.me2.entryconfig(0, foreground=color_33, activeforeground=color_33)
            self.me2.entryconfig(1, foreground=color_33, activeforeground=color_33)
        else:
            self.me1.entryconfig(0, foreground=color_37, activeforeground=color_30)
            self.me1.entryconfig(3, foreground=color_37, activeforeground=color_30)
            self.me1.entryconfig(5, foreground=color_37, activeforeground=color_30)
            self.me2.entryconfig(0, foreground=color_37, activeforeground=color_30)
            self.me2.entryconfig(1, foreground=color_37, activeforeground=color_30)

    def add_display(self, number, dis):
        self.list_display[number] = dis

    def command0(self):
        self.list_display[0].display()

    def command4(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 4
        self.list_display[4].display(arg)

    def command5(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 5
        self.list_display[5].display(arg)

    def command6(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 6
        self.list_display[6].display(arg)

    def command7(self):
        self.list_display[self.num_display].hide()
        self.num_display = 7
        self.list_display[7].display()

    def command8(self):
        self.list_display[self.num_display].hide()
        self.num_display = 8
        self.list_display[8].display()

    def command9(self, arg2=None):
        self.list_display[self.num_display].hide()
        self.num_display = 9
        self.list_display[9].display(arg2)

    def command10(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 10
        self.list_display[10].display(arg)

    def command11(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 11
        self.list_display[11].display(arg)

    def command12(self, arg2=None):
        self.list_display[self.num_display].hide()
        self.num_display = 12
        self.list_display[12].display(arg2)

    def command13(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 13
        self.list_display[13].display(arg)

    def command14(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 14
        self.list_display[14].display(arg)

    def command3(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 3
        self.list_display[3].display(arg)

    def command15(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 15
        self.list_display[15].display(arg)

    def command16(self):
        self.list_display[self.num_display].hide()
        self.num_display = 16
        self.list_display[16].display()

    def command17(self):
        if int(self.master.an.get()) == date.today().year:
            self.list_display[self.num_display].hide()
            self.num_display = 17
            self.list_display[17].display()

    def command18(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 18
        self.list_display[18].display(arg)

    def command19(self):
        self.list_display[self.num_display].hide()
        self.num_display = 19
        self.list_display[19].display()

    def command20(self):
        self.list_display[self.num_display].hide()
        self.num_display = 20
        self.list_display[20].display()

    def command21(self):
        self.list_display[self.num_display].hide()
        self.num_display = 21
        self.list_display[21].display()

    def command22(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 22
        self.list_display[22].display(arg)

    def command23(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 23
        self.list_display[23].display(arg)

    def command24(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 24
        self.list_display[24].display(arg)

    def command25(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 25
        self.list_display[25].display(arg)

    def command26(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 26
        self.list_display[26].display(arg)

    def command27(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 27
        self.list_display[27].display(arg)

    def command28(self):
        self.list_display[self.num_display].hide()
        self.num_display = 28
        self.list_display[28].display()

    def command29(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 29
        self.list_display[29].display(arg)

    def command30(self):
        # commande inactive si je ne suis pas dans l'année active
        if int(self.master.an.get()) == date.today().year:
            self.list_display[self.num_display].hide()
            self.num_display = 30
            self.list_display[30].display()

    def command31(self):
        if int(self.master.an.get()) == date.today().year:
            self.list_display[self.num_display].hide()
            self.num_display = 31
            self.list_display[31].display()

    def command32(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 32
        self.list_display[32].display(arg)

    def command33(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 33
        self.list_display[33].display(arg)

    def command34(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 34
        self.list_display[34].display(arg)

    def command35(self, arg=False):
        self.list_display[self.num_display].hide()
        self.num_display = 35
        self.list_display[35].display(arg)

    def command36(self):
        self.list_display[self.num_display].hide()
        self.num_display = 36
        self.list_display[36].display()

    def command37(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 37
        self.list_display[37].display(arg)

    def command38(self):
        self.list_display[self.num_display].hide()
        self.num_display = 38
        self.list_display[38].display()

    def command39(self, arg):
        self.list_display[self.num_display].hide()
        self.num_display = 39
        self.list_display[39].display(arg)

    def command40(self):
        self.master.base.fermer()
        self.master.master.destroy()

    def command41(self):
        self.master.master.wm_iconify()

    def command42(self):
        if int(self.master.an.get()) == date.today().year:
            self.list_display[self.num_display].hide()
            self.num_display = 42
            self.list_display[42].display()

    def command43(self):
        self.list_display[self.num_display].hide()
        self.num_display = 43
        self.list_display[43].display()

    def command44(self):
        self.list_display[self.num_display].hide()
        self.num_display = 44
        self.list_display[44].display()

    def command45(self):
        self.list_display[self.num_display].hide()
        self.num_display = 45
        self.list_display[45].display()

    def command46(self):
        self.list_display[self.num_display].hide()
        self.num_display = 46
        self.list_display[46].display()

    def command47(self):
        self.list_display[self.num_display].hide()
        self.num_display = 47
        self.list_display[47].display()

    def command48(self):
        if self.g.get():
            self.mb_g.pack(**pad_1)
            self.sep_g.pack(side=LEFT)
        else:
            self.mb_g.pack_forget()
            self.sep_g.pack_forget()

    def command49(self):
        self.list_display[self.num_display].hide()
        self.num_display = 49
        self.list_display[49].display()

    def command50(self):
        self.list_display[self.num_display].hide()
        self.num_display = 50
        self.list_display[50].display()

    def command51(self):
        self.list_display[self.num_display].hide()
        self.num_display = 51
        self.list_display[51].display()

    def command52(self):
        if int(self.master.an.get()) == date.today().year:
            self.list_display[self.num_display].hide()
            self.num_display = 52
            self.list_display[52].display()

    def command53(self):
        self.list_display[self.num_display].hide()
        self.num_display = 53
        self.list_display[53].display()

    def command54(self):
        self.list_display[self.num_display].hide()
        self.num_display = 54
        self.list_display[54].display()

    def command55(self):
        self.list_display[self.num_display].hide()
        self.num_display = 55
        self.list_display[55].display()
            
    def command56(self):
        self.list_display[self.num_display].hide()
        self.num_display = 56
        self.list_display[56].display()
        
    def command57(self):
        self.list_display[self.num_display].hide()
        self.num_display = 57
        self.list_display[57].display()
        
    def command58(self):
        self.list_display[self.num_display].hide()
        self.num_display = 58
        self.list_display[58].display()

    def command59(self):
        self.list_display[self.num_display].hide()
        self.num_display = 59
        self.list_display[59].display()


class Frame2(Frame):

    def __init__(self, boss=None, menu=None):
        Frame.__init__(self, boss)
        self.configure(**kw_f2)

        self.menu = menu

        self.frame0 = Frame0(self)
        menu.add_display(0, self.frame0)

        self.frame3 = Frame3(self)
        menu.add_display(3, self.frame3)

        self.frame4 = Frame4(self)
        menu.add_display(4, self.frame4)

        self.frame5 = Frame5(self)
        menu.add_display(5, self.frame5)

        self.frame6 = Frame6(self)
        menu.add_display(6, self.frame6)

        self.frame7 = Frame7(self)
        menu.add_display(7, self.frame7)

        self.frame8 = Frame8(self)
        menu.add_display(8, self.frame8)

        self.frame9 = Frame9(self)
        menu.add_display(9, self.frame9)

        self.frame10 = Frame10(self)
        menu.add_display(10, self.frame10)

        self.frame11 = Frame11(self)
        menu.add_display(11, self.frame11)

        self.frame12 = Frame12(self)
        menu.add_display(12, self.frame12)

        self.frame13 = Frame13(self)
        menu.add_display(13, self.frame13)

        self.frame14 = Frame14(self)
        menu.add_display(14, self.frame14)

        self.frame15 = Frame15(self)
        menu.add_display(15, self.frame15)

        self.frame16 = Frame16(self)
        menu.add_display(16, self.frame16)

        self.frame17 = Frame17(self)
        menu.add_display(17, self.frame17)

        self.frame18 = Frame18(self)
        menu.add_display(18, self.frame18)

        self.frame19 = Frame19(self)
        menu.add_display(19, self.frame19)

        self.frame20 = Frame20(self)
        menu.add_display(20, self.frame20)

        self.frame21 = Frame21(self)
        menu.add_display(21, self.frame21)

        self.frame22 = Frame22(self)
        menu.add_display(22, self.frame22)

        self.frame23 = Frame23(self)
        menu.add_display(23, self.frame23)

        self.frame24 = Frame24(self)
        menu.add_display(24, self.frame24)

        self.frame25 = Frame25(self)
        menu.add_display(25, self.frame25)

        self.frame26 = Frame26(self)
        menu.add_display(26, self.frame26)

        self.frame27 = Frame27(self)
        menu.add_display(27, self.frame27)

        self.frame28 = Frame28(self)
        menu.add_display(28, self.frame28)

        self.frame29 = Frame29(self)
        menu.add_display(29, self.frame29)

        self.frame30 = Frame30(self)
        menu.add_display(30, self.frame30)

        self.frame31 = Frame31(self)
        menu.add_display(31, self.frame31)

        self.frame32 = Frame32(self)
        menu.add_display(32, self.frame32)

        self.frame33 = Frame33(self)
        menu.add_display(33, self.frame33)

        self.frame34 = Frame34(self)
        menu.add_display(34, self.frame34)

        self.frame35 = Frame35(self)
        menu.add_display(35, self.frame35)

        self.frame36 = Frame36(self)
        menu.add_display(36, self.frame36)

        self.frame37 = Frame37(self)
        menu.add_display(37, self.frame37)

        self.frame38 = Frame38(self)
        menu.add_display(38, self.frame38)

        self.frame39 = Frame39(self)
        menu.add_display(39, self.frame39)

        self.frame42 = Frame42(self)
        menu.add_display(42, self.frame42)

        self.frame43 = Frame43(self)
        menu.add_display(43, self.frame43)

        self.frame44 = Frame44(self)
        menu.add_display(44, self.frame44)

        self.frame45 = Frame45(self)
        menu.add_display(45, self.frame45)

        self.frame46 = Frame46(self)
        menu.add_display(46, self.frame46)

        self.frame47 = Frame47(self)
        menu.add_display(47, self.frame47)

        self.frame49 = Frame49(self)
        menu.add_display(49, self.frame49)

        self.frame50 = Frame50(self)
        menu.add_display(50, self.frame50)

        self.frame51 = Frame51(self)
        menu.add_display(51, self.frame51)

        self.frame52 = Frame52(self)
        menu.add_display(52, self.frame52)

        self.frame53 = Frame53(self)
        menu.add_display(53, self.frame53)

        self.frame54 = Frame54(self)
        menu.add_display(54, self.frame54)
        
        self.frame55 = Frame55(self)
        menu.add_display(55, self.frame55)
        
        self.frame58 = Frame58(self)
        menu.add_display(58, self.frame58)

        self.frame59 = Frame59(self)
        menu.add_display(59, self.frame59)
        
        self.frame56 = Frame56(self)
        menu.add_display(56, self.frame56)
        
        self.frame57 = Frame57(self)
        menu.add_display(57, self.frame57)


class Frame42(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, text='analyse des articles'.upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        e1 = Entry(cadre7, width=l_path, textvariable=self.path, **kw_12)
        e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, textvariable=self.filename, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_42(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment)
        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def next(event):
            b2.focus_set()

        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        self.e2.bind('<Return>', next)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_42(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)

        self.e2.focus_set()
        self.e2.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame59(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.cat, self.inv, self.comp, self.non, self.tie, self.emp, self.ven, self.typ = \
            IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        self.comment = StringVar()

        # structure
        Label(self, text='Imprimer les données'.upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrew = Frame(cadre1, **kw_cx)
        cadrew.pack(side=LEFT)

        cadrex = Frame(cadrew, **kw_cx)
        cadrex.pack()

        cadrey = Frame(cadrex, **kw_c6)
        cadrez = Frame(cadrex, **kw_c6)

        cadrez.pack(side=LEFT, **pad_c6)
        cadrey.pack(side=LEFT, **pad_c6)

        Frame(cadrew, **kw_c8).pack(**pad_c8)
        Frame(cadrew, **kw_c8).pack(**pad_c8)

        cadret = Frame(cadrew, **kw_c6)
        cadret.pack(**pad_c6)
        cadre7 = Frame(cadret, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadret, **kw_c8)
        cadre8.pack(**pad_c8)

        # détails cadre w
        cadre9 = Frame(cadrez, **kw_c7)
        cadre10 = Frame(cadrez, **kw_c7)
        cadre11 = Frame(cadrez, **kw_c7)
        cadre12 = Frame(cadrez, **kw_c7)
        cadre13 = Frame(cadrey, **kw_c7)
        cadre14 = Frame(cadrey, **kw_c7)
        cadre15 = Frame(cadrey, **kw_c7)
        cadre16 = Frame(cadrey, **kw_c7)
        cadre9.pack(**pad_c7)
        cadre10.pack(**pad_c7)
        cadre11.pack(**pad_c7)
        cadre12.pack(**pad_c7)
        cadre13.pack(**pad_c7)
        cadre14.pack(**pad_c7)
        cadre15.pack(**pad_c7)
        cadre16.pack(**pad_c7)

        Checkbutton(cadre9, text="Catégories d'articles".upper(), variable=self.cat, **kw_47).pack(**pad_48)
        Checkbutton(cadre13, text="articles inventoriés".upper(), variable=self.inv, **kw_47).pack(**pad_48)
        Checkbutton(cadre10, text="articles composés".upper(), variable=self.comp, **kw_47).pack(**pad_48)
        #Checkbutton(cadre14, text="articles non-inventoriés".upper(), variable=self.non, **kw_47).pack(**pad_48)
        Checkbutton(cadre14, text="articles en vente".upper(), variable=self.ven, **kw_47).pack(**pad_48) #11
        Checkbutton(cadre11, text="tiers".upper(), variable=self.tie, **kw_47).pack(**pad_48) # 15
        Checkbutton(cadre15, text="employés".upper(), variable=self.emp, **kw_47).pack(**pad_48)#12
        Checkbutton(cadre12, text="types de charges".upper(), variable=self.typ, **kw_47).pack(**pad_48)#16
        Label(cadre16, text='', **kw_47b).pack(**pad_48)
        # détails cadre t
        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        e1 = Entry(cadre7, width=l_path, textvariable=self.path, **kw_12)
        e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, textvariable=self.filename, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_59(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment,
                                                cat=self.cat,
                                                inv=self.inv,
                                                comp=self.comp,
                                                non=self.non,
                                                tie=self.tie,
                                                typ=self.typ,
                                                emp=self.emp,
                                                ven=self.ven)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def next(event):
            b2.focus_set()

        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        self.e2.bind('<Return>', next)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_59(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)

        self.e2.focus_set()
        self.e2.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame47(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.nom = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, text='''créer une database'''.upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)

        Label(cadre7, text='NOUVELLE DATABASE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_baseC + 1, textvariable=self.nom, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        def refresh():
            self.comment.set('')

        def action(event):
            self.comment.set('')
            if self.master.master.base.action_47(nom=self.nom,
                                                 comment=self.comment):
                self.nom.set('')
                self.focus_set()
                root.bell()
                root.after(attenteLongue, refresh)
            else:
                self.e1.focus_set()
                self.e1.icursor(END)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def next(event):
            b2.focus_set()

        b2 = Button(cadre2, text="CRÉER", **kw_45)
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', action)
        b2.bind('<Return>', action)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        self.e1.bind('<Return>', next)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.comment.set('')
        self.nom.set('')

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()
        
class Frame57(Frame):
    
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.nom = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, text='clôner une database'.upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)

        Label(cadre7, text='NOUVELLE DATABASE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_baseC + 1, textvariable=self.nom, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        def refresh():
            self.comment.set('')

        def action(event):
            self.comment.set('')
            if self.master.master.base.action_57(nom=self.nom,
                                                 comment=self.comment):
                self.nom.set('')
                self.focus_set()
                root.bell()
                root.after(attenteLongue, refresh)
            else:
                self.e1.focus_set()
                self.e1.icursor(END)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def next(event):
            b2.focus_set()

        b2 = Button(cadre2, text="clôner".upper(), **kw_45)
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', action)
        b2.bind('<Return>', action)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        self.e1.bind('<Return>', next)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.comment.set('')
        self.nom.set('')

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame0(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.comment = StringVar()

        # structure
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)

        Label(cadre7, text='GESX', **kw_13).pack(side=LEFT)

    def display(self):
        self.comment.set('')
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame30(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, text='''IMPRIMER L'INVENTAIRE''', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        e1 = Entry(cadre7, width=l_path, textvariable=self.path, **kw_12)
        e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, textvariable=self.filename, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_30(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def next(event):
            b2.focus_set()

        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        self.e2.bind('<Return>', next)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_30(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)

        self.e2.focus_set()
        self.e2.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame43(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.comment = StringVar()
        self.dat_i = StringVar()
        self.dat_f = StringVar()

        # structure
        Label(self, text='''BILAN INTERMÉDIAIRE''', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)
        cadre9 = Frame(cadrex, **kw_c8)
        cadre9.pack(**pad_c8)

        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        e1 = Entry(cadre7, width=l_path, textvariable=self.path, takefocus=0, **kw_12)
        e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        e2 = Entry(cadre8, width=l_filename, takefocus=0, textvariable=self.filename, **kw_12)
        e2.pack(**pad_12, side=LEFT)

        Label(cadre9, text='   DATE INITIALE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre9, width=l_date, textvariable=self.dat_i, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e3 = Entry(cadre9, width=l_date, textvariable=self.dat_f, **kw_12)
        e3.pack(**pad_12, side=RIGHT)
        Label(cadre9, text='DATE FINALE', **kw_11).pack(**pad_11, side=RIGHT)

        def document(event):
            self.master.master.base.document_43(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment,
                                                d_i=self.dat_i,
                                                d_f=self.dat_f)

        # détails cadre 2
        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def etoile(event=None):
            if self.dat_i.get().strip() == '*':
                self.dat_i.set(func_8(datetime.now()))
        
        def etoile2(event=None):
            if self.dat_f.get().strip() == '*':
                self.dat_f.set(func_8(datetime.now()))     
       

        self.e1.bind('<FocusOut>', etoile)
        e3.bind('<FocusOut>', etoile2)
        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_43(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame51(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.titre = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, textvariable=self.titre, **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_path, textvariable=self.path, takefocus=0, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, takefocus=0, textvariable=self.filename, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_51(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment)

        # détails cadre 2
        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_51(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)
        self.titre.set('BILAN ANNUEL ' + str(self.master.master.base.get_exercice()))
        self.e2.focus_set()
        self.e2.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame52(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.titre = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, textvariable=self.titre, **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_path, textvariable=self.path, takefocus=0, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, takefocus=0, textvariable=self.filename, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_52(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment)

        # détails cadre 2
        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_52(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)
        self.titre.set('TRACER LES ENREGISTREMENTS')
        self.e2.focus_set()
        self.e2.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame38(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master

        self.partage = StringVar()
        
        self.def_partage = IntVar()
        
        self.comment = StringVar()

        # structure
        Label(self, text="PARTAGER LA DATABASE", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
       

        # détails cadre 1
        Checkbutton(cadre7, text='DÉFINIR PAR DÉFAUT', variable=self.def_partage, **kw_49) \
            .pack(side='right', padx=10)
        self.e1 = Entry(cadre7, width=l_path, textvariable=self.partage, **kw_12)
        self.e1.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='RÉPERTOIRE DE PARTAGE', **kw_11).pack(**pad_11, side=RIGHT)


        def refresh(event=None):
            self.comment.set('')

        def record(event):
            arg = "PARTAGE"
            

            if self.master.master.base.record_38(arg=arg,
                                                 partage=self.partage,
                                                 
                                                 def_partage=self.def_partage,
                                                
                                                 comment=self.comment):
                self.focus_set()
                root.bell()
                root.after(attenteLongue, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b2 = Button(cadre2, text="PARTAGER", width=l_button1, **kw_45)
        
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_38(partage=self.partage,
                                           def_partage=self.def_partage,
                                           comment=self.comment)
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()

class Frame56(Frame):
    
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master

        
        self.sauvegarde = StringVar()
        
        self.def_sauvegarde = IntVar()
        self.comment = StringVar()

        # structure
        Label(self, text="SAUVEGARDER LA DATABASE", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        # détails cadre 1
        

        Label(cadre8, text='RÉPERTOIRE DE SAUVEGARDE', **kw_11).pack(**pad_11, side=LEFT)

        self.e2 = Entry(cadre8, width=l_path, textvariable=self.sauvegarde, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)
        Checkbutton(cadre8, text='DÉFINIR PAR DÉFAUT', variable=self.def_sauvegarde, **kw_49) \
            .pack(side='left', padx=10)

        def refresh(event=None):
            self.comment.set('')

        def record(event):
           
            arg = "SAUVEGARDE"

            if self.master.master.base.record_56(arg=arg,
                                                 
                                                 sauvegarde=self.sauvegarde,
                                                 
                                                 def_sauvegarde=self.def_sauvegarde,
                                                 comment=self.comment):
                self.focus_set()
                root.bell()
                root.after(attenteLongue, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

       
        b3 = Button(cadre2, text="SAUVEGARDER", width=l_button1, **kw_45)

       
        b3.pack(side='left', **pad_45)
        b3.bind('<ButtonRelease-1>', record)
        b3.bind('<Return>', record)
        b3.bind('<Enter>', on_enter)
        b3.bind('<FocusIn>', on_enter)
        b3.bind('<Leave>', on_leave)
        b3.bind('<FocusOut>', on_leave)
       

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_56(
                                           sauvegarde=self.sauvegarde,
                                           
                                           def_sauvegarde=self.def_sauvegarde,
                                           comment=self.comment)
        self.e2.focus_set()
        self.e2.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()

class Frame58(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master
        self.importe = StringVar()
        self.nom = StringVar()
        self.def_importe = IntVar()
        self.comment = StringVar()
        self.arg = False

        # structure
        Label(self, text="IMPORTER UNE VENTE", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        # détails cadre 1
        def check1():
            pass

        Checkbutton(cadre7, text='DÉFINIR PAR DÉFAUT', variable=self.def_importe, command=check1, **kw_49) \
            .pack(side='right', padx=10)
        e1 = Entry(cadre7, width=l_path, textvariable=self.importe, **kw_12)
        e1.pack(**pad_12, side=RIGHT)
        Label(cadre7, text="RÉPERTOIRE-SOURCE", **kw_11).pack(**pad_11, side=RIGHT)
        Label(cadre8, text='   NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, textvariable=self.nom, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def action(event):
            self.arg = self.master.master.base.action_58(importe=self.importe,
                                                         nom=self.nom,
                                                         def_importe=self.def_importe,
                                                         comment=self.comment)
            if self.arg:
                root.bell()
                root.after(attenteLongue, back)

        def back(event=None):
            self.master.menu.command3(arg=self.arg)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # cadre 2
        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="IMPORTER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)

        # liens
        b2.bind('<ButtonRelease-1>', action)
        b1.bind('<ButtonRelease-1>', back)
        b2.bind('<Return>', action)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Enter>', on_enter)
        b1.bind('<Enter>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Leave>', on_leave)
        b1.bind('<Leave>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_58(importe=self.importe,
                                           nom=self.nom,
                                           def_importe=self.def_importe,
                                           comment=self.comment)
        self.arg = False
        self.e2.focus_set()
        self.e2.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame54(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.repertoire = StringVar()
        self.d_i = StringVar()
        self.d_f = StringVar()
        self.def_rep = IntVar()
        self.comment = StringVar()

        # structure
        Label(self, text="IMPRIMER LES TICKETS", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        # détails cadre 1
        Checkbutton(cadre7, text='DÉFINIR PAR DÉFAUT', variable=self.def_rep, **kw_49) \
            .pack(side='right', padx=10)
        e1 = Entry(cadre7, width=l_path, textvariable=self.repertoire, **kw_12)
        e1.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='   DATE INITIALE', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_date, textvariable=self.d_i, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)
        Label(cadre8, text='   DATE FINALE', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_date, textvariable=self.d_f, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_54(repertoire=self.repertoire,
                                                d_i=self.d_i,
                                                d_f=self.d_f,
                                                def_rep=self.def_rep,
                                                comment=self.comment)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # détails cadre 2
        b2 = Button(cadre2, text="IMPRIMER(.txt)", **kw_45)
        b2.pack(side='left', **pad_45)

        # liens
        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_54(repertoire=self.repertoire,
                                           d_i=self.d_i,
                                           d_f=self.d_f,
                                           def_rep=self.def_rep,
                                           comment=self.comment)
        self.e2.focus_set()
        self.e2.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame55(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        # variables dynamiques
        self.n = nbr_categorie_fix
        self.cat = [StringVar() for _ in range(self.n)]
        self.pc = [StringVar() for _ in range(self.n)]
        self.couplage = IntVar()
        self.comment = StringVar()

        # structure
        Label(self, text="fixer des catégories".upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)      
        cadre = [Frame(cadrex, **kw_c7) for _ in range(self.n)] 
          
        ## ligne1
        cadre[0].pack(**pad_c7)
        Label(cadre[0], text='catégorie'.upper(), **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre[0], width=l_code, textvariable=self.cat[0], **kw_12)
        self.e1.pack(**pad_12, side=LEFT)
        
        Label(cadre[0], text='   % VENTE', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre[0], width=l_pc, textvariable=self.pc[0], **kw_12).pack(**pad_12, side=LEFT) 
          
        #Checkbutton(cadre[0], text="couplage".upper(), variable=self.couplage, **kw_47).pack(**pad_47c)     

        # lignes suivantes
        for i in range(1, self.n):
            cadre[i].pack(**pad_c7)
            Label(cadre[i], text='catégorie'.upper(), **kw_11).pack(**pad_11, side=LEFT)
            Entry(cadre[i], width=l_code, textvariable=self.cat[i], **kw_12).pack(**pad_12, side=LEFT)         
            Label(cadre[i], text='   % VENTE', **kw_11).pack(**pad_11, side=LEFT)
            Entry(cadre[i], width=l_pc, textvariable=self.pc[i], **kw_12).pack(**pad_12, side=LEFT)
      
        def refresh():
            self.comment.set('')

        def record(event):
            if self.master.master.base.record_55(cat=self.cat,
                                                pc=self.pc,
                                                couplage=self.couplage,
                                                comment=self.comment,
                                                n = self.n):
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # détails cadre 2
        b2 = Button(cadre2, text="ENREGISTRER", **kw_45)
        b2.pack(side='left', **pad_45)

        # liens
        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_55(cat=self.cat,
                                           pc=self.pc,
                                           couplage=self.couplage,
                                           comment=self.comment,
                                           n = self.n)
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame49(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master
        print('root', root)

        self.importe = StringVar()
        self.nom = StringVar()                           
        self.def_importe = IntVar()
        self.def_nom = IntVar()
        self.comment = StringVar()

        # structure
        Label(self, text="IMPORTER UNE DATABASE", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        # détails cadre 1
        Checkbutton(cadre7, text='DÉFINIR PAR DÉFAUT', variable=self.def_importe, **kw_49) \
            .pack(side='right', padx=10)
        e1 = Entry(cadre7, width=l_path, textvariable=self.importe, **kw_12)
        e1.pack(**pad_12, side=RIGHT)
        Label(cadre7, text=" RÉPERTOIRE-SOURCE", **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text="NOM DE LA DATABASE", **kw_11).pack(**pad_11, side=LEFT)

        self.e2 = Entry(cadre8, width=l_base, textvariable=self.nom, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)
        Checkbutton(cadre8, text='DÉFINIR PAR DÉFAUT', variable=self.def_nom, **kw_49) \
            .pack(side='right', padx=10)

        def refresh():
            self.comment.set('')
            self.focus_set()

        def action(event):
            if self.master.master.base.action_49(importe=self.importe,
                                                 nom=self.nom,
                                                 def_importe=self.def_importe,
                                                 def_nom=self.def_nom,
                                                 comment=self.comment):
                self.comment.set('Importation effectuée')
                root.after(attenteLongue, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b2 = Button(cadre2, text="IMPORTER", width=l_button1, **kw_45)

        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', action)
        b2.bind('<Return>', action)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Leave>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_49(importe=self.importe,
                                           nom=self.nom,
                                           def_importe=self.def_importe,
                                           def_nom=self.def_nom,
                                           comment=self.comment)
        self.e2.focus_set()
        self.e2.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame50(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master

        self.name = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, text="MODIFIER LE NOM DE LA DATABASE", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre8 = Frame(cadrex, **kw_c7)
        cadre8.pack(**pad_c7)

        # détails cadre 1
        Label(cadre8, text='NOUVEAU NOM', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_baseC + 1, textvariable=self.name, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def refresh():
            self.comment.set('')
            self.focus_set()

        def action(event):
            if self.master.master.base.action_50(name=self.name,
                                                 comment=self.comment):
                self.comment.set('Modification effectuée')
                root.after(attenteLongue, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b2 = Button(cadre2, text="MODIFIER", width=l_button1, **kw_45)
        b2.pack(**pad_45)

        b2.bind('<ButtonRelease-1>', action)
        b2.bind('<Return>', action)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Leave>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.comment.set('')
        self.e2.focus_set()
        self.e2.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame44(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.p = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        self.comment = StringVar()

        # structure
        Label(self, text="PONDÉRER LES JOURS", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre8 = Frame(cadrex, **kw_c7)
        cadre9 = Frame(cadrex, **kw_c7)
        cadre10 = Frame(cadrex, **kw_c7)
        cadre11 = Frame(cadrex, **kw_c7)
        cadre12 = Frame(cadrex, **kw_c7)
        cadre13 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8.pack(**pad_c7)
        cadre8.pack(**pad_c7)
        cadre9.pack(**pad_c7)
        cadre10.pack(**pad_c7)
        cadre11.pack(**pad_c7)
        cadre12.pack(**pad_c7)
        cadre13.pack(**pad_c7)

        # détails cadre 1
        Label(cadre7, text='MON', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_qte, textvariable=self.p[0], **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='TUE', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre8, width=l_qte, textvariable=self.p[1], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre9, text='WED', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre9, width=l_qte, textvariable=self.p[2], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre10, text='THU', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre10, width=l_qte, textvariable=self.p[3], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre11, text='FRI', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre11, width=l_qte, textvariable=self.p[4], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre12, text='SAT', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre12, width=l_qte, textvariable=self.p[5], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre13, text='SUN', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre13, width=l_qte, textvariable=self.p[6], **kw_12).pack(**pad_12, side=LEFT)

        def refresh():
            self.comment.set('')

        def record(event):
            if self.master.master.base.record_44(p=self.p,
                                                 comment=self.comment):
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # détails cadre 2
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(**pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_44(p=self.p,
                                           comment=self.comment)
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame45(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.p = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        self.comment = StringVar()

        # structure
        Label(self, text="LIMITER LE PRIX DES ARTICLES", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre8 = Frame(cadrex, **kw_c7)
        cadre9 = Frame(cadrex, **kw_c7)
        cadre10 = Frame(cadrex, **kw_c7)
        cadre11 = Frame(cadrex, **kw_c7)
        cadre12 = Frame(cadrex, **kw_c7)
        cadre13 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8.pack(**pad_c7)
        cadre8.pack(**pad_c7)
        cadre9.pack(**pad_c7)
        cadre10.pack(**pad_c7)
        cadre11.pack(**pad_c7)
        cadre12.pack(**pad_c7)
        cadre13.pack(**pad_c7)

        # détails cadre 1
        Label(cadre7, text='MON', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_prix, textvariable=self.p[0], **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='TUE', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre8, width=l_prix, textvariable=self.p[1], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre9, text='WED', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre9, width=l_prix, textvariable=self.p[2], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre10, text='THU', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre10, width=l_prix, textvariable=self.p[3], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre11, text='FRI', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre11, width=l_prix, textvariable=self.p[4], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre12, text='SAT', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre12, width=l_prix, textvariable=self.p[5], **kw_12).pack(**pad_12, side=LEFT)

        Label(cadre13, text='SUN', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre13, width=l_prix, textvariable=self.p[6], **kw_12).pack(**pad_12, side=LEFT)

        def refresh():
            self.comment.set('')

        def record(event):
            if self.master.master.base.record_45(p=self.p,
                                                 comment=self.comment):
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # détails cadre 2
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(**pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_45(p=self.p,
                                           comment=self.comment)
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame46(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.dat_i, self.dat_f, self.montant = StringVar(), StringVar(), StringVar()
        self.vente_nulle = StringVar()
        self.caisse = StringVar()
        self.comment = StringVar()

        # structure
        Label(self, text="GÉNÉRER DES VENTES", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre8 = Frame(cadrex, **kw_c7)
        cadre9 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8.pack(**pad_c7)
        cadre9.pack(**pad_c7)

        # détails cadre 1
        Label(cadre7, text='DATE INITIALE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_date, textvariable=self.dat_i, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        Label(cadre7, text=' DATE FINALE', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre7, width=l_date, textvariable=self.dat_f, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        Label(cadre8, text='MONTANT TOTAL', **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre8, width=l_prix, textvariable=self.montant, **kw_12).pack(**pad_12, side=LEFT)

        Entry(cadre8, width=l_qte, textvariable=self.vente_nulle, **kw_12).pack(**pad_12, side=RIGHT)
        Label(cadre8, text='VENTES NULLES %', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre9, text='CAISSIER(ère)'.upper(), **kw_11).pack(**pad_11, side=LEFT)
        Entry(cadre9, width=l_code, textvariable=self.caisse, **kw_12).pack(**pad_12, side=LEFT)

        def refresh():
            pass
            #self.comment.set('')

        def action(event):
            etoile1()
            etoile2()
            self.comment.set('en cours...') # ne fonctionne pas
            
            self.master.master.base.action_46(dat_i=self.dat_i,
                                                 dat_f=self.dat_f,
                                                 caisse=self.caisse,
                                                 montant=self.montant,
                                                 vente_nulle=self.vente_nulle,
                                                 comment=self.comment)
            #self.focus_set()
            root.bell()
            #root.after(attenteCourte, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def etoile1(event=None):
            if self.dat_i.get().strip() == '*':
                self.dat_i.set(func_8(datetime.now()))

        def etoile2(event=None):
            if self.dat_f.get().strip() == '*':
                self.dat_f.set(func_8(datetime.now()))

        # détails cadre 2
        b2 = Button(cadre2, text="GÉNÉRER", width=l_button1, **kw_45)
        b2.pack(**pad_45)

        # liens
        self.e1.bind('<FocusOut>', etoile1)
        self.e2.bind('<FocusOut>', etoile2)
        b2.bind('<ButtonRelease-1>', action)
        b2.bind('<Return>', action)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.comment.set('')
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame31(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        self.filename = StringVar()
        self.path = StringVar()
        self.comment = StringVar()

        # structure

        Label(self, text='''IMPRIMER LES ALERTES-STOCK''', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # structure cadre 1

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='RÉPERTOIRE-CIBLE', **kw_11).pack(**pad_11, side=LEFT)
        e1 = Entry(cadre7, width=l_path, textvariable=self.path, **kw_12)
        e1.pack(**pad_12, side=LEFT)

        Label(cadre8, text='  NOM DU FICHIER', **kw_11).pack(**pad_11, side=LEFT)
        self.e2 = Entry(cadre8, width=l_filename, textvariable=self.filename, **kw_12)
        self.e2.pack(**pad_12, side=LEFT)

        def document(event):
            self.master.master.base.document_31(path=self.path,
                                                filename=self.filename,
                                                comment=self.comment)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def next(event):
            b2.focus_set()

        b2 = Button(cadre2, text="IMPRIMER(.CSV)", **kw_45)
        b2.pack(side='left', **pad_45)
        b2.bind('<ButtonRelease-1>', document)
        b2.bind('<Return>', document)
        b2.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        self.e2.bind('<Return>', next)

    def display(self, arg=''):                                 
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.display_31(path=self.path,
                                           filename=self.filename,
                                           comment=self.comment)

        self.e2.focus_set()
        self.e2.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame4(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###

        self.code, self.des, self.cat, self.pv, self.stockmin = \
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.comment = StringVar()
        self.envente = IntVar()

        ### STRUCTURE ###

        Label(self, text='AJOUTER UN ARTICLE', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_des, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='CATÉGORIE', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_code, textvariable=self.cat, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        def check():
            if self.envente.get():
                e4.configure(state='normal')
            else:
                e4.configure(state='disabled')

        Label(cadre8, text=' PRIX DE VENTE', **kw_11).pack(**pad_11, side=LEFT)
        e6 = Checkbutton(cadre8, variable=self.envente, command=check, **kw_47)
        e6.pack(side=LEFT, **pad_47)
        e4 = Entry(cadre8, width=l_pv, textvariable=self.pv, **kw_12)
        e4.pack(**pad_12, side=LEFT)

        Label(cadre8, text=' STOCK MINIMUM', **kw_11).pack(**pad_11, side=LEFT)
        e5 = Entry(cadre8, width=l_min, textvariable=self.stockmin, **kw_12)
        e5.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###
        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        def refresh():
            self.comment.set('')
            back(arg=self.arg)
            
        def record(event):
            self.arg = self.master.master.base.record_4(code=self.code,
                                                   des=self.des,
                                                   cat=self.cat,
                                                   pv=self.pv,
                                                   envente=self.envente,
                                                   stockmin=self.stockmin,
                                                   comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
            else:
                self.e1.focus_set()
                self.e1.icursor(END)

        def back(event=None, arg=False):
            self.master.menu.command10(arg=self.arg)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)

    def display(self, arg=''):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set(arg)
        self.des.set('')
        self.cat.set('')
        self.pv.set('')
        self.stockmin.set('0')
        self.comment.set('')
        self.envente.set(1)

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame33(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### VARIABLES DE CONTROLE ###

        self.code, self.des, self.cat = StringVar(), StringVar(), StringVar()
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='AJOUTER UN ARTICLE NON-INVENTORIÉ', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre7.pack(**pad_c7)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_code, textvariable=self.cat, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text=' CATÉGORIE', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_des, textvariable=self.des, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            arg = self.master.master.base.record_33(code=self.code,
                                                    des=self.des,
                                                    cat=self.cat,
                                                    comment=self.comment)
            if arg:
                back(arg=arg)

        def back(event=None, arg=False):
            self.master.menu.command32(arg=arg)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg=''):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set('')
        self.des.set('')
        self.cat.set('')

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame18(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###

        self.code, self.des, self.theorique, self.physique, self.explication = \
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='RÉGULER UN STOCK', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)
        # cadre9 = Frame(cadrex, **kw_c8)
        # cadre9.pack(**pad_c8)
        cadre10 = Frame(cadrex, **kw_c8)
        cadre10.pack(**pad_c8)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, state='disabled', **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_des, textvariable=self.des, state='disabled', **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='STOCK THÉORIQUE', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_qte, textvariable=self.theorique, state='disabled', **kw_12)
        e3.pack(**pad_12, side=LEFT)

        Label(cadre8, text=' STOCK PHYSIQUE ', **kw_11).pack(**pad_11, side=LEFT)
        self.e4 = Entry(cadre8, width=l_qte, textvariable=self.physique, **kw_12)
        self.e4.pack(**pad_12, side=LEFT)

        Label(cadre10, text='EXPLICATION', **kw_11).pack(**pad_11, side=LEFT)
        e5 = Entry(cadre10, width=l_explication, textvariable=self.explication, **kw_12)
        e5.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            if self.master.master.base.record_18(
                    code=self.code,
                    theorique=self.theorique,
                    physique=self.physique,
                    explication=self.explication,
                    comment=self.comment):
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        def back(event=None):
            self.master.menu.command17()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set(arg)

        self.master.master.base.display_18(
            code=self.code,
            des=self.des,
            theorique=self.theorique,
            physique=self.physique,
            explication=self.explication)

        self.physique.set('')
        self.comment.set('')

        self.e4.focus_set()
        self.e4.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame8(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        ### VARIABLES DE CONTROLE ###
        self.code, self.des = StringVar(), StringVar()
        self.comment = StringVar()
        self.arg=False

        ### STRUCTURE ###
        Label(self, text='AJOUTER UN TIERS', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###
        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)
        Label(cadre7, text='NOM', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)
        e2 = Entry(cadre7, width=l_contact, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='CONTACT', **kw_11).pack(**pad_11, side=RIGHT)

        ### DETAILS STRUCTURE CADRE 2 ###
        def record(event):
            self.arg = self.master.master.base.record_8(code=self.code,
                                                   des=self.des,
                                                   comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)

        def back(event=None, arg=False):
            if self.arg:
                arg=self.arg
            self.master.menu.command5(arg)
            
        def refresh():
                self.comment.set('')
                back()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set('')
        self.des.set('')
        self.arg=False

        self.comment.set('')
        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame28(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        ### VARIABLES DE CONTROLE ###

        self.code, self.des = StringVar(), StringVar()
        self.comment = StringVar()
        self.arg=False

        ### STRUCTURE ###

        Label(self, text='AJOUTER UN EMPLOYÉ', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)

        Label(cadre7, text='NOM', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_contact, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='CONTACT', **kw_11).pack(**pad_11, side=RIGHT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            self.arg = self.master.master.base.record_28(code=self.code,
                                                    des=self.des,
                                                    comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        def back(event=None, arg=False):
            if self.arg:
                arg=self.arg
            self.master.menu.command13(arg)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set('')
        self.des.set('')
        self.arg=False

        self.comment.set('')
        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame7(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        ### VARIABLES DE CONTROLE ###

        self.code = StringVar()
        self.comment = StringVar()
        self.arg=False

        ### STRUCTURE ###

        Label(self, text='AJOUTER UNE CATÉGORIE', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)
        Label(cadre7, text='catégorie'.upper(), **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###
        def refresh():
            self.comment.set('')
            back(arg=self.arg)

        def record(event):
            self.arg = self.master.master.base.record_7(code=self.code,
                                                   comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
            else:
                self.e1.focus_set()
                self.e1.icursor(END)
                
        def back(event=None, arg=False):
            if self.arg:
                arg=self.arg
            self.master.menu.command6(arg)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set('')
        self.arg=False
        self.comment.set('')

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame36(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###

        self.code = StringVar()
        self.comment = StringVar()
        self.arg=False

        ### STRUCTURE ###

        Label(self, text='AJOUTER UN TYPE DE CHARGE', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)

        Label(cadre7, text='TYPE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_type, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            self.arg = self.master.master.base.record_36(code=self.code,
                                                    comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        def back(event=None, arg=False):
            if self.arg:
                arg=self.arg
            self.master.menu.command35(arg)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set('')
        self.arg=False
        self.comment.set('')

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame16(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.comment = StringVar()
        self.var_spin = IntVar()

        # structure
        Label(self, text="changer d'EXERCICE".upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # détails cadre1
        def select(event=None):
            pass
        
        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)
        Label(cadre7, text='EXERCICE', **kw_11).pack(**pad_11, side=LEFT)

        box = Spinbox(cadre7, textvariable=self.var_spin, width=8, from_=2000, to=2100, command=select, **kw_32)
        box.pack(side=LEFT, padx=5)

        # détails cadre2
        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b1.pack_forget()
        
        def refresh():
            self.comment.set('')
            
        def record(event):
            self.master.master.base.fermer()
            self.master.master.base.fix_exercice(self.var_spin.get())
            self.focus_set()
            self.comment.set('OK')
            root.bell()
            root.after(attenteLongue, refresh)
        
        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

       
        b2 = Button(cadre2, text="CONFIRMER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.var_spin.set(self.master.master.base.get_exercice())
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame21(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        self.comment = StringVar()
        self.var_spin = StringVar()

        # structure
        Label(self, text="sélectionner la database".upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # détails cadre1
        def select(event=None):
            pass
            
        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)
        Label(cadre7, text='DATABASE', **kw_11).pack(**pad_11, side=LEFT)

        self.spin = Spinbox(cadre7, textvariable=self.var_spin,
                            from_=2000, to=2100, command=select,
                            width=l_base, **kw_32)
        self.spin.pack(side=LEFT, padx=5)

        # détails cadre2
        
        def refresh():
            self.comment.set('')
            
        def record(event):
            self.master.master.base.fermer()
            self.master.master.base.fix_database(self.var_spin.get())
            self.focus_set()
            self.comment.set('OK')
            root.bell()
            root.after(attenteLongue, refresh)
            
        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

       
        b2 = Button(cadre2, text="CONFIRMER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)
        

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.display_21(var_spin=self.var_spin,
                                           spin=self.spin,
                                           comment=self.comment)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame20(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        cadre1 = Frame(self, **kw_c11)
        cadre1.pack(**pad_c11)

        Label(cadre1, text="EXPORTER L'INVENTAIRE", **kw_10).pack(**pad_10)

        def export(event):
            print('passage dans export')
            Inventory(base=self.master.master.base, file_name="inventaire01.csv").out()

        b1 = Button(cadre1, text='EXPORTER', **kw_45)
        b1.pack(**pad_45)
        b1.bind('<Button-1>', export)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame6(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='ÉDITER LES CATÉGORIES', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###

        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        print('cat', h_03)
        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        Label(cadre1, text="catégorie".upper(), **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###
        b1 = Button(cadre2, text="NOUVELLE CATÉGORIE", **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_6(code=self.code,
                                              list_box=self.list_box,
                                              var_box=self.var_box,
                                              arg=False,
                                              box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command25(arg)

        def add(event):
            self.master.menu.command7()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # liens
        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        b1.bind('<Return>', add)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg=False):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_6(code=self.code,
                                       list_box=self.list_box,
                                       var_box=self.var_box,
                                       arg=self.arg,
                                       box=self.box)
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame35(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='ÉDITER LES TYPES DE CHARGE', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###

        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_type, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_type + 2, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        Label(cadre1, text="TYPE", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###
        b1 = Button(cadre2, text="NOUVEAU TYPE DE CHARGE", **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_35(code=self.code,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               arg=False,
                                               box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command37(arg)

        def add(event):
            self.master.menu.command36()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg=None):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_35(code=self.code,
                                        list_box=self.list_box,
                                        var_box=self.var_box,
                                        arg=self.arg,
                                        box=self.box)
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame10(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###
        Label(self, text='ÉDITER LES ARTICLES', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_03, **kw_28)
        self.box.pack(**pad_28, side=BOTTOM)
        Label(cadre1, text="CODE", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###
        b1 = Button(cadre2, text="NOUVEL ARTICLE", **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_10(code=self.code,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               box=self.box,
                                               arg=False) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command11(arg)

        def add(event):
            self.master.menu.command4(arg='')

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # liens
        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg=None):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.list_10(code=self.code,
                                        list_box=self.list_box,
                                        var_box=self.var_box,
                                        box=self.box,
                                        arg=self.arg)
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame32(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###
        Label(self, text='ARTICLES NON-INVENTORIÉS', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_03, **kw_28)
        self.box.pack(**pad_28, side=BOTTOM)
        Label(cadre1, text="CODE", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###
        b1 = Button(cadre2, text="NOUVEL ARTICLE", width=l_code + 2, **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_32(code=self.code,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               arg=False,
                                               box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command34(arg)

        def add(event):
            self.master.menu.command33(arg='')

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # liens
        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg=False):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.list_32(list_box=self.list_box,
                                        var_box=self.var_box,
                                        code=self.code,
                                        arg=self.arg,
                                        box=self.box)

        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame17(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###
        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)

        ### STRUCTURE ###
        Label(self, text='RÉGULER LES STOCKS', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)

        ### Détails cadre 1 ###
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_08, **kw_28)
        self.box.pack(**pad_28, side=BOTTOM)
        Label(cadre1, text="CODE", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        def add(event):
            self.master.menu.command4(arg=self.code.get().strip())

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def filtrer(event):
            if self.master.master.base.list_10(code=self.code,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               arg=False,
                                               box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command18(arg)

        # liens
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.list_10(code=self.code,
                                        list_box=self.list_box,
                                        var_box=self.var_box,
                                        arg=False,
                                        box=self.box)

        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame5(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='ÉDITER LES TIERS', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###

        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        Label(cadre1, text="NOM", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###
        b1 = Button(cadre2, text="NOUVEAU TIERS", width=l_code, **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_5(code=self.code,
                                              list_box=self.list_box,
                                              var_box=self.var_box,
                                              arg=False,
                                              box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command26(arg)

        def add(event):
            self.master.menu.command8()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg=False):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_5(code=self.code,
                                       list_box=self.list_box,
                                       var_box=self.var_box,
                                       arg=self.arg,
                                       box=self.box)
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame11(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###
        self.code, self.des, self.cat, self.pv, self.stockmin = \
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.envente = IntVar()
        self.comment = StringVar()
        self.art_id = ''

        ### STRUCTURE ###
        Label(self, text='ÉDITER UN ARTICLE', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_des, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='CATÉGORIE', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_code, textvariable=self.cat, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        def check():
            if self.envente.get():
                self.e4.configure(state='normal')
            else:
                self.e4.configure(state='disabled')

        Label(cadre8, text=' PRIX DE VENTE', **kw_11).pack(**pad_11, side=LEFT)
        e6 = Checkbutton(cadre8, variable=self.envente, command=check, **kw_47)
        e6.pack(side=LEFT, **pad_47)
        self.e4 = Entry(cadre8, width=l_pv, textvariable=self.pv, **kw_12)
        self.e4.pack(**pad_12, side=LEFT)

        Label(cadre8, text=' STOCK MINIMUM', **kw_11).pack(**pad_11, side=LEFT)
        e5 = Entry(cadre8, width=l_min, textvariable=self.stockmin, **kw_12)
        e5.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###
        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)
        
        def refresh():
                self.comment.set('')
                back(arg=self.arg)
        
        def record(event):
            self.arg = self.master.master.base.record_11(art_id=self.art_id,
                                                 code=self.code,
                                                 envente=self.envente,
                                                 des=self.des,
                                                 cat=self.cat,
                                                 pv=self.pv,
                                                 stockmin=self.stockmin,
                                                 comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)

        def back(event=None, arg=''):
            self.master.menu.command10(arg = self.arg)

        def on_enter(event):

            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # liens
        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg):

        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.art_id = self.master.master.base.function_2(arg)

        self.code.set(arg)

        self.master.master.base.display_11(art_id=self.art_id,
                                           des=self.des,
                                           cat=self.cat,
                                           envente=self.envente,
                                           pv_widget=self.e4,
                                           pv=self.pv,
                                           stockmin=self.stockmin,
                                           comment=self.comment)

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame14(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        self.arg2 = None

        ### VARIABLES DE CONTROLE ###
        self.arg = ''
        self.dat, self.num, self.type, self.tiers, self.des, self.montant = \
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.amor = IntVar()
        self.repart = IntVar()
        self.mois = StringVar()
        self.debut = StringVar()
        self.comment = StringVar()
        self.titre = StringVar()

        ### STRUCTURE ###

        Label(self, textvariable=self.titre, **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)
        cadre9 = Frame(cadrex, **kw_c8)
        cadre9.pack(**pad_c8)
        cadre11 = Frame(cadrex, **kw_c8)
        cadre11.pack(**pad_c8)

        Label(cadre7, text='DATE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_date, textvariable=self.dat, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        cadre10 = Frame(cadre7, **kw_c8)
        cadre10.pack(side=LEFT, padx=40, fill='x', expand=1)
        Label(cadre10, text='N°PIÈCE', **kw_11).pack(**pad_11, side=LEFT)
        e2 = Entry(cadre10, width=l_num, textvariable=self.num, **kw_12)
        e2.pack(**pad_12, side=LEFT)

        Label(cadre7, text='MONTANT', **kw_11).pack(**pad_11, side=LEFT)
        e10 = Entry(cadre7, width=l_prix, textvariable=self.montant, **kw_12)
        e10.pack(**pad_12, side=LEFT)

        Label(cadre8, text='TYPE DE CHARGE', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_type, textvariable=self.type, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        e4 = Entry(cadre8, width=l_code, textvariable=self.tiers, **kw_12)
        e4.pack(**pad_12, side=RIGHT)
        Label(cadre8, text='TIERS', **kw_11).pack(**pad_11, side=RIGHT)

        def check1():
            if self.repart.get():
                self.e5.configure(state='normal')
                self.e6.configure(state='normal')
                self.amor.set(0)
                self.e6.focus_set()
            else:
                self.e5.configure(state='disabled')
                self.e6.configure(state='disabled')
                self.debut.set('')
                self.mois.set('')

        def check2():
            if self.amor.get():
                self.e5.configure(state='normal')
                self.e6.configure(state='normal')
                self.repart.set(0)
                self.e6.focus_set()
            else:
                self.e5.configure(state='disabled')
                self.e6.configure(state='disabled')
                self.debut.set('')
                self.mois.set('')

        Label(cadre9, text='DESCRIPTION', **kw_11).pack(**pad_11, side=LEFT)
        e9 = Entry(cadre9, width=l_descript, textvariable=self.des, **kw_12)
        e9.pack(**pad_12, side=RIGHT)

        cadre12 = Frame(cadre11, **kw_c8)
        cadre12.pack(side=LEFT, padx=0)
        e7 = Checkbutton(cadre12, text="amortissement".upper(), variable=self.amor, command=check2, **kw_47)
        e7.pack(side=TOP, **pad_47)
        e8 = Checkbutton(cadre12, text="répartition  ".upper(), variable=self.repart, command=check1, **kw_47)
        e8.pack(side=BOTTOM, **pad_47, padx=0)

        cadre13 = Frame(cadre11, **kw_c8)
        cadre13.pack(side=LEFT)

        Label(cadre13, text=' ' * 6 + 'date début'.upper(), **kw_11).pack(**pad_11, side=LEFT)
        self.e6 = Entry(cadre13, width=l_date, textvariable=self.debut, **kw_12)
        self.e6.pack(**pad_12, side=LEFT)

        self.e5 = Entry(cadre11, width=l_qte, textvariable=self.mois, **kw_12)
        self.e5.pack(**pad_12, side=RIGHT)
        Label(cadre11, text='# MOIS', **kw_11).pack(**pad_11, side=RIGHT)

        ### DETAILS STRUCTURE CADRE 2 ###
        def record(event):
            
            etoile()
            self.arg2 = self.master.master.base.record_14(arg=self.arg,
                                                     dat=self.dat,
                                                     num=self.num,
                                                     type=self.type,
                                                     tiers=self.tiers,
                                                     des=self.des,
                                                     montant=self.montant,
                                                     amor=self.amor,
                                                     repart=self.repart,
                                                     comment=self.comment,
                                                     debut=self.debut,
                                                     mois=self.mois)
            if self.arg2 is not None:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()
                
        def erase(event=None):
            self.master.master.base.erase_14(arg=self.arg)
            self.comment.set('Supprimé')
            self.focus_set()
            root.bell()
            root.after(attenteCourte, refresh)

        def back(event=None, arg2=None):
            if self.arg2:
                arg2 = self.arg2
            self.master.menu.command9(arg2)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def etoile(event=None):
            if self.dat.get().strip() == '*':
                self.dat.set(func_8(datetime.now()))

        self.e1.bind('<FocusOut>', etoile)
        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)

        self.b5 = Button(cadre2, text="SUPPRIMER", width=l_button1, takefocus=0, **kw_45)
        self.b4 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)

        self.b4.bind('<ButtonRelease-1>', record)
        self.b5.bind('<ButtonRelease-1>', erase)
        self.b4.bind('<Return>', record)

        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        self.b5.bind('<Enter>', on_enter)
        self.b4.bind('<Enter>', on_enter)
        self.b4.bind('<FocusIn>', on_enter)
        self.b4.bind('<Leave>', on_leave)
        self.b5.bind('<Leave>', on_leave)
        self.b4.bind('<FocusOut>', on_leave)

    def display(self, arg):

        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.arg = arg
        self.arg2 = None

        self.b4.pack_forget()
        self.b5.pack_forget()

        self.dat.set('')
        self.num.set('')
        self.type.set('')
        self.tiers.set('')
        self.montant.set('')
        self.amor.set(0)
        self.des.set('')
        self.repart.set(0)
        self.comment.set('')
        self.debut.set('')
        self.mois.set('')
        self.e5.config(state='disabled')
        self.e6.config(state='disabled')
        if not self.arg:
            self.titre.set('ajouter une charge'.upper())
            self.b4.pack(side='left', **pad_45)
        else:
            # édition
            self.titre.set('éditer une charge'.upper())
            self.b5.pack(side='left', **pad_45)
            self.b4.pack(side='left', **pad_45)
            self.master.master.base.display_14(arg=self.arg,
                                               dat=self.dat,
                                               num=self.num,
                                               type=self.type,
                                               tiers=self.tiers,
                                               des=self.des,
                                               montant=self.montant,
                                               amor=self.amor,
                                               repart=self.repart,
                                               comment=self.comment,
                                               debut=self.debut,
                                               debut_w=self.e6,
                                               mois=self.mois,
                                               mois_w=self.e5)

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame34(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### VARIABLES DE CONTROLE ###

        self.code, self.des, self.cat = StringVar(), StringVar(), StringVar()
        self.comment = StringVar()
        self.non_id = ''

        ### STRUCTURE ###

        Label(self, text='ÉDITER UN ARTICLE NON-INVENTORIÉ', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre7.pack(**pad_c7)
        cadre8.pack(**pad_c8)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_code, textvariable=self.cat, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text=' CATÉGORIE', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_des, textvariable=self.des, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            if self.master.master.base.record_34(non_id=self.non_id,
                                                 code=self.code,
                                                 des=self.des,
                                                 cat=self.cat,
                                                 comment=self.comment):
                back()

        def back(event=None):
            self.master.menu.command32()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b1.bind('<ButtonRelease-1>', back)
        b2.bind('<FocusIn>', on_enter)
        b1.bind('<Enter>', on_enter)
        b2.bind('<FocusOut>', on_leave)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)

    def display(self, arg):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.non_id = self.master.master.base.function_27(arg)

        self.code.set(arg)

        self.master.master.base.display_34(non_id=self.non_id,
                                           cat=self.cat,
                                           des=self.des,
                                           comment=self.comment)

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame12(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        # déclaration des variables
        self.filtre = StringVar()
        self.indice = -1
        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        # structure
        Label(self, text="ÉDITER LES FACTURES D'ACHAT", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # cadre1 détails
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.filtre, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_2, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        item = ligne_2.format('DATE', 'N°PIÈCE', 'TIERS', 'TOTAL')
        Label(cadre1, text=item, width=l_2, **kw_40).pack(side=BOTTOM, **pad_40)

        # cadre 2 détails
        b1 = Button(cadre2, text="NOUVELLE FACTURE D'ACHAT", **kw_45)
        b1.pack(**pad_45)

        # liens
        def select(event):
            i = self.box.curselection()
            if i:
                self.indice = i[0]
                self.master.menu.command27(arg=self.list_ref[self.indice][1])

        def filtrer(event):
            if self.master.master.base.list_12(filtre=self.filtre,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               list_ref=self.list_ref,
                                               arg=False,
                                               box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def add(event):
            self.master.menu.command27(arg=False)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.box.bind('<Return>', select)
        self.e0.bind('<Return>', filtrer)

    def display(self, arg):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_12(list_box=self.list_box,
                                        var_box=self.var_box,
                                        list_ref=self.list_ref,
                                        filtre=self.filtre,
                                        arg=self.arg,
                                        box=self.box)

        # module de sélection
        if arg:
            liste = [e[1] for e in self.list_ref]
            self.indice = liste.index(arg)

        elif self.indice == self.box.size():
            self.indice -= 1

        if self.indice > -1:
            self.box.selection_clear(0, END)
            self.box.selection_set(self.indice)
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame3(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        # déclaration des variables
        self.filtre = StringVar()
        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()
        self.indice = -1

        # structure
        Label(self, text="ÉDITER LES FACTURES DE VENTE", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # cadre1 détails
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.filtre, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_4, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        item = ligne_4.format('DATE', 'CAISSIER(ÈRE)', 'TOTAL')
        Label(cadre1, text=item, width=l_4, **kw_40).pack(side=BOTTOM, **pad_40)

        # cadre 2 détails
        b1 = Button(cadre2, text="ENCODER UNE VENTE", **kw_45)
        b2 = Button(cadre2, text="IMPORTER UNE VENTE", **kw_45)
        b1.pack(**pad_45, side=LEFT)
        b2.pack(**pad_45, side=LEFT)

        # liens
        def select(event):
            i = self.box.curselection()
            if i:
                self.indice = i[0]
                self.master.menu.command15(arg=self.list_ref[self.indice][1])

        def filtrer(event):
            if self.master.master.base.list_3(filtre=self.filtre,
                                              list_box=self.list_box,
                                              var_box=self.var_box,
                                              list_ref=self.list_ref,
                                              arg=False,
                                              box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def add(event):
            self.master.menu.command15(arg=False)

        def importer(event):
            self.master.menu.command58()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1.bind('<ButtonRelease-1>', add)
        b2.bind('<ButtonRelease-1>', importer)
        b1.bind('<Return>', add)
        b2.bind('<Return>', importer)

        b1.bind('<Enter>', on_enter)
        b2.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        b2.bind('<FocusOut>', on_leave)
        self.box.bind('<Return>', select)
        self.e0.bind('<Return>', filtrer)

    def display(self, arg):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_3(filtre=self.filtre,
                                       list_box=self.list_box,
                                       var_box=self.var_box,
                                       list_ref=self.list_ref,
                                       arg=self.arg,
                                       box=self.box)

        ## module de sélection
        # cas de la suppression avec indice qui était le dernier
        if arg:
            liste = [e[1] for e in self.list_ref]
            self.indice = liste.index(arg)

        elif self.indice == self.box.size():
            self.indice -= 1

        if self.indice > -1:
            self.box.selection_clear(0, END)
            self.box.selection_set(self.indice)

        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame9(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        # déclaration des variables
        self.filtre = StringVar()
        self.indice = -1
        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        # structure
        Label(self, text="ÉDITER LES CHARGES", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # cadre1 détails
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.filtre, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_3, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        item = item = ligne_3.format('DATE', 'N°PIÈCE', 'TYPE', 'TIERS', 'MONTANT', '*')
        Label(cadre1, text=item, width=l_3, **kw_40).pack(side=BOTTOM, **pad_40)

        # cadre 2 détails

        b1 = Button(cadre2, text="NOUVELLE CHARGE", **kw_45)
        b1.pack(**pad_45)

        # liens

        def select(event):
            i = self.box.curselection()
            if i:
                self.indice = i[0]
                self.master.menu.command14(arg=self.list_ref[self.indice][1])

        def filtrer(event):
            if self.master.master.base.list_9(filtre=self.filtre,
                                              list_box=self.list_box,
                                              var_box=self.var_box,
                                              list_ref=self.list_ref,
                                              arg2=None,
                                              box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def add(event):
            self.master.menu.command14(arg='')

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.box.bind('<Return>', select)
        self.e0.bind('<Return>', filtrer)

    def display(self, arg2=None):
        self.arg2=arg2
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_9(list_box=self.list_box,
                                       var_box=self.var_box,
                                       list_ref=self.list_ref,
                                       filtre=self.filtre,
                                       arg2=self.arg2,
                                       box=self.box)
        # module de sélection
        if self.indice == self.box.size():
            self.indice -= 1
        if self.indice > -1 and self.indice + 1 <= self.box.size():
            self.box.selection_set(self.indice)
        else:
            self.indice = -1
        self.box.focus_set()

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame13(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='ÉDITER LES EMPLOYÉS', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###

        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_03, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        Label(cadre1, text="NOM", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###

        b1 = Button(cadre2, text="NOUVEL EMPLOYÉ", width=l_code + 1, **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_13(code=self.code,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               arg=False,
                                               box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command29(arg)

        def add(event):
            self.master.menu.command28()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg=False):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_13(code=self.code,
                                        list_box=self.list_box,
                                        var_box=self.var_box,
                                        arg=self.arg,
                                        box=self.box)
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame27(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###

        self.arg = ''
        self.titre = StringVar()
        self.num, self.dat, self.tiers = StringVar(), StringVar(), StringVar()
        self.remise, self.total = StringVar(), StringVar()
        self.list_box, self.list_ref = [], []
        self.var_box = StringVar(value=self.list_box)
        self.code, self.des, self.qte, self.prix = StringVar(), StringVar(), StringVar(), StringVar()
        self.comment = StringVar()

        ### STRUCTURE

        Label(self, textvariable=self.titre, **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ## cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre9 = LabelFrame(cadrex, **kw_c9)
        cadre9.pack(**pad_c9)

        # cadre 7

        Label(cadre7, text='DATE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_date, textvariable=self.dat, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        cadre17 = Frame(cadre7, **kw_c17)
        cadre17.pack(padx=reglage_3, **pad_c17, side=LEFT)
        Label(cadre17, text='N°PIÈCE', **kw_11).pack(**pad_11, side=LEFT)
        e2 = Entry(cadre17, width=l_num, textvariable=self.num, **kw_12)
        e2.pack(**pad_12)

        e3 = Entry(cadre7, width=l_code, textvariable=self.tiers, **kw_12)
        e3.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='TIERS', **kw_11).pack(**pad_11, side=RIGHT)

        # cadre 9

        Label(cadre9, text=ligne_8.format('CODE', 'DÉSIGNATION', 'QTÉ', 'PRIX'), **kw_40).pack(**pad_40)

        self.box = Listbox(cadre9, listvariable=self.var_box, width=l_8, height=h_27, **kw_28)
        self.box.pack(padx=5, **pad_28)

        cadre15 = Frame(cadre9, **kw_c15)
        cadre15.pack(**pad_c15)
        cadre16 = Frame(cadre9, **kw_c16)
        cadre16.pack(**pad_c16)

        cadre13 = Frame(cadre9, **kw_c13)
        cadre13.pack(**pad_c13)

        cadre14 = Frame(cadre9, **kw_c14)
        cadre14.pack(**pad_c14)

        # cadre 15

        e4 = Entry(cadre15, textvariable=self.remise, width=l_prix, takefocus=0, **kw_12)
        e4.pack(side='right')
        Label(cadre15, text='REMISE', **kw_11).pack(**pad_11, side='right')

        # cadre 16

        e5 = Entry(cadre16, textvariable=self.total, width=l_prix, state='disabled', **kw_12)
        e5.pack(side='right')
        Label(cadre16, text='TOTAL', **kw_11).pack(**pad_11, side='right')

        # cadre 13

        Label(cadre13, text=ligne_8.format('CODE', 'DÉSIGNATION', 'QTÉ', 'PRIX'), **kw_40).pack(**pad_40)
        cadre12 = Frame(cadre13, **kw_c12)
        cadre12.pack(**pad_c12)

        # cadre 12

        e7 = Entry(cadre12, textvariable=self.code, width=l_code, **kw_12)
        e7.pack(side=LEFT, padx=5, )
        e8 = Entry(cadre12, textvariable=self.des, width=l_des, state='disabled', **kw_12)
        e8.pack(side=LEFT, padx=reglage_2, )
        e9 = Entry(cadre12, textvariable=self.qte, width=l_qte, **kw_12)
        e9.pack(side=LEFT, padx=0, )
        e10 = Entry(cadre12, textvariable=self.prix, width=l_prix, **kw_12)
        e10.pack(side=RIGHT, padx=5, )

        # cadre 14

        b3 = Button(cadre14, text="EFFACER", width=l_button1, takefocus=0, **kw_45)
        b3.pack(side='left', pady=5, **pad_45)
        b1 = Button(cadre14, text='VALIDER', width=l_button1, **kw_45)
        b1.pack(side='left', pady=5, **pad_45)

        ### détails dans cadre 2

        b2 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b2.pack(side='left', **pad_45)
        self.b5 = Button(cadre2, text="SUPPRIMER", width=l_button1, takefocus=0, **kw_45)
        self.b4 = Button(cadre2, text="ENREGISTRER", width=l_button1, takefocus=0, **kw_45)

        def delete(event):
            self.code.set('')
            self.des.set('')
            self.qte.set('')
            self.prix.set('')
            self.comment.set('')

        def validate(event):

            hide_selection()
            self.master.master.base.validate_27(code=self.code,
                                                des=self.des,
                                                qte=self.qte,
                                                prix=self.prix,
                                                list_box=self.list_box,
                                                list_ref=self.list_ref,
                                                var_box=self.var_box,
                                                comment=self.comment,
                                                remise=self.remise,
                                                total=self.total)

            e7.focus_set()
            e7.icursor(END)

        def back(event=None, arg2=None):
            self.master.menu.command12(arg2)

        def record(event):
            etoile()
            hide_selection()
            self.arg2 = self.master.master.base.record_27(code=self.code,
                                                     des=self.des,
                                                     qte=self.qte,
                                                     prix=self.prix,
                                                     list_box=self.list_box,
                                                     list_ref=self.list_ref,
                                                     comment=self.comment,
                                                     remise=self.remise,
                                                     total=self.total,
                                                     tiers=self.tiers,
                                                     dat=self.dat,
                                                     num=self.num,
                                                     arg=self.arg)
            if self.arg2 is not None:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
        
        def refresh():
                self.comment.set('')
                back(arg2=self.arg2)
                
        def erase(event=None):
            self.master.master.base.erase_27(arg=self.arg)
            self.comment.set('Supprimé')
            self.focus_set()
            root.bell()
            root.after(attenteCourte, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def design(event):
            self.des.set(self.master.master.base.function_3(self.code.get().strip()))

        def hide_selection(event=None):
            self.box.selection_clear(0, END)

        def select(event):
            tup = self.box.curselection()
            if tup:
                indice = tup[0]
                self.master.master.base.select_27(indice=indice,
                                                  list_box=self.list_box,
                                                  var_box=self.var_box,
                                                  list_ref=self.list_ref,
                                                  code=self.code,
                                                  des=self.des,
                                                  qte=self.qte,
                                                  prix=self.prix,
                                                  total=self.total)
                hide_selection()
                e7.focus_set()
                e7.icursor(END)

        def etoile(event=None):
            if self.dat.get().strip() == '*':
                self.dat.set(func_8(datetime.now()))

        self.e1.bind('<FocusOut>', etoile)
        b1.bind('<ButtonRelease-1>', validate)
        b1.bind('<Return>', validate)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)
        b3.bind('<Enter>', on_enter)
        b3.bind('<Leave>', on_leave)
        self.b4.bind('<Enter>', on_enter)
        self.b4.bind('<Leave>', on_leave)
        self.b5.bind('<Enter>', on_enter)
        self.b5.bind('<Leave>', on_leave)
        e7.bind('<FocusOut>', design)
        self.b4.bind('<ButtonRelease-1>', record)
        b2.bind('<ButtonRelease-1>', back)
        b3.bind('<ButtonRelease-1>', delete)
        self.b5.bind('<ButtonRelease-1>', erase)
        self.box.bind("<Return>", select)
        self.box.bind("<FocusOut>", hide_selection)

    def display(self, arg):

        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.b4.pack_forget()
        self.b5.pack_forget()

        self.list_box = []
        self.list_ref = []
        self.var_box.set(value=self.list_box)

        if not arg:
            self.titre.set("AJOUTER UNE FACTURE D'ACHAT")
            self.b4.pack(side='left', **pad_45)
            self.dat.set('')
            self.num.set('')
            self.tiers.set('')
            self.total.set(func_5(0))
            self.remise.set('')

        else:
            self.titre.set("ÉDITER UNE FACTURE D'ACHAT")
            self.b5.pack(side='left', **pad_45)
            self.b4.pack(side='left', **pad_45)
            self.master.master.base.display_27(
                list_box=self.list_box,
                list_ref=self.list_ref,
                num=self.num,
                dat=self.dat,
                tiers=self.tiers,
                remise=self.remise,
                total=self.total,
                var_box=self.var_box,
                arg=self.arg)

        self.code.set('')
        self.des.set('')
        self.qte.set('')
        self.prix.set('')
        self.comment.set('')
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame15(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        # VARIABLES DE CONTROLE #
        self.arg = False
        self.titre = StringVar()
        self.dat, self.caisse = StringVar(), StringVar()
        self.total = StringVar()
        self.list_box, self.list_ref = [], []
        self.var_box = StringVar(value=self.list_box)
        self.code, self.des, self.qte, self.prix = StringVar(), StringVar(), StringVar(), StringVar()
        self.comment = StringVar()

        # STRUCTURE
        Label(self, textvariable=self.titre, **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ## cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre9 = LabelFrame(cadrex, **kw_c9)
        cadre9.pack(**pad_c9)

        # cadre 7
        Label(cadre7, text='DATE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_date, textvariable=self.dat, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)
        e3 = Entry(cadre7, width=l_code, textvariable=self.caisse, **kw_12)
        e3.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='CAISSIER(ÈRE)', **kw_11).pack(**pad_11, side=RIGHT)

        # cadre 9
        Label(cadre9, text=ligne_8.format('CODE', 'DÉSIGNATION', 'QTÉ', 'PRIX'), **kw_40).pack(**pad_40)

        self.box = Listbox(cadre9, listvariable=self.var_box, width=l_8, height=h_15, **kw_28)
        self.box.pack(padx=5, **pad_28)

        cadre16 = Frame(cadre9, **kw_c16)
        cadre16.pack(**pad_c16)

        cadre13 = Frame(cadre9, **kw_c13)
        cadre13.pack(**pad_c13)

        cadre14 = Frame(cadre9, **kw_c14)
        cadre14.pack(**pad_c14)

        # cadre 16

        e5 = Entry(cadre16, textvariable=self.total, width=l_prix, state='disabled', **kw_12)
        e5.pack(side='right')
        Label(cadre16, text='TOTAL', **kw_11).pack(**pad_11, side='right')

        # cadre 13

        Label(cadre13, text=ligne_8.format('CODE', 'DÉSIGNATION', 'QTÉ', 'PRIX'), **kw_40).pack(**pad_40)
        cadre12 = Frame(cadre13, **kw_c12)
        cadre12.pack(**pad_c12)

        # cadre 12

        e7 = Entry(cadre12, textvariable=self.code, width=l_code, **kw_12)
        e7.pack(side=LEFT, padx=5, )
        e8 = Entry(cadre12, textvariable=self.des, width=l_des, state='disabled', **kw_12)
        e8.pack(side=LEFT, padx=reglage_2, )
        e9 = Entry(cadre12, textvariable=self.qte, width=l_qte, **kw_12)
        e9.pack(side=LEFT, padx=0, )
        e10 = Entry(cadre12, textvariable=self.prix, width=l_prix, **kw_12)
        e10.pack(side=RIGHT, padx=5, )

        # cadre 14

        b3 = Button(cadre14, text="EFFACER", width=l_button1, takefocus=0, **kw_45)
        b3.pack(side='left', pady=5, **pad_45)
        b1 = Button(cadre14, text='VALIDER', width=l_button1, **kw_45)
        b1.pack(side='left', pady=5, **pad_45)

        ### détails dans cadre 2
        b2 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b2.pack(side='left', **pad_45)
        self.b5 = Button(cadre2, text="SUPPRIMER", width=l_button1, takefocus=0, **kw_45)
        self.b4 = Button(cadre2, text="ENREGISTRER", width=l_button1, takefocus=0, **kw_45)

        def delete(event):
            self.code.set('')
            self.des.set('')
            self.qte.set('')
            self.prix.set('')
            self.comment.set('')

        def validate(event):
            hide_selection()
            self.master.master.base.validate_15(code=self.code,
                                                des=self.des,
                                                qte=self.qte,
                                                prix=self.prix,
                                                list_box=self.list_box,
                                                list_ref=self.list_ref,
                                                var_box=self.var_box,
                                                comment=self.comment,
                                                total=self.total)
            e7.focus_set()
            e7.icursor(END)

        def back(event=None):
            self.master.menu.command3(arg=self.arg)

        def record(event):
            etoile()
            hide_selection()
            self.arg = self.master.master.base.record_15(code=self.code,
                                                    des=self.des,
                                                    qte=self.qte,
                                                    prix=self.prix,
                                                    list_box=self.list_box,
                                                    list_ref=self.list_ref,
                                                    comment=self.comment,
                                                    total=self.total,
                                                    caisse=self.caisse,
                                                    dat=self.dat,
                                                    arg=self.arg)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
        
        def refresh():
                self.comment.set('')
                back()
                
        def erase(event=None):
            if self.master.master.base.erase_15(arg=self.arg):
                self.arg = False
                self.comment.set('Supprimé')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def design(event):
            self.des.set(self.master.master.base.function_3(self.code.get().strip()))

        def hide_selection(event=None):
            self.box.selection_clear(0, END)

        def select(event):
            tup = self.box.curselection()
            if tup:
                indice = tup[0]
                self.master.master.base.select_27(indice=indice,
                                                  list_box=self.list_box,
                                                  var_box=self.var_box,
                                                  list_ref=self.list_ref,
                                                  code=self.code,
                                                  des=self.des,
                                                  qte=self.qte,
                                                  prix=self.prix,
                                                  total=self.total)
                hide_selection()
                e7.focus_set()
                e7.icursor(END)

        def etoile(event=None):
            if self.dat.get().strip() == '*':
                self.dat.set(func_8(datetime.now()))

        self.e1.bind('<FocusOut>', etoile)
        b1.bind('<ButtonRelease-1>', validate)
        b1.bind('<Return>', validate)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)
        b3.bind('<Enter>', on_enter)
        b3.bind('<Leave>', on_leave)
        self.b4.bind('<Enter>', on_enter)
        self.b4.bind('<Leave>', on_leave)
        self.b5.bind('<Enter>', on_enter)
        self.b5.bind('<Leave>', on_leave)
        e7.bind('<FocusOut>', design)
        self.b4.bind('<ButtonRelease-1>', record)
        b2.bind('<ButtonRelease-1>', back)
        b3.bind('<ButtonRelease-1>', delete)
        self.b5.bind('<ButtonRelease-1>', erase)
        self.box.bind("<Return>", select)
        self.box.bind("<FocusOut>", hide_selection)

    def display(self, arg):
        self.arg = arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.b4.pack_forget()
        self.b5.pack_forget()

        self.list_box = []
        self.list_ref = []
        self.var_box.set(value=self.list_box)

        if not self.arg:
            self.titre.set("AJOUTER UNE FACTURE DE VENTE")
            self.b4.pack(side='left', **pad_45)
            self.dat.set('')
            self.caisse.set('')
            self.total.set(func_5(0))

        else:
            self.titre.set("ÉDITER UNE FACTURE DE VENTE")
            self.b5.pack(side='left', **pad_45)
            self.b4.pack(side='left', **pad_45)
            self.master.master.base.display_15(list_box=self.list_box,
                                               list_ref=self.list_ref,
                                               dat=self.dat,
                                               caisse=self.caisse,
                                               total=self.total,
                                               var_box=self.var_box,
                                               arg=self.arg)
        self.code.set('')
        self.des.set('')
        self.qte.set('')
        self.prix.set('')
        self.comment.set('')
        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame22(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### déclaration des vaiables ###

        self.code = StringVar()
        self.list_box = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        ### STRUCTURE ###
        Label(self, text='ÉDITER LES COMPOSÉS', **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        ### Détails cadre 1 ###
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.code, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_code + 2, height=h_03, **kw_28)
        self.box.pack(**pad_28, side=BOTTOM)
        Label(cadre1, text="CODE", **kw_40, width=l_code).pack(**pad_40, side=BOTTOM)

        ### Détails cadre 2 ###
        b1 = Button(cadre2, text="NOUVEAU COMPOSÉ", width=l_code + 2, **kw_45)
        b1.pack(**pad_45)

        def filtrer(event):
            if self.master.master.base.list_22(code=self.code,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               arg=False,
                                               box=self.box) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def select(event):
            i = self.box.curselection()
            if i:
                arg = self.box.get(i[0]).strip()
                self.master.menu.command24(arg)

        def add(event):
            self.master.menu.command23(arg='')

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # liens
        b1.bind('<ButtonRelease-1>', add)
        b1.bind('<Return>', add)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        self.e0.bind('<Return>', filtrer)
        self.box.bind('<Return>', select)

    def display(self, arg):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.master.master.base.list_22(list_box=self.list_box,
                                        var_box=self.var_box,
                                        code=self.code,
                                        arg=self.arg,
                                        box=self.box)

        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame23(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        ### VARIABLES DE CONTROLE ###

        self.code = StringVar()
        self.des = StringVar()
        self.cat = StringVar()
        self.pv = StringVar()

        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        self.code_i = StringVar()
        self.des_i = StringVar()
        self.proportion = StringVar()
        self.envente = IntVar()
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='AJOUTER UN ARTICLE COMPOSÉ', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)

        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)
        cadre9 = LabelFrame(cadrex, text='composition', **kw_c9)
        cadre9.pack(**pad_c9)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_des, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='CATÉGORIE', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_code, textvariable=self.cat, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        def check():
            hide_selection()
            if self.envente.get():
                e4.configure(state='normal')
            else:
                e4.configure(state='disabled')

        e4 = Entry(cadre8, width=l_pv, textvariable=self.pv, **kw_12)
        e4.pack(**pad_12, side=RIGHT)
        e6 = Checkbutton(cadre8, variable=self.envente, command=check, **kw_47)
        e6.pack(side=RIGHT, **pad_47)
        Label(cadre8, text='PRIX DE VENTE', **kw_11).pack(**pad_11, side=RIGHT)

        ### détails dans le cadre 9 (inclus dans le cadre 1)

        Label(cadre9, text=ligne_7.format('CODE', 'DÉSIGNATION', 'PROPORTION'), **kw_40).pack(**pad_40)

        self.box = Listbox(cadre9, listvariable=self.var_box, width=l_7, height=h_09, **kw_28)
        self.box.pack(**pad_28)

        cadre13 = Frame(cadre9, **kw_c13)
        cadre13.pack(**pad_c13)

        Label(cadre13, text=ligne_7.format('CODE', 'DÉSIGNATION', 'PROPORTION'), **kw_40).pack(**pad_40)

        cadre12 = Frame(cadre13, **kw_c12)
        cadre12.pack(**pad_c12)

        e7 = Entry(cadre12, textvariable=self.code_i, width=l_code, **kw_12)
        e7.pack(side=LEFT, padx=5, )
        e8 = Entry(cadre12, textvariable=self.des_i, width=l_des, state='disabled', **kw_12)
        e8.pack(side=LEFT, padx=reglage_1, )
        e9 = Entry(cadre12, textvariable=self.proportion, width=l_proportion, **kw_12)
        e9.pack(side=LEFT, padx=5, )

        cadre14 = Frame(cadre9, **kw_c14)
        cadre14.pack(**pad_c14)

        b3 = Button(cadre14, text="EFFACER", width=l_button1, takefocus=0, **kw_45)
        b3.pack(side='left', pady=5, **pad_45)

        b1 = Button(cadre14, text='VALIDER', width=l_button1, **kw_45)
        b1.pack(pady=5, **pad_45)

        ### détails dans cadre 2

        b2 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b2.pack(side='left', **pad_45)

        b4 = Button(cadre2, text="ENREGISTRER", width=l_button1, takefocus=0, **kw_45)
        b4.pack(side='left', **pad_45)

        def delete(event):
            self.code_i.set('')
            self.des_i.set('')
            self.proportion.set('')
            self.comment.set('')

        def validate(event):
            hide_selection()
            self.master.master.base.validate_23(code=self.code,
                                                des_i=self.des_i,
                                                code_i=self.code_i,
                                                list_box=self.list_box,
                                                list_ref=self.list_ref,
                                                var_box=self.var_box,
                                                comment=self.comment,
                                                proportion=self.proportion)
            e7.focus_set()
            e7.icursor(END)

        def back(event=None, arg=False):
            self.master.menu.command22(arg)

        def record(event):
            hide_selection()
            self.arg = self.master.master.base.record_23(code=self.code,
                                                    des=self.des,
                                                    cat=self.cat,
                                                    pv=self.pv,
                                                    code_i=self.code_i,
                                                    des_i=self.des_i,
                                                    proportion=self.proportion,
                                                    envente=self.envente,
                                                    list_ref=self.list_ref,
                                                    comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
            else:
                self.e1.focus_set()
                self.e1.icursor(END)
            
        def refresh():
            self.comment.set('')
            back(arg=self.arg)    
                
        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def design(event):
            self.des_i.set(self.master.master.base.function_3(self.code_i.get().strip()))

        def hide_selection(event=None):
            self.box.selection_clear(0, END)

        def select(event):
            tup = self.box.curselection()
            if tup:
                indice = tup[0]
                self.master.master.base.select_24(indice=indice,
                                                  list_box=self.list_box,
                                                  var_box=self.var_box,
                                                  list_ref=self.list_ref,
                                                  code_i=self.code_i,
                                                  des_i=self.des_i,
                                                  proportion=self.proportion)
                hide_selection()
                e7.focus_set()
                e7.icursor(END)

        b1.bind('<ButtonRelease-1>', validate)
        b1.bind('<Return>', validate)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)
        b3.bind('<Enter>', on_enter)
        b3.bind('<Leave>', on_leave)
        b4.bind('<Enter>', on_enter)
        b4.bind('<Leave>', on_leave)
        e7.bind('<FocusOut>', design)
        b4.bind('<ButtonRelease-1>', record)
        b2.bind('<ButtonRelease-1>', back)
        b3.bind('<ButtonRelease-1>', delete)
        self.box.bind("<Return>", select)
        self.box.bind("<FocusOut>", hide_selection)

    def display(self, arg=''):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.code.set(arg)
        self.des.set('')
        self.cat.set('')
        self.pv.set('')

        self.list_box = []
        self.list_ref = []
        self.code_i.set('')
        self.des_i.set('')
        self.proportion.set('')
        self.envente.set(1)
        self.comment.set('')

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame24(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###
        self.code = StringVar()
        self.des = StringVar()
        self.cat = StringVar()
        self.pv = StringVar()

        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        self.code_i = StringVar()
        self.des_i = StringVar()
        self.proportion = StringVar()
        self.envente = IntVar()
        self.comment = StringVar()

        ### STRUCTURE DE c1 ###
        Label(self, text="ÉDITER UN COMPOSÉ", **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)
        # cadre 9 : contient la listbox
        cadre9 = LabelFrame(cadrex, text='composition', **kw_c9)
        cadre9.pack(**pad_c9)

        ## détails des c7 et c8

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_des, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='DÉSIGNATION', **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre8, text='CATÉGORIE', **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_code, textvariable=self.cat, **kw_12)
        e3.pack(**pad_12, side=LEFT)

        def check():
            hide_selection()
            if self.envente.get():
                self.e4.configure(state='normal')
            else:
                self.e4.configure(state='disabled')

        self.e4 = Entry(cadre8, width=l_pv, textvariable=self.pv, **kw_12)
        self.e4.pack(**pad_12, side=RIGHT)
        e6 = Checkbutton(cadre8, variable=self.envente, command=check, **kw_47)
        e6.pack(side=RIGHT, **pad_47)
        Label(cadre8, text='PRIX DE VENTE', **kw_11).pack(**pad_11, side=RIGHT)

        ## structure de c9

        # étiquette de la listbox
        Label(cadre9, text=ligne_7.format('CODE', 'DÉSIGNATION', 'PROPORTION'), **kw_40).pack(**pad_40)
        # listbox
        self.box = Listbox(cadre9, listvariable=self.var_box, width=l_7, height=h_09, **kw_28)
        self.box.pack(**pad_28)
        # zone d'encodage
        cadre13 = Frame(cadre9, **kw_c13)
        cadre13.pack(**pad_c13)
        # buttons
        cadre14 = Frame(cadre9, **kw_c14)
        cadre14.pack(**pad_c14)

        # détails dans le cadre 13
        Label(cadre13, text=ligne_7.format('CODE', 'DÉSIGNATION', 'PROPORTION'), **kw_40).pack(**pad_40)
        cadre12 = Frame(cadre13, **kw_c12)
        cadre12.pack(**pad_c12)
        e7 = Entry(cadre12, textvariable=self.code_i, width=l_code, **kw_12)
        e7.pack(side=LEFT, padx=5, )
        e8 = Entry(cadre12, textvariable=self.des_i, width=l_des, state='disabled', **kw_12)
        e8.pack(side=LEFT, padx=reglage_1, )
        e9 = Entry(cadre12, textvariable=self.proportion, width=l_proportion, **kw_12)
        e9.pack(side=LEFT, padx=5, )

        # détails cadre 14
        b3 = Button(cadre14, text="EFFACER", width=l_button1, takefocus=0, **kw_45)
        b3.pack(pady=5, side='left', **pad_45)
        b1 = Button(cadre14, text='VALIDER', width=l_button1, **kw_45)
        b1.pack(pady=5, **pad_45)

        ### détails dans cadre 2
        b2 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b2.pack(side='left', **pad_45)
        b4 = Button(cadre2, text="ENREGISTRER", width=l_button1, takefocus=0, **kw_45)
        b4.pack(side='left', **pad_45)

        def delete(event):
            self.code_i.set('')
            self.des_i.set('')
            self.proportion.set('')
            self.comment.set('')

        def validate(event):
            hide_selection()
            self.master.master.base.validate_23(code=self.code,
                                                des_i=self.des_i,
                                                code_i=self.code_i,
                                                list_box=self.list_box,
                                                list_ref=self.list_ref,
                                                var_box=self.var_box,
                                                comment=self.comment,
                                                proportion=self.proportion)
            e7.focus_set()
            e7.icursor(END)

        def back(event=None, arg=''):
            self.master.menu.command22(arg)

        def record(event):
            hide_selection()
            self.arg = self.master.master.base.record_24(compo_id=self.compo_id,
                                                    code=self.code,
                                                    des=self.des,
                                                    cat=self.cat,
                                                    pv=self.pv,
                                                    code_i=self.code_i,
                                                    des_i=self.des_i,
                                                    proportion=self.proportion,
                                                    envente=self.envente,
                                                    list_ref=self.list_ref,
                                                    comment=self.comment)
            if self.arg:
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
        
        def refresh():
                self.comment.set('')
                back(arg=self.arg)
                
        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def design(event):
            self.des_i.set(self.master.master.base.function_3(self.code_i.get().strip()))

        def hide_selection(event=None):
            self.box.selection_clear(0, END)

        def select(event):
            tup = self.box.curselection()
            if tup:
                indice = tup[0]
                self.master.master.base.select_24(indice=indice,
                                                  list_box=self.list_box,
                                                  var_box=self.var_box,
                                                  list_ref=self.list_ref,
                                                  code_i=self.code_i,
                                                  des_i=self.des_i,
                                                  proportion=self.proportion)
                # hide_selection()
                e7.focus_set()
                e7.icursor(END)

        b1.bind('<ButtonRelease-1>', validate)
        b1.bind('<Return>', validate)
        b1.bind('<Enter>', on_enter)
        b1.bind('<FocusIn>', on_enter)
        b1.bind('<Leave>', on_leave)
        b1.bind('<FocusOut>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)
        b3.bind('<Enter>', on_enter)
        b3.bind('<Leave>', on_leave)
        b4.bind('<Enter>', on_enter)
        b4.bind('<Leave>', on_leave)
        e7.bind('<FocusOut>', design)
        b4.bind('<ButtonRelease-1>', record)
        b2.bind('<ButtonRelease-1>', back)
        b3.bind('<ButtonRelease-1>', delete)
        self.box.bind("<Return>", select)
        self.box.bind('<FocusOut>', hide_selection)

    def display(self, arg):
        self.arg=arg
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.compo_id = self.master.master.base.function_4(arg)

        self.code.set(arg)
        self.list_box.clear()
        self.list_ref.clear()
        self.code_i.set('')
        self.proportion.set('')
        self.des_i.set('')

        self.master.master.base.display_24(compo_id=self.compo_id,
                                           list_box=self.list_box,
                                           list_ref=self.list_ref,
                                           var_box=self.var_box,
                                           code=self.code,
                                           des=self.des,
                                           cat=self.cat,
                                           pv=self.pv,
                                           pv_widget=self.e4,
                                           envente=self.envente,
                                           comment=self.comment)

        self.e1.focus_set()
        self.e1.icursor(END)

        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame39(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###
        self.arg = ''
        self.explication = StringVar()
        self.comment = StringVar()
        self.ph = StringVar()
        self.th = StringVar()
        self.des = StringVar()
        self.dat = StringVar()
        self.code = StringVar()
        self.corr = StringVar()

        # structure
        Label(self, text="EXPLIQUER UNE CORRECTION", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # détails cadre 1
        cadrex = Frame(cadre1, **kw_cx)
        cadrex.pack(side=LEFT)
        cadre7 = Frame(cadrex, **kw_c7)
        cadre7.pack(**pad_c7)
        cadre8 = Frame(cadrex, **kw_c8)
        cadre8.pack(**pad_c8)
        cadre9 = Frame(cadrex, **kw_c8)
        cadre9.pack(**pad_c8)

        Label(cadre7, text='CODE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, state='disabled', **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        Label(cadre7, text=' DÉSIGNATION', **kw_11).pack(**pad_11, side=LEFT)
        e2 = Entry(cadre7, width=l_des, textvariable=self.des, state='disabled', **kw_12)
        e2.pack(**pad_12, side=LEFT)

        Label(cadre8, text='{}'.format('STOCK THEORIQUE'), **kw_11).pack(**pad_11, side=LEFT)
        e3 = Entry(cadre8, width=l_qte, textvariable=self.th, state='disabled', **kw_12)
        e3.pack(**pad_12, side=LEFT)

        Label(cadre8, text='{}'.format(' STOCK PHYSIQUE'), **kw_11).pack(**pad_11, side=LEFT)
        e4 = Entry(cadre8, width=l_qte, textvariable=self.ph, state='disabled', **kw_12)
        e4.pack(**pad_12, side=LEFT)

        e5 = Entry(cadre8, width=l_qte, textvariable=self.corr, state='disabled', **kw_12)
        e5.pack(**pad_12, side=RIGHT)
        Label(cadre8, text='{}'.format('CORRECTION'), **kw_11).pack(**pad_11, side=RIGHT)

        Label(cadre9, text='EXPLICATION', **kw_11).pack(**pad_11, side=LEFT)
        self.e6 = Entry(cadre9, width=l_explication, textvariable=self.explication, **kw_12)
        self.e6.pack(**pad_12, side=RIGHT)

        def record(event):
            if self.master.master.base.record_39(arg=self.arg,
                                                 explication=self.explication,
                                                 comment=self.comment):
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        def back(event=None):
            self.master.menu.command19()

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.arg = arg
        self.master.master.base.display_39(arg=self.arg,
                                           dat=self.dat,
                                           ph=self.ph,
                                           th=self.th,
                                           corr=self.corr,
                                           code=self.code,
                                           des=self.des,
                                           explication=self.explication,
                                           comment=self.comment)

        self.e6.focus_set()
        self.e6.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame19(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### VARIABLES DE CONTROLE ###
        self.indice = -1
        self.filtre = StringVar()
        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        # self.comment = StringVar()

        # structure
        Label(self, text="EXPLIQUER LES CORRECTIONS", **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        # cadre2 = Frame(self, **kw_c2)
        # cadre2.pack(**pad_c2)
        # Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # détails c1
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.filtre, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        item = ligne_5.format('DATE', 'CODE', '+/-', 'EXPLICATION')

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_5, height=h_08, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        Label(cadre1, text=item, **kw_40).pack(side=BOTTOM, **pad_40)

        def select(event):
            i = self.box.curselection()
            if i:
                self.indice = self.box.curselection()[0]
                self.master.menu.command39(arg=self.list_ref[self.indice][1])

        def filtrer(event):
            if self.master.master.base.list_19(filtre=self.filtre,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               list_ref=self.list_ref) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # b1.bind('<Enter>', on_enter)
        # b1.bind('<Leave>', on_leave)
        self.box.bind('<Return>', select)
        self.e0.bind('<Return>', filtrer)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_19(list_box=self.list_box,
                                        var_box=self.var_box,
                                        list_ref=self.list_ref,
                                        filtre=self.filtre)
        # module de sélection
        if self.indice == self.box.size():
            self.indice -= 1
        if self.indice > -1 and self.indice + 1 <= self.box.size():
            self.box.selection_set(self.indice)
        else:
            self.indice = -1
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame53(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)

        ### VARIABLES DE CONTROLE ###
        self.indice = -1
        self.filtre = StringVar()
        self.list_box = []
        self.list_ref = []
        self.var_box = StringVar(value=self.list_box)
        self.comment = StringVar()

        # structure
        Label(self, text="Ouvrir un document".upper(), **kw_42).pack(**pad_42)
        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(pady=p_03, **pad_c1)
        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)
        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        # détails c1
        cadre20 = Frame(cadre1, **kw_c20)
        cadre20.pack(side=TOP, **pad_c20)
        Label(cadre20, text='SÉLECTION', **kw_11).pack(side=LEFT, **pad_11)
        self.e0 = Entry(cadre20, textvariable=self.filtre, width=l_code, **kw_12)
        self.e0.pack(side=LEFT, **pad_12)
        item = 'DOCUMENTS'

        self.box = Listbox(cadre1, listvariable=self.var_box, width=l_filename + 8, height=h_10, **kw_28)
        self.box.pack(side=BOTTOM, **pad_28)
        Label(cadre1, text=item, **kw_40).pack(side=BOTTOM, **pad_40)

        def select(event):
            i = self.box.curselection()
            if i:
                self.indice = self.box.curselection()[0]
                self.master.master.base.document_53(comment=self.comment,
                                                    filename=self.list_ref[self.indice][1:])

        def filtrer(event):
            if self.master.master.base.list_53(filtre=self.filtre,
                                               list_box=self.list_box,
                                               var_box=self.var_box,
                                               list_ref=self.list_ref) == 1:
                self.box.selection_set(0)
                self.box.focus_set()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        # b1.bind('<Enter>', on_enter)
        # b1.bind('<Leave>', on_leave)
        self.box.bind('<Return>', select)
        self.e0.bind('<Return>', filtrer)

    def display(self):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.master.master.base.list_53(list_box=self.list_box,
                                        var_box=self.var_box,
                                        list_ref=self.list_ref,
                                        filtre=self.filtre)
        # module de sélection
        if self.indice == self.box.size():
            self.indice -= 1
        if self.indice > -1 and self.indice + 1 <= self.box.size():
            self.box.selection_set(self.indice)
        else:
            self.indice = -1
        self.box.focus_set()
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame25(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master

        ### VARIABLES DE CONTROLE ###

        self.code = StringVar()
        self.arg = ''
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='ÉDITER UNE CATÉGORIE', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)

        Label(cadre7, text='catégorie'.upper(), **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            if self.master.master.base.record_25(arg=self.arg,
                                                 code=self.code,
                                                 comment=self.comment):
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        def erase(event):
            if self.master.master.base.erase_25(arg=self.arg,
                                                code=self.code,
                                                comment=self.comment):
                
                self.comment.set('Supprimé')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def back(event=None):
            self.master.menu.command6()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b3 = Button(cadre2, text="SUPPRIMER", width=l_button1, takefocus=0, **kw_45)
        b3.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b3.bind('<ButtonRelease-1>', erase)
        b3.bind('<Return>', erase)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b3.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b3.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.arg = arg
        self.code.set(arg)
        self.comment.set('')

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame37(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###

        self.code = StringVar()
        self.arg = ''
        self.comment = StringVar()

        ### STRUCTURE ###

        Label(self, text='ÉDITER UN TYPE DE CHARGE', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)

        Label(cadre7, text='TYPE', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_type, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        ### DETAILS STRUCTURE CADRE 2 ###

        def record(event):
            if self.master.master.base.record_37(arg=self.arg,
                                                 code=self.code,
                                                 comment=self.comment):
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        def back(event=None):
            self.master.menu.command35()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<Leave>', on_leave)

    def display(self, arg):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()
        self.arg = arg
        self.code.set(arg)
        self.comment.set('')

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame26(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###
        
        self.code, self.des = StringVar(), StringVar()
        self.comment = StringVar()
        self.arg = ''

        ### STRUCTURE ###

        Label(self, text='ÉDITER UN TIERS', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)

        Label(cadre7, text='NOM', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_contact, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='CONTACT', **kw_11).pack(**pad_11, side=RIGHT)

        def record(event):
            if self.master.master.base.record_26(arg=self.arg,
                                                 code=self.code,
                                                 des=self.des,
                                                 comment=self.comment):
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        #### Détails de la structure dans CADRE 2 ###

        def back(event=None):
            self.master.menu.command5()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.arg = arg
        self.master.master.base.display_26(arg=self.arg,
                                           code=self.code,
                                           des=self.des,
                                           comment=self.comment)

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


class Frame29(Frame):

    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure(**kw_fx)
        root = self.master.master.master
        
        ### VARIABLES DE CONTROLE ###

        self.code, self.des = StringVar(), StringVar()
        self.comment = StringVar()
        self.arg = ''

        ### STRUCTURE ###

        Label(self, text='ÉDITER UN EMPLOYÉ', **kw_42).pack(**pad_42)

        cadre1 = Frame(self, **kw_c1)
        cadre1.pack(**pad_c1)

        cadre2 = Frame(self, **kw_c2)
        cadre2.pack(**pad_c2)

        Label(self, textvariable=self.comment, **kw_14).pack(**pad_14)

        #### Détails de la structure dans CADRE 1 ###

        cadre7 = Frame(cadre1, **kw_c7)
        cadre7.pack(side=LEFT, **pad_c7)

        Label(cadre7, text='NOM', **kw_11).pack(**pad_11, side=LEFT)
        self.e1 = Entry(cadre7, width=l_code, textvariable=self.code, **kw_12)
        self.e1.pack(**pad_12, side=LEFT)

        e2 = Entry(cadre7, width=l_contact, textvariable=self.des, **kw_12)
        e2.pack(**pad_12, side=RIGHT)
        Label(cadre7, text='CONTACT', **kw_11).pack(**pad_11, side=RIGHT)

        def record(event):
            if self.master.master.base.record_29(arg=self.arg,
                                                 code=self.code,
                                                 des=self.des,
                                                 comment=self.comment):
                self.comment.set('Enregistré')
                self.focus_set()
                root.bell()
                root.after(attenteCourte, refresh)
                
        def refresh():
                self.comment.set('')
                back()

        #### Détails de la structure dans CADRE 2 ###

        def back(event=None):
            self.master.menu.command13()

        def on_enter(event):
            e = event.widget
            e['bg'] = color_6

        def on_leave(event):
            e = event.widget
            e['bg'] = color_33

        b1 = Button(cadre2, text=" ← ", takefocus=0, **kw_45)
        b1.pack(side='left', **pad_45)
        b2 = Button(cadre2, text="ENREGISTRER", width=l_button1, **kw_45)
        b2.pack(side='left', **pad_45)

        b2.bind('<ButtonRelease-1>', record)
        b2.bind('<Return>', record)
        b1.bind('<ButtonRelease-1>', back)
        b1.bind('<Enter>', on_enter)
        b1.bind('<Leave>', on_leave)
        b2.bind('<Enter>', on_enter)
        b2.bind('<FocusIn>', on_enter)
        b2.bind('<Leave>', on_leave)
        b2.bind('<FocusOut>', on_leave)

    def display(self, arg):
        self.master.master.base.fermer()
        self.master.master.base.ouvrir()

        self.arg = arg
        self.master.master.base.display_29(arg=self.arg,
                                           code=self.code,
                                           des=self.des,
                                           comment=self.comment)

        self.e1.focus_set()
        self.e1.icursor(END)
        self.pack(**pad_fx)

    def hide(self):
        self.pack_forget()


if __name__ == '__main__':
    pf = PF()
    pf.mainloop()
