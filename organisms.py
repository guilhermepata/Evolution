# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""

from random import uniform
from numpy import exp

def sigmoid(x,y):
    return 2*1/(1+exp(-1*(x)))-1*1

def w_choice(seq):
    total_prob = sum(item[1] for item in seq)
    chosen = uniform(0, total_prob)
    cumulative = 0
    for item, probality in seq:
        cumulative += probality
        if cumulative > chosen:
            return item
        
def randex(f,x,prob):
    l=[(True,prob),(False,1-prob)]
    var = w_choice(l)
    if var:
        return f(x)

class org:
    def __init__(self,sex='m',gene1='0.5',age=0):
        self._sex = sex
        self._gene1 = gene1
        self._age = age
        
    def sex(self):
        return self._sex
    def gene1(self):
        return self._gene1
    def age(self):
        return self._age
    def show(self):
        return (self._sex,self._gene1,self._age)
        
    def grow(l,y):
        for i in l:
            i._age = i._age + y
        
class pop:
    def __init__(self,r=False):
        self._content = []
        self.run(r)
        
    def content(self):
        return self._content
    def show(self):
        for i in self._content:
            print(i.show())
    def size(self):
        return len(self._content)
    def gene1pool(self):
        l=[i/10 for i in range(1,11)]
        return l
    def num_sex(self,sex):
        return len([i for i in self._content if i.sex()==sex])
    def freq_sex(self,sex):
        return self.num_sex(sex)/self.size()
    def num_a1(self,a):
        return len([i for i in self._content if i.gene1()==a])
    def freq_a1(self,a):
        return self.num_a1(a)/self.size()
    def sex_num_a1(self,a,sex):
        return len([i for i in self._content if i.gene1()==a and i.sex()==sex])
    def sex_freq_a1(self,a,sex):
        return self.sex_num_a1(a,sex)/self.num_sex(sex)
        
    def create(self,org):
        self._content = self._content + [org]
    def remove(self,org):
        self._content.remove(org)
    def populate(self,sex,gene1,n):
        for x in range(n):
            self.create(org(sex,gene1))
    def c_populate(self,ratio=0.9,n=1000):
        l=[1,10,5]
        for x in l:
            self.populate('m',x/10,int(round(ratio*n)/len(l)))
            self.populate('f',x/10,int(round((1-ratio)*n)/len(l)))
    def run(self,r):
        if r:
            self.c_populate()
        
    def breed(self):
        #kids per each male (two per female they breed with)
        org.grow(self._content,1)
        kpm = 2*self.num_sex('f')/self.num_sex('m')
        #males each male gene a generates
        mpa = [(a,a*kpm*self.sex_num_a1(a,'m')) for a in self.gene1pool()]
        #print(mpa)
        #of which inherit a
        mpa_inha = [(['m',i[0]],i[1]/2) for i in mpa]
        #print(mpa_inha)
        #of which inherit b, the female gene
        mpa_inhb = [(['m',b],sum([i[1]*self.sex_freq_a1(b,'f') for i  in mpa_inha])) for b in self.gene1pool()]
        #print(mpa_inhb)
        #females each male gene generates
        fpa = [(a,(1-a)*kpm*self.sex_num_a1(a,'m')) for a in self.gene1pool()]
        #print(fpa)
        #of which inherit a
        fpa_inha = [(['f',i[0]],i[1]/2) for i in fpa]
        #print(fpa_inha)
        #of which inherit b, the female gene
        fpa_inhb = [(['f',b],sum([i[1]*self.sex_freq_a1(b,'f') for i  in fpa_inha])) for b in self.gene1pool()]
        #print(fpa_inhb)
        prob = mpa_inha+mpa_inhb+fpa_inha+fpa_inhb
        for x in range(int(kpm*self.num_sex('m'))):
            sex,gene1=w_choice(prob)
            self.create(org(sex,gene1))
            
    def kill(self):
        #for i in self._content:
            #randex(self.remove,i,sigmoid(i.age(),self.size()))
        for i in self._content:
            if i.age()!=0:
                self.remove(i)
            
    def evolve(self,gens):
        for x in range(gens):
            print(self.size())
            print(str(round(self.freq_sex('m')*100))+'%')
            print([(a,str(round(self.freq_a1(a)*100))+'%') for a in self.gene1pool()])
            self.breed()
            self.kill()
        print(self.size())
        print(str(round(self.freq_sex('m')*100))+'%')
        print([(a,str(round(self.freq_a1(a)*100))+'%') for a in self.gene1pool()])
        
        
        
        
        
        
###
