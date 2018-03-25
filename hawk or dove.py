# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 13:36:58 2018

@author: Guilherme Pata
"""

def hawkdead(pop):
    return 0.5*(pop.freq('bird','hawk'))+0.5
    
def hawkoff(pop):
    return 2*( 0.5*pop.freq('bird','hawk') + 1*pop.freq('bird','dove') )
    
def dovedead(pop):
    return 0.5
    
def doveoff(pop):
    return 2*( 0*pop.freq('bird','hawk') + 1*pop.freq('bird','dove') )