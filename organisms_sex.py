# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""   

def fun1(x,y,z):
    return 2
    
def fun2(x,y,z):
    return 0.5

class allele:
    def __init__(self,val,homofreq,heterofreq,dominant=False,locus='?'):
        self._val = val
        self._homofreq = homofreq
        self._heterofreq = heterofreq
        self._dominant = dominant
        self._locus = locus
        
    def val(self):
        return self._val
    def homofreq(self):
        return self._homofreq
    def heterofreq(self):
        return self._heterofreq
    def h_heterofreq(self):
        return self._heterofreq/sum([a.heterofreq() for a in self.locus().genepool()])
    def freq(self):
        return self._homofreq+self._heterofreq
    def dominant(self):
        return self._dominant
    def locus(self):
        return self._locus
        
    def copy(self):
        return allele(self._val,self._homofreq,self._heterofreq,self._dominant)
        
    def set_locus(self,locus):
        self._locus = locus
    
    def set_homofreq(self,homofreq):
        assert(homofreq <= 1)
        self._homofreq = homofreq
    def set_heterofreq(self,heterofreq):
        assert(heterofreq <= 1)
        self._heterofreq = heterofreq
        
    def homo_os(self):
        if self._homofreq!=0:
            return self.locus().offspring(self.val(),self.val())
        else:
            return 0
    def homo_dr(self):
        if self._homofreq!=0:
            return self.locus().deathrate(self.val(),self.val())
        else:
            return 0
        
    def hetero_os(self):
        if self._heterofreq!=0:
            return sum([self.locus().offspring(self.val(),a.val())*a.heterofreq() for a in self.locus().genepool() if a is not self])/sum([b.heterofreq() for b in self.locus().genepool() if b is not self])
        else:
            return 0
    def hetero_dr(self):
        if self._heterofreq!=0:
            return sum([self.locus().deathrate(self.val(),a.val())*a.heterofreq() for a in self.locus().genepool() if a is not self])/sum([b.heterofreq() for b in self.locus().genepool() if b is not self])
        else:
            return 0
        
    def hetero_os_wo(self,gene):
        return sum([self.locus().offspring(self.val(),a.val())*a.heterofreq() for a in self.locus().genepool() if a is not self and a is not gene])/sum([b.heterofreq() for b in self.locus().genepool() if b is not self and b is not gene])
    def hetero_dr_wo(self,gene):
        return sum([self.locus().deathrate(self.val(),a.val())*a.heterofreq() for a in self.locus().genepool() if a is not self and a is not gene])/sum([b.heterofreq() for b in self.locus().genepool() if b is not self and b is not gene])
        
class locus:
    def __init__(self,name,pop='?',offspring=fun1,deathrate=fun2):
        self._name = name
        self._pop = pop
        self._genepool = []
        self._offspring = offspring
        self._deathrate = deathrate
        
    def name(self):
        return self._name
    def pop(self):
        return self._pop
    def genepool(self):
        return self._genepool
        
    def offspring(self,val1,val2):
        return self._offspring(val1,val2,self.pop())
    def deathrate(self,val1,val2):
        return self._deathrate(val1,val2,self.pop())
        
    def set_pop(self,pop):
        self._pop = pop
        
    def add_allele(self,allele):
        #for i in self._genepool:
            #i.set_freq(i.freq()*allele.freq()*(1/allele.freq()-1))
        allele.set_locus(self)
        self._genepool = self._genepool + [allele]
        
    def copy(self):
        copy = locus(self._name,self._pop,self._offspring,self._deathrate)
        for a in self._genepool:
            copy.add_allele(a.copy())
        return copy
        
class pop:
    def __init__(self,l=[],size=1000):
        self._genome = l
        self._size = size
        
    def genome(self):
        return self._genome
    def size(self):
        return self._size
    
    def add_locus(self,locus):
        locus.set_pop(self)
        self._genome = self._genome + [locus]
        
    def freq(self,name,val):
        locus = [l for l in self.genome() if l.name()==name][0]
        allele = [a for a in locus.genepool() if a.val()==val][0]
        return allele.freq()
    
    def copy(self):
        copy = pop(size=self._size)
        for locus in self._genome:
            copy.add_locus(locus.copy())
        return copy
        
    def grow(self):
        m_pop = self.copy()
        for locus in self.genome():
            m_locus = [l for l in m_pop.genome() if l.name() == locus.name()][0]
            
            pondgrowth = sum([ a.homofreq()*(a.homo_os()-a.homo_dr()) + 0.5*a.heterofreq()*(a.hetero_os()-a.hetero_dr()) for a in m_locus.genepool() ])  
            
            print(sum([a.homofreq() + 0.5*a.heterofreq() for a in m_locus.genepool()]))
            
            for allele in locus.genepool():
                ma = [a for a in m_locus.genepool() if a.val() == allele.val()][0]
                
                new_homofreq = 1*ma.homofreq()*ma.homofreq()*2*ma.homo_os() + 0.5*ma.homofreq()*ma.heterofreq()*(ma.homo_os()+ma.hetero_os()) + 0.25*ma.heterofreq()*ma.heterofreq()*2*ma.hetero_os() - ma.homofreq()*ma.homo_dr()
                
                allele.set_homofreq(new_homofreq/pondgrowth)
                
                new_heterofreq1 = 0.5*ma.homofreq()*ma.heterofreq()*(ma.homo_os()+ma.hetero_os()) + 0.5*ma.heterofreq()*ma.heterofreq()*(2*ma.hetero_os()) - ma.heterofreq()*ma.hetero_dr()
                
                
                if sum([a.homofreq() for a in m_locus.genepool() if a is not ma])!=0:
                    homo_o_else = sum([a.homo_os()*a.homofreq() for a in m_locus.genepool() if a is not ma])/sum([b.homofreq() for b in m_locus.genepool() if b is not ma])
                else:
                    homo_o_else = 0
                
                if sum([a.heterofreq() for a in m_locus.genepool() if a is not ma])-ma.heterofreq()!=0:
                    hetero_o_else = sum([a.hetero_os_wo(ma)*a.homofreq() for a in m_locus.genepool() if a is not ma])/sum([b.homofreq() for b in m_locus.genepool() if b is not ma])
                else:
                    hetero_o_else = 0
                
                new_heterofreq2 = 0.5*ma.heterofreq()*(1-ma.freq())*(ma.hetero_os()+homo_o_else+hetero_o_else) + 1*ma.homofreq()*(1-ma.freq())*(ma.homo_os()+homo_o_else+hetero_o_else)
                
                allele.set_homofreq((new_heterofreq1+new_heterofreq2)/pondgrowth)
                
    def evolve(self,gens,name='none',val='none'):
        if not (name,val)==('none','none'):
            print(self.freq(name,val))
        for x in range(gens):
            self.grow()
            if not (name,val)==('none','none'):
                print(self.freq(name,val))
        
