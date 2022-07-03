
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# importation des modules
import control  # les vues sont contrôlées par la base se trouvant dans control
import vue

if __name__ == '__main__':
   
    pf = vue.PF()
    
    base = control.Base()

    pf.setBase(base) 

    # fixation du lien : base > cadre_principal
    base.fix_cp(pf)

    pf.accueil()

    # création éventuelle du système de fichiers, établissement de la base de départ et de l'exercice actuel
    base.create_f()

    # boucle principale (attente des événements)
    pf.mainloop()
    
fin = input("SORTIE ")
                
                           
                                    




 



      
