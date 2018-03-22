# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 19:30:31 2018

@author: Guilherme Pata
"""
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
        
    def grow(l,y):
        for i in l:
            i._age = i._age + y
        
class pop:
    def __init__(self):
        self._content = []
        
    def content(self):
        return self._content
    def size(self):
        return len(self._content)
    def gene1pool(self):
        l=[]
        for i in self._content:
            if not i.gene1() in l:
                l=l+[i.gene1()]
        return l
    def num_sex(self,sex):
        return len([i for i in self._content if i.sex()==sex])
    def freq_sex(self,sex):
        return self.num_sex(sex)/self.size()
    def sex_num_a1(self,a,sex):
        return len([i for i in self._content if i.gene1()==a and i.sex()==sex])
    def sex_freq_a1(self,a,sex):
        return self.sex_num_a1(a,sex)/self.size()
        
    def create(self,org):
        self._content = self._content + [org]
    def populate(self,sex,gene1,n):
        for x in range(n):
            self.create(org(sex,gene1))
    def c_populate(self,ratio,n):
        for x in range(1,11):
            self.populate('m',x/10,int(round(ratio*n)/10))
            self.populate('f',x/10,int(round((1-ratio)*n)/10))
        
    def breed(self):
        #kids per each male (two per female they breed with)
    
        org.grow(self._content,1)
    
        kpm = 2*self.num_sex('f')/self.num_sex('m')
        
        #males each male gene generates
        mpa = [(a*kpm*self.sex_num_a1(a,'m'),a) for a in self.gene1pool()]
        #of which inherit a
        mpa_inha = [(i[0]/2,i[1]) for i in mpa]
        #of which inherit b, the female gene
        mpa_inhb = [(sum([i[0]*self.sex_freq_a1(b,'f') for i  in mpa_inha]),b) for b in self.gene1pool()]
        
        #females each male gene generates
        fpa = [((1-a)*kpm*self.sex_num_a1(a,'m'),a) for a in self.gene1pool()]
        #of which inherit a
        fpa_inha = [(i[0]/2,i[1]) for i in fpa]
        #of which inherit b, the female gene
        fpa_inhb = [(sum([i[0]*self.sex_freq_a1(b,'f') for i  in fpa_inha]),b) for b in self.gene1pool()]
        
        l1 = [(round(i[0]),i[1]) for i in mpa_inha]
        l2 = [(round(i[0]),i[1]) for i in mpa_inhb]
        l3 = [(round(i[0]),i[1]) for i in fpa_inha]
        l4 = [(round(i[0]),i[1]) for i in fpa_inhb]
        
        lists = [(l1,'m'),(l2,'m'),(l3,'f'),(l4,'f')]
        
        for l in lists:
            for i in l[0]:
                for x in range(int(i[0])):
                    self.create(org(l[1],i[1]))
        
        
        
        
        
        
        
        
###
