# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""   

from sympy import symbols

def fun1(x,y,z):
    return 4
def fun2(x,y,z):
    return 1

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
        #assert(freq <= 1)
        if kind == 'homo':
            self._homofreq = freq
        elif kind == 'hetero':
            self._heterofreq = freq
        
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
        return self._offspring(a,b,self.pop())
    def survival(self,a,b):
        assert (type(a) is allele and type(b) is allele)
        return self._survival(a,b,self.pop())
        
    def set_pop(self,pop):
        self._pop = pop
        
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
        self._genepairs = '?'
        self._size = size
        
    def genome(self):
        return self._genome
    def size(self):
        return self._size
    def genepairs(self):
        if self._genepairs!='?':
            return self._genepairs
        else:
            l=[]
            for locus in self._genome:
                subl=[[a,b] for a in locus.genepool() for b in locus.genepool()]
                for i in subl:
                    c = subl[:]
                    c.remove(i)
                    if [i[1],i[0]] in c:
                        subl.remove(i)
                for i in subl:
                    if i[0]==i[1]:
                        i.append(i[0].freq('homo'))
                    elif i[0]!=i[1]:
                        i.append(i[0].freq('hetero')*i[1].freq('hetero')/sum([b.freq('hetero') for b in locus.genepool() if b is not i[0]]))
                l=l+[[locus]+subl]
            self._genepairs = l
            return l
                    
    
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
        #print(self._size)
        m_pop = self.copy()
        for x in m_pop.genepairs():
            locus = x[0]
            genotypes = x[1:]
            couples=[[a,b] for a in genotypes for b in genotypes]
            for i in couples:
                    c = couples[:]
                    c.remove(i)
                    if [i[1],i[0]] in c:
                        couples.remove(i)
            for i in couples:
                i.append(m_pop.size()*i[0][2]*i[1][2]*(locus.offspring(i[0][0],i[0][1])+locus.offspring(i[1][0],i[1][1])))
            new_size = m_pop.size()+sum([i[2] for i in couples])
                
    def evolve(self,gens,name='none',val='none'):
        if not (name,val)==('none','none'):
            print(self.freq(name,val))
        for x in range(gens):
            self.grow()
            if not (name,val)==('none','none'):
                print(self.freq(name,val))
                
i,x = symbols('i x')
p=pop()
bird = locus('bird')
bird.add_allele(allele('a',0.5))
bird.add_allele(allele('b',0.5))
p.add_locus(bird)
p.evolve(5)
        
