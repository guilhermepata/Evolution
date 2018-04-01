# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""   

from sympy import symbols
from hawk_or_dove import f_survival, f_offspring

def fun1(x,y,z):
    return 1
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
    def freq(self,kind='none'):
        if kind == 'none':
            return self._homofreq + self._heterofreq
        elif kind == 'homo':
            return self._homofreq
        elif kind == 'hetero':
            return self._heterofreq
    def num(self,kind='none'):
        if kind == 'none':
            return (self._homofreq + self._heterofreq)*self._locus.pop().size()
        elif kind == 'homo':
            return self._homofreq*self._locus.pop().size()
        elif kind == 'hetero':
            return self._heterofreq*self._locus.pop().size()
    def dominant(self):
        return self._dominant
    def locus(self):
        return self._locus
        
    def copy(self):
        return allele(self._val,self._homofreq,self._heterofreq,self._dominant)
        
    def set_locus(self,locus):
        self._locus = locus
    def set_freq(self,kind,freq):
        assert(freq <= 1)
        if kind == 'homo':
            self._homofreq = freq
        elif kind == 'hetero':
            self._heterofreq = freq
        
    def offspring(self,kind,gene='none'):
        if kind == 'homo' and self._homofreq!=0:
            return self.locus().offspring(self,self)
        elif kind == 'hetero' and self._heterofreq!=0:
            if gene == 'none':
                return sum([self.locus().offspring(self,a)*a.freq('hetero') for a in self.locus().genepool() if a is not self])/sum([a.freq('hetero') for a in self.locus().genepool() if a is not self])
            else:
                return sum([self.locus().offspring(self,a)*a.freq('hetero') for a in self.locus().genepool() if a is not self and a is not gene])/sum([a.freq('hetero') for a in self.locus().genepool() if a is not self and a is not gene])
        else:
            return 0
            
    def survival(self,kind):
        if kind == 'homo' and self._homofreq!=0:
            return self.locus().survival(self,self)
        elif kind == 'hetero' and self._heterofreq!=0:
            return sum([self.locus().survival(self,a)*a.freq('hetero') for a in self.locus().genepool() if a is not self])/sum([a.freq('hetero') for a in self.locus().genepool() if a is not self])
        else:
            return 0
        
class locus:
    def __init__(self,name,pop='?',offspring=fun1,survival=fun2):
        self._name = name
        self._pop = pop
        self._genepool = []
        self._offspring = offspring
        self._survival = survival
        
    def name(self):
        return self._name
    def pop(self):
        return self._pop
    def genepool(self):
        return self._genepool
        
    def offspring(self,a,b):
        assert (type(a) is allele and type(b) is allele)
        return self._offspring(self,a,b)
    def survival(self,a,b):
        assert (type(a) is allele and type(b) is allele)
        return self._survival(self,a,b)
        
    def set_pop(self,pop):
        self._pop = pop
    def set_offspring(self,function):
        self._offspring = function
    def set_survival(self,function):
        self._survival = function
        
    def add_allele(self,allele):
        #for i in self._genepool:
            #i.set_freq(i.freq()*allele.freq()*(1/allele.freq()-1))
        allele.set_locus(self)
        self._genepool = self._genepool + [allele]
        
    def copy(self):
        copy = locus(self._name,self._pop,self._offspring,self._survival)
        for a in self._genepool:
            copy.add_allele(a.copy())
        return copy
        
class pop:
    def __init__(self,l=[],size=1024):
        self._genome = l
        self._size = size
        
    def genome(self):
        return self._genome
    def size(self):
        return self._size
    
    def add_locus(self,locus):
        locus.set_pop(self)
        self._genome = self._genome + [locus]
        
    def freq(self,name,val,kind='none'):
        locus = [l for l in self.genome() if l.name()==name][0]
        allele = [a for a in locus.genepool() if a.val()==val][0]
        return allele.freq(kind)
    
    def copy(self):
        copy = pop(size=self._size)
        for locus in self._genome:
            copy.add_locus(locus.copy())
        return copy
        
    def grow(self):
        #print(self._size)
        m_pop = self.copy()
        for locus in self.genome():
            m_locus = [l for l in m_pop.genome() if l.name() == locus.name()][0]
            
            resize = sum([ a.freq('homo')*(a.offspring('homo')+a.survival('homo')) + 0.5*a.freq('hetero')*(a.offspring('hetero')+a.survival('hetero')) for a in m_locus.genepool() ])  
            
            if resize <= 0 or self._size <= 1:
                print( "Everyone is dead" )
                return True
            
            print(sum([a.freq('homo') + 0.5*a.freq('hetero') for a in m_locus.genepool()]))
            
            for allele in locus.genepool():
                
                ma = [a for a in m_locus.genepool() if a.val() == allele.val()][0]
                
                from_homo = ma.freq('homo')*ma.offspring('homo')
                new_homo_from_homo = from_homo*(ma.freq('homo')*1+ma.freq('hetero')*0.5+(1-ma.freq())*0)
                new_hetero_from_homo = from_homo*(ma.freq('homo')*0+ma.freq('hetero')*0.5+(1-ma.freq())*1)
                
                from_hetero = ma.freq('hetero')*ma.offspring('hetero')
                new_homo_from_hetero = from_hetero*(ma.freq('homo')*0.5+ma.freq('hetero')*0.25+(1-ma.freq())*0)
                new_hetero_from_hetero = from_hetero*(ma.freq('homo')*0.5+ma.freq('hetero')*0.5+(1-ma.freq())*0.5)
                
                if sum([b.freq('homo') for b in m_locus.genepool() if b is not ma])!=0:
                    from_other1 = sum([b.freq('homo')*b.offspring('homo') for b in m_locus.genepool() if b is not ma])
                else:
                    from_other1 = 0
                if sum([sum([c.freq('hetero') for c in m_locus.genepool() if c is not b and c is not ma]) for b in m_locus.genepool() if b is not ma])!=0:
                    from_other2 = 0.5*sum([b.freq('hetero')*(1-ma.freq('hetero')/sum([c.freq('hetero') for c in m_locus.genepool() if c is not b]))*b.offspring('hetero',ma) for b in m_locus.genepool() if b is not ma])
                else:
                    from_other2 = 0
                new_hetero_from_other = (from_other1+from_other2)*(ma.freq('homo')*1+ma.freq('hetero')*0.5+(1-ma.freq())*0)
                
                allele.set_freq('homo',(new_homo_from_homo+new_homo_from_hetero+ma.freq('homo')*ma.survival('homo'))/resize)
                allele.set_freq('hetero',(new_hetero_from_homo+new_hetero_from_hetero+new_hetero_from_other+ma.freq('hetero')*ma.survival('hetero'))/resize)                   
                
            self._size = self._size*resize
                
                
    def evolve(self,gens,name='none',val1='none',val2='none',kind='none'):
        if not (name,val1,val2)==('none','none','none'):
            print([val1,self.freq(name,val1,kind)],[val2,self.freq(name,val2,kind)],round(self.size()))
        stop = False
        while gens>0 and not stop:
            gens = gens-1
            stop = self.grow()
            if not (name,val1,val2)==('none','none','none') and not stop:
                print([val1,self.freq(name,val1,kind)],[val2,self.freq(name,val2,kind)],round(self.size()))
                
i,x = symbols('i x')
p=pop()
bird = locus('bird')
bird.set_offspring(f_offspring)
bird.set_survival(f_survival)
bird.add_allele(allele('hawk',0.5,0))
bird.add_allele(allele('dove',0.5,0))
p.add_locus(bird)
p.evolve(600,'bird','hawk','dove')
        
