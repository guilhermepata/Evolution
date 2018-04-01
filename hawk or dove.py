# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 13:36:58 2018

@author: Guilherme Pata
"""
    
def f_survival(locus,a,b,totalfood=128,indfood=1):
    avl_indfood = min(indfood,totalfood/locus.pop().size())
    avg_fights_per_bird=(indfood - avl_indfood)/indfood
    if a.val() == 'hawk' or b.val() == 'hawk':
        #Hawks will fight doves and hawks. They alwyas win against birds, but never kill them. They win against hawks and kill them half of the time, and the other half they are the ones who die. Fighting hawks wastes time...
        return avl_indfood/indfood - avg_fights_per_bird*0.5*locus.pop().freq('bird','hawk') + avg_fights_per_bird*avl_indfood/indfood*(0.9*0.5*locus.pop().freq('bird','hawk')+locus.pop().freq('bird','dove','homo'))
    else:
        #Doves will also fight hawks and doves. They always lose food from hawks, but are never killed by hawks. They fight other doves for their food, but never kill them, losing and winning half of their fights. Fighting doves wastes time...
        return avl_indfood/indfood - avg_fights_per_bird*avl_indfood/indfood*(locus.pop().freq('bird','hawk')+0.5*locus.pop().freq('bird','dove','homo')) + avg_fights_per_bird*0.9*0.5*locus.pop().freq('bird','dove','homo')

def f_offspring(locus,a,b,totalfood=1000,indfood=1):
    avl_indfood = min(indfood,totalfood/locus.pop().size())
    return 2*avl_indfood/indfood