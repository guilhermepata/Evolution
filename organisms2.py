# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""   

def fun1(x):
    return 2
    
def fun2(x):
    return 0.5

class allele:
    def __init__(self,val,freq,dominant=False,sexlinked=False,of=fun1,df=fun2):
        self._val = val
        self._freq = freq
        self._dominant = dominant
        self._sexlinked = sexlinked
        self._of = of
        self._df = df
        
    def val(self):
        return self._val
    def freq(self):
        return self._freq
    def dominant(self):
        return self._dominant
    def sexlinked(self):
        return self._sexlinked
    def of(self):
        return self._of
    def df(self):
        return self._df
    
    def set_freq(self,freq):
        self._freq = freq
        
    def offspring(self,pop):
        return self._of(pop)
    def deathrate(self,pop):
        return self._df(pop)
        
    def heredity(self,pop):
        if pop.rep() == 'asex':
            return 1
        elif pop.rep() == 'sex':
            if self._sexlinked:
                return 1/2
            else:
                return 1/2*(self._freq-self._freq**2)+1*(self._freq**2)
            
        
class locus:
    def __init__(self,name):
        self._name = name
        self._genepool = []
        
    def name(self):
        return self._name
    def genepool(self):
        return self._genepool
        
    def add_allele(self,allele):
        #for i in self._genepool:
            #i.set_freq(i.freq()*allele.freq()*(1/allele.freq()-1))
        self._genepool = self._genepool + [allele]
        
    def copy(self):
        copy = locus(self._name)
        for a in self._genepool:
            copy.add_allele(
                allele(a.val(),a.freq(),a.dominant(),a.sexlinked(),a.of(),a.df())
            )
        return copy
        
class pop:
    def __init__(self,l=[],rep='asex'):
        self._genome = l
        self._rep = rep
        
    def genome(self):
        return self._genome
    def rep(self):
        return self._rep
    
    def add_locus(self,locus):
        self._genome = self._genome + [locus]
        
    def freq(self,name,val):
        locus = [l for l in self.genome() if l.name()==name][0]
        allele = [a for a in locus.genepool() if a.val()==val][0]
        return allele.freq()
    
    def copy(self):
        copy = pop()
        for locus in self._genome:
            copy.add_locus(locus.copy())
        return copy
        
    def grow(self):
        if self._rep == 'asex':
            m_pop = self.copy()
            for locus in self.genome():
                m_locus = [l for l in m_pop.genome() if l.name() == locus.name()][0]
                for allele in locus.genepool():
                    m_allele = [a for a in m_locus.genepool() if a.val() == allele.val()][0]
                    
                    x = m_allele.freq() * ( m_allele.offspring(m_pop)*m_allele.heredity(m_pop) - m_allele.deathrate(m_pop) )
                    y = sum([a.freq() * ( a.offspring(m_pop) - a.deathrate(m_pop) ) for a in m_locus.genepool()])
                    
                    allele.set_freq(x/y)
                
    def evolve(self,gens,name='none',val='none'):
        if not (name,val)==('none','none'):
            print(self.freq(name,val))
        for x in range(gens):
            self.grow()
            if not (name,val)==('none','none'):
                print(self.freq(name,val))
        
