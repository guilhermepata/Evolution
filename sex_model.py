# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""   

def fun1(x,y,z):
    return 1  
def fun2(x,y,z):
    return 0

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
            
    def deathrate(self,kind):
        if kind == 'homo' and self._homofreq!=0:
            return self.locus().deathrate(self,self)
        elif kind == 'hetero' and self._heterofreq!=0:
            return sum([self.locus().deathrate(self,a)*a.freq('hetero') for a in self.locus().genepool() if a is not self])/sum([a.freq('hetero') for a in self.locus().genepool() if a is not self])
        else:
            return 0
        
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
        
    def offspring(self,a,b):
        assert (type(a) is allele and type(b) is allele)
        return self._offspring(a,b,self.pop())
    def deathrate(self,a,b):
        assert (type(a) is allele and type(b) is allele)
        return self._deathrate(a,b,self.pop())
        
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
        print(self._size)
        m_pop = self.copy()
        for locus in self.genome():
            m_locus = [l for l in m_pop.genome() if l.name() == locus.name()][0]
            
            new_size = sum([ a.num('homo')*(1+a.offspring('homo')-a.deathrate('homo')) + 0.5*a.num('hetero')*(1+a.offspring('hetero')-a.deathrate('hetero')) for a in m_locus.genepool() ])  
            
            print(sum([a.freq('homo') + 0.5*a.freq('hetero') for a in m_locus.genepool()]))
            
            for allele in locus.genepool():
                
                ma = [a for a in m_locus.genepool() if a.val() == allele.val()][0]
                
                #list_of_homo_offspring = [ ma.num('homo')*ma.freq('homo')*2*ma.offspring('homo')*1, ma.num('homo')*ma.freq('hetero')*(ma.offspring('homo')+ma.offspring('hetero'))*0.5, ma.num('hetero')*ma.freq('hetero')*2*ma.offspring('hetero')*0.25 ]
                
                #new_homo_a = sum( list_of_homo_offspring ) - ma.num('homo')*ma.deathrate('homo')
                
                #allele.set_freq('homo',new_homo_a/new_size)
                
                #list_of_hetero_offspring1 = [ ma.num('homo')*ma.freq('hetero')*(ma.offspring('homo')+ma.offspring('hetero'))*0.5, ma.num('hetero')*ma.freq('hetero')*2*ma.offspring('hetero')*0.5 ]
                
                #if (1-ma.freq())>0:
                #    print(sum([b.freq('homo') for b in m_locus.genepool() if b is not ma]))
                #    if sum([b.freq('homo') for b in m_locus.genepool() if b is not ma])!=0:
                #        avg_other_homo_offspring = sum([b.offspring('homo')*b.freq('homo') for b in m_locus.genepool() if b is not ma])/sum([b.freq('homo') for b in m_locus.genepool() if b is not ma])
                #    else:
                #        avg_other_homo_offspring = 0
                #
                #    print((1-ma.freq()-sum([b.freq('homo') for b in m_locus.genepool() if b is not ma])))
                #    if (1-ma.freq()-sum([b.freq('homo') for b in m_locus.genepool() if b is not ma]))!=0:
                #        avg_other_hetero_offspring = sum([b.offspring('hetero',ma)*b.freq('hetero') for b in m_locus.genepool() if b is not ma])/sum([b.freq('hetero') for b in m_locus.genepool() if b is not ma])
                #    else:
                #        avg_other_hetero_offspring = 0
                #
                #    avg_other_offspring = ( avg_other_homo_offspring * sum([b.freq('homo') for b in m_locus.genepool() if b is not ma]) + avg_other_hetero_offspring * (1-ma.freq()-sum([b.freq('homo') for b in m_locus.genepool() if b is not ma])) ) / (1-ma.freq())
                #
                #else:
                #    avg_other_offspring = 0
                #
                #list_of_hetero_offspring2 = [ ma.num('homo')*(1-ma.freq())*(ma.offspring('homo')+avg_other_offspring)*1, ma.num('hetero')*(1-ma.freq())*(ma.offspring('hetero')+avg_other_offspring)*0.5]
                #
                #new_hetero_a = sum( list_of_hetero_offspring1 + list_of_hetero_offspring2 ) - ma.num('hetero')*ma.deathrate('hetero')
                
                #allele.set_freq('hetero',new_hetero_a/new_size)
                
                new_homo_from_homo = ma.num('homo')*ma.offspring('homo')*(ma.freq('homo')*1+ma.freq('hetero')*0.5)
                
                new_hetero_from_homo = ma.num('homo')*ma.offspring('homo')*(ma.freq('hetero')*0.5+(1-ma.freq())*1)
                
                #print(ma.offspring('hetero'))    
                
                new_homo_from_hetero = ma.num('hetero')*ma.offspring('hetero')*(ma.freq('homo')*0.5+ma.freq('hetero')*0.25)
                
                new_hetero_from_hetero = ma.num('hetero')*ma.offspring('hetero')*(ma.freq('homo')*0.5+ma.freq('hetero')*0.5+(1-ma.freq())*0.5)
                                
                allele.set_freq('homo',(new_homo_from_homo+new_homo_from_hetero+ma.num('homo')*(1-ma.deathrate('homo')))/new_size)
                
                allele.set_freq('hetero',(new_hetero_from_homo+new_hetero_from_hetero+ma.num('hetero')*(1-ma.deathrate('hetero')))/new_size)                
                
            self._size = new_size
                
                
    def evolve(self,gens,name='none',val='none'):
        if not (name,val)==('none','none'):
            print(self.freq(name,val))
        for x in range(gens):
            self.grow()
            if not (name,val)==('none','none'):
                print(self.freq(name,val))
                
p=pop()
bird = locus('bird')
bird.add_allele(allele('a',0.5,0))
bird.add_allele(allele('b',0.5,0.0))
p.add_locus(bird)
p.evolve(10)
        
